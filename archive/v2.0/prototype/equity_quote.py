"""A nominal quotation per fixed aggregate share, separate from book equity.

Activation recognizes the currently displayed quote; it creates no cash,
claim, forgiveness or expectation reset. Prices still come from the auction.
"""
import numpy as np

def enable(e):
    if e.p.portfolio_mode!='joint_equity':
        raise ValueError('Independent quote requires the joint equity auction')
    if e.p.equity_valuation_mode=='market_quote' and hasattr(e,'_equity_quote'):
        return e
    quote=float(e.pE*e.equity_book())
    if not np.isfinite(quote) or quote<=0:raise ValueError('Invalid inherited equity quotation')
    e._equity_quote=quote
    e.p.equity_valuation_mode='market_quote'
    e.events.append(dict(t=e.t,event='independent_equity_quote',quote=quote,
                         cash_created=0.,source='displayed_legacy_quote',
                         nominal_unit=float(getattr(e,'_audit_unit',1.))))
    return e

def close_auction(e,cap):
    if e.p.equity_valuation_mode=='market_quote':e._equity_quote=float(cap)

def detach_dividends(e,cap,dividend):
    # Preserve the historical positive numerical quote floor in the original
    # accounting numeraire. Its conversion is explicit, never a nominal reset.
    floor=1e-6*float(getattr(e,'_audit_unit',1.))
    quote=max(float(cap-dividend),floor)
    e._equity_quote=quote
    return quote
