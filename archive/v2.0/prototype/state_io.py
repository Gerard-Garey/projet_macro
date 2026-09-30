"""Portable JSON snapshots; no pickle, eval or executable payloads."""
import json
from pathlib import Path
import numpy as np
from .model import Economy,Params,Ledger,MODEL_VERSION

def encode(x):
    if isinstance(x,np.ndarray):return {'array':x.tolist(),'dtype':str(x.dtype)}
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,tuple):return {'tuple':[encode(v) for v in x]}
    if isinstance(x,list):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if x is None or isinstance(x,(str,int,float,bool)):return x
    raise TypeError(type(x).__name__)

def decode(x):
    if isinstance(x,dict):
        if set(x)=={'array','dtype'}:return np.asarray(x['array'],dtype=x['dtype'])
        if set(x)=={'tuple'}:return tuple(decode(v) for v in x['tuple'])
        return {k:decode(v) for k,v in x.items()}
    if isinstance(x,list):return [decode(v) for v in x]
    return x

def save_state(e,path,metadata=None):
    if e.world is not None or e.pol_override is not None:raise ValueError('Snapshot national sans fonction de taux imposée requis')
    data=state_payload(e,metadata)
    write_json(path,data)

def state_payload(e,metadata=None):
    if e.pol_override is not None:raise ValueError("Callable policy cannot be serialized")
    return dict(version=MODEL_VERSION,params=encode(e.p.__dict__),ledger=encode(e.led.__dict__),
        rng=encode(e.rng.bit_generator.state),state=encode({k:v for k,v in e.__dict__.items() if k not in ('p','led','rng','world','pol_override')}),
        metadata=metadata or {})

def write_json(path,data):
    path=Path(path);temp=path.with_suffix(path.suffix+'.part');temp.write_text(json.dumps(data,separators=(',',':'),allow_nan=False));temp.replace(path)

def load_state(path,allow_failed=False):
    return economy_from_payload(json.loads(Path(path).read_text()),allow_failed)

def economy_from_payload(d,allow_failed=False):
    metadata=d.get('metadata',{})
    if not allow_failed and (d.get('state',{}).get('_step_failed') or metadata.get('certified_resume') is False or metadata.get('failure')):
        raise ValueError('Diagnostic snapshot from an interrupted week; not a valid continuation. Use allow_failed=True for inspection only.')
    if d['version'] not in (MODEL_VERSION,'2.3-equity-quote-20260914','2.2-workplan-20260913','2.1-audit-continuous-20260913','2.0-eight-rebuilt-20260913','2.0-corrections-research8','2.0-closure-research7','2.0-medium-research6','2.0-closure-research1','2.0-h7-research2','2.0-cycle-research3','2.0-wiu-research4','2.0-structural-research5'):
        raise ValueError('Version du snapshot incompatible')
    if d['params'].get('equity_valuation_mode')=='market_quote' and '_equity_quote' not in d['state']:
        raise ValueError('Independent equity quotation missing from snapshot')
    e=Economy(Params(**decode(d['params'])))
    e.__dict__.update(decode(d['state']));e.led.__dict__.update(decode(d['ledger']))
    e.rng.bit_generator.state=decode(d['rng']);e.world=None;e.pol_override=None
    metadata=dict(d['metadata'])
    if d['version']!=MODEL_VERSION:metadata['source_snapshot_version']=d['version']
    if '_bank_shares' not in d['state']:
        e._bank_shares=e.p.omega.copy()
        e._bank_dividends_last=e.div_bank_last*e.p.omega
        metadata['bank_claim_migration']='Recognized existing omega dividend rights at limited-liability book value; no cash flow'
    if e.p.eight_corrections:
        from .eight_points import enable
        enable(e)
    return e,metadata


def save_world(world,path,metadata=None):
    """Exact synchronous checkpoint, including all country RNGs and world memory."""
    failed=world._failed or any(e.t!=world.t or getattr(e,'_step_failed',False) for e in world.countries)
    data=dict(format='nations-world-v1',version=MODEL_VERSION,certified_resume=not failed,
        world=encode({k:v for k,v in world.__dict__.items() if k!='countries'}),
        countries=[state_payload(e) for e in world.countries],metadata=metadata or {})
    write_json(path,data)

def load_world(path,allow_failed=False):
    from .worldn import World
    d=json.loads(Path(path).read_text())
    if d.get('format')!='nations-world-v1' or d.get('version') not in (MODEL_VERSION,'2.3-equity-quote-20260914','2.2-workplan-20260913'):
        raise ValueError('Unsupported world format; diagnostic legacy worlds lack restart data')
    if not d.get('certified_resume',False) and not allow_failed:
        raise ValueError('Interrupted world checkpoint is diagnostic only')
    countries=[economy_from_payload(x,allow_failed)[0] for x in d['countries']]
    w=World.__new__(World);w.__dict__.update(decode(d['world']));w.countries=countries
    if len(countries)!=w.n:raise ValueError('Country count mismatch')
    if not allow_failed and any(e.t!=w.t for e in countries):raise ValueError('World calendars differ')
    if not d.get('certified_resume',False):w._failed=True
    for i,e in enumerate(countries):e.world=w;e.idx=i
    if w.shares.shape!=(w.n,w.n,4):raise ValueError('Invalid trade memory shape')
    return w,d.get('metadata',{})
