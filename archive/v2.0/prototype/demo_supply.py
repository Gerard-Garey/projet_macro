"""N-country example: equipment supply, wealth buffer and monetary/fiscal closures, with assets."""
import argparse
import json
import numpy as np
from .worldn import World
from .model import MODEL_VERSION

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--countries',type=int,default=3)
    ap.add_argument('--years',type=int,default=20);args=ap.parse_args()
    w=World.homogeneous(args.countries)
    w.run(args.years)
    print(json.dumps(dict(version=MODEL_VERSION,stationary_validation=False,
        countries=[dict(unemployment=100*float(np.mean(e.hist['u'][-52:])),
                        inflation=100*float(np.mean(e.hist['pi'][-52:])),
                        capital_output=float(e.K.sum()/e.hist['Y'][-1]),
                        treasury_cash_gdp=float(e.led.dep['G']/e.Y_nom_prev())) for e in w.countries]),indent=2))

if __name__=='__main__':main()
