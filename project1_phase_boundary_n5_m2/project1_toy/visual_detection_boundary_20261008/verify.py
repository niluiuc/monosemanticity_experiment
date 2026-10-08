"""Independent saved-output verification; do not import experimental runner."""
import hashlib,json,time
from pathlib import Path
import numpy as np
from scipy.stats import norm
H=Path(__file__).parent;O=H/'run_v1'
result=json.loads((O/'result.json').read_text());f=json.loads((O/'frozen_prediction_hashes.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for name,digest in f['hashes'].items():
 p=H/name if name in ['run.py','PROTOCOL.md'] else O/name
 assert sha(p)==digest,(name,'frozen file changed')
ids=np.load(O/'split_ids.npz');assert len(np.intersect1d(ids['train'],ids['calibration']))==0
assert len(set(ids['test'].tolist()))==len(ids['test'])
if result['status']!='complete':
 report=dict(status='verified_prerequisite_failure',frozen_hashes_verified=True,test_not_scored=not (O/'test_results.npz').exists(),result=result)
else:
 pred=np.load(O/'prediction.npz');a=np.load(O/'test_results.npz');noise=np.load(O/'test_noise.npz')['noise'];B=np.load(O/'sharing_test_codes.npz')['states'];cnt=B.sum(1);P=a['p'];S=a['sigma'];pr=P[None,:]**cnt[:,None]*(1-P[None,:])**(5-cnt[:,None])
 alpha=2*np.pi*np.arange(5)/5;V=np.array([np.cos(alpha),np.sin(alpha)]);W=V*np.sqrt(2/5)
 mono=np.zeros((2,5));mono[0,0]=mono[1,1]=1
 specs=[('sharing',W,V,np.ones(5)*np.sqrt(2/5)/2),('mono',mono,mono,np.array([.5,.5,0,0,0]))]
 before_test=f['time_ns']<min((O/f'{name}_test_codes.npz').stat().st_mtime_ns for name,_,_,_ in specs);assert before_test
 max_mc=0.;mc=[];theory={key:[] for key in ['calibration','test','ideal']}
 clean=[]
 for s in S:
  errors=[]
  for name,w,v,t in specs:
   code=np.load(O/f'{name}_test_codes.npz')['codes'];score=np.einsum('bsdk,ki->bsdi',code[:,:,None,:]+s*noise,v)
   predic=score>t
   if name=='mono':predic[...,2:]=False
   errors.append(np.count_nonzero(predic!=B[None,:,None,:],axis=-1).mean(-1))
  gap=errors[0]-errors[1];i=len(mc);max_mc=max(max_mc,float(abs(gap-a['state_background_gaps'][i]).max()));mc.append(gap)
  for split in theory:
   vals=[]
   for name,w,v,t in specs:
    code=(B@w.T)[None,:,:] if split=='ideal' else np.load(O/f'{name}_{split}_codes.npz')['codes'] if split=='test' else np.load(O/f'{name}_calibration.npz')['codes']
    means=np.einsum('bsk,ki->bsi',code,v);e=np.zeros_like(means)
    for j in range(5):
     if name=='mono' and j>=2:e[:,:,j]=B[None,:,j]
     else:e[:,:,j]=np.where(B[None,:,j]==1,norm.cdf((t[j]-means[:,:,j])/s),norm.sf((t[j]-means[:,:,j])/s))
    vals.append(e.sum(2).mean(0))
   theory[split].append((vals[0]-vals[1])@pr)
 np.testing.assert_allclose(np.array(mc),a['state_background_gaps'],atol=1e-12)
 np.testing.assert_allclose(np.array(mc).mean(1)@pr,a['simulation_gap'],atol=1e-12)
 np.testing.assert_allclose(theory['calibration'],pred['calibration_gap'],atol=1e-12)
 np.testing.assert_allclose(theory['ideal'],pred['ideal_gap'],atol=1e-12)
 np.testing.assert_allclose(theory['test'],a['test_exact_gap'],atol=1e-12)
 # Conditional mean agreement, with background variation for Monte Carlo uncertainty.
 pr2=.2**cnt*.8**(5-cnt);expected=np.array(theory['test'])[:,6];sample=np.array(mc)@pr2
 errors=sample.mean(1)-expected;se=sample.std(1,ddof=1)/np.sqrt(128)
 report=dict(status='verified',frozen_hashes_verified=True,prediction_precedes_test=before_test,training_calibration_backgrounds_disjoint=True,test_from_official_test_split=True,all_saved_state_noise_losses_recomputed=True,max_loss_discrepancy=max_mc,max_formula_discrepancy=float(abs(np.array(theory['test'])-a['test_exact_gap']).max()),max_p02_mc_minus_exact=float(abs(errors).max()),max_p02_standardized_error=float((abs(errors)/np.maximum(se,1e-12)).max()),result=result,limitation='One controlled visual construction and one fixed trained pair; code targets imposed; code noise only.')
(O/'independent_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
