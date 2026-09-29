"""Explicit, reproducible entry point for the reconstructed eight-point profile."""
import argparse
import json
from pathlib import Path
import sys
from .model import Economy, Params, MODEL_VERSION
from .reference import reference_parameters
from .state_io import load_state, save_state, encode
from .eight_points import enable, valuations, gdp_growth


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path)
    parser.add_argument('--weeks', type=int, default=52)
    parser.add_argument('--out', type=Path, default=Path('results/eight_run'))
    args=parser.parse_args()
    if args.weeks<1:parser.error('--weeks must be positive')
    e,meta=load_state(args.state) if args.state else (Economy(Params(**reference_parameters())),{})
    enable(e);e.p.audit_strict=True
    args.out.mkdir(parents=True,exist_ok=True)
    start=e.t;failure=None
    try:
        for _ in range(args.weeks):e.step()
    except Exception as exc:
        failure=dict(type=type(exc).__name__,message=str(exc),week=e.t)
    rows=[r for r in e.measurement_history if r['t']>=start]
    growth=None;reason=None
    if len(rows)>1:
        try:growth=gdp_growth(e,rows[0]['t'],rows[-1]['t'])
        except ValueError as exc:reason=str(exc)
    result=dict(version=MODEL_VERSION,start_week=start,completed_weeks=e.t-start,
        requested_weeks=args.weeks,failure=failure,collapsed=e.collapsed,
        gdp_growth=growth,gdp_comparison_refused=reason,stationarity='not_tested',
        valuations=valuations(e),source=meta,parameters=e.p.__dict__)
    (args.out/'summary.json').write_text(json.dumps(encode(result),indent=2,allow_nan=False))
    # A failed in-flight state is diagnostic only, not a certified resume point.
    save_state(e,args.out/('failed_diagnostic_state.json' if failure else 'state.json'),metadata=encode(result))
    print(json.dumps(dict(completed_weeks=e.t-start,failure=failure,collapsed=e.collapsed)))
    return 1 if failure else 0


if __name__=='__main__':sys.exit(main())
