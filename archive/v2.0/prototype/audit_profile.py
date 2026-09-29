"""Audit 2026-09: explicit, reversible mechanisms, with no wealth/belief reset.

Defaults preserve old profiles. enable() selects the new accounting/numeraire
profile; pricing and funded wage agreements remain explicit decisions.
"""
import numpy as np

PROFILE='audit-continuous-20260913'

def enable(e):
    from .eight_points import enable as eight_enable
    eight_enable(e)
    first=not getattr(e,'audit_profile',None)
    e.p.audit_corrections=True
    e.p.crisis_accounting='continuous'
    e.p.neutral_redenomination=True
    e.p.joint_proxy_domain_guard=True
    e.audit_profile=PROFILE
    if not hasattr(e,'_audit_unit'):e._audit_unit=1.
    if not hasattr(e,'wage_agreements'):e.wage_agreements=[]
    if not hasattr(e,'audit_history'):e.audit_history=[]
    if not hasattr(e,'recovery_count'):e.recovery_count=0
    if first:
        e.events.append(dict(t=e.t,event='audit_migration',profile=PROFILE,
            inherited_collapsed=bool(e.collapsed),stocks_changed=False,
            note='Existing survival losses and imputed contracts retained; future weeks use continuous accounts.'))
    return e

def conditional_joint_proxy(e,*args):
    """A feasible portfolio need not admit a balanced-growth Euler proxy.

    A negative labor surplus can be financed by existing wealth. It invalidates
    this auxiliary interior diagnostic, not the already solved household budget.
    Retain the previous proxy estimate and explicitly record the unavailable
    observation; never reset the anchor, wealth or household plan.
    """
    from .closure import balanced_household
    try:return balanced_household(*args)
    except ValueError as exc:
        e._joint_balance=dict(eligible=False,reason=str(exc),
            net_income=float(args[2]),previous_anchor_retained=hasattr(e,'_joint_anchor_log'))
        return None

def enter_crisis(e):
    if e.collapsed:return
    e.collapsed=True;e.collapses+=1;e.collapse_t=e.t;e.recovery_count=0
    e.events.append(dict(t=e.t,event='continuous_crisis_entry',expectation=float(e.pi_e),
                         credibility=float(e.cred),stocks_changed=False))

def recovery(e):
    """A status changes after observed recovery; it never causes recovery."""
    if not e.collapsed:return
    loans=e.Loans.sum()+ (e.LZ.sum()+e.LE if e.p.assets else 0.)
    ok=(abs(e.pi_e)<=e.p.crisis_recovery_inflation and abs(e.pi)<=e.p.crisis_recovery_inflation
        and e.E_bank>=e.p.kappa_CAR*loans and e._wage_shortfall==0.
        and not np.any(e.zombie>0) and e.s_surv<.01)
    e.recovery_count=e.recovery_count+1 if ok else 0
    if e.recovery_count>=e.p.crisis_recovery_weeks:
        e.collapsed=False;e.cap_weeks=0
        e.events.append(dict(t=e.t,event='continuous_crisis_recovery',observed_weeks=e.recovery_count,stocks_changed=False))

def schedule_wage_agreement(e,indexation=.5,duration_weeks=156,transfer_share=.01):
    """Time-limited agreement financed by H2, compensating H0 via Treasury.

    A design experiment: compensation is a transparent negotiated levy, not an
    estimated welfare equivalent. No free indexation cut when funding is absent.
    """
    if not e.p.audit_corrections:raise ValueError('Activate audit profile first')
    if e.t%4:raise ValueError('Agreements are decided at four-week decision dates')
    if not np.isfinite([indexation,transfer_share]).all() or not 0<=indexation<=1 or not 0<transfer_share<=e.p.agreement_max_share:
        raise ValueError('Invalid agreement or unfunded compensation')
    if not isinstance(duration_weeks,int) or duration_weeks<4 or duration_weeks%4:
        raise ValueError('Agreement duration must be positive four-week periods')
    start=e.t+e.p.agreement_notice_weeks;end=start+duration_weeks
    if any(start<a['end'] and end>a['start'] for a in e.wage_agreements):raise ValueError('Overlapping wage agreements')
    a=dict(decision=e.t,start=start,end=end,indexation=float(indexation),transfer_share=float(transfer_share),
           nominal_paid=0.,funding_shortfall_weeks=0)
    e.wage_agreements.append(a);e.events.append(dict(t=e.t,event='wage_agreement_scheduled',**a))
    return dict(a)

def agreement_payment(e):
    e._agreement_indexation=e.p.varpi_w;e._agreement_paid=0.;e._agreement_due=0.
    income=np.zeros(3)
    for a in e.wage_agreements:
        if a['start']<=e.t<a['end']:
            due=a['transfer_share']*e.Y_nom_prev()/52
            paid=min(due,e.p.agreement_deposit_cap*max(e.led.dep['H2'],0.))
            e.led.transfer('H2','G',paid);e.led.transfer('G','H0',paid)
            coverage=paid/due if due>0 else 0.
            e._agreement_indexation=e.p.varpi_w*(1-coverage)+a['indexation']*coverage
            e._agreement_paid=paid;e._agreement_due=due
            income[0]=paid;income[2]=-paid
            a['nominal_paid']+=paid;a['funding_shortfall_weeks']+=int(paid<due)
            break
    return income

def marginal_order_prices(e,forecast_output,forecast_labor):
    """Short-run marginal cost, capital held fixed; zero output has no division.

    This is an explicit structural alternative, not a recalibrated average cost.
    Accounting still deducts actual depreciation and actual paid wages.
    """
    p=e.p;q=np.asarray(forecast_output);labor=np.asarray(forecast_labor)
    marginal_labor=np.divide(labor,(1-p.alpha)*q,out=np.zeros_like(q),where=q>0)
    cost=(p.a*e.p_[:,None]).sum(axis=0)+e.W*(1+p.tauS)*marginal_labor
    return (1+e.markup)*cost

def after_week(e,Y,x_obt,price_target):
    """Actual delivered consumption and constraints, not merely planned budgets."""
    e.audit_history.append(dict(t=e.t,collapsed=bool(e.collapsed),
        output=np.asarray(Y).tolist(),delivered_consumption=np.asarray(x_obt).tolist(),
        price_target=np.asarray(price_target).tolist(),price_unit=float(e._audit_unit),
        compensation_paid=float(getattr(e,'_agreement_paid',0.)),
        compensation_due=float(getattr(e,'_agreement_due',0.)),
        effective_indexation=float(getattr(e,'_agreement_indexation',e.p.varpi_w)),
        corporate_credit_closed=(e.Loans>=(e.p.ell_bar+.4)*e.capital_price()*e.K).tolist(),
        recovery_count=int(e.recovery_count)))

def apply_action(e,kind,**kwargs):
    if kind=='wage_agreement':return schedule_wage_agreement(e,**kwargs)
    if kind=='corporate_resolution':
        from .workplan import schedule_resolution
        return schedule_resolution(e,**kwargs)
    if kind=='stop_monetization':return e.reform()
    raise ValueError('Unknown action')
