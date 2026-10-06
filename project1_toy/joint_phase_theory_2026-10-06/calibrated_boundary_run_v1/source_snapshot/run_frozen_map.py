"""Fixed six-case population map; no fit, training or claimed global optimizer."""
import argparse, csv, hashlib, json, shutil, time
from pathlib import Path
import mpmath as mp

HERE=Path(__file__).resolve().parent
mp.mp.dps=70
pc=(3-mp.sqrt(5))/2; qc=1-pc; Dc=1-pc+pc**2
K=mp.sqrt(5)/(6*pc*qc); C=5*mp.sqrt(5)/(216*Dc*pc*qc)
B=qc*(1-2*pc)/2; coefficient=mp.sqrt(C/B)
EPS=['.02','.01','.005','.0025','.001','.0005']
phi=lambda z:mp.exp(-z*z/2)/mp.sqrt(2*mp.pi)
Phi=lambda z:mp.erfc(-z/mp.sqrt(2))/2

def moments(mu,sd):
    if sd==0:return max(mu,0),max(mu,0)**2
    z=mu/sd
    return sd*phi(z)+mu*Phi(z),(mu*mu+sd*sd)*Phi(z)+mu*sd*phi(z)

def clean_delta(k,p):
    q=1-p; D=1-p+p*p; c=k*k/(1+k*k); r=k/(1+k*k)
    return p*q*c/D*(p-D/2+(1-2*p)*c+2*p*q*r)

def geometry(k,p):
    a=1/(1+k*k); c=k*k/(1+k*k); r=k/(1+k*k); D=1-p+p*p
    return [mp.sqrt(a),-mp.sqrt(c)],[p*(c+p*r)/D,p*(a+r)]

def risk(w,beta,p,sigma):
    out=mp.mpf(0); q=1-p
    for x in [(0,0),(0,1),(1,0),(1,1)]:
        prob=mp.fprod([p if bit else q for bit in x]); h=sum(wi*xi for wi,xi in zip(w,x))
        for i,I in enumerate([mp.mpf(1),mp.mpf('.5')]):
            m1,m2=moments(w[i]*h+beta[i],sigma*abs(w[i]))
            out+=prob*I*(m2-2*x[i]*m1+x[i]**2)
    return out

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=HERE/'frozen_run_v1')
    folder=parser.parse_args().output
    folder.mkdir(parents=True,exist_ok=False)
    snap=folder/'source_snapshot';snap.mkdir()
    for p in [Path(__file__),HERE/'frozen_map_protocol.md']:
        shutil.copy2(p,snap/p.name)
    settings={'epsilon':EPS,'noise_grid_count':121,'noise_min':'1e-7','noise_max':'2',
              'precision_digits':70,'relative_bracket_width':'1e-5','bisection_limit':100,
              'importance':['1','.5'],'geometry_global_certificate':'pending; local stationarity only',
              'outcome':'weighted population reconstruction MSE','policy':'frozen clean biases'}
    (folder/'settings.json').write_text(json.dumps(settings,indent=2))
    rows=[];cases=[];intervals=[];start=time.time()
    grid=[mp.mpf(0)]+[mp.exp(mp.log(mp.mpf('1e-7'))+j*(mp.log(2)-mp.log(mp.mpf('1e-7')))/120) for j in range(121)]
    for raw in EPS:
        eps=mp.mpf(raw);p=pc-eps
        k=mp.findroot(lambda k:mp.diff(lambda v:clean_delta(v,p),k)/k,(K*eps*mp.mpf('.8'),K*eps*mp.mpf('1.2')))
        residual=mp.diff(lambda v:clean_delta(v,p),k)
        assert abs(residual)<mp.mpf('1e-55') and 0<k<p/(1-p)
        w,beta=geometry(k,p)
        def evaluate(sigma):
            rs=risk(w,beta,p,sigma);rm=risk([mp.mpf(1),mp.mpf(0)],[mp.mpf(0),p],p,sigma)
            return rs,rm,rs-rm
        values=[evaluate(s) for s in grid]
        for sigma,(rs,rm,d) in zip(grid,values):
            rows.append(dict(epsilon=raw,p=str(p),sigma=str(sigma),sharing=str(rs),mono=str(rm),delta=str(d)))
        roots=[]
        for j in range(len(grid)-1):
            lo,hi=grid[j],grid[j+1];flo,fhi=values[j][2],values[j+1][2]
            bracket=flo*fhi<0
            intervals.append(dict(epsilon=raw,lower=str(lo),upper=str(hi),delta_lower=str(flo),delta_upper=str(fhi),detected_sign_bracket=bracket))
            if bracket:
                original=[str(lo),str(hi)]
                for it in range(100):
                    mid=(lo+hi)/2;fm=evaluate(mid)[2]
                    if flo*fm<=0:hi=mid;fhi=fm
                    else:lo=mid;flo=fm
                    if (hi-lo)/((hi+lo)/2)<mp.mpf('1e-5'):break
                roots.append(dict(initial_bracket=original,lower=str(lo),upper=str(hi),delta_lower=str(flo),delta_upper=str(fhi),iterations=it+1,
                                  sigma_over_epsilon_3_2=str((lo+hi)/2/eps**mp.mpf('1.5'))))
        checks=[]
        for scale,m in [('critical',coefficient/2),('critical',coefficient*2),('gate',mp.mpf('.05')),('gate',mp.mpf(10))]:
            sigma=m*eps**mp.mpf('1.5') if scale=='critical' else k*m
            checks.append(dict(scale=scale,multiplier=str(m),sigma=str(sigma),delta=str(evaluate(sigma)[2])))
        case=dict(epsilon=raw,p=str(p),k=str(k),weights=[str(v) for v in w],bias=[str(v) for v in beta],stationarity_residual=str(residual),
                  k_over_epsilon=str(k/eps),clean_gain_over_epsilon_cubed=str(-clean_delta(k,p)/eps**3),
                  branch_feasible=True,finite_global_certificate=False,detected_crossings=roots,prescribed_checks=checks)
        cases.append(case)
        print(raw,'detected crossings',len(roots),'critical scaled roots',[float(r['sigma_over_epsilon_3_2']) for r in roots],flush=True)
    with (folder/'population_map.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (folder/'results.json').write_text(json.dumps(dict(constants={'K':str(K),'C':str(C),'frozen_coefficient':str(coefficient)},cases=cases,seconds=time.time()-start),indent=2))
    (folder/'all_grid_intervals.json').write_text(json.dumps(intervals,indent=2))
    files=[p for p in folder.rglob('*') if p.is_file()]
    (folder/'sha256_manifest.json').write_text(json.dumps({p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))

if __name__=='__main__':main()
