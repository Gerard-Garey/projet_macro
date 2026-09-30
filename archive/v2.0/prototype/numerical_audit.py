"""Floating-point allowance for a cancellation-prone balance identity only.

The original tolerance remains 1e-8*max(1,abs(CB equity)). A separate
64*machine-epsilon*sum(abs(balance components)) allowance covers numerical
roundoff at large nominal scales. Raw error is retained. No ledger mutation.
"""
import math
import numpy as np

def central_bank_check(e):
    terms=[e.B_cb,e.AG,e.L_cb,e.led.dep['FX'],e.e*e.R_fx,-e.Res,-e.cash_out]
    e.E_cb_check=math.fsum(terms)
    residual=abs(math.fsum([*terms,-e.E_cb]))
    # Include the components used to construct commercial-bank reserves.
    gross=math.fsum(abs(x) for x in terms+[e.E_cb,e.Loans.sum(),e.LZ.sum(),e.LE,e.B_bank,e.E_bank,e.led.total()])
    rounding=64*np.finfo(float).eps*gross
    denominator=max(1.,abs(e.E_cb))
    e._cb_numerics=dict(absolute_residual=residual,roundoff_allowance=rounding,gross_scale=gross,
                       raw_relative=residual/denominator,original_absolute_tolerance=1e-8*denominator)
    return max(residual-rounding,0.)/denominator
