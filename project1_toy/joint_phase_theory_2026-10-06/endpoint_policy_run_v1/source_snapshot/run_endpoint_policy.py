"""Two fixed comparisons of decoder policy at the importance endpoint."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,shutil,time
import mpmath as mp
import run_frozen_map as model
import run_critical_calibration as calibration
from run_importance_validation import risk,number

H=Path(__file__).resolve().parent;mp.mp.dps=70

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--review',type=Path,required=True)
    ap.add_argument('--output',type=Path,default=H/'endpoint_policy_run_v1');args=ap.parse_args()
    assert args.review.is_file() and (H/'endpoint_calibration_derivation.tex').is_file()
    out=args.output;out.mkdir(parents=True,exist_ok=False);snap=out/'source_snapshot';snap.mkdir()
    for path in [Path(__file__),H/'run_importance_validation.py',H/'run_frozen_map.py',H/'run_critical_calibration.py',
                 H/'endpoint_policy_protocol.md',H/'endpoint_calibration_derivation.tex',args.review]:
        shutil.copy2(path,snap/path.name)
    eta=mp.mpf(2)/3;C=mp.mpf(16)/81
    z=mp.findroot(lambda z:z/2+(z*model.Phi(z)+model.phi(z))/2,-.4)
    v=(1+z*z)/2+model.moments(z,mp.mpf(1))[1]/2;Bc=mp.mpf('.75')-v;coefficient=mp.sqrt(C/Bc)
    (out/'settings.json').write_text(json.dumps(dict(epsilons=['.005','.001'],eta='2/3',multiplier=2,
        precision_digits=70,slack=str(calibration.SLACK),maximum_expansions=calibration.LIMIT,
        C=str(C),v=str(v),Bcal=str(Bc),coefficient=str(coefficient)),indent=2))
    results=[];states=[(0,0),(0,1),(1,0),(1,1)];start=time.time()
    for raw in ['.005','.001']:
        eps=mp.mpf(raw);pr=F(1,2)-F(raw);qr=1-pr;Dr=1-pr+pr*pr;A=pr-F(2,3)*Dr;E=1-pr-F(2,3)*Dr
        J=lambda k:A+3*pr*qr*k+(2*E-A)*k*k-pr*qr*k**3
        lo,hi=F(0),F(1,8);assert J(lo)<0<J(hi)
        for _ in range(200):
            mid=(lo+hi)/2
            if J(mid)<0:lo=mid
            else:hi=mid
        assert J(lo)<0<J(hi)
        p=number(pr);k=(number(lo)+number(hi))/2;w,b=model.geometry(k,p);mono=([mp.mpf(1),mp.mpf(0)],[mp.mpf(0),p])
        sigma=2*coefficient*eps**mp.mpf('1.5');tol=min(mp.mpf('1e-10'),C*eps**3/100)
        folder=out/f'epsilon_{raw}';folder.mkdir();frozen={};calibrated={}
        P=[mp.fprod([p if bit else 1-p for bit in x]) for x in states]
        for name,ww,bb in [('sharing',w,b),('mono',*mono)]:
            frozen[name]=risk(ww,bb,p,sigma,eta)
            lower=upper=mp.mpf(0);resolved=True
            for i,I in enumerate([mp.mpf(1),eta]):
                offsets=[ww[i]*sum(ww[j]*x[j] for j in range(2)) for x in states]
                ledger=calibration.calibrate(offsets,[mp.mpf(x[i]) for x in states],P,sigma*abs(ww[i]),bb[i],tol/(1+eta))
                (folder/f'{name}_feature_{i}.json').write_text(json.dumps(calibration.serial(ledger),indent=2))
                lower+=I*ledger['lower'];upper+=I*ledger['upper'];resolved=resolved and ledger['resolved']
            calibrated[name]=dict(lower=lower,upper=upper,resolved=resolved)
        delta=frozen['sharing']-frozen['mono'];dl=calibrated['sharing']['lower']-calibrated['mono']['upper'];du=calibrated['sharing']['upper']-calibrated['mono']['lower']
        row=dict(epsilon=raw,p=p,k=k,weights=w,bias=b,sigma=sigma,
            exact_root=dict(lower=str(lo),upper=str(hi),lower_value=str(J(lo)),upper_value=str(J(hi))),
            frozen_models=frozen,frozen_delta=delta,frozen_delta_over_epsilon_cubed=delta/eps**3,
            calibrated_models=calibrated,calibrated_delta_lower=dl,calibrated_delta_upper=du,
            calibration_gap_target=tol,calibrated_sign='positive' if dl>0 else 'negative' if du<0 else 'unresolved',
            opposite_policy_orderings=(delta<0 and dl>0))
        results.append(row);(out/'results.json').write_text(json.dumps(calibration.serial(dict(cases=results)),indent=2))
        print(raw,'frozen delta',mp.nstr(delta,12),'calibrated sign',row['calibrated_sign'],'opposite',row['opposite_policy_orderings'],flush=True)
    (out/'timing.json').write_text(json.dumps(dict(seconds=time.time()-start)))
    (out/'sha256_manifest.json').write_text(json.dumps({p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()},indent=2))

if __name__=='__main__':main()
