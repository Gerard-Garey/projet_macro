"""Floating-rate mortgages with frozen origination LTV/amortization.

Legacy snapshots have no origination records: their single imputed cohort
per household is explicitly tagged. Construction cancellation targets its
own new contract. Interest arrears stay in the original contract. A change
in regulation cannot accelerate old principal or revalue its collateral.
Amortization is an annual fraction of remaining principal, as in research8.
"""
import numpy as np


def initialize(e):
    if hasattr(e, 'mortgage_vintages'):
        return
    e.mortgage_vintages = []
    e._mortgage_next_id = 0
    for h, amount in enumerate(e.LZ):
        if amount > 0:
            originate(e, h, float(amount), 'legacy_imputed',
                      price=float(getattr(e, 'pZ_3y', e.pZ)))


def originate(e, h, amount, kind, price=None, collateral_value=None):
    if amount <= 0:
        return None
    price = float(e.pZ if price is None else price)
    collateral_value = amount/e.p.LTV if collateral_value is None else float(collateral_value)
    if collateral_value<=0 or amount>e.p.LTV*collateral_value+1e-9*max(amount,1.):
        raise ValueError('Origination exceeds current LTV limit')
    identity = e._mortgage_next_id
    e._mortgage_next_id += 1
    e.mortgage_vintages.append(dict(id=identity, household=int(h), balance=float(amount),
        initial_principal=float(amount), origin_week=None if kind=='legacy_imputed' else e.t,
        kind=kind, ltv_initial=float(amount/collateral_value), ltv_limit_initial=float(e.p.LTV), amortization=float(e.p.mortgage_amortization),
        price_initial=price, collateral_units=float(collateral_value/price),
        default_exposure=.30 if kind=='legacy_imputed' else 1., interest_type='floating'))
    v=e.mortgage_vintages[-1]
    if e.p.mortgage_contract_mode=='finite_linear' and kind!='legacy_imputed':
        v.update(contract_mode='finite_linear',term_weeks=e.p.mortgage_term_weeks,
                 maturity_week=e.t+e.p.mortgage_term_weeks)
    if e.p.mortgage_registry:
        v.update(registry_week=e.t,registry_units=(collateral_value/e.capital_price() if kind=='construction' else v['collateral_units']),
                 delivery_week=e.t+e.p.T_Z if kind=='construction' else e.t,
                 registry_imputed=(kind=='legacy_imputed'))
    return identity


def lots(e, h):
    return [v for v in e.mortgage_vintages if v['household']==h and v['balance']>0]


def annual_amortization(e, h):
    cohort=lots(e,h)
    if all(v.get('contract_mode')!='finite_linear' for v in cohort):
        return sum(v['amortization']*v['balance'] for v in cohort)
    return sum(52*principal_due(e,v,at_week=e.t+1) if v.get('contract_mode')=='finite_linear' else v['amortization']*v['balance'] for v in cohort)


def capacity(e, h, weekly_income, interest):
    # Effective weekly interest, consistent with pay_household_debt.
    annual_interest = 52*np.expm1(np.log1p(max(interest, 0.))/52)
    budget = e.p.mortgage_service_share*max(weekly_income, 0.)*52
    existing = annual_interest*e.LZ[h]+annual_amortization(e, h)
    return max(budget-existing, 0.)/max(annual_interest+(52/e.p.mortgage_term_weeks if e.p.mortgage_contract_mode=='finite_linear' else e.p.mortgage_amortization), 1e-6)


def capitalize(e, h, amount):
    cohort = lots(e, h)
    total = sum(v['balance'] for v in cohort)
    if amount and not total:
        raise AssertionError('Mortgage arrears without contract')
    for v in cohort:
        v['balance'] += amount*v['balance']/total


def scheduled_payment(e, h, cash):
    cohort = lots(e, h)
    due = [principal_due(e,v) for v in cohort]
    total = sum(due)
    ratio = min(max(cash, 0.)/total, 1.) if total else 0.
    for v, amount in zip(cohort, due):
        v['balance'] -= amount*ratio
    return total*ratio


def cancel(e, identity, amount):
    if amount <= 0:
        return
    v = next(v for v in e.mortgage_vintages if v['id']==identity)
    if amount > v['balance']+1e-8*max(v['balance'], 1.):
        raise AssertionError('Cancellation exceeds originated construction loan')
    ratio = max(1-amount/v['balance'], 0.)
    v['collateral_units'] *= ratio
    v['initial_principal'] *= ratio
    if 'registry_units' in v:v['registry_units']*=ratio
    v['balance'] = max(v['balance']-amount, 0.)


def defaults(e):
    loss = np.zeros(3)
    if e.p.mortgage_registry:registry(e)
    for v in e.mortgage_vintages:
        collateral=v.get('effective_collateral_units',0.) if e.p.mortgage_registry else v['collateral_units']
        uncovered = max(v['balance']-e.pZ*collateral, 0.)
        amount = min(v['balance'], e.p.phi_npl/52*v['default_exposure']*uncovered)
        v['balance'] -= amount
        loss[v['household']] += amount
    return loss


def check(e):
    total = np.zeros(3)
    for v in e.mortgage_vintages:
        if not np.isfinite(v['balance']) or v['balance'] < -1e-10:
            raise AssertionError('Invalid mortgage contract balance')
        total[v['household']] += v['balance']
    residual = total-e.LZ
    if np.max(abs(residual)) > 1e-9*max(float(abs(e.LZ).max()), 1.):
        raise AssertionError(('Mortgage vintage reconciliation', residual))
    e._mortgage_residual = residual
    return residual


def redenominate(e, factor):
    for v in getattr(e, 'mortgage_vintages', []):
        for key in ('balance', 'initial_principal', 'price_initial'):
            v[key] /= factor


def principal_due(e,v,at_week=None):
    if v.get('contract_mode')!='finite_linear':return min(v['balance'],v['balance']*v['amortization']/52)
    elapsed=max((e.t if at_week is None else at_week)-v['origin_week'],0)
    target=v['initial_principal']*max(1-elapsed/v['term_weeks'],0.)
    # Missed principal is still due next week; at maturity the remaining claim
    # is all payable, never silently renewed or forgiven.
    return min(v['balance'],max(v['balance']-target,0.))

def registry(e):
    """Aggregate pro-rata allocation, NOT a fabricated property-level cadastre.

    Legacy face collateral is retained. If claimed units exceed the observed
    household stock plus construction pipeline, effective recoverable backing
    is capped pro rata; no principal or origination LTV is rewritten.
    New refinancings can pledge only unused completed housing capacity.
    """
    pool=np.asarray(e.Z,float)+np.asarray(e.pipeline_h,float).sum(axis=0)
    requested=np.zeros(3);live=[]
    for v in e.mortgage_vintages:
        if 'registry_week' not in v:
            v.update(registry_week=e.t,registry_units=v['collateral_units'],delivery_week=e.t,registry_imputed=True)
        age=max(e.t-max(v['registry_week'],v['delivery_week']),0)
        units=v['registry_units']*(1-e.p.delta_Z/52)**age if v['balance']>0 else 0.
        requested[v['household']]+=units;live.append(units)
    factor=np.minimum(1.,np.divide(pool,requested,out=np.ones(3),where=requested>0))
    effective=np.zeros(3)
    for v,q in zip(e.mortgage_vintages,live):
        v['effective_collateral_units']=q*factor[v['household']]
        effective[v['household']]+=v['effective_collateral_units']
    e._collateral_registry=dict(t=e.t,pool=pool,requested=requested,effective=effective,
                                excess=np.maximum(requested-pool,0.),allocation='aggregate_pro_rata')
    return e._collateral_registry

def unpledged_capacity(e,h):
    reg=registry(e)
    # Conservatively reserve all live claims against existing homes. New-build
    # guarantees do not supply cash-out headroom before construction delivery.
    free=max(float(e.Z[h]-reg['requested'][h]),0.)
    return e.p.LTV*e.pZ*free
