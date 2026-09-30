"""Weekly concave portfolio solver with a banded, bound constrained Newton step.

The Hessian couples adjacent dates only. Keeping every week is therefore
linear in horizon length for each Newton subproblem; no time aggregation is
needed. Public arrays retain the historical [all deposits, all equity] order.
"""
import numpy as np
from scipy.linalg import solveh_banded
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack


class PortfolioInfeasible(ValueError):
    """A phase-I upper bound rules out positive surplus at the stated tolerance."""


class PortfolioConvergenceError(RuntimeError):
    """Numerical failure; this is not an economic infeasibility certificate."""


class MarketClearingError(RuntimeError):
    """Individual demands did not yield a verified market-clearing price."""


def solve(*args,**kwargs):
    """Preserve the exact failed input for reproducible diagnostic archives."""
    try:return _solve(*args,**kwargs)
    except (PortfolioInfeasible,PortfolioConvergenceError) as ex:
        from inspect import signature
        inputs=signature(_solve).bind(*args,**kwargs);inputs.apply_defaults()
        ex.problem={k:v for k,v in inputs.arguments.items() if v is not None and k not in ('terminal','_fallback_allowed')}
        if inputs.arguments['terminal'] is not None:
            ex.problem.update({'terminal_'+k:v for k,v in inputs.arguments['terminal'].items()})
        raise


def _solve(cash,asset,income,R,G,dividend,weights,phi=0.,buffer=1.,fee=.02,
          scale=1.,risk=0.,warm=None,tol=1e-8,terminal=None,_fallback_allowed=True):
    """Maximize discounted log surplus, wealth services and an equity penalty.

    cash is *net* current resources: it may be negative after subsistence.
    Deposits and equity holdings remain nonnegative. A sale pays its convex
    fee in the same budget. A feasible warm start precedes any seed search.
    """
    y=np.asarray(income,float);n=len(y)
    def vec(x):return np.broadcast_to(x,y.shape).astype(float).copy()
    R,G,D,w,B,S=map(vec,[R,G,dividend,weights,buffer,scale])
    if n<2 or min(asset,phi,fee,risk)<0 or not np.isfinite(np.r_[cash,asset,phi,fee,risk,y,R,G,D,w,B,S]).all() or min(R.min(),G.min(),w.min(),B.min(),S.min())<=0 or D.min()<0:
        raise ValueError('Invalid joint portfolio problem')
    tw=0.;ti=0.;tc=np.zeros(2)
    if terminal is not None:
        if not np.isfinite(list(terminal.values())).all() or terminal['weight']<=0 or terminal['equity_income']<0:
            raise ValueError('Invalid stationary-policy continuation')
        tw=terminal['weight'];ti=terminal['income']
        tc=np.array([terminal['liquid_income'],terminal['equity_income']])
    rw=w.copy();rw[-1]+=tw

    def parts(z):
        x=z.reshape(n,2);b=x[:,0];a=x[:,1]
        d=a-np.r_[asset,G[1:]*a[:-1]]
        c=y+np.r_[cash,R[1:]*b[:-1]+D[1:]*a[:-1]]-b-d-.5*fee*d*d/S
        v=b+a+B
        tail=ti+tc@x[-1] if terminal is not None else 1.
        return x,d,c,v,tail

    def feasible(z):
        if z is None or len(z)!=2*n or not np.isfinite(z).all() or np.min(z)<0:return False
        _,_,c,_,tail=parts(z)
        return min(c.min(),tail)>1e-10

    def value(z):
        x,d,c,v,tail=parts(z)
        if c.min()<=0 or tail<=0:return np.inf
        ans=-w@(np.log(c)+phi*np.log(v))+.5*risk*rw@((x[:,1]/S)**2)
        if terminal is not None:ans-=tw*(np.log(tail)+phi*np.log(v[-1]))
        return float(ans)

    def derivatives(z):
        x,d,c,v,tail=parts(z);m=w/c;u=1+fee*d/S
        cur=np.column_stack([-np.ones(n),-u])
        prev=np.column_stack([R[1:],G[1:]*u[1:]+D[1:]])
        grad=-cur*m[:,None];grad[:-1]-=prev*m[1:,None]
        grad-= (w*phi/v)[:,None];grad[:,1]+=rw*risk*x[:,1]/S**2
        diag=(w/c**2)[:,None,None]*cur[:,:,None]*cur[:,None,:]
        diag[:-1]+=(w[1:]/c[1:]**2)[:,None,None]*prev[:,:,None]*prev[:,None,:]
        off=(w[1:]/c[1:]**2)[:,None,None]*cur[1:,:,None]*prev[:,None,:]
        q=m*fee/S
        diag[:,1,1]+=q;diag[:-1,1,1]+=q[1:]*G[1:]**2
        off[:,1,1]-=q[1:]*G[1:]
        diag[:,1,1]+=rw*risk/S**2
        diag+=(w*phi/v**2)[:,None,None]
        if terminal is not None:
            grad[-1]-=tw*tc/tail+tw*phi/v[-1]
            diag[-1]+=tw*np.outer(tc,tc)/tail**2+tw*phi/v[-1]**2
        ab=np.zeros((4,2*n))
        ab[0,0::2]=diag[:,0,0];ab[0,1::2]=diag[:,1,1]
        ab[1,0::2]=diag[:,1,0];ab[1,1:-1:2]=off[:,0,1]
        ab[2,0:-2:2]=off[:,0,0];ab[2,1:-2:2]=off[:,1,1]
        ab[3,0:-3:2]=off[:,1,0]
        return grad.ravel(),ab,np.repeat(m,2)

    def mv(ab,z):
        out=ab[0]*z
        for k in range(1,4):
            out[k:]+=ab[k,:-k]*z[:-k];out[:-k]+=ab[k,:-k]*z[k:]
        return out

    def phase_one():
        # Outer approximation of convex transaction fees. Every LP enlarges
        # the true feasible set: a nonpositive LP optimum is an upper-bound
        # certificate, whereas failure to close the approximation is numerical.
        # Variables: interleaved b,a; fee epigraph f; common surplus eta.
        rows=[];cols=[];vals=[];rhs=[]
        for t in range(n):
            row=len(rhs);rhs.append(float(y[t]+(cash+asset if t==0 else 0.)))
            entries=[(2*t,1.),(2*t+1,1.),(2*n+t,1.),(3*n,1.)]
            if t:entries += [(2*t-2,-R[t]),(2*t-1,-G[t]-D[t])]
            for col,val in entries:rows.append(row);cols.append(col);vals.append(val)
        if terminal is not None:
            row=len(rhs);rhs.append(float(ti))
            for col,val in [(2*n-2,-tc[0]),(2*n-1,-tc[1]),(3*n,1.)]:rows.append(row);cols.append(col);vals.append(val)
        A=coo_matrix((vals,(rows,cols)),shape=(len(rhs),3*n+1)).tocsr();rhs=np.asarray(rhs)
        objective=np.zeros(3*n+1);objective[-1]=-1.
        for iteration in range(100):
            lp=linprog(objective,A_ub=A,b_ub=rhs,bounds=[(0,None)]*(3*n)+[(None,None)],method='highs')
            if not lp.success:raise PortfolioConvergenceError('Portfolio phase-I LP failed: '+lp.message)
            if lp.x[-1]<=1e-10:
                ex=PortfolioInfeasible(f'No positive-surplus budget at 1e-10 tolerance; phase-I upper bound {lp.x[-1]:.12g}')
                ex.upper_bound=float(lp.x[-1]);raise ex
            z=lp.x[:2*n]
            if feasible(z):return z,iteration+1
            d=parts(z)[1];slope=fee*d/S
            rr=[];cc=[];vv=[];bb=[]
            for t in range(n):
                rr.extend([t,t]);cc.extend([2*t+1,2*n+t]);vv.extend([slope[t],-1.])
                if t:rr.append(t);cc.append(2*t-1);vv.append(-slope[t]*G[t])
                bb.append(.5*fee*d[t]**2/S[t]+(slope[t]*asset if t==0 else 0.))
            A=vstack([A,coo_matrix((vv,(rr,cc)),shape=(n,3*n+1))],format='csr');rhs=np.r_[rhs,bb]
        raise PortfolioConvergenceError('Portfolio phase-I approximation limit; infeasibility not established')

    z=None;phase_iterations=0
    if warm is not None and len(warm)==2*n:
        candidate=np.column_stack([warm[:n],warm[n:]]).ravel()
        if feasible(candidate):z=candidate.copy()
    if z is None:
        x=np.zeros((n,2));last_b=0.;last_a=asset
        for t in range(n):
            marked=asset if t==0 else G[t]*last_a
            available=y[t]+(cash if t==0 else R[t]*last_b+D[t]*last_a)
            sold=0.
            if available<=1e-8:
                sold=min(marked,S[t]/fee if fee else marked)
                available+=sold-.5*fee*sold*sold/S[t]
            if available<=1e-10:break
            x[t,1]=marked-sold
            x[t,0]=max(available-min(.9*available,max(y[t],max(cash,0.)*.01 if t==0 else 1e-6)),.05*available)
            last_b,last_a=x[t]
        candidate=x.ravel()
        if feasible(candidate):z=candidate
        else:z,phase_iterations=phase_one()
    residual=np.inf
    for it in range(300):
        grad,ab,mu=derivatives(z)
        active=(z<1e-8)&(grad>=0)
        residual=float(np.max(abs(np.where(active,0.,grad))/np.maximum(mu,1e-12)))
        if residual<tol:break
        ab[0]+=1e-12*np.maximum(ab[0],1e-16)
        # Fast bulk active-set search, with a primal-feasible fallback if
        # active sets repeat. Both paths solve the same bound-constrained QP.
        scaling=1/np.sqrt(np.maximum(ab[0],1e-300))
        scaled=ab.copy()
        for k in range(1,4):scaled[k,:-k]*=scaling[:-k]*scaling[k:]
        scaled[0]=1.
        def qp_direction(active):
            fixed=np.where(active,-z,0.)
            rhs=(-grad-mv(ab,fixed))*scaling;rhs[active]=0.
            matrix=scaled.copy()
            for k in range(1,4):matrix[k,:-k]*=~(active[:-k]|active[k:])
            try:return fixed+scaling*solveh_banded(matrix,rhs,lower=True,check_finite=False)
            except np.linalg.LinAlgError as ex:raise PortfolioConvergenceError('Portfolio Newton matrix not positive definite') from ex
        seen=set();solved=False
        for qp in range(32):
            key=active.tobytes()
            if key in seen:break
            seen.add(key);direction=qp_direction(active)
            extra=(z+direction < -1e-12)&~active
            if extra.any():active|=extra;continue
            multipliers=grad+mv(ab,direction)
            release=active&(multipliers < -1e-10*np.maximum(mu,1e-12))
            if release.any():active[release]=False;continue
            solved=True;break
        if not solved:
            # Move to the first blocking bound, then release one negative
            # multiplier. This avoids bulk add/release cycling at zero cash.
            active=(z<1e-8)&(grad>=0);direction=np.where(active,-z,0.)
            for qp in range(8*n+1):
                candidate=qp_direction(active)
                extra=(z+candidate < -1e-12)&~active
                if extra.any():
                    step=candidate-direction
                    ratios=np.full(2*n,np.inf)
                    ratios[extra]=(z+direction)[extra]/(-step[extra])
                    hit=int(np.argmin(ratios));fraction=float(np.clip(ratios[hit],0.,1.))
                    direction+=fraction*step
                    direction[hit]=-z[hit];active[hit]=True
                    continue
                direction=candidate
                multipliers=grad+mv(ab,direction)
                release=active&(multipliers < -1e-10*np.maximum(mu,1e-12))
                if release.any():
                    hit=int(np.argmin(np.where(release,multipliers/np.maximum(mu,1e-12),np.inf)))
                    active[hit]=False
                    continue
                break
            else:raise PortfolioConvergenceError('Portfolio quadratic subproblem failed')
        tiny=(z<1e-12)&(direction<0)&(direction>=-1e-10);direction[tiny]=0.
        alpha=1.;neg=direction<0
        if neg.any():alpha=min(alpha,float(np.min(-z[neg]/direction[neg])))
        before=value(z);slope=float(grad@direction)
        if slope>=0 or alpha<1e-15:raise PortfolioConvergenceError(f'Portfolio Newton stalled: KKT={residual}; alpha={alpha}; slope={slope}')
        for _ in range(60):
            trial=np.maximum(z+alpha*direction,0.)
            if value(trial)<=before+1e-4*alpha*slope+1e-11:break
            alpha*=.5
        else:raise PortfolioConvergenceError('Portfolio line search failed')
        z=trial
    else:raise PortfolioConvergenceError(f'Portfolio convergence limit: KKT={residual}')
    x,d,c,v,tail=parts(z)
    return dict(consumption=c,terminal_consumption=float(tail) if terminal is not None else None,
        liquid=x[:,0],asset=x[:,1],transfer=d,fees=.5*fee*d*d/S,objective=-value(z),
        iterations=it,kkt_relative=residual,warm=np.r_[x[:,0],x[:,1]],fallback=False,phase_iterations=phase_iterations)
