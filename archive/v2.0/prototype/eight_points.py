"""Reconstruction of F02/F13/F15/F16/F18/F19/F20/F25 on research8.

Opt in explicitly, including for old snapshots. This is not a recovered
research10 executable, nor a claim of macroeconomic stationarity.
"""
import numpy as np


def enabled(e):
    return e.p.eight_corrections


def enable(e):
    """Activate contracts and diagnostics without resetting stocks/beliefs."""
    e.p.eight_corrections = True
    if not hasattr(e, '_bank_public_share'):
        e._bank_public_share = 0.
    try:from .mortgage_vintages import initialize
    except ImportError:from mortgage_vintages import initialize
    initialize(e)
    if not hasattr(e, 'measurement_history'):
        e.measurement_history = []
    e.eight_profile = 'eight-points-rebuilt-20260913'
    return e


def valuations(e):
    try:from .bank_equity import balance
    except ImportError:from bank_equity import balance
    book = float((e.K*e.capital_price()).sum()+(e.Sinv*e.p_).sum()
                 +(e.Xinv*e.p_[:, None]).sum()-e.Loans.sum()
                 +sum(e.led.dep[f'F{j}'] for j in range(e.p.nsec)))
    market = e.equity_market_value()
    price_index = float(e.P_hist[-1] if e.P_hist else float(e.p_.mean()))
    return dict(book_value_signed=book, market_cap_nominal=market,
                market_cap_real=market/price_index, total_shares=1.,
                share_price_nominal=market, share_price_real=market/price_index,
                internal_quote=float(e.pE), market_to_book=market/book if book>0 else None,
                market_to_book_valid=book>0, price_index=price_index,
                bank=balance(e))


def observe(e, regime):
    """The production method, not the post-step collapse flag, labels GDP."""
    if not enabled(e):
        return
    try:from .mortgage_vintages import check
    except ImportError:from mortgage_vintages import check
    check(e)
    rows = e.measurement_history
    method = 'normal_value_added' if regime == 'normal' else 'legacy_survival_output'
    segment = rows[-1]['segment'] if rows else 0
    broken = bool(rows and rows[-1]['method'] != method)
    if broken:
        segment += 1
    rows.append(dict(t=e.t, method=method, segment=segment, series_break=broken,
                     annual_real_gdp=float(e.hist['Y'][-1])))
    if broken:
        e.events.append(dict(t=e.t, event='gdp_measurement_break', method=method))
    if not hasattr(e, 'monetary_history'):
        e.monetary_history = []
    e.monetary_history.append(dict(t=e.t, regime=regime, decision_week=e.t%4==0,
        components=dict(getattr(e, '_policy_components', {})),
        components_valid_for_regime=regime=='normal',
        rate_diagnostics=dict(getattr(e, '_policy_limits', {})),
        conditional_proxy=dict(getattr(e, '_rstar_diagnostic', {})),
        credibility=float(e.cred), inflation_expectation=float(e.pi_e),
        expectation_at_upper_bound=bool(e.pi_e >= 12.-1e-10),
        credibility_at_floor=bool(e.cred <= 1e-10),
        credibility_ceiling=float(max(1-e.p.nu9*e.M_hist,e.p.cred_floor)),
        belief_limits=dict(getattr(e,"_belief_limits",{})),
        tax_scale=float(e.tax_scale)))


def gdp_growth(e, start, end):
    """Only recorded observations from one uninterrupted method are comparable.

    start/end are simulation weeks, inclusive. Legacy unlabelled observations
    cannot be silently used. Old raw hist['Y'] remains a compatibility field.
    """
    if end <= start:
        raise ValueError('GDP interval must have positive length')
    rows = [r for r in getattr(e, 'measurement_history', []) if start <= r['t'] <= end]
    if len(rows) != end-start+1 or rows[0]['t'] != start or rows[-1]['t'] != end:
        raise ValueError('GDP observations missing or not labelled')
    if len({(r['method'], r['segment']) for r in rows}) != 1:
        raise ValueError('GDP measurement break: comparison refused')
    if rows[0]['annual_real_gdp'] <= 0:
        raise ValueError('Nonpositive GDP denominator')
    return rows[-1]['annual_real_gdp']/rows[0]['annual_real_gdp']-1


def monetary_reform(e):
    """Player stops monetization; existing beliefs and obligations survive."""
    previous = float(e.monetize)
    e.monetize = 0.
    e.events.append(dict(t=e.t, event='stop_monetization', previous=previous,
                         credibility=float(e.cred), inflation_expectation=float(e.pi_e)))

