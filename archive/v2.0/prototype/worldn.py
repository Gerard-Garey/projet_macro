"""Monde fermé à N économies avec actifs et compensation multilatérale.

Les titres privés restent domestiques. R_fx est une position extérieure nette
signée en unité de règlement, et non une réserve disponible sans contrepartie.
Les commandes finales choisissent leur origine ; les intrants restent locaux.
"""
from dataclasses import dataclass
import numpy as np
from .model import Economy, Params, WEEKS
from .reference import reference_parameters

@dataclass
class MarketPlan:
    country: int
    supply: np.ndarray
    orders: list

class World:
    def __init__(self, countries, openness=.15, elasticity=2., share_speed=.1,
                 tariffs=0., credit_limit=.25, exchange_regime='fixed', fx_speed=.1,
                 reallocate_blocked_imports=True):
        self.countries=list(countries); self.n=len(self.countries)
        if not self.n: raise ValueError('Au moins un pays est requis')
        if len({id(e) for e in self.countries})!=self.n: raise ValueError('Pays dupliqué')
        if any(not isinstance(e,Economy) or not e.p.assets for e in self.countries):
            raise ValueError('Chaque pays doit être une Economy avec actifs')
        if len({e.t for e in self.countries})!=1: raise ValueError('Calendriers nationaux différents')
        if any(e.world is not None or e.collapsed or abs(e.R_fx)>1e-9 or abs(e.led.dep['FX'])>1e-9 for e in self.countries):
            raise ValueError('Pays déjà relié, effondré ou position extérieure initiale non nulle')
        if not 0<=openness<1 or elasticity<=1 or not 0<share_speed<=1:
            raise ValueError('Ouverture, élasticité > 1 et vitesse de parts requises')
        if not np.isfinite([openness,elasticity,share_speed,credit_limit,fx_speed]).all() or credit_limit<0 or fx_speed<0:
            raise ValueError('Paramètres internationaux invalides')
        if exchange_regime not in ('fixed','floating'): raise ValueError('Régime inconnu')
        if not isinstance(reallocate_blocked_imports,bool): raise ValueError('Réaffectation : booléen requis')
        self.openness=openness;self.elasticity=elasticity;self.share_speed=share_speed
        self.credit_limit=credit_limit;self.exchange_regime=exchange_regime;self.fx_speed=fx_speed
        self.reallocate_blocked_imports=reallocate_blocked_imports
        self.t=self.countries[0].t;self.history=[];self.trade_history=[];self._failed=False
        self.chiK=np.array([e.p.chi_K for e in self.countries]);self.energy_world=False
        tariff=np.broadcast_to(np.asarray(tariffs,dtype=float),(self.n,4)).copy()
        if not np.isfinite(tariff).all() or np.any(tariff<0): raise ValueError('Droits de douane invalides')
        self.tariffs=tariff
        self.preference=np.zeros((self.n,self.n,4))
        sizes=np.array([e.Y_nom_prev()/e.e for e in self.countries])
        for i,e in enumerate(self.countries):
            partners=sizes.copy();partners[i]=0.
            if self.n>1:self.preference[i]=openness*(partners/max(partners.sum(),1e-12))[:,None]
            self.preference[i,i]=1-openness if self.n>1 else 1.
            e.world=self;e.idx=i
        self.shares=self.preference.copy();self._prepare_quotes(update=False)
        self.last_trade=np.zeros((self.n,self.n,4))

    @classmethod
    def homogeneous(cls,n,**kwargs):
        if not isinstance(n,int) or n<1: raise ValueError('Nombre de pays entier positif requis')
        return cls([Economy(Params(**reference_parameters()),seed=i) for i in range(n)],**kwargs)

    def _prepare_quotes(self,update=True):
        self.rates=np.array([e.e for e in self.countries])
        self.producer_prices=np.array([e.p_ for e in self.countries])
        landed=self.producer_prices[None,:,:]/self.rates[None,:,None]*self.rates[:,None,None]
        landed=np.broadcast_to(landed,(self.n,self.n,4)).copy()
        for i in range(self.n):
            for j in range(self.n):
                if i!=j:landed[i,j]*=1+self.tariffs[i]
        self.landed=landed
        if update:
            # Parts physiques : réponse d'origine aux prix, graduelle. Pas d'indice
            # de bien-être CES ; les unités d'un secteur sont additives par convention.
            rel=landed/self.producer_prices[:,None,:]
            score=self.preference*np.exp(np.clip(-self.elasticity*np.log(rel),-100,100))
            desired=score/score.sum(axis=1,keepdims=True)
            self.shares+=(desired-self.shares)*self.share_speed
        self.prices=(self.shares*landed).sum(axis=1)
        self.capital_prices=self.prices[:,3].copy()

    def _refresh_capital_prices(self):
        prices=np.array([e.p_[3]/e.e for e in self.countries])
        for i,e in enumerate(self.countries):
            landed=prices*e.e*(1+self.tariffs[i,3]);landed[i]=e.p_[3]
            self.capital_prices[i]=self.shares[i,:,3]@landed

    def composite_price(self,e):return self.prices[e.idx].copy()
    def home_share(self,e):return self.shares[e.idx,e.idx].copy()
    def import_price(self,e):
        i=e.idx;foreign=self.shares[i].copy();foreign[i]=0.
        return np.divide((foreign*self.landed[i]).sum(axis=0),foreign.sum(axis=0),
                         out=e.p_.copy(),where=foreign.sum(axis=0)>1e-15)

    def make_plan(self,e,supply,xh,Iw,G_cons,G_inv,IZ_new,Xdem):
        orders=[]
        for h in range(3):
            for k in range(3):orders.append((f'H{h}','C',k,h,float(xh[h,k])))
        orders.extend([('G','GC',2,0,float(G_cons)),('G','GI',3,0,float(G_inv))])
        for j in range(4):
            orders.append((f'F{j}','I',3,j,float(Iw[j])))
            for k in range(4):orders.append((f'F{j}','X',k,j,float(Xdem[k,j])))
        for h in range(3):orders.append((f'H{h}','IZ',3,h,float(IZ_new*e._IZ_share[h])))
        return MarketPlan(e.idx,supply.copy(),orders)

    def construction_refunds(self,e,market,planned_quantity):
        """Un prêt de construction n'est annulé que sur le budget non dépensé.

        Une substitution vers un fournisseur moins cher peut livrer davantage
        d'unités ; elle ne doit jamais déclencher un remboursement négatif.
        Le chemin historique est conservé quand la réaffectation est inactive.
        """
        if not self.reallocate_blocked_imports or self.financing['import_fraction'][e.idx]==1.:
            got=market['IZ_h'].sum()
            return (1-got/max(planned_quantity,1e-12))*e._IZ_loan if planned_quantity>0 else np.zeros(3)
        planned=planned_quantity*self.prices[e.idx,3]*e._IZ_share
        unspent=np.maximum(planned-market['IZ_spend_h'],0.)
        fraction=np.divide(unspent,planned,out=np.zeros(3),where=planned>0)
        return np.clip(fraction,0.,1.)*e._IZ_loan

    def _clear(self,plans):
        demand=np.zeros((self.n,self.n,4))
        for plan in plans:
            i=plan.country
            for account,kind,k,owner,q in plan.orders:
                if kind=='X':demand[i,i,k]+=q
                else:demand[i,:,k]+=q*self.shares[i,:,k]
        supply=np.array([p.supply for p in plans]);foreign_scale=np.ones(self.n)
        opening=np.array([e.R_fx for e in self.countries])
        # Plancher de crédit fixé avant les échanges. Une baisse du PIB ne force
        # pas une saisie rétroactive ; elle suspend les nouvelles sorties nettes.
        limits=np.maximum(self.credit_limit*np.array([e.Y_nom_prev()/e.e for e in self.countries]),-opening)
        border_prices=self.producer_prices/self.rates[:,None]
        for iteration in range(1000):
            requested=demand.copy()
            for i in range(self.n):
                for j in range(self.n):
                    if i!=j:requested[i,j]*=foreign_scale[i]
            redirected=np.zeros((self.n,4))
            if self.reallocate_blocked_imports:
                for i in range(self.n):
                    # Le budget importé refusé est proposé au producteur local
                    # du même secteur. Le rapport de prix conserve la dépense,
                    # droits de douane compris, et non la quantité initiale.
                    rejected=demand[i]*(1-foreign_scale[i]);rejected[i]=0.
                    redirected[i]=(rejected*self.landed[i]).sum(axis=0)/self.landed[i,i]
                    requested[i,i]+=redirected[i]
            seller_fraction=np.minimum(1.,supply/np.maximum(requested.sum(axis=0),1e-30))
            delivery=requested*seller_fraction[None,:,:]
            invoices=delivery*border_prices[None,:,:]
            for i in range(self.n):invoices[i,i]=0.
            imports=invoices.sum(axis=(1,2));exports=invoices.sum(axis=(0,2))
            available=np.maximum(opening+limits+exports,0.)
            violation=imports-available
            if np.max(violation/np.maximum(1.,imports))<1e-12:break
            foreign_scale*=np.minimum(1.,available/np.maximum(imports,1e-30))
        else:raise RuntimeError('Compensation extérieure sans convergence')
        # Toute demande réaffectée subit aussi la limite de l'offre locale.
        # Les intrants, déjà domestiques, et les budgets de chaque ordre restent
        # inchangés. Les ventes supplémentaires réduisent éventuellement les
        # exportations : leur effet financier est inclus dans l'itération.
        executions=[];quantity=np.zeros_like(delivery);trade=np.zeros_like(invoices)
        for plan in plans:
            i=plan.country;e=self.countries[i]
            r=dict(Q=np.zeros(4),D=requested[:,i,:].sum(axis=0),x_obt=np.zeros((3,3)),Xgot=np.zeros((4,4)),
                   Igot=np.zeros(4),IZ_h=np.zeros(3),IZ_spend_h=np.zeros(3),C=0.,VAT=0.,I=0.,IZ=0.,G=0.,GC=0.,GI=0.,tariff=0.,EX=0.,IM=0.)
            executions.append(r)
        def pay(e,frm,to,amount):
            paid=e.led.transfer(frm,to,float(amount))
            if abs(paid-amount)>1e-9*max(1.,amount):raise AssertionError('Paiement international non financé')
        for plan in plans:
            i=plan.country;e=self.countries[i];r=executions[i]
            for account,kind,k,owner,q in plan.orders:
                if q<=0:continue
                parts=self.shares[i,:,k].copy() if kind!='X' else np.eye(self.n)[i]
                if kind!='X' and self.reallocate_blocked_imports:
                    rejected=parts*(1-foreign_scale[i]);rejected[i]=0.
                    parts[i]+=rejected@self.landed[i,:,k]/self.landed[i,i,k]
                for j in range(self.n):
                    got=q*parts[j]*seller_fraction[j,k]*(foreign_scale[i] if i!=j else 1.)
                    if got<=0:continue
                    price=self.landed[i,j,k];spend=got*price
                    quantity[i,j,k]+=got;executions[j]['Q'][k]+=got
                    if i==j:pay(e,account,f'F{k}',spend)
                    else:
                        border=got*border_prices[j,k];tariff=spend-border*e.e
                        pay(e,account,'FX',spend);pay(e,'FX','G',tariff)
                        pay(self.countries[j],'FX',f'F{k}',border*self.rates[j])
                        trade[i,j,k]+=border;r['tariff']+=tariff
                    if kind=='C':
                        r['x_obt'][owner,k]+=got;r['C']+=spend
                        vat=spend*e.p.tauC;pay(e,account,'G',vat);r['VAT']+=vat
                    elif kind=='I':r['Igot'][owner]+=got;r['I']+=spend
                    elif kind=='IZ':r['IZ_h'][owner]+=got;r['IZ_spend_h'][owner]+=spend;r['IZ']+=spend
                    elif kind=='X':r['Xgot'][k,owner]+=got
                    else:r[kind]+=got;r['G']+=spend
        self.last_trade=trade;self.last_quantities=quantity
        self.financing=dict(import_fraction=foreign_scale.copy(),
            redirected_budget=(redirected*self.producer_prices).sum(axis=1),
            redirected_quantity=redirected.copy(),
            redirected_delivered=redirected*seller_fraction)
        total_imp=trade.sum(axis=(1,2));total_exp=trade.sum(axis=(0,2))
        for i,e in enumerate(self.countries):
            r=executions[i];r['IM']=total_imp[i]*e.e;r['EX']=total_exp[i]*e.e
            net=total_exp[i]-total_imp[i]
            # Clôture du compte de passage : le virement modifie les dépôts et
            # la position extérieure de la BC, sans création mondiale de créance nette.
            if abs(e.led.dep['FX']+e.e*net)>1e-8*max(1.,r['IM']+r['EX']):
                raise AssertionError('Compte de passage de change non rapproché')
            e.led.dep['FX']=0.;e.R_fx+=net
            e.IMV_last=r['IM'];e.EXV_last=r['EX']
            e.IMq_last=quantity[i].sum(axis=0)-quantity[i,i]
            e.EXq_last=quantity[:,i].sum(axis=0)-quantity[i,i]
            e.IMVj_last=trade[i].sum(axis=0)*e.e
        positions=np.array([e.R_fx for e in self.countries])
        self.accounting=dict(global_position=float(positions.sum()),trade_value=float(total_exp.sum()-total_imp.sum()),
            supply_violation=float(np.max(np.maximum(quantity.sum(axis=0)-supply,0.))),
            delivery_residual=float(np.max(abs(quantity-delivery))),
            balance_of_payments=float(np.max(abs(positions-opening-(total_exp-total_imp)))),
            credit_violation=float(np.max(np.maximum(-positions-limits,0.))),iterations=iteration+1)
        scale=max(1.,float(sum(e.Y_nom_prev()/e.e for e in self.countries)))
        for k,v in self.accounting.items():
            # Les résidus de quantités se normalisent par une offre physique,
            # indépendamment de l'unité monétaire commune choisie.
            unit_scale=max(1.,float(supply.sum())) if k in ('supply_violation','delivery_residual') else scale
            if k!='iterations' and abs(v)>1e-8*unit_scale:raise AssertionError((k,v))
        self.trade_history.append(dict(t=self.t,value=trade.copy(),quantity=quantity.copy()))
        return executions

    def set_exchange_rates(self,rates):
        rates=np.asarray(rates,dtype=float)
        if rates.shape!=(self.n,) or not np.isfinite(rates).all() or np.any(rates<=0):
            raise ValueError('Un cours strictement positif par pays est requis')
        changes=[]
        for e,new in zip(self.countries,rates):
            valuation=(new-e.e)*e.R_fx;e.E_cb+=valuation;e.e=float(new);changes.append(valuation)
            e.E_cb_check=e.B_cb+e.AG+e.L_cb+e.e*e.R_fx-e.Res-e.cash_out
        self._prepare_quotes(update=False)
        return changes

    def step(self):
        if self._failed:raise RuntimeError('Monde interrompu : restaurer un état sauvegardé avant de poursuivre')
        if any(e.collapsed and e.p.crisis_accounting!='continuous' for e in self.countries):
            raise NotImplementedError('Effondrement et réforme internationaux hors périmètre du prototype')
        if any(e.t!=self.t for e in self.countries):raise RuntimeError('Calendriers nationaux désynchronisés')
        self._failed=True;self._prepare_quotes();generators=[];plans=[]
        for e in self.countries:
            gen=e._step_normal();generators.append(gen);plans.append(next(gen))
        executions=self._clear(plans)
        for gen,r in zip(generators,executions):
            if gen.send(r)!='prices':raise RuntimeError('Barrière de prix attendue')
        self._refresh_capital_prices()
        for gen in generators:
            try:gen.send(None)
            except StopIteration:pass
            else:raise RuntimeError('Barrière de marché supplémentaire inattendue')
        valuations=np.zeros(self.n)
        if self.exchange_regime=='floating':
            # Fermeture expérimentale, sans prétention UIP : différentiel d'inflation
            # et correction commerciale. Numéraire géométrique symétrique.
            sizes=np.array([e.Y_nom_prev()/e.e for e in self.countries]);weights=sizes/sizes.sum()
            inflation=np.log1p(np.maximum([e.pi for e in self.countries],-.99))/WEEKS
            balance=self.last_trade.sum(axis=(0,2))-self.last_trade.sum(axis=(1,2))
            change=inflation-self.fx_speed*balance/np.maximum(sizes/WEEKS,1e-9)/WEEKS
            change=np.clip(change-change@weights,-.02,.02);change-=change@weights
            valuations=self.set_exchange_rates(np.array([e.e for e in self.countries])*np.exp(change))
        self._refresh_capital_prices()
        for e in self.countries:
            closing=dict(K_value=float(e.capital_price()*e.K.sum()),Z_replacement=float(e.capital_price()*e.Z.sum()),
                         equity_market=e.equity_market_value())
            e._flows.update(closing);e.flow_history[-1].update(closing)
            e.hist['Ecb'][-1]=e.E_cb
        self.history.append(dict(t=self.t,positions=[e.R_fx for e in self.countries],rates=[e.e for e in self.countries],
            valuations=list(valuations),accounting=self.accounting.copy(),financing=self.financing.copy()))
        self.t+=1;self._failed=False

    def run(self,years):
        for _ in range(round(years*WEEKS)):self.step()
        return self.history
