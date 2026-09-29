"""Explicit household-wealth, monetary-anchor and income-tax closures.

These are transparent prototype rules, not estimated Laubach-Williams or a
general-equilibrium interest-rate estimate. The optional buffer-stock rule
uses the same long-return gap. No balance-sheet stocks are reset.
"""
import numpy as np
WEEKS=52
PERIODS=13

def public_productivity_feedback(e,annual_output):
    """Public-service level elasticity or the preserved historical growth rule.

    In level mode a constant public/private capital ratio has no cumulative
    growth effect. The initial switch preserves the current technology level.
    """
    p=e.p
    if p.public_productivity_mode=='legacy_growth':
        ratio=e.KG/max(annual_output,1e-9)
        return p.eta_G*(ratio**p.zeta_G-e.KG_ratio0**p.zeta_G),np.ones(len(e.K))
    ratio=e.KG/max(float(e.K.sum()),1e-12)
    previous=getattr(e,'_public_ratio_previous',ratio)
    factor=(ratio/previous)**(p.public_capital_elasticity*(1-p.alpha))
    e._public_ratio_previous=ratio
    return 0.,factor

def wealth_buffer_weeks(p):
    return p.hh_buffer_weeks if p.hh_liquid_wealth_ratio is None else WEEKS*p.hh_liquid_wealth_ratio

def income_tax_rates(e):
    scale=e.tax_scale if e.p.tax_rule else 1.
    return np.clip(e.p.tauW*scale,0.,.90),float(np.clip(e.p.tauK*scale,0.,.90))

def natural_anchor(e):
    p=e.p
    if p.rstar_anchor=='joint_euler' and hasattr(e,'_joint_anchor_log'):
        try:from .closure import policy_from_net_log
        except ImportError:from closure import policy_from_net_log
        _,tax=income_tax_rates(e)
        value,attainable=policy_from_net_log(e._joint_anchor_log,p.pi_star,tax,p.mD)
        e._joint_anchor_attainable=attainable
        return value
    g=float(np.clip(getattr(e,'g_prod',p.g0/(1-float(np.mean(p.alpha)))),p.hh_growth_min,p.hh_growth_max))
    net_log=p.rho+p.sigma*g-p.hh_return_gap-p.wiu_epsilon
    if p.rstar_anchor=='ramsey':return net_log
    # Match the *weekly* after-tax deposit return at target inflation to the
    # long-horizon real return used by the household planner.
    _,tax=income_tax_rates(e)
    weekly_net=np.expm1((net_log+np.log1p(p.pi_star))/WEEKS)
    nominal_deposit=np.expm1(WEEKS*np.log1p(weekly_net/(1-tax)))
    nominal_policy=nominal_deposit+p.mD
    return nominal_policy-p.pi_star  # additive real-rate intercept in Taylor

def update_natural_rate(e,u):
    p=e.p
    innovation=p.lam_rstar*(e.pi_s-p.pi_star)-p.lam_rstar_u*(u-p.u_n)
    anchor=natural_anchor(e);e._rstar_anchor=anchor
    if p.rstar_mode=='legacy':
        updated=e.rstar_est+innovation
        desired=float(np.clip(updated,-.01,.06))
    else:
        updated=anchor+(e.rstar_est-anchor)*np.exp(-p.rstar_reversion/PERIODS)+innovation
        desired=float(np.clip(updated,anchor-p.rstar_band,anchor+p.rstar_band))
    if not p.eight_corrections:return desired
    limit=p.rate_speed_limit/PERIODS
    result=float(np.clip(desired,e.rstar_est-limit,e.rstar_est+limit))
    e._rstar_diagnostic=dict(kind='conditional_policy_proxy_not_general_equilibrium',
        anchor=float(anchor),anchor_mode=p.rstar_anchor,previous=float(e.rstar_est),
        innovation=float(innovation),raw_estimate=float(updated),bounded_estimate=desired,
        applied=result,max_step=limit,speed_limited=bool(abs(result-desired)>1e-12))
    return result

def update_taxes(e):
    """Monthly controller using only completed weekly fiscal accounts.

    D = B+AG. Since deficit = dD - dcash, balanced growth with gross debt b
    and cash k requires deficit/Y = 52*(b-k)*(1-exp(-nominal_growth/52)).
    A debt correction lowers the desired deficit when net debt is above target.
    Personal income tax rates share one multiplier; other taxes are unchanged.
    """
    p=e.p
    if not p.tax_rule or len(e.flow_history)<4:return
    rows=e.flow_history[-4:];yn=e.Y_nom_prev()
    # Nominal growth from trend real productivity and smoothed inflation;
    # bound short-run extrapolation, do not cumulate an inflation gap.
    growth=float(np.clip(getattr(e,'g_prod',p.g0/(1-float(np.mean(p.alpha))))+np.log1p(max(e.pi_s,-.5)),-.10,.20))
    net=(e.B+e.AG-e.led.dep['G'])/yn;target_net=p.b_target-p.gov_cash_ratio
    steady=52*target_net*(-np.expm1(-growth/52))
    desired=steady-p.tax_debt_feedback*(net-target_net)
    actual=np.mean([r['deficit'] for r in rows])*52/yn
    base=np.mean([r.get('household_tax_base',0.) for r in rows])*52/yn
    if base>1e-8:
        target=np.clip(e.tax_scale+(actual-desired)/base,p.tax_scale_min,p.tax_scale_max)
        e.tax_scale+=(-np.expm1(-p.tax_adjust_speed/PERIODS))*(target-e.tax_scale)
    e._tax_deficit_target=float(desired);e._tax_steady_deficit=float(steady)
    e._tax_net_debt=float(net);e._tax_base_ratio=float(base)
