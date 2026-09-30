"""Research7 partial-equilibrium closures, not a GE natural-rate solver.

Weekly joint-utility Euler conditions and a cost-minimizing capital target.
The capital target is conditional on expected sales, wages and user cost;
it is not marginal q, and secondary equity purchases do not fund investment.
"""
import numpy as np

def balanced_household(liquid, equity, income, dividend, growth, rho, phi,
                       buffer=1., risk=.01, scale=52.):
    """Weekly real quantities; b,a are last-period stocks in a common unit.

    c=income+(R-G)b+D*a, 1=phi*c/(G*(b+a+buffer))+beta*R/G.
    Wealth services are on post-decision stocks G*b,G*a (and growing buffer).
    The two Euler equations are interior conditions. No rate is imposed here.
    """
    b,a,y,D=liquid,equity,income,dividend
    if min(b,a,D,phi,risk)<0 or y<=0 or buffer<=0 or scale<=0:
        raise ValueError('Invalid balanced household inputs')
    G=np.exp(growth/52);beta=np.exp(-rho/52)
    k=phi/(G*(b+a+buffer))
    R=(1-k*(y-G*b+D*a))/(beta/G+k*b)
    c=y+(R-G)*b+D*a
    if R<=0 or c<=0 or not np.isfinite([R,c]).all():
        raise ValueError('No feasible interior balanced household return')
    # At date t post-decision stocks and income scales have grown by G.
    wealth_wedge=k*c
    equity_residual=1-wealth_wedge+risk*a*c/(G*scale**2)-beta*(G+D)/G
    return dict(R=float(R),net_log_return=float(52*np.log(R)),consumption=float(c),
                wealth_wedge=float(wealth_wedge),equity_residual=float(equity_residual))

def policy_from_net_log(net_log, inflation, tax, deposit_margin):
    """Unconstrained Taylor intercept, matching weekly deposit taxation.

    Negative nominal deposits are unattainable in this model. The caller
    records this fact; do not replace the desired intercept by a fake floor.
    """
    net_nominal=np.expm1((net_log+np.log1p(inflation))/52)
    gross_weekly=net_nominal/(1-tax)
    nominal_deposit=np.expm1(52*np.log1p(gross_weekly))
    return float(nominal_deposit+deposit_margin-inflation),bool(nominal_deposit>=0)

def structural_growth(p):
    """Exact log trend induced by monthly technology updates, fixed labor."""
    if p.tfp_trend_mode=='balanced_sectoral':
        return np.full(p.nsec,13*np.log1p(p.g0/(13*(1-np.mean(p.alpha)))))
    return 13*np.log1p(p.g0/13)/(1-p.alpha)

def capital_target(output, technology, human, wage, alpha, payroll_tax, price_k, user_cost):
    """Minimize 52*W*(1+tau)*L(K,Q) + pK*uc*K, holding weekly Q fixed.

    Inputs are current weekly technology/output/wages, annual capital cost.
    Positive user cost gives a unique finite target for 0<alpha<1.
    """
    output,technology,wage,alpha,user_cost=map(np.asarray,(output,technology,wage,alpha,user_cost))
    if np.any(output<=0) or np.any(technology<=0) or np.any(wage<=0) or np.any(user_cost<=0) or price_k<=0 or human<=0 or np.any((alpha<=0)|(alpha>=1)):
        raise ValueError('Capital cost minimization requires positive inputs and user cost')
    return (52*wage*(1+payroll_tax)*alpha/((1-alpha)*price_k*user_cost))**(1-alpha)*output/(technology*human**(1-alpha))

def taxed_debt_cost(loan_real,inflation,marginal_tax):
    """Annual real log cost of a nominal, weekly deductible coupon.

    The expected nominal loan rate is reconstructed from the investment
    block's real-rate forecast and expected inflation. There is no shield in
    a loss regime (the engine has neither refunds nor loss carryforwards).
    """
    tax=np.asarray(marginal_tax,float)
    if loan_real<=-1 or inflation<=-1 or np.any((tax<0)|(tax>=1)):
        raise ValueError('Invalid after-tax debt forecast')
    nominal_week=np.expm1((np.log1p(loan_real)+np.log1p(inflation))/52)
    return 52*np.log1p((1-tax)*nominal_week)-np.log1p(inflation)

def investment_plan(e,output,price_k,loan_real,leverage,bank_factor):
    p=e.p;growth=structural_growth(p)
    relative_growth=float(getattr(e,'_capital_relative_growth',0.)) if p.capital_price_forecast=='adaptive' else 0.
    if p.capital_finance=='legacy_loan':
        funding=np.full(p.nsec,loan_real+p.rho_E)
        uc=funding+p.delta
        equity_return=0.  # unused in this ablation; keep snapshots finite
        marginal_tax=np.zeros(p.nsec);tax_base=np.zeros(p.nsec)
        debt_cost=np.full(p.nsec,loan_real)
    else:
        j=e._joint_diag
        # The same dividend forecast and real capital-gain forecast as the
        # households. This is a forecast hurdle, not an estimated risk premium.
        equity_return=52*np.log(np.exp(j['growth']/52)+j['dividend_yield_pre_week'])
        debt_weight=np.clip(e.Loans/np.maximum(price_k*e.K,1e-12),0.,1.)
        nominal_week=np.expm1((np.log1p(loan_real)+np.log1p(e.pi_e))/52)
        tax_base=e.Pi_brut_bar-p.delta/52*price_k*e.K-nominal_week*e.Loans
        # Conditional forecast of the same accrual tax base as model.py.
        # At the kink use the loss-side derivative (zero); no tax refund is
        # invented. Cash rationing of remittances remains in the main ledger.
        marginal_tax=p.tauPi*(tax_base>0)
        debt_cost=taxed_debt_cost(loan_real,e.pi_e,marginal_tax)
        funding=debt_weight*debt_cost+(1-debt_weight)*equity_return
        # Replacement-cost depreciation and the profit-tax gross-up use the
        # same conditional tax regime. This remains a static user-cost target.
        uc=(funding-relative_growth)/(1-marginal_tax)+p.delta
    finite=uc>0
    # A nonpositive user cost has no finite unconstrained static optimum.
    # Use the existing order-cap limit in that regime and record it explicitly.
    target=capital_target(output,e._A_eff,e.H,e.W,p.alpha,p.tauS,price_k,np.where(finite,uc,1.))
    loggap=np.where(finite,np.log(target/e.K),0.)
    trend_week=np.expm1(growth/52)
    correction=-np.expm1(-p.capital_adjust_speed/52)*loggap
    net=trend_week+correction
    net=np.where(finite,net,p.inv_cap*p.delta/52)
    # Finance constraints damp expansion, not the retirement of excess stock.
    net=np.where(net>0,net*leverage*bank_factor,net)
    net=np.clip(net,-p.delta/52,p.inv_cap*p.delta/52)
    orders=e.K*(p.delta/52+net)
    e._capital_diag=dict(target_ratio=np.where(finite,target/e.K,0.),finite=finite,
        user_cost=uc,funding=funding,relative_growth=relative_growth,
        debt_cost=debt_cost,marginal_tax=marginal_tax,expected_tax_base=tax_base,
        equity_return=equity_return,structural_growth=growth,net_annual=net*52)
    return orders

def update_capital_price_forecast(e,real_price_step):
    """Observe realized relative equipment inflation, not the policy rate."""
    speed=-np.expm1(-1/(52*e.p.capital_price_years))
    old=float(getattr(e,'_capital_relative_growth',0.))
    e._capital_relative_growth=old+speed*(52*real_price_step-old)
