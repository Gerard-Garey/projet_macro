"""CLI portable : python -m prototype.simulate --assets --years 30."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from .model import Economy, Params, MODEL_VERSION
from .reference import reference_parameters
from .state_io import load_state,save_state


def export_csv(e, path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); fields=list(e.hist)
        extra_fields=['treasury_cash','treasury_target','treasury_dividend','redemption_households','redemption_bank','redemption_cb','redemption_advances','redemption_total','household_taxes','household_tax_base','tax_scale','tauK_effective','tax_deficit_target','rstar','rstar_anchor']
        w.writerow(['week','year']+fields+['C_nom_week','I_nom_week','IZ_nom_week','Y_nom_week','wage_share','G_nom_week','Y_potential_nom_week','K_value','Z_replacement','Z_market','equity_market','P_food_relative','output_food','I_real','IZ_real']+extra_fields)
        for i in range(min(len(e.hist['Y']),len(e.flow_history))):
            flows=e.flow_history[i]
            w.writerow([i,(i+1)/52]+[e.hist[k][i] for k in fields]+[flows.get(k,'') for k in ('C','I','IZ','Y','wage_share','G','Y_potential','K_value','Z_replacement','Z_market','equity_market','P_food_relative','output_food','I_real','IZ_real')]+[flows.get(k,0.) for k in extra_fields])


def json_ready(x):
    if isinstance(x,np.ndarray): return x.tolist()
    if isinstance(x,np.generic): return x.item()
    raise TypeError(type(x).__name__)


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--years',type=float,default=30)
    a.add_argument('--assets',action='store_true')
    a.add_argument('--params',type=Path,help='Objet JSON de paramètres explicites')
    a.add_argument('--seed',type=int,default=0)
    a.add_argument('--state',type=Path,help='État JSON de continuation ; les paramètres sont ceux de cet état')
    a.add_argument('--snapshot-out',type=Path)
    a.add_argument('--output',type=Path,default=Path('results/simulation.csv'))
    args=a.parse_args()
    if args.years<=0 or not np.isfinite(args.years): a.error('--years doit être positif et fini')
    if args.state and args.params:a.error('--state et --params sont incompatibles')
    kw={**reference_parameters(),**(json.loads(args.params.read_text()) if args.params else {})}
    if args.assets: kw['assets']=True
    kw['audit_strict']=True
    e=load_state(args.state)[0] if args.state else Economy(Params(**kw),seed=args.seed)
    if not e.p.assets:a.error('Cette livraison est validée uniquement avec actifs')
    e.p.audit_strict=True;e.run(args.years)
    if args.snapshot_out:save_state(e,args.snapshot_out,dict(method='Continuation; fixed point not certified'))
    export_csv(e,args.output)
    args.output.with_suffix('.json').write_text(json.dumps(dict(version=MODEL_VERSION,seed=args.seed,years=args.years,params=e.p.__dict__,accounting=e.accounting,events=e.events),default=json_ready,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{args.output} : {e.t} semaines, chômage final {100*e.hist["u"][-1]:.2f} %, inflation {100*e.pi:.2f} %')


if __name__=='__main__': main()
