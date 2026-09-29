"""Explicit activation and safe continuation of the audited profile."""
import argparse,json,sys,traceback
from pathlib import Path
from .model import MODEL_VERSION,Params
from .state_io import load_state,save_state,encode
from .audit_profile import enable,apply_action
from .eight_points import valuations,gdp_growth

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--state',type=Path,required=True)
    ap.add_argument('--weeks',type=int,default=52)
    ap.add_argument('--out',type=Path,default=Path('results/audit_run'))
    ap.add_argument('--settings',type=Path,help='JSON containing explicit Params overrides')
    ap.add_argument('--action',type=Path,help='JSON containing kind and funded action terms')
    args=ap.parse_args()
    if args.weeks<1:ap.error('--weeks must be positive')
    e,meta=load_state(args.state);enable(e);e.p.audit_strict=True
    overrides=json.loads(args.settings.read_text()) if args.settings else {}
    if overrides:e.p=Params(**(e.p.__dict__|overrides))
    action=json.loads(args.action.read_text()) if args.action else None
    args.out.mkdir(parents=True,exist_ok=True)
    if action:apply_action(e,**action)
    save_state(e,args.out/'initial_state.json',{'source':str(args.state),'overrides':overrides,'action':action,'certified_resume':True})
    start=e.t;failure=None;completed=0
    try:
        for _ in range(args.weeks):e.step();completed+=1
    except Exception as exc:failure=dict(type=type(exc).__name__,message=str(exc),week=e.t,traceback=traceback.format_exc())
    growth=None;reason=None
    if completed>1:
        try:growth=gdp_growth(e,start,start+completed-1)
        except ValueError as exc:reason=str(exc)
    result=dict(version=MODEL_VERSION,start_week=start,completed_weeks=completed,requested_weeks=args.weeks,
        failure=failure,collapsed=e.collapsed,gdp_growth=growth,gdp_comparison_refused=reason,
        stationarity='not_established',valuations=valuations(e),source=meta,
        parameters=e.p.__dict__,overrides=overrides,action=action,certified_resume=failure is None)
    (args.out/'summary.json').write_text(json.dumps(encode(result),indent=2,allow_nan=False))
    save_state(e,args.out/('failed_diagnostic_state.json' if failure else 'state.json'),encode(result))
    print(json.dumps({'completed_weeks':completed,'failure':failure,'collapsed':e.collapsed}))
    return int(failure is not None)

if __name__=='__main__':sys.exit(main())
