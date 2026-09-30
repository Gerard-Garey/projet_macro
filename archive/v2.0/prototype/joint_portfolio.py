"""Concave two-asset household problem and a funded equity call auction.

Liquid savings b, illiquid marked wealth a, transfers d=a-G*a_previous.
Quadratic transaction fees enter the cash budget, not a fictitious return.
Future labor income, dividends and capital gains remain forecasts, not GE.
"""
import numpy as np
from scipy.optimize import brentq
try:from .joint_solver import solve,PortfolioInfeasible,PortfolioConvergenceError,MarketClearingError
except ImportError:from joint_solver import solve,PortfolioInfeasible,PortfolioConvergenceError,MarketClearingError

def dividend_forecast(e,price_index):
    """Adaptive expectation of actual real dividends, never a cash payment.

    A zero parameter preserves the immediate extrapolation for ablation.
    No positive floor: a persistently zero stream tends to zero.
    """
    now=float(e.div_last.sum())/price_index
    speed=1. if e.p.joint_dividend_years==0 else -np.expm1(-1/(52*e.p.joint_dividend_years))
    old=getattr(e,'_equity_dividend_forecast_real',now)
    e._equity_dividend_forecast_real=old+speed*(now-old)
    return e._equity_dividend_forecast_real

def market(cash,holdings,income,dividend_flow,deposit_rate,growth,rho,phi,buffer,
           price_guess,fee=.02,years=10,periods=24,mix=None,tax=0.,risk=.01,subsistence=None,terminal_mode='none',search_mode='legacy',search_steps=12):
    """Clear a fixed supply of equity among participating households.

    Common unit: a real good. Price is value of all outstanding equity.
    Every decision covers exactly one week, including the future horizon.
    periods is accepted for snapshot compatibility but no longer coarsens
    time. Current dividends are already in cash.
    """
    cash=np.asarray(cash,float);holdings=np.asarray(holdings,float);income=np.asarray(income,float)
    h=len(cash);mix=np.ones(h) if mix is None else np.asarray(mix,float)
    subsistence=np.zeros(h) if subsistence is None else np.asarray(subsistence,float)
    if cash.shape!=holdings.shape or np.any(holdings<0) or holdings.sum()<=0 or np.any(income<=0) or not 0<=tax<=1:raise ValueError('Invalid market inputs')
    if years<=0 or not np.isclose(52*years,round(52*years)):
        raise ValueError('Portfolio horizon must contain an integer number of weeks')
    periods=int(round(52*years))
    times=np.arange(periods)/52
    weights=np.exp(-rho*times)
    interval=np.full(periods,1/52)
    if terminal_mode not in ('none','balanced_policy') or (terminal_mode=='balanced_policy' and rho<=0):raise ValueError('Invalid portfolio continuation')
    returns=np.exp(np.log1p(deposit_rate)*interval)
    gains=np.exp(growth*interval);gains[0]=1.
    cache={};previous_plans=[None]*h
    def demand(log_price):
        if log_price in cache:
            _,trades,price=cache[log_price]
            return float(trades.sum())/max(price*holdings.sum(),1e-9)
        price=float(np.exp(log_price));plans=[];trades=[]
        for i in range(h):
            if mix[i]==0:plans.append(None);trades.append(0.);continue
            unit=income[i]
            y=np.exp(growth*times)-subsistence[i]/unit;y[0]=0.
            div=np.full(periods,dividend_flow/price)*(1-tax);div[0]=0.
            tail=None
            if terminal_mode=='balanced_policy':
                # Exact infinite tail conditional on constant wealth/income
                # ratios after the horizon, not an optimal Bellman value.
                gg=np.exp(growth/52);rr=np.exp(np.log1p(deposit_rate)/52)
                tail=dict(weight=np.exp(-rho*(times[-1]+1/52))/(-np.expm1(-rho/52)),
                   income=gg*(np.exp(growth*times[-1])-subsistence[i]/unit),
                   liquid_income=rr-gg,equity_income=dividend_flow/price*(1-tax))
            plan=solve((cash[i]-subsistence[i])/unit,holdings[i]*price/unit,y,returns,gains,div,weights,
                       phi=phi[i],buffer=buffer[i]*np.exp(growth*times),fee=fee,scale=52*np.exp(growth*times),risk=risk,tol=1e-8,terminal=tail,warm=previous_plans[i])
            previous_plans[i]=plan['warm']
            plans.append(plan);trades.append(mix[i]*unit*plan['transfer'][0])
        imbalance=float(sum(trades));cache[log_price]=(plans,np.array(trades),price)
        return imbalance/max(price*holdings.sum(),1e-9)
    # A tiny ex-dividend price can make D/price ~1e12 at the first trial,
    # despite a regular positive root elsewhere. One year's forecast payouts
    # supplies a numerical starting scale only: it is not a price floor, and
    # the bracket may expand below it. Budgets/objective/root tolerances do not
    # change. Zero-dividend markets keep the historical starting guess.
    trials=[]
    if search_mode=='legacy':
        center=float(np.log(max(price_guess,52*dividend_flow)));fc=demand(center);lo=hi=center;fl=fh=fc
        for _ in range(12):
            if abs(fc)<1e-10 or fl*fh<=0:break
            if fc>0:hi+=1.;fh=demand(hi)
            else:lo-=1.;fl=demand(lo)
        else:raise MarketClearingError('No equity market-clearing price bracket')
        root=center if abs(fc)<1e-10 else brentq(demand,lo,hi,xtol=1e-8,rtol=1e-10)
    elif search_mode=='feasible_scan':
        center=float(np.log(max(price_guess,52*dividend_flow)))
        valid={};last_problem=None
        def attempt(x):
            nonlocal last_problem
            try:
                v=demand(x);valid[x]=v
                trials.append(dict(log_price=float(x),relative_imbalance=float(v),status='feasible'))
                return v
            except PortfolioInfeasible as ex:
                last_problem=getattr(ex,'problem',None)
                trials.append(dict(log_price=float(x),status='conditional_infeasible',reason=str(ex)))
                return None
        root=None;bracket=None
        # Try the inherited direction first when center is feasible. If the
        # center is infeasible, explore both sides. No infeasible demand is
        # assigned a fabricated sign, and no failed KKT solve is swallowed.
        fc=attempt(center)
        for k in range(search_steps+1):
            ordered=sorted(valid)
            for x in ordered:
                if abs(valid[x])<1e-10:root=x;break
            if root is not None:break
            for a,b in zip(ordered,ordered[1:]):
                if valid[a]*valid[b]<=0:bracket=(a,b);break
            if bracket is not None:break
            if k==search_steps:break
            if fc is None:
                attempt(center+k+1);attempt(center-k-1)
            elif fc>0:attempt(center+k+1)
            else:attempt(center-k-1)
        if root is None and bracket is not None:
            try:root=brentq(demand,*bracket,xtol=1e-8,rtol=1e-10)
            except PortfolioInfeasible as ex:
                error=MarketClearingError('Conditional infeasibility inside candidate bracket; no general-equilibrium nonexistence certificate')
                error.problem=getattr(ex,'problem',{});error.market_diagnostic=dict(trials=trials,bracket=bracket)
                raise error from ex
        if root is None:
            error=MarketClearingError('No verified feasible equity-price bracket in finite scan; general-equilibrium existence undetermined')
            error.market_diagnostic=dict(trials=trials,search_steps=search_steps)
            if last_problem is not None:error.problem=last_problem
            raise error
    else:raise ValueError('Unknown equity price search')
    residual=demand(root);plans,trades,price=cache[root]
    if abs(residual)>1e-5:raise MarketClearingError(f'Equity market residual: {residual}')
    return dict(price=price,trades=trades,plans=plans,relative_imbalance=residual,price_search_trials=trials,
                consumption=np.array([cash[i] if plans[i] is None else subsistence[i]+income[i]*plans[i]['consumption'][0] for i in range(h)]),
                fees=np.array([0. if plans[i] is None else .5*fee*(trades[i]/income[i])**2/52*income[i] for i in range(h)]))

def decision_and_settlement(e,cash,other_income,subsistence,price_index,growth,tax):
    """Secondary equity trading transfers deposits between households.

    Fees are paid to bank equity; no new corporate shares or loan is created.
    Income-rule households keep their holdings. Mixed households implement a
    convex mixture of a no-trade plan and the optimal joint plan.
    """
    try:from .wealth_utility import calibrated_phi
    except ImportError:from wealth_utility import calibrated_phi
    try:from .bank_equity import change_book
    except ImportError:from bank_equity import change_book
    p=e.p;ownership=e.equity_ownership().copy()
    unit=float(price_index);inc=np.asarray(other_income)/unit
    phi=[calibrated_phi(p.wiu_epsilon,p.wiu_targets[h],p.wiu_shift_weeks,p.rho) for h in range(3)]
    rate=np.expm1(52*np.log1p((1-tax)*np.expm1(np.log1p(max(e.i_cb-p.mD,0.))/52))-np.log1p(e.pi_e)) if e.E_bank>0 else 1/(1+e.pi_e)-1
    forecast=dividend_forecast(e,unit)
    result=market(np.asarray(cash)/unit,ownership,inc,forecast,
        rate,growth,p.rho,phi,[p.wiu_shift_weeks]*3,e.equity_market_value()/unit,
        fee=p.joint_fee,years=p.joint_years,periods=p.joint_periods,mix=p.euler_share,tax=tax,risk=p.joint_risk,subsistence=np.asarray(subsistence)/unit,terminal_mode=p.joint_terminal,search_mode=p.joint_price_search,search_steps=p.joint_price_search_steps)
    wanted=result['trades']*unit;buy=np.maximum(wanted,0.);sell=np.maximum(-wanted,0.)
    amount=min(float(buy.sum()),float(sell.sum()))
    buy*=amount/max(float(buy.sum()),1e-30);sell*=amount/max(float(sell.sum()),1e-30)
    done=np.zeros(3);cap=result['price']*unit
    for seller in range(3):
        remaining=float(sell[seller])
        for buyer in range(3):
            available=float(ownership[seller])*cap
            volume=min(remaining,float(buy[buyer]),available) if p.audit_corrections else min(remaining,float(buy[buyer]))
            if volume<=0:continue
            paid=e.led.transfer(f'H{buyer}',f'H{seller}',volume)
            if abs(paid-volume)>1e-7*max(1.,volume):raise RuntimeError('Unfunded joint equity order')
            shares=float(ownership[seller]) if p.audit_corrections and paid==available else paid/cap
            ownership[buyer]+=shares;ownership[seller]-=shares
            done[buyer]+=paid;done[seller]-=paid;remaining-=paid;buy[buyer]-=paid
    fees=.5*p.joint_fee*(done/np.asarray(other_income))**2/52*np.asarray(other_income)
    for h in range(3):
        if fees[h]>e.led.dep[f'H{h}']+1e-8:raise RuntimeError('Unfunded equity transaction fee')
        e.led.dep[f'H{h}']-=fees[h];change_book(e,fees[h],'equity_transaction_fee')
    if ownership.min()<-1e-12 or abs(ownership.sum()-1)>1e-10:raise RuntimeError('Equity share conservation')
    e._equity_shares=ownership;e.pE=cap/e.equity_book();e._equity_market_value=cap
    from .equity_quote import close_auction
    close_auction(e,cap)
    e._joint_diag=dict(price=float(cap),dividend_forecast_real=float(forecast),fees=fees.tolist(),trades=done.tolist(),relative_imbalance=float(result['relative_imbalance']),
        kkt=max(x['kkt_relative'] for x in result['plans'] if x is not None),
        iterations=max(x['iterations'] for x in result['plans'] if x is not None),
        fallback=sum(x['fallback'] for x in result['plans'] if x is not None),
        binding=[0 if x is None else int(np.count_nonzero(x['liquid']<1e-8)) for x in result['plans']],
        price_search_trials=result.get('price_search_trials',[]),
        weekly_dates=int(round(52*p.joint_years)),
        phase_iterations=sum(x['phase_iterations'] for x in result['plans'] if x is not None))
    # Research7 diagnostics use normalized real quantities only. The fully
    # optimizing stratum H supplies a conditional Euler proxy; mixed/income
    # rules and future borrowing corners do not become fictitious equalities.
    try:from .closure import balanced_household,update_capital_price_forecast
    except ImportError:from closure import balanced_household,update_capital_price_forecast
    e._joint_diag.update(growth=growth,dividend_yield_pre_week=float(forecast/result['price']))
    h=2;plan=result['plans'][h]
    if plan is not None and p.euler_share[h]==1 and plan['liquid'][0]>1e-8:
        b=float(plan['liquid'][0]);a=float(plan['asset'][0]);sub=float(subsistence[h]/unit/inc[h])
        G=np.exp(growth/52)
        arguments=(b,a,G*(1-sub),forecast/result['price']*(1-tax),growth,p.rho,phi[h],p.wiu_shift_weeks,p.joint_risk)
        if p.joint_proxy_domain_guard:
            from .audit_profile import conditional_joint_proxy
            balanced=conditional_joint_proxy(e,*arguments)
        else:balanced=balanced_household(*arguments)
        if balanced is not None:
            speed=-np.expm1(-1/(52*p.joint_anchor_years))
            old=getattr(e,'_joint_anchor_log',balanced['net_log_return'])
            e._joint_anchor_log=old+speed*(balanced['net_log_return']-old)
            e._joint_balance=balanced|dict(eligible=True,liquid=b,equity=a,phi=float(phi[h]),future_liquid_corners=int(np.count_nonzero(plan['liquid']<1e-8)))
    else:
        e._joint_balance=dict(eligible=False)
    relative_price=e.p_[3]/unit
    previous=getattr(e,'_capital_real_price',relative_price)
    update_capital_price_forecast(e,np.log(relative_price/previous))
    e._capital_real_price=relative_price
    return result['consumption']*unit
