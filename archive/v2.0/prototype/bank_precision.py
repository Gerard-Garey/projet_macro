"""Independently replay bank additions and currency divisions.

No balance, flow, threshold or policy is changed. The raw discrepancy is
split into predicted binary representation error and unexplained discrepancy.
Fraction evaluates the stored binary numbers exactly, not decimal ideal money.
"""
from fractions import Fraction
import math

def enable(e):
    if getattr(e,'_step_failed',False):raise ValueError('Interrupted state is not a continuation')
    if e.p.bank_reconciliation_mode!='transaction_replay':
        e.p.bank_reconciliation_mode='transaction_replay'
        e.events.append(dict(t=e.t,event='bank_transaction_audit_enabled',stocks_changed=False,
                             scope='Next weekly journal; historical journals stay historical'))
    return e

def F(x):
    x=float(x)
    if not math.isfinite(x):raise ValueError('Nonfinite bank journal value')
    return Fraction.from_float(x)

def explain(journal,closing,trace):
    """Predict from the opening and operations, never from the observed close.

    The duplicate amount trace is checked against the displayed journal; a
    missing/mutated entry cannot be absorbed into the predicted error term.
    """
    expected=float(trace['opening']);ideal=F(expected);opening=expected;amounts=[]
    for op in trace['operations']:
        value=float(op['value']);F(value)
        if op['op']=='add':
            expected=float(expected+value);ideal+=F(value);amounts.append(value)
        elif op['op']=='divide':
            if value<=0:raise ValueError('Invalid recorded currency conversion')
            expected=float(expected/value);ideal/=F(value)
            opening=float(opening/value);amounts=[float(x/value) for x in amounts]
        else:raise ValueError('Unknown bank journal operation')
        F(expected)
    displayed=[float(entry['book_flow']) for entry in journal['entries']]
    if opening!=journal['opening_book'] or amounts!=displayed:
        raise ValueError('Bank journal and independently replayed operation trace disagree')
    economic_sum=F(opening)+sum((F(x) for x in displayed),Fraction())
    arithmetic_error=F(expected)-ideal
    display_error=ideal-economic_sum
    predicted=arithmetic_error+display_error
    raw=F(closing)-economic_sum
    unexplained=raw-predicted
    assert unexplained==F(closing)-F(expected)
    return dict(book_expected_closing=expected,book_residual_raw_exact=float(raw),
                book_predicted_rounding=float(predicted),book_arithmetic_rounding=float(arithmetic_error),
                book_conversion_display_rounding=float(display_error),book_residual=float(unexplained),
                book_residual_exact=dict(numerator=unexplained.numerator,denominator=unexplained.denominator),
                book_audit_scope='stored binary additions and divisions; not an independent sectoral ledger')

def explain_legacy(journal,closing):
    """Forensic addition-only hypothesis, validated or rejected by the close.

    Does not claim that a historical currency conversion can be inferred.
    """
    trace=dict(opening=journal['opening_book'],operations=[dict(op='add',value=x['book_flow']) for x in journal['entries']])
    return explain(journal,closing,trace)
