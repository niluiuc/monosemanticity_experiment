"""High-precision numerical global-gap bias calibration on12 fixed comparisons."""
import argparse,hashlib,heapq,json,shutil,time
from pathlib import Path
import mpmath as mp
import run_frozen_map as model

HERE=Path(__file__).resolve().parent
mp.mp.dps=70
SLACK=mp.mpf('1e-40')
LIMIT=100000

def serial(value):
    if isinstance(value,mp.mpf):return str(value)
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [serial(v) for v in value]
    return value

def objective(beta,offsets,y,P,sd):
    f=g=mp.mpf(0)
    for o,target,prob in zip(offsets,y,P):
        mu=o+beta;m1,m2=model.moments(mu,sd)
        f+=prob*(m2-2*target*m1+target*target)
        g+=2*prob*((mu-target)*model.Phi(mu/sd)+sd*model.phi(mu/sd))
    return f,g

def calibrate(offsets,y,P,sd,beta_clean,tolerance):
    if sd==0:
        prior=sum(pi*yi for pi,yi in zip(P,y));f=sum(pi*(prior-yi)**2 for pi,yi in zip(P,y))
        return {'beta':prior,'lower':f,'upper':f,'gap':mp.mpf(0),'resolved':True,'nodes':[],'active_heap':[],'expansions':0}
    lo=-max(offsets)-12*sd-1;hi=1-min(offsets)
    best_beta=beta_clean; best=objective(best_beta,offsets,y,P,sd)[0]
    # Local stationary candidates improve incumbents only, never supply global proof.
    for initial in [beta_clean,-sd/2]:
        try:
            b=mp.findroot(lambda b:objective(b,offsets,y,P,sd)[1],(initial,initial+sd/10),maxsteps=60)
            if lo<=b<=hi:
                f=objective(b,offsets,y,P,sd)[0]
                if f<best:best=f;best_beta=b
        except (ValueError,ZeroDivisionError):pass
    upper=best+SLACK
    far_left=sum(pi*yi**2 for pi,yi in zip(P,y))-2*sum(pi*yi*model.moments(o+lo,sd)[0] for o,yi,pi in zip(offsets,y,P))-SLACK
    far_right=objective(hi,offsets,y,P,sd)[0]-SLACK
    nodes=[];heap=[]
    def add(a,b,parent):
        nonlocal best,best_beta,upper
        mid=(a+b)/2;radius=(b-a)/2;f,g=objective(mid,offsets,y,P,sd)
        density_sum=mp.mpf(0)
        for o,yi,pi in zip(offsets,y,P):
            left=o+a;right=o+b
            distance=mp.mpf(0) if left<=0<=right else min(abs(left),abs(right))
            density_sum+=pi*yi*model.phi(distance/sd)/sd
        H=2*(1+density_sum)
        lower=max(mp.mpf(0),f-abs(g)*radius-H*radius**2/2-SLACK)
        if f<best:best=f;best_beta=mid;upper=f+SLACK
        idx=len(nodes);nodes.append(dict(id=idx,parent=parent,lo=a,hi=b,mid=mid,f=f,g=g,H=H,lower=lower,upper_after=upper))
        if lower<upper:heapq.heappush(heap,(lower,idx,a,b))
    add(lo,hi,None);expansions=0
    while True:
        while heap and heap[0][0]>=upper:heapq.heappop(heap)
        lower=min(upper,far_left,far_right,heap[0][0] if heap else upper)
        gap=upper-lower
        if gap<=tolerance or expansions>=LIMIT or not heap:break
        _,idx,a,b=heapq.heappop(heap);mid=(a+b)/2
        add(a,mid,idx);add(mid,b,idx);expansions+=1
    return dict(beta=best_beta,lower=lower,upper=upper,gap=gap,resolved=gap<=tolerance,
                expansions=expansions,nodes=nodes,active_heap=heap,
                excluded_lower_halfline=far_left,excluded_upper_halfline=far_right)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--review',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=HERE/'calibrated_run_v1');args=parser.parse_args()
    assert args.review.is_file(),'Independent method review required'
    out=args.output;out.mkdir(parents=True,exist_ok=False);snap=out/'source_snapshot';snap.mkdir()
    for p in [Path(__file__),HERE/'run_frozen_map.py',HERE/'calibration_precision_protocol.md',args.review]:shutil.copy2(p,snap/p.name)
    shutil.copy2(HERE/'frozen_run_v1/results.json',snap/'frozen_geometry_results.json')
    frozen=json.loads((HERE/'frozen_run_v1/results.json').read_text())
    z=mp.findroot(lambda z:model.pc*z+model.qc*(z*model.Phi(z)+model.phi(z)),-.4)
    v=model.pc*(1+z*z)+model.qc*model.moments(z,mp.mpf(1))[1]
    coefficient=mp.sqrt(model.C/(model.Dc-v))
    settings=dict(precision_digits=70,slack=str(SLACK),maximum_expansions=LIMIT,
                  coefficient=str(coefficient),multipliers=['.5','2'],method='Numerical midpoint Taylor B&B, interval-specific analytic curvature bound')
    (out/'settings.json').write_text(json.dumps(settings,indent=2));results=[];start=time.time()
    states=[(0,0),(0,1),(1,0),(1,1)]
    for case in frozen['cases']:
        eps=mp.mpf(case['epsilon']);p=mp.mpf(case['p']);P=[mp.fprod([p if bit else 1-p for bit in x]) for x in states]
        tolerance=min(mp.mpf('1e-10'),model.C*eps**3/100)
        for multiplier in [mp.mpf('.5'),mp.mpf(2)]:
            sigma=multiplier*coefficient*eps**mp.mpf('1.5');totals={}
            folder=out/f"epsilon_{case['epsilon']}_multiplier_{multiplier}";folder.mkdir()
            for name,w,bias in [('sharing',[mp.mpf(t) for t in case['weights']],[mp.mpf(t) for t in case['bias']]),('mono',[mp.mpf(1),mp.mpf(0)],[mp.mpf(0),p])]:
                lower=upper=mp.mpf(0);resolved=True
                for i,I in enumerate([mp.mpf(1),mp.mpf('.5')]):
                    offsets=[w[i]*sum(w[j]*x[j] for j in range(2)) for x in states]
                    result=calibrate(offsets,[mp.mpf(x[i]) for x in states],P,sigma*abs(w[i]),bias[i],tolerance/mp.mpf('1.5'))
                    (folder/f'{name}_feature_{i}.json').write_text(json.dumps(serial(result),indent=2))
                    lower+=I*result['lower'];upper+=I*result['upper'];resolved=resolved and result['resolved']
                totals[name]=dict(lower=lower,upper=upper,resolved=resolved)
            dl=totals['sharing']['lower']-totals['mono']['upper'];du=totals['sharing']['upper']-totals['mono']['lower']
            row=dict(epsilon=case['epsilon'],multiplier=str(multiplier),sigma=str(sigma),target_total_gap=str(tolerance),models=serial(totals),delta_lower=str(dl),delta_upper=str(du),
                     sign='positive' if dl>0 else 'negative' if du<0 else 'unresolved')
            results.append(row);(out/'comparisons.json').write_text(json.dumps(results,indent=2))
            print(case['epsilon'],str(multiplier),row['sign'],flush=True)
    (out/'timing.json').write_text(json.dumps(dict(seconds=time.time()-start)))
    (out/'sha256_manifest.json').write_text(json.dumps({p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()},indent=2))

if __name__=='__main__':main()
