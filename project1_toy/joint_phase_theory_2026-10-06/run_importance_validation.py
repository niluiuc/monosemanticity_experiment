"""Four predeclared importance cases; exact roots and reviewed population risks."""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, shutil, time
import mpmath as mp
import sympy as sy
import run_frozen_map as model
import run_critical_calibration as calibration

HERE=Path(__file__).resolve().parent
mp.mp.dps=70

def number(f): return mp.mpf(f.numerator)/f.denominator

def exact_root(eta,epsilon):
    rad=1+2*eta-3*eta*eta
    def add(a,b): return a[0]+b[0],a[1]+b[1]
    def scale(a,z): return a[0]*z,a[1]*z
    def mul(a,b): return a[0]*b[0]+rad*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
    def con(x): return F(x),F(0)
    def sign(a):
        u,v=a
        if v==0:return (u>0)-(u<0)
        if u==0:return (v>0)-(v<0)
        if u>0 and v>0:return 1
        if u<0 and v<0:return -1
        cmp=(u*u>rad*v*v)-(u*u<rad*v*v)
        return cmp if u>0 else -cmp
    p=((1+eta)/(2*eta)-epsilon,-1/(2*eta));q=add(con(1),scale(p,-1))
    D=add(q,mul(p,p));pq=mul(p,q)
    A=add(p,scale(D,-eta));E=add(q,scale(D,-eta))
    coefficients=[scale(pq,-1),add(scale(E,2),scale(A,-1)),scale(pq,3),A]
    def value(k):
        r=con(0)
        for c in coefficients:r=add(scale(r,k),c)
        return r
    lo,hi=F(0),F(1,8)
    assert sign(value(lo))==-1 and sign(value(hi))==1
    for _ in range(200):
        mid=(lo+hi)/2
        if sign(value(mid))<0:lo=mid
        else:hi=mid
    assert sign(value(lo))==-1 and sign(value(hi))==1
    assert sign(add(p,con(-F(7,20))))>=0 and sign(add(con(F(21,50)),scale(p,-1)))>=0
    pnum=number(p[0])+number(p[1])*mp.sqrt(number(rad))
    return pnum,(number(lo)+number(hi))/2,dict(radicand=str(rad),p_pair=[str(v) for v in p],
        cubic_pairs=[[str(v) for v in c] for c in coefficients],root_lower=str(lo),root_upper=str(hi),
        lower_value=[str(v) for v in value(lo)],upper_value=[str(v) for v in value(hi)],lower_sign=-1,upper_sign=1)

def risk(w,bias,p,sigma,eta):
    result=mp.mpf(0)
    for x in [(0,0),(0,1),(1,0),(1,1)]:
        prob=mp.fprod([p if v else 1-p for v in x]);h=sum(wi*xi for wi,xi in zip(w,x))
        for i,importance in enumerate([mp.mpf(1),eta]):
            m1,m2=model.moments(w[i]*h+bias[i],sigma*abs(w[i]))
            result+=prob*importance*(m2-2*x[i]*m1+x[i]*x[i])
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--review',type=Path,required=True)
    ap.add_argument('--output',type=Path,default=HERE/'importance_run_v1');args=ap.parse_args()
    assert args.review.is_file()
    proof=HERE/'importance_interval_derivation.tex'
    if not proof.exists():proof=HERE.parents[1]/'output/pdf/Superposition_Recursive_Training_Derivations.pdf'
    assert proof.is_file(),'Reviewed derivation source or public derivations PDF required'
    out=args.output;out.mkdir(parents=True,exist_ok=False);snap=out/'source_snapshot';snap.mkdir()
    for path in [Path(__file__),HERE/'run_frozen_map.py',HERE/'run_critical_calibration.py',
                 HERE/'importance_validation_protocol.md',args.review]:
        shutil.copy2(path,snap/path.name)
    (snap/'proof_provenance.json').write_text(json.dumps(dict(path=str(proof),sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),note='Proof referenced without duplicating excluded LaTeX or PDF files.'),indent=2))
    p,k,e=sy.symbols('p k e');q=1-p;D=1-p+p*p;A=p-e*D;E=1-p-e*D
    delta=p*q/D*k*k*(A+2*p*q*k+E*k*k)/(1+k*k)**2
    J=A+3*p*q*k+(2*E-A)*k*k-p*q*k**3
    identity=sy.factor(sy.diff(delta,k)-2*p*q/D*k*J/(1+k*k)**3)==0
    assert identity
    settings=dict(etas=['.48','.52'],epsilons=['.005','.001'],digits=70,slack=str(calibration.SLACK),
        calibration_expansion_limit=calibration.LIMIT,multipliers=['.5','2'],root_bisections=200,
        frozen_crossing_relative_width='1e-5',stationarity_identity=identity)
    (out/'settings.json').write_text(json.dumps(settings,indent=2));cases=[];start=time.time()
    states=[(0,0),(0,1),(1,0),(1,1)]
    for eraw in settings['etas']:
        eta=mp.mpf(eraw);rad=1+2*eta-3*eta*eta;pc=2*eta/(1+eta+mp.sqrt(rad));qc=1-pc;Dc=1-pc+pc*pc
        slope=mp.sqrt(rad);K=slope/(3*pc*qc);C=slope**3/(27*Dc*pc*qc);B=qc*(1-2*pc)/2
        z=mp.findroot(lambda z:pc*z+qc*(z*model.Phi(z)+model.phi(z)),-.4)
        v=pc*(1+z*z)+qc*model.moments(z,mp.mpf(1))[1];Bc=Dc-v
        cf=mp.sqrt(C/B);cc=mp.sqrt(C/Bc)
        for raw in settings['epsilons']:
            eps=mp.mpf(raw);p,k,exact=exact_root(F(eraw),F(raw));w,bias=model.geometry(k,p)
            assert abs(p-(pc-eps))<mp.mpf('1e-65')
            folder=out/f'eta_{eraw}_epsilon_{raw}';folder.mkdir()
            mono=([mp.mpf(1),mp.mpf(0)],[mp.mpf(0),p])
            def difference(s):return risk(w,bias,p,s,eta)-risk(*mono,p,s,eta)
            lo=cf*eps**mp.mpf('1.5')/2;hi=cf*eps**mp.mpf('1.5')*2
            flo,fhi=difference(lo),difference(hi);frozen=dict(lower=lo,upper=hi,delta_lower=flo,delta_upper=fhi)
            history=[]
            if flo*fhi<0:
                for step in range(100):
                    mid=(lo+hi)/2;fm=difference(mid);history.append(dict(step=step,lower=lo,upper=hi,midpoint=mid,delta=fm))
                    if flo*fm<=0:hi,fhi=mid,fm
                    else:lo,flo=mid,fm
                    if (hi-lo)/((lo+hi)/2)<mp.mpf('1e-5'):break
                frozen['crossing']=dict(lower=lo,upper=hi,delta_lower=flo,delta_upper=fhi,
                    scaled_lower=lo/eps**mp.mpf('1.5'),scaled_upper=hi/eps**mp.mpf('1.5'))
            (folder/'frozen_bisection.json').write_text(json.dumps(calibration.serial(history),indent=2))
            P=[mp.fprod([p if bit else 1-p for bit in x]) for x in states];tol=min(mp.mpf('1e-10'),C*eps**3/100)
            comparisons=[]
            for mult in [mp.mpf('.5'),mp.mpf(2)]:
                sigma=mult*cc*eps**mp.mpf('1.5');totals={}
                for name,ww,bb in [('sharing',w,bias),('mono',*mono)]:
                    lower=upper=mp.mpf(0);resolved=True
                    for i,I in enumerate([mp.mpf(1),eta]):
                        offsets=[ww[i]*sum(ww[j]*x[j] for j in range(2)) for x in states]
                        ledger=calibration.calibrate(offsets,[mp.mpf(x[i]) for x in states],P,sigma*abs(ww[i]),bb[i],tol/(1+eta))
                        (folder/f'calibration_{mult}_{name}_feature_{i}.json').write_text(json.dumps(calibration.serial(ledger),indent=2))
                        lower+=I*ledger['lower'];upper+=I*ledger['upper'];resolved=resolved and ledger['resolved']
                    totals[name]=dict(lower=lower,upper=upper,resolved=resolved)
                dl=totals['sharing']['lower']-totals['mono']['upper'];du=totals['sharing']['upper']-totals['mono']['lower']
                comparisons.append(dict(multiplier=mult,sigma=sigma,models=totals,delta_lower=dl,delta_upper=du,
                    sign='positive' if dl>0 else 'negative' if du<0 else 'unresolved'))
            case=dict(eta=eraw,epsilon=raw,p=p,k=k,weights=w,bias=bias,exact=exact,
                constants=dict(pc=pc,K=K,C=C,B=B,Bcal=Bc,frozen_coefficient=cf,calibrated_coefficient=cc),
                k_over_epsilon=k/eps,clean_gain_over_epsilon_cubed=-difference(0)/eps**3,
                frozen=frozen,calibrated=comparisons,calibration_total_gap_target=tol)
            cases.append(case);(out/'results.json').write_text(json.dumps(calibration.serial(dict(cases=cases)),indent=2))
            print(eraw,raw,'frozen bracket',bool(frozen.get('crossing')),'calibrated signs',[x['sign'] for x in comparisons],flush=True)
    (out/'timing.json').write_text(json.dumps(dict(seconds=time.time()-start)))
    (out/'sha256_manifest.json').write_text(json.dumps({x.relative_to(out).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in out.rglob('*') if x.is_file()},indent=2))

if __name__=='__main__':main()
