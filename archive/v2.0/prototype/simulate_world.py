"""Simulation N pays, CSV nationaux + journal bilatéral + comptes mondiaux."""
import argparse,csv,json,re
from pathlib import Path
from .model import Economy,Params,MODEL_VERSION
from .worldn import World
from .simulate import export_csv,json_ready
from .reference import reference_parameters

def load_world(config=None,n=3):
    cfg=json.loads(Path(config).read_text()) if config else {'countries':[{'name':f'P{i+1}'} for i in range(n)]}
    specs=cfg.pop('countries');countries=[];names=[]
    for i,spec in enumerate(specs):
        name=spec.get('name',f'P{i+1}')
        if not re.fullmatch(r'[A-Za-z0-9_-]+',name) or name in names:raise ValueError('Identifiant national invalide ou dupliqué')
        e=Economy(Params(**{**reference_parameters(),**spec.get('params',{})}),seed=spec.get('seed',i),shock_sd=spec.get('shock_sd',0.))
        factor=spec.get('currency_divisor',1.)
        if factor!=1:e.redenominate(factor)
        countries.append(e);names.append(name)
    return World(countries,**cfg),names

def export_world(w,directory,names=None):
    out=Path(directory);out.mkdir(parents=True,exist_ok=True)
    names=names or [f'P{i+1}' for i in range(w.n)]
    for e,name in zip(w.countries,names):
        export_csv(e,out/(name+'.csv'))
        with (out/('accounts_'+name+'.csv')).open('w',newline='') as f:
            fields=sorted(set().union(*(r.keys() for r in e.flow_history)))
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(e.flow_history)
    with (out/'trade.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['week','importer','exporter','sector','quantity','settlement_value'])
        for row in w.trade_history:
            for i in range(w.n):
                for j in range(w.n):
                    if i==j:continue
                    for k in range(4):writer.writerow([row['t'],names[i],names[j],k,row['quantity'][i,j,k],row['value'][i,j,k]])
    payload=dict(version=MODEL_VERSION,countries=names,weeks=w.t,exchange_regime=w.exchange_regime,
        openness=w.openness,elasticity=w.elasticity,credit_limit=w.credit_limit,tariffs=w.tariffs,
        reallocate_blocked_imports=w.reallocate_blocked_imports,
        history=w.history,limitations=['Actifs privés domestiques','Intrants domestiques','Pas de réforme internationale'])
    (out/'world.json').write_text(json.dumps(payload,default=json_ready,ensure_ascii=False,indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--config');p.add_argument('--countries',type=int,default=3)
    p.add_argument('--years',type=float,default=30.);p.add_argument('--output',default='results/world_demo');args=p.parse_args()
    if args.years<=0:raise ValueError('Horizon positif requis')
    w,names=load_world(args.config,args.countries);w.run(args.years);export_world(w,args.output,names)
    print(f'{w.n} pays, {w.t} semaines ; résultats dans {args.output}')
if __name__=='__main__':main()
