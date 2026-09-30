"""One marked balance sheet per household, distinct from spendable liquidity.

Construction in progress belongs to its funder at equipment replacement cost.
Corporate equity uses its market shares; bank equity uses book-value claims.
This reporting perimeter is distinct from the liquid/corporate-equity utility
problem. Margin loans retain the historical omega allocation.
"""
import numpy as np
try:from .bank_equity import claims
except ImportError:from bank_equity import claims

def household_balance_sheets(e):
    p=e.p
    assets=dict(deposits=np.array([e.led.dep[f'H{h}'] for h in range(3)]),currency=e.cash_h.copy(),bonds=e.Bh.copy(),
                equity=(e.equity_market_value()*e.equity_ownership() if e.p.equity_valuation_mode=='market_quote' else e.pE*e.equity_ownership()*e.equity_book()),bank_equity=claims(e),housing=e.pZ*e.Z,construction=e.capital_price()*e.pipeline_h.sum(axis=0))
    liabilities=dict(mortgage=e.LZ.copy(),margin=p.omega*e.LE)
    net=sum(assets.values())-sum(liabilities.values())
    result=dict(assets=assets,liabilities=liabilities,net=net,external=net-assets['deposits'])
    if e.p.eight_corrections:
        result['bank_institutional']=dict(tradable=False,spendable=False,
            decision_rule='fixed_holdings_outside_liquid_portfolio_problem',
            wealth=assets['bank_equity'].copy(),
            cash_income=np.asarray(e._bank_dividends_last).copy())
    return result
