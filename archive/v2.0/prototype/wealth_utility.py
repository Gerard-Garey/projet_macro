"""Concave finite-horizon wealth-in-utility problem, actual returns in budgets.

Objective: sum beta**t [log(c[t]) + phi[t]*log(s[t]+buffer[t])].
Budget: c[t] = R[t-1]*s[t-1] + income[t] - subsistence[t] - s[t],
with cash replacing the first term at t=0. s>=0, R[-1]*s[-1]>=terminal.
The Newton Hessian in post-consumption savings s is tridiagonal. No fictitious
return, cash reset, consumption multiplier or unconstrained Euler integration.
"""
import numpy as np
from scipy.linalg import solveh_banded
try:
    from .households import initial_consumption,ConsumptionChoice
except ImportError:
    from households import initial_consumption,ConsumptionChoice

def optimum(cash,income,returns,phi=0.,buffer=1.,subsistence=0.,terminal=0.,rho=.01,dt=1/52,warm=None,tol=2e-9,maxiter=100):
    y=np.asarray(income,dtype=float);n=len(y)
    R=np.broadcast_to(returns,y.shape).astype(float)
    B=np.broadcast_to(buffer,y.shape).astype(float);ph=np.broadcast_to(phi,y.shape).astype(float)
    subs=np.broadcast_to(subsistence,y.shape).astype(float)
    if n<2 or not all(np.all(np.isfinite(x)) for x in [y,R,B,ph,subs,[cash,terminal,rho,dt]]) or cash<0 or terminal<0 or np.any(R<=0) or np.any(B<=0) or np.any(ph<0) or np.any(subs<0) or rho<0 or dt<=0:
        raise ValueError('Invalid wealth-utility problem')
    w=np.exp(-rho*dt*np.arange(n));net=y-subs;lo=np.zeros(n);lo[-1]=terminal/R[-1]
    def consumption(s):return np.r_[cash,R[:-1]*s[:-1]]+net-s
    # The old prefix solver supplies a feasible interior start, not the new
    # optimum. Reducing its positive surplus slightly keeps all budgets safe.
    if warm is not None and len(warm)==n and np.all(warm>=lo) and np.all(consumption(warm)>1e-12):
        s=np.asarray(warm).copy()
    else:
        seed=initial_consumption(cash,y,R,1.,rho,dt,subs,terminal)
        if not seed.feasible or seed.surplus<=1e-14:raise ValueError('Infeasible positive-surplus consumption')
        logR=np.r_[0,np.cumsum(np.log(R))];D=np.exp(-logR[:-1])
        cc=seed.surplus*(1-1e-7)*np.exp(logR[:-1]-rho*dt*np.arange(n))
        s=np.exp(logR[:-1])*(cash+np.cumsum(D*(net-cc)))
        s=np.maximum(s,lo)
    def obj(s,c):return -float(w@(np.log(c)+ph*np.log(s+B)))
    for it in range(maxiter):
        c=consumption(s)
        if np.any(c<=0):raise RuntimeError('Lost feasible consumption in Newton method')
        mu=w/c;g=mu-w*ph/(s+B);g[:-1]-=R[:-1]*mu[1:]
        active=(s-lo<1e-8)&(g>=0)
        projected=np.where(active,0,g)
        residual=float(np.max(abs(projected)/np.maximum(mu,1e-12)))
        if residual<tol:
            return c,s,dict(iterations=it,kkt_relative=residual,binding=int(np.count_nonzero(active)),objective=-obj(s,c))
        diag=w/c**2+w*ph/(s+B)**2;diag[:-1]+=R[:-1]**2*w[1:]/c[1:]**2
        off=-R[:-1]*w[1:]/c[1:]**2
        # Preserve the cheap local active-set step for ordinary problems.
        # If active bounds keep arriving, switch to the global bound-QP step.
        if it<6:
            for _ in range(n+1):
                dd=diag.copy();oo=off.copy();gg=g.copy();dd[active]=1;gg[active]=0
                oo[active[:-1]|active[1:]]=0
                band=np.zeros((2,n));band[0]=dd;band[1,:-1]=oo
                direction=solveh_banded(band,-gg,lower=True,check_finite=False)
                extra=(s-lo<1e-8)&(direction<0)&~active
                if not np.any(extra):break
                active|=extra
        else:
            # Solve the bound-constrained quadratic Newton subproblem. A warm
            # start can require hundreds of future borrowing bounds to bind at
            # once. Fix their displacement to lo-s (not zero), then solve the
            # reduced tridiagonal system, and release negative multipliers.
            seen_active=set()
            for _ in range(2*n+1):
                fixed=np.where(active,lo-s,0.)
                gg=g+diag*fixed
                gg[:-1]+=off*fixed[1:];gg[1:]+=off*fixed[:-1]
                dd=diag.copy();oo=off.copy();dd[active]=1;gg[active]=-fixed[active]
                oo[active[:-1]|active[1:]]=0
                band=np.zeros((2,n));band[0]=dd;band[1,:-1]=oo
                direction=solveh_banded(band,-gg,lower=True,check_finite=False)
                extra=(s+direction<lo-1e-12)&~active
                if np.any(extra):active|=extra;continue
                multiplier=g+diag*direction
                multiplier[:-1]+=off*direction[1:];multiplier[1:]+=off*direction[:-1]
                release=active&(multiplier < -1e-10*np.maximum(mu,1e-12))
                if np.any(release):
                    signature=active.tobytes()
                    if signature in seen_active:
                        idx=np.argmin(np.where(release,multiplier/np.maximum(mu,1e-12),np.inf));active[idx]=False
                    else:
                        seen_active.add(signature);active[release]=False
                    continue
                break
            else:raise RuntimeError('Bound-constrained Newton subproblem did not converge')
        dc=np.r_[0,R[:-1]*direction[:-1]]-direction
        alpha=1.
        neg=direction<0
        if np.any(neg):alpha=min(alpha,float(np.min((s[neg]-lo[neg])/(-direction[neg]))))
        negc=dc<0
        if np.any(negc):alpha=min(alpha,.995*float(np.min(c[negc]/(-dc[negc]))))
        value=obj(s,c);slope=float(g@direction)
        if alpha<1e-14 or slope>=0:raise RuntimeError(f'Wealth solver stalled: KKT={residual}')
        for _ in range(45):
            trial=np.maximum(s+alpha*direction,lo);ct=consumption(trial)
            if np.all(ct>0) and obj(trial,ct)<=value+1e-4*alpha*slope+1e-12:break
            alpha*=.5
        else:raise RuntimeError('Wealth-utility line search failed')
        s=trial
    raise RuntimeError(f'Wealth-utility convergence limit: {residual}')

def calibrated_phi(epsilon,target_years,shift_weeks=1.,rho=.01,external_target_years=0.):
    """Exact weekly log-utility BGP calibration, c=1+(R/G-1)*s.
    target is post-consumption savings / annual noninterest income. It is a
    calibration point, never a cash constraint or a stock-reset instruction.
    """
    if not np.all(np.isfinite([epsilon,target_years,shift_weeks,rho,external_target_years])) or rho<0 or external_target_years<0:
        raise ValueError('Invalid wealth-utility calibration')
    s=52*target_years;x=np.exp((rho-epsilon)/52);c=1+(x-1)*s
    if not 0<=epsilon<=.08 or target_years<=0 or shift_weeks<=0 or c<=0:
        raise ValueError('Infeasible wealth-utility calibration')
    return float((1-np.exp(-rho/52)*x)*(s+52*external_target_years+shift_weeks)/c)

def plan_wealth(cash,noninterest_income,subsistence,annual_deposit_rate,tax_rate,expected_inflation,
                sigma,rho,growth,horizon_years=20.,terminal_buffer_weeks=234.,rate_reversion=2.,
                epsilon=.03,target_years=1.35,shift_weeks=1.,warm=None,utility_scale=1.,return_mode='anchored',external_wealth=0.,external_target_years=0.):
    if sigma!=1.:raise ValueError('Wealth-utility solver currently requires log consumption (sigma=1)')
    if return_mode not in ('anchored','current'):raise ValueError('Invalid return expectation mode')
    scalars=[cash,noninterest_income,subsistence,annual_deposit_rate,tax_rate,expected_inflation,
             rho,growth,horizon_years,terminal_buffer_weeks,rate_reversion,epsilon,target_years,shift_weeks,utility_scale,external_wealth,external_target_years]
    if (not np.all(np.isfinite(scalars)) or cash<0 or subsistence<0 or rho<0
        or not 0<=tax_rate<=1 or expected_inflation<=-1 or not 0<horizon_years<=100
        or terminal_buffer_weeks<0 or rate_reversion<=0 or not 0<=utility_scale<=1
        or abs(growth)*horizon_years>100 or external_wealth<0 or external_target_years<0):
        raise ValueError('Invalid wealth-utility forecast inputs')
    phi=utility_scale*calibrated_phi(epsilon,target_years,shift_weeks,rho,external_target_years)
    netweek=np.expm1(np.log1p(max(annual_deposit_rate,0.))/52)
    real_log=np.log1p((1-tax_rate)*netweek)-np.log1p(expected_inflation)/52
    if noninterest_income<=0 or cash<=subsistence:
        expense=min(cash,max(noninterest_income,0.))
        return expense,ConsumptionChoice(max(expense-subsistence,0),1,0,False),float(np.expm1(real_log*52)),None,dict(fallback=True)
    unit=noninterest_income;n=max(2,round(horizon_years*52));t=np.arange(n)/52
    growth_income=np.exp(growth*t);y=growth_income.copy();y[0]=0
    long=real_log if return_mode=='current' else (rho+growth-epsilon)/52
    R=np.exp(long+(real_log-long)*np.exp(-t/rate_reversion))
    terminal=terminal_buffer_weeks*np.exp(growth*horizon_years)
    old=None if warm is None else warm[0]*warm[1]/unit
    try:
        c,s,diag=optimum(cash/unit,y,R,phi,(shift_weeks+external_wealth/unit)*growth_income,subsistence/unit,terminal,rho,warm=old)
    except ValueError as ex:
        if str(ex)!='Infeasible positive-surplus consumption':raise
        expense=min(cash,max(noninterest_income,0.))
        return expense,ConsumptionChoice(max(expense-subsistence,0),1,0,False),float(np.expm1(real_log*52)),None,dict(fallback=True)
    expense=min(cash,subsistence+unit*c[0])
    diag.update(phi=phi,actual_real_return=float(np.expm1(real_log*52)),long_net_log_return=long*52,first_surplus_growth=float(52*np.log(c[1]/c[0])))
    return expense,ConsumptionChoice(float(c[0]*unit),diag['binding'],float(c[0]*unit),True),float(np.expm1(real_log*52)),(s,unit),diag
