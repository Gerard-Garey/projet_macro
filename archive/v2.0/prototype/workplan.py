"""Explicit work-plan profile and costed resolution experiments.

No calibration is changed by import or old-snapshot load. Pricing and contract
rules are opt-in. The resolution action is a negotiated corporate write-down,
not a claim that it produces recovery or that the bank can absorb the loss.
"""
import math
import numpy as np

PROFILE='workplan-20260913'

def enable(e,pricing=False,mortgages=False):
    from .audit_profile import enable as audit_enable
    audit_enable(e)
    first=not getattr(e,'workplan_profile',None)
    e.p.precise_fiscal_deltas=True
    e.p.joint_price_search='feasible_scan'
    if pricing:e.p.pricing_cost_mode='capacity_average'
    if mortgages:
        e.p.mortgage_contract_mode='finite_linear';e.p.mortgage_registry=True
        from .mortgage_vintages import registry
        registry(e)
    if not hasattr(e,'resolution_actions'):e.resolution_actions=[]
    e.workplan_profile=PROFILE
    if first:e.events.append(dict(t=e.t,event='workplan_migration',stocks_changed=False,profile=PROFILE,pricing=pricing,new_mortgages=mortgages))
    return e

def capacity_prices(e,capacity,output,wages,capital,replacement_price):
    """Allocate committed weekly costs over capacity BEFORE input rationing.

    This is a short-run pricing design, not an IFRS-compliant inventory system.
    Actual wages and depreciation stay in the existing profit and SFC accounts.
    Idle costs are reported, never erased. Zero capacity retains the quote.
    """
    q=np.asarray(capacity,float);actual=np.asarray(output,float)
    fixed=np.asarray(wages)+e.p.delta/52*replacement_price*np.asarray(capital)
    input_unit=e.p.a.T@e.p_
    allocated=np.divide(fixed,q,out=np.zeros_like(q),where=q>0)
    target=np.where(q>0,(1+e.markup)*(input_unit+allocated),e.p_)
    absorbed=np.minimum(np.divide(actual,q,out=np.zeros_like(q),where=q>0),1.)*fixed
    e._capacity_costs=dict(capacity=q.copy(),actual=actual.copy(),committed=fixed.copy(),absorbed=absorbed,
                           idle=fixed-absorbed,nominal_unit=float(getattr(e,'_audit_unit',1.)))
    return target

def schedule_resolution(e,sector,haircut):
    if not e.p.audit_corrections or e.t%4:raise ValueError('Resolution needs audit profile and a decision date')
    if not isinstance(sector,int) or not 0<=sector<4 or not np.isfinite(haircut) or not 0<haircut<=e.p.resolution_max_haircut:
        raise ValueError('Invalid negotiated haircut')
    if not hasattr(e,'resolution_actions'):e.resolution_actions=[]
    if any(a['sector']==sector and e.t-a['decision']<e.p.resolution_cooldown_weeks for a in e.resolution_actions):
        raise ValueError('Resolution cooldown or pending action')
    a=dict(decision=e.t,execution=e.t+e.p.resolution_notice_weeks,sector=sector,haircut=float(haircut),
           nominal_ceiling=float(e.Loans[sector]*haircut),status='pending',written_off=0.,nominal_unit=float(getattr(e,'_audit_unit',1.)))
    e.resolution_actions.append(a);e.events.append(dict(t=e.t,event='resolution_scheduled',**a))
    return dict(a)

def execute_resolutions(e):
    from .bank_equity import change_book
    for a in e.resolution_actions:
        if a['status']!='pending' or e.t<a['execution']:continue
        j=a['sector'];amount=min(float(e.Loans[j]*a['haircut']),a['nominal_ceiling'])
        # Creditor loss and debtor gain; no cash, real capital or beliefs change.
        e.Loans[j]-=amount;change_book(e,-amount,'negotiated_corporate_writeoff')
        a['written_off']=amount;a['status']='executed'
        e.events.append(dict(t=e.t,event='resolution_executed',sector=j,amount=amount,bank_equity_after=float(e.E_bank),cash_created=0.,nominal_unit=float(getattr(e,'_audit_unit',1.))))

def redenominate(e,factor):
    for a in e.resolution_actions:
        a['nominal_ceiling']/=factor;a['written_off']/=factor
        if 'nominal_unit' in a:a['nominal_unit']/=factor
    if hasattr(e,'_capacity_costs'):
        for k in ('committed','absorbed','idle'):e._capacity_costs[k]/=factor
        e._capacity_costs['nominal_unit']/=factor
