"""Unlisted bank equity at net book value, with limited household liability.

Existing snapshots implicitly allocate bank dividends by omega; migration
recognizes those claims without a cash flow. New subscriptions issue shares
at pre-money book value. Government rescues retain the existing model's
capital-transfer policy only in compatibility mode. The eight-point profile
issues explicit public shares. Holdings are nontradable institutional claims,
not a household portfolio choice or spendable money.
"""
import numpy as np


def ownership(e):
    return np.asarray(getattr(e,'_bank_shares',e.p.omega),float).copy()


def claims(e):
    return ownership(e)*max(float(e.E_bank),0.)


def public_claim(e):
    return float(getattr(e,'_bank_public_share',0.))*max(float(e.E_bank),0.)


def balance(e):
    issued=max(float(e.E_bank),0.)
    return dict(household_claims=claims(e),issued_equity=issued,
                bank_net_after_issued_equity=float(e.E_bank)-issued,
                public_equity=public_claim(e),valuation='net_book_value_limited_liability',
                holding_rule='fixed_nontradable_institutional_claim',
                spendable_bank_wealth=np.zeros(3),
                private_dividends=np.asarray(getattr(e,'_bank_dividends_last',np.zeros(3))).copy())

def begin_reconciliation(e):
    e._bank_journal=dict(opening_book=float(e.E_bank),opening_claims=claims(e),opening_public=public_claim(e),entries=[])
    if e.p.bank_reconciliation_mode=='transaction_replay':
        e._bank_journal['precision_trace']=dict(opening=float(e.E_bank),operations=[])


def _record(e,amount,kind,before_claims,before_public):
    if hasattr(e,'_bank_journal'):
        e._bank_journal['entries'].append(dict(kind=kind,book_flow=float(amount),
                                             claim_flow=claims(e)-before_claims,public_flow=public_claim(e)-before_public))
        if 'precision_trace' in e._bank_journal:
            e._bank_journal['precision_trace']['operations'].append(dict(op='add',value=float(amount)))


def change_book(e,amount,kind):
    """Journal a specified bank income, expense or default without changing it."""
    before=claims(e);pub=public_claim(e);e.E_bank+=amount;_record(e,amount,kind,before,pub)


def reconcile(e):
    """Opening stock + separately journaled flows = closing stock, by holder.

    Income retained by the bank revalues household book-value claims; it is
    not a household cash receipt. Insolvency losses beyond limited liability
    remain in the bank's residual net worth. No residual is plugged.
    """
    j=e._bank_journal;groups={}
    for entry in j['entries']:
        kind=entry['kind']
        if kind not in groups:groups[kind]=dict(book_flow=0.,claim_flow=np.zeros(3),public_flow=0.)
        groups[kind]['book_flow']+=entry['book_flow'];groups[kind]['claim_flow']+=entry['claim_flow']
        groups[kind]['public_flow']+=entry.get('public_flow',0.)
    book_flows=sum(x['book_flow'] for x in groups.values())
    claim_flows=sum((x['claim_flow'] for x in groups.values()),np.zeros(3))
    result=dict(opening_book=j['opening_book'],closing_book=float(e.E_bank),
        opening_claims=j['opening_claims'],closing_claims=claims(e),flows=groups,
        book_residual=float(e.E_bank-j['opening_book']-book_flows),
        household_claim_residual=claims(e)-j['opening_claims']-claim_flows,
        public_claim_residual=float(public_claim(e)-j.get('opening_public',0.)-sum(x['public_flow'] for x in groups.values())),
        closing_public=public_claim(e),opening_public=j.get('opening_public',0.),
        issued_claim_residual=float(claims(e).sum()+public_claim(e)-max(e.E_bank,0.)),
        bank_net_after_issued_equity=min(float(e.E_bank),0.))
    if e.p.bank_reconciliation_mode=='transaction_replay' and 'precision_trace' in j:
        from .bank_precision import explain
        result['book_residual_legacy_sum']=result['book_residual']
        result.update(explain(j,e.E_bank,j['precision_trace']))
    e._bank_reconciliation=result
    return result


def redenominate_journal(e,factor):
    if hasattr(e,'_bank_journal'):
        j=e._bank_journal;j['opening_book']/=factor;j['opening_claims']/=factor
        if 'precision_trace' in j:
            j['precision_trace']['operations'].append(dict(op='divide',value=float(factor)))
        if 'opening_public' in j:j['opening_public']/=factor
        for entry in j['entries']:
            entry['book_flow']/=factor;entry['claim_flow']/=factor
            if 'public_flow' in entry:entry['public_flow']/=factor
        if hasattr(e,'_bank_reconciliation'):reconcile(e)


def subscribe(e,requested):
    """Fund an issuance at book value; partial subscriptions dilute precisely.

    This function cannot recapitalize a bank of nonpositive book value:
    insolvency resolution requires the explicit public rescue mechanism.
    """
    requested=np.asarray(requested,float)
    if requested.shape!=(3,) or not np.isfinite(requested).all() or requested.min()<0:
        raise ValueError('Invalid bank subscription')
    if e.E_bank<=0:raise ValueError('Positive pre-money bank value required')
    before=float(e.E_bank);old=ownership(e)
    paid=np.minimum(requested,[max(e.led.dep[f'H{h}'],0.) for h in range(3)])
    total=float(paid.sum())
    if total:
        old_claims=claims(e);old_public=public_claim(e)
        for h in range(3):e.led.dep[f'H{h}']-=paid[h]
        e.E_bank=before+total
        e._bank_shares=(old*before+paid)/e.E_bank
        if e.p.eight_corrections:e._bank_public_share=old_public/e.E_bank
        _record(e,total,'private_subscription',old_claims,old_public)
    e._bank_issue_last=paid
    return paid


def pay_dividends(e,amount):
    if not np.isfinite(amount) or amount<0 or amount>max(e.E_bank,0.):
        raise ValueError('Unfunded bank dividend')
    paid=amount*ownership(e)
    for h in range(3):e.led.dep[f'H{h}']+=paid[h]
    public_paid=amount*getattr(e,'_bank_public_share',0.)
    e.led.dep['G']+=public_paid
    e._bank_public_dividend=getattr(e,'_bank_public_dividend',0.)+public_paid
    change_book(e,-amount,'dividends');e.div_bank_last=float(paid.sum()) if e.p.eight_corrections else float(amount);e._bank_dividends_last=paid
    return paid


def public_grant(e,amount):
    """Debt-financed public subscription; legacy mode retains the grant."""
    if not np.isfinite(amount) or amount<0:raise ValueError('Invalid bank rescue')
    if e.p.eight_corrections:
        if amount==0:return
        if e.E_bank+amount<=0:raise ValueError('Rescue must restore positive bank equity')
        old_book=float(e.E_bank);private=claims(e);public=public_claim(e)
        e.E_bank+=amount
        e._bank_shares=private/e.E_bank
        e._bank_public_share=(e.E_bank-float(private.sum()))/e.E_bank
        _record(e,amount,'public_subscription',private,public)
        e.B_cb+=amount;e.B+=amount;e.Res+=amount
        e.events.append(dict(t=e.t,event='public_bank_subscription',cost=float(amount),
            acquired_claim=float(public_claim(e)-public),absorbed_deficit=max(-old_book,0.)))
    else:
        e.B_cb+=amount;change_book(e,amount,'public_capital_transfer')
    e.recap+=amount;e.last_recap=e.t
    e._recap_tick=getattr(e,'_recap_tick',0.)+float(amount) if e.p.eight_corrections else float(amount)
