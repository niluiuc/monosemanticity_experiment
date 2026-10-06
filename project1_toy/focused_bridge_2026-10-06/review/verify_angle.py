"""Independent audit of the two saved Armijo diagnostics, not a new sweep."""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np
from verify_toy import scalar_bias_mask_minimum, latent_risk

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'toy/run_angle_diagnostic_v1'


def read_csv(p):
    with p.open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))


def main():
    errors=[]
    config=json.loads((RUN/'settings.json').read_text(encoding='utf-8'))
    manifest=json.loads((RUN/'sha256_manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest.items():
        if hashlib.sha256((RUN/name).read_bytes()).hexdigest()!=digest:
            errors.append('Hash mismatch '+name)
    summaries=json.loads((RUN/'summaries.json').read_text(encoding='utf-8'))
    risks=read_csv(RUN/'risks.csv')
    geometry=read_csv(RUN/'geometry.csv')
    max_bias=max_grad=max_loss=max_armijo=max_risk=max_energy=0.
    trace_count=0
    for summary in summaries:
        p=summary['p']; folder=RUN/f'p_{p:.2f}'
        raw=np.load(folder/'final.npz')
        states=raw['states']; prob=raw['probabilities']; importance=np.array([1.,.5])
        trace=read_csv(folder/'trace.csv')
        for j,row in enumerate(trace):
            trace_count+=1
            theta=float(row['theta']); w=np.array([float(row['W_0']),float(row['W_1'])])
            bias=np.array([float(row['bias_0']),float(row['bias_1'])])
            h=states@w; scores=h[:,None]*w[None,:]; z=scores+bias
            residual=np.maximum(z,0)-states
            loss=float(np.sum(prob[:,None]*importance*residual**2))
            max_loss=max(max_loss,abs(loss-float(row['loss'])))
            for i in range(2):
                opt=scalar_bias_mask_minimum(scores[:,i],states[:,i],prob)
                actual=np.sum(prob*residual[:,i]**2)
                max_bias=max(max_bias,abs(actual-opt))
            wp=np.array([-np.sin(theta),np.cos(theta)])
            zp=(states@wp)[:,None]*w[None,:]+h[:,None]*wp[None,:]
            grad=float(2*np.sum(prob[:,None]*importance*residual*(z>0)*zp))
            max_grad=max(max_grad,abs(grad-float(row['angle_gradient'])))
            max_energy=max(max_energy,abs(w@w-1))
            if row['accepted_step']:
                step=float(row['accepted_step'])
                nextloss=float(row['next_loss'])
                rhs=loss-config['armijo_coefficient']*step*grad*grad
                max_armijo=max(max_armijo,nextloss-rhs)
                if j+1>=len(trace): errors.append('Missing next iterate')
                elif abs(float(trace[j+1]['theta'])-(theta-step*grad))>1e-12:
                    errors.append('Angle update mismatch')
                if nextloss>loss+1e-12: errors.append('Objective increased')
        if summary['stop_reason']!='angle_gradient_tolerance': errors.append('Did not reach prescribed gradient stop')
        if abs(float(trace[-1]['angle_gradient']))>1e-8: errors.append('Gradient above tolerance')
        expected_start=-(.5)*p*(1-p)**2*(1+p)/(1-p+p*p)
        if abs(float(trace[0]['angle_gradient'])-expected_start)>1e-12:
            errors.append('Initial derivative contradicts reviewed formula')
        for g in [x for x in geometry if float(x['p'])==p]:
            W=np.array([[float(g['W_0']),float(g['W_1'])]])
            bias=np.array([float(g['bias_0']),float(g['bias_1'])])
            for row in [x for x in risks if float(x['p'])==p and x['label']==g['label']]:
                risk,fp,fn=latent_risk(W,bias,states,prob,float(row['sigma']),row['detector'])
                discrepancy=max([abs(risk[i]-float(row[f'error_{i}'])) for i in range(2)]+
                    [abs(fp[i]-float(row[f'fp_{i}'])) for i in range(2)]+
                    [abs(fn[i]-float(row[f'fn_{i}'])) for i in range(2)])
                max_risk=max(max_risk,discrepancy)
    for value,name in [(max_bias,'bias'),(max_grad,'gradient'),(max_loss,'loss'),(max_risk,'risk')]:
        if value>1e-10: errors.append(name+' mismatch')
    if max_armijo>1e-12: errors.append('Armijo violation')
    result={'cases':len(summaries),'hashes_checked':len(manifest),'iterates_checked':trace_count,
            'risk_rows_checked':len(risks),'max_bias_loss_discrepancy':max_bias,
            'max_angle_gradient_discrepancy':max_grad,'max_objective_discrepancy':max_loss,
            'max_positive_armijo_excess':max_armijo,'max_risk_discrepancy':max_risk,
            'max_energy_discrepancy':max_energy,'errors':errors,
            'scope':'Two prescribed starting geometries; no global optimization or new cases inferred.'}
    (ROOT/'review/angle_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    if errors: raise SystemExit(1)


if __name__=='__main__': main()
