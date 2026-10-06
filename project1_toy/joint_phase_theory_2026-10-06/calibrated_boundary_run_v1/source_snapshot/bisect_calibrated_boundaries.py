"""Bisect only the six saved successful critical brackets; retain ambiguous signs."""
import argparse,hashlib,json,shutil,time
from pathlib import Path
import mpmath as mp
import run_frozen_map as model
import run_critical_calibration as calibration

HERE=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'calibrated_boundary_run_v1')
    args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=False)
    snap=out/'source_snapshot';snap.mkdir()
    sources=[Path(__file__),HERE/'run_critical_calibration.py',HERE/'run_frozen_map.py',
             HERE/'calibration_precision_protocol.md',HERE/'critical_calibration_method_review.md',
             HERE/'frozen_run_v1/results.json',HERE/'calibrated_run_v1/comparisons.json']
    for p in sources:
        name='frozen_geometry_results.json' if p.parent.name=='frozen_run_v1' else p.name
        shutil.copy2(p,snap/name)
    settings=dict(precision_digits=70,relative_bracket_width='1e-5',maximum_bisections=30,
                  loss_gap_target='unchanged:min(1e-10,C epsilon^3/100)',
                  ambiguous_midpoint_policy='stop and preserve last sign-certified bracket; no precision retuning')
    (out/'settings.json').write_text(json.dumps(settings,indent=2))
    frozen=json.loads((HERE/'frozen_run_v1/results.json').read_text());old=json.loads((HERE/'calibrated_run_v1/comparisons.json').read_text())
    results=[];states=[(0,0),(0,1),(1,0),(1,1)];start=time.time()
    for case in frozen['cases']:
        raw=case['epsilon'];eps=mp.mpf(raw);p=mp.mpf(case['p'])
        brackets=[r for r in old if r['epsilon']==raw]
        assert brackets[0]['sign']=='negative' and brackets[1]['sign']=='positive'
        lo=mp.mpf(brackets[0]['sigma']);hi=mp.mpf(brackets[1]['sigma'])
        P=[mp.fprod(p if b else 1-p for b in x) for x in states]
        tolerance=min(mp.mpf('1e-10'),model.C*eps**3/100)
        folder=out/f'epsilon_{raw}';folder.mkdir();history=[]
        stop='maximum bisections'
        for step in range(30):
            if (hi-lo)/((hi+lo)/2)<mp.mpf('1e-5'):
                stop='relative bracket width';break
            sigma=(lo+hi)/2;totals={}
            step_folder=folder/f'midpoint_{step:02}';step_folder.mkdir()
            for name,w,beta in [('sharing',[mp.mpf(t) for t in case['weights']],[mp.mpf(t) for t in case['bias']]),('mono',[mp.mpf(1),mp.mpf(0)],[mp.mpf(0),p])]:
                lower=upper=mp.mpf(0);resolved=True
                for i,I in enumerate([mp.mpf(1),mp.mpf('.5')]):
                    offsets=[w[i]*sum(w[j]*x[j] for j in range(2)) for x in states]
                    r=calibration.calibrate(offsets,[mp.mpf(x[i]) for x in states],P,sigma*abs(w[i]),beta[i],tolerance/mp.mpf('1.5'))
                    (step_folder/f'{name}_feature_{i}.json').write_text(json.dumps(calibration.serial(r),indent=2))
                    lower+=I*r['lower'];upper+=I*r['upper'];resolved=resolved and r['resolved']
                totals[name]=dict(lower=lower,upper=upper,resolved=resolved)
            dl=totals['sharing']['lower']-totals['mono']['upper'];du=totals['sharing']['upper']-totals['mono']['lower']
            sign='negative' if du<0 else 'positive' if dl>0 else 'unresolved'
            history.append(dict(step=step,sigma=str(sigma),delta_lower=str(dl),delta_upper=str(du),sign=sign,models=calibration.serial(totals)))
            if sign=='unresolved':stop='ambiguous midpoint at unchanged gap target';break
            if sign=='negative':lo=sigma
            else:hi=sigma
        result=dict(epsilon=raw,lower=str(lo),upper=str(hi),scaled_lower=str(lo/eps**mp.mpf('1.5')),scaled_upper=str(hi/eps**mp.mpf('1.5')),
                    stop_reason=stop,relative_width=str((hi-lo)/((hi+lo)/2)),history=history,
                    scope='At least one calibrated crossing in sign-certified bracket; no uniqueness/root-count guarantee')
        results.append(result);(out/'results.json').write_text(json.dumps(results,indent=2))
        print(raw,float(result['scaled_lower']),float(result['scaled_upper']),stop,flush=True)
    (out/'timing.json').write_text(json.dumps(dict(seconds=time.time()-start)))
    (out/'sha256_manifest.json').write_text(json.dumps({p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()},indent=2))

if __name__=='__main__':main()
