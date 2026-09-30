"""Experimental infinite-tail CRRA saving rule, weekly endogenous grids.

This is an individual planning problem, NOT an estimated household distribution.
Risk is iid on discretionary noninterest income. Subsistence is paid first;
the forecast assumes discretionary income grows at g. No random aggregate
cash flow is created. Portfolio purchases remain the engine's separate rules.
"""
from functools import lru_cache
import numpy as np
try:
    from .households import ConsumptionChoice
except ImportError:
    from households import ConsumptionChoice

def interp(x, m, c):
    x=np.asarray(x)
    # Linear extrapolation only for the Bellman operator beyond the grid;
    # the actual current decision refuses resources outside the solved grid.
    slope=(c[-1]-c[-2])/(m[-1]-m[-2])
    return np.minimum(x,np.where(x>m[-1],c[-1]+slope*(x-m[-1]),np.interp(x,m,c)))

def backward(m, c, assets, r, growth, rho, sigma, probability, loss):
    shocks=np.array([1-loss,1+probability*loss/(1-probability)])
    prob=np.array([probability,1-probability])
    gross=np.exp(r/52);gamma=np.exp(growth/52)
    nxt=gross/gamma*assets[:,None]+shocks
    cn=np.maximum(interp(nxt,m,c),1e-14)
    mu=np.exp(-rho/52)*gross*gamma**(-sigma)*(cn**(-sigma)@prob)
    cc=mu**(-1/sigma)
    return np.r_[0,assets+cc],np.r_[0,cc]

@lru_cache(maxsize=32)
def stationary_policy(sigma=1.,rho=.01,growth=.0225,gap=.01,probability=.02,loss=.9,points=500,max_assets=1500.):
    if not np.all(np.isfinite([sigma,rho,growth,gap,probability,loss,points,max_assets])) or rho<=(1-sigma)*growth or not(sigma>0 and rho>0 and 0<gap<=.05 and 0<probability<1 and 0<loss<1 and points>=100 and max_assets>10):
        raise ValueError('Invalid buffer-stock parameters / strict growth impatience required')
    r=rho+sigma*growth-gap
    # Strict GIC applies here: no permanent-income shocks, iid transitory risk.
    factor=np.exp(-gap/(52*sigma))
    assets=np.r_[0,np.geomspace(1e-5,max_assets,points-1)]
    m=np.r_[0,assets[1:]+1];c=m.copy()
    error=np.inf
    for iteration in range(1,60001):
        mm,cc=backward(m,c,assets,r,growth,rho,sigma,probability,loss)
        error=float(np.max(np.abs(interp(assets,m,c)-interp(assets,mm,cc))))
        m,c=mm,cc
        if error<1e-8:break
    if error>=1e-8:raise RuntimeError('Stationary household policy did not converge')
    m.flags.writeable=False;c.flags.writeable=False;assets.flags.writeable=False
    return m,c,assets,dict(iterations=iteration,policy_error=error,growth_impatience=factor,long_net_log_return=r)

@lru_cache(maxsize=1024)
def transition_policy(sigma,rho,growth,gap,probability,loss,spread,rate_reversion,front_years=10.):
    # sigma=1 makes the normalized stationary problem independent of g.
    base_growth=0. if sigma==1. else growth
    m,c,assets,info=stationary_policy(sigma,rho,base_growth,gap,probability,loss)
    long=rho+sigma*growth-gap
    for t in np.arange(round(front_years*52)-1,-1,-1)/52:
        r=long+spread*np.exp(-t/rate_reversion)
        m,c=backward(m,c,assets,r,growth,rho,sigma,probability,loss)
    return m,c,info

def plan_buffer_stock(cash,noninterest_income,subsistence,annual_deposit_rate,tax_rate,
                      expected_inflation,sigma,rho,growth,gap=.01,probability=.02,
                      loss=.9,rate_reversion=2.):
    values=[cash,noninterest_income,subsistence,annual_deposit_rate,tax_rate,expected_inflation,
            sigma,rho,growth,gap,probability,loss,rate_reversion]
    if not np.all(np.isfinite(values)) or min(cash,subsistence)<0 or not 0<=tax_rate<1 or expected_inflation<=-1 or rate_reversion<=0:
        raise ValueError('Invalid buffer-stock forecast')
    net_week=(1+max(annual_deposit_rate,0.))**(1/52)-1
    r=52*np.log1p((1-tax_rate)*net_week)-np.log1p(expected_inflation)
    discretionary=noninterest_income-subsistence
    if discretionary<=0 or cash<=subsistence:
        expense=min(cash,max(noninterest_income,0.))
        return expense,ConsumptionChoice(max(expense-subsistence,0),1,0.,False),float(np.expm1(r))
    spread=r-(rho+sigma*growth-gap)
    # Quantization of annual rate spread to 1bp is a numerical approximation,
    # separately checked against unrounded policies in validation.
    m,c,info=transition_policy(sigma,rho,round(growth,5),gap,probability,loss,round(spread,4),rate_reversion)
    resources=(cash-subsistence)/discretionary
    if resources>m[-1]:raise ValueError('Household resources exceed buffer-stock grid')
    consumption=float(interp(resources,m,c))*discretionary
    expense=min(cash,subsistence+consumption)
    return expense,ConsumptionChoice(consumption,1 if cash-expense<1e-10 else 0,consumption,True),float(np.expm1(r))
