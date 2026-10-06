"""Prescribed same-outcome decoder calibration: no new representation learning.

Numerical branch-and-bound provides a declared floating-slack global-loss gap,
not an exact-arithmetic theorem. Independent senior approval precedes execution.
"""
import argparse
import csv
import hashlib
import heapq
import json
import platform
import shutil
import sys
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.special import ndtr
from scipy.optimize import minimize_scalar
from toy_math_snapshot import binary_population,exact_decoder_mse
from bridge_math_snapshot import optimal_biases

SETTINGS={'p':.5,'importance':[1.,1.],'n':2,'m':1,'encoder_energy':1.,
          'geometries':['shared_same_sign','shared_opposite_sign','mono_retain_0'],
          'sigmas':[0.,.30,.60],'primary_outcome':'summed population reconstruction MSE',
          'population':'four equally probable independent Bernoulli(.5) states',
          'noise':'Gaussian code noise h+sigma*epsilon,epsilon N(0,1)',
          'fixed_W':True,'bias_calibration':'oracle population separately for EVERY geometry',
          'global_feature_loss_tolerance':1e-8,'floating_slack':1e-12,
          'maximum_interval_expansions':100000,
          'curvature_bound':'2*(1+1/(sd*sqrt(2*pi)))',
          'upper_beta':'1-min(offsets)','lower_beta':'-max(offsets)-12*sd-1',
          'bounded_local_incumbent':{'method':'bounded','xatol':1e-12,'maxiter':500},
          'global_claim':'numerical bounded global-gap check, not exact rational proof',
          'linear_control_added':False,'no_new_training':True}
ACTIVE_OUTPUT=None


def write_json(path,data):
    path.write_text(json.dumps(data,indent=2,allow_nan=True),encoding='utf-8')


def write_csv(path,rows):
    if not rows:return
    with path.open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def scalar_moments(mu,sd):
    if sd==0:
        first=np.maximum(mu,0);return first,first**2
    z=mu/sd;density=np.exp(-z*z/2)/np.sqrt(2*np.pi);cdf=ndtr(z)
    first=sd*density+mu*cdf
    second=(mu*mu+sd*sd)*cdf+mu*sd*density
    return first,second


def scalar_objective_gradient(beta,offsets,labels,probabilities,sd):
    mu=offsets+beta
    first,second=scalar_moments(mu,sd)
    loss=float(probabilities@(second-2*labels*first+labels**2))
    z=mu/sd;density=np.exp(-z*z/2)/np.sqrt(2*np.pi)
    gradient=float(2*probabilities@((mu-labels)*ndtr(z)+sd*density))
    return loss,gradient


def calibrate_feature(offsets,labels,probabilities,sd,clean_beta,folder):
    """Numerical global B&B with explicit excluded-tail lower checks."""
    start=time.perf_counter();slack=SETTINGS['floating_slack']
    if sd==0:
        # Here sd=0 in a positive-noise case means an exactly zero encoder column.
        # Its offset is identically zero and optimum output is the label mean.
        if np.any(offsets!=0):
            raise AssertionError('Zero-column offsets must be exactly zero')
        beta=float(probabilities@labels)
        loss=float(probabilities@((beta-labels)**2))
        result={'resolved':True,'method':'exact zero-column optimal constant','beta':beta,
                'objective':loss,'global_lower':loss,'global_upper':loss,'global_gap':0.,
                'interval_expansions':0,'seconds':time.perf_counter()-start}
        write_json(folder/'result.json',result);return result
    B=float(-max(offsets)-12*sd-1);U=float(1-min(offsets))
    H=float(2*(1+1/(sd*np.sqrt(2*np.pi))))
    feasible=[]
    for label,beta in [('clean_bias',float(clean_beta)),('lower_boundary',B),('upper_boundary',U)]:
        loss,gradient=scalar_objective_gradient(beta,offsets,labels,probabilities,sd)
        feasible.append({'source':label,'beta':beta,'loss':loss,'gradient':gradient})
    local=minimize_scalar(lambda b:scalar_objective_gradient(b,offsets,labels,probabilities,sd)[0],
                          bounds=(B,U),method='bounded',
                          options={k:SETTINGS['bounded_local_incumbent'][k] for k in ['xatol','maxiter']})
    local_loss,local_g=scalar_objective_gradient(float(local.x),offsets,labels,probabilities,sd)
    feasible.append({'source':'bounded local feasible incumbent, not a global proof',
                     'beta':float(local.x),'loss':local_loss,'gradient':local_g})
    best=min(feasible,key=lambda c:c['loss'])
    best_beta=best['beta'];best_value=best['loss'];best_upper=best_value+slack
    first_B,_=scalar_moments(offsets+B,sd)
    mean_label=float(probabilities@labels)
    excluded_lower=float(mean_label-2*probabilities@(labels*first_B)-slack)
    upper_loss,_=scalar_objective_gradient(U,offsets,labels,probabilities,sd)
    excluded_upper=upper_loss-slack
    boundary_check={'B':B,'U':U,'sd':sd,'curvature_bound':H,
                    'excluded_lower_halfline_loss_bound':excluded_lower,
                    'upper_halfline_loss_lower_bound':excluded_upper,
                    'initial_feasible_upper':best_upper,
                    'lower_halfline_cannot_beat_feasible_upper':excluded_lower>=best_upper,
                    'upper_halfline_cannot_beat_feasible_upper':excluded_upper>=best_upper,
                    'local_minimizer_status':{'success':bool(local.success),'message':str(local.message),
                                               'nfev':int(local.nfev)}}
    write_json(folder/'boundary_checks.json',boundary_check)
    write_json(folder/'initial_feasible_candidates.json',feasible)
    if excluded_lower<best_upper or excluded_upper<best_upper:
        result={'resolved':False,'reason':'excluded-region bound cannot rule out better minimum',
                'beta':best_beta,'objective':best_value,'global_upper':best_upper,
                'global_lower':min(excluded_lower,excluded_upper),
                'global_gap':best_upper-min(excluded_lower,excluded_upper),
                'interval_expansions':0,'seconds':time.perf_counter()-start}
        write_json(folder/'result.json',result);return result
    nodes=[];queue=[];actions=[];expansions=0
    def add_node(lo,hi,parent):
        nonlocal best_beta,best_value,best_upper
        mid=(lo+hi)/2;r=(hi-lo)/2
        f,g=scalar_objective_gradient(mid,offsets,labels,probabilities,sd)
        lower=max(0.,f-abs(g)*r-H*r*r/2-slack)
        idx=len(nodes)
        if f<best_value:
            best_beta=mid;best_value=f;best_upper=f+slack
        pruned=lower>=best_upper
        nodes.append({'node':idx,'parent':parent,'lo':lo,'hi':hi,'midpoint':mid,'radius':r,
                      'midpoint_loss':f,'midpoint_gradient':g,'lower_bound':lower,
                      'best_upper_after_evaluation':best_upper,'pruned_at_creation':pruned})
        if not pruned:heapq.heappush(queue,(lower,idx,lo,hi))
    add_node(B,U,None)
    stop_reason=None
    while True:
        while queue and queue[0][0]>=best_upper:
            item=heapq.heappop(queue)
            actions.append({'action':'prune_after_incumbent_improvement','node':item[1],
                            'lower_bound':item[0],'best_upper':best_upper,'expansions':expansions})
        finite_lower=queue[0][0] if queue else best_upper
        global_lower=min(finite_lower,excluded_lower,excluded_upper,best_upper)
        gap=max(0.,best_upper-global_lower)
        if gap<=SETTINGS['global_feature_loss_tolerance']:
            stop_reason='numerical global gap tolerance';break
        if expansions>=SETTINGS['maximum_interval_expansions']:
            stop_reason='interval expansion budget';break
        if not queue:
            stop_reason='queue empty with unresolved excluded-region bound';break
        lower,idx,lo,hi=heapq.heappop(queue)
        actions.append({'action':'expand','node':idx,'lower_bound':lower,
                        'best_upper':best_upper,'expansions':expansions})
        mid=(lo+hi)/2
        add_node(lo,mid,idx);add_node(mid,hi,idx);expansions+=1
    final_loss,final_g=scalar_objective_gradient(best_beta,offsets,labels,probabilities,sd)
    result={'resolved':gap<=SETTINGS['global_feature_loss_tolerance'],
            'reason':stop_reason,'method':'midpoint Taylor lower bound numerical B&B',
            'beta':best_beta,'objective':final_loss,'gradient':final_g,
            'global_lower':global_lower,'global_upper':best_upper,'global_gap':gap,
            'interval_expansions':expansions,'generated_nodes':len(nodes),'remaining_nodes':len(queue),
            'seconds':time.perf_counter()-start}
    write_csv(folder/'interval_ledger.csv',nodes);write_json(folder/'actions.json',actions)
    write_json(folder/'remaining_intervals.json',[{'lower':x[0],'node':x[1],'lo':x[2],'hi':x[3]} for x in sorted(queue)])
    write_json(folder/'result.json',result)
    return result


def main():
    global ACTIVE_OUTPUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--senior-review',required=True,help='Saved independent method approval before execution.')
    parser.add_argument('--output',default='run_v1',help='Fresh directory; overwriting refused.')
    args=parser.parse_args();base=Path(__file__).resolve().parent
    review=Path(args.senior_review).resolve()
    if not review.is_file():raise SystemExit('Senior method approval missing; no cases executed.')
    output=Path(args.output).resolve();output.mkdir(exist_ok=False,parents=True)
    ACTIVE_OUTPUT=output
    snapshot=output/'source_snapshot';snapshot.mkdir()
    for name in ['run_calibration_control.py','toy_math_snapshot.py','bridge_math_snapshot.py','calibration_protocol.md']:
        shutil.copy2(base/name,snapshot/name)
    shutil.copy2(review,snapshot/'senior_method_review.md')
    write_json(output/'settings.json',SETTINGS)
    write_json(output/'environment.json',{'python':sys.version,'executable':sys.executable,
               'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),
               'senior_review':str(review)})
    start=time.perf_counter();states,P=binary_population(2,.5)
    a=(1+1/np.sqrt(2))/2;c=1-a
    models=[('shared_same_sign',np.array([[np.sqrt(a),np.sqrt(c)]])),
            ('shared_opposite_sign',np.array([[np.sqrt(a),-np.sqrt(c)]])),
            ('mono_retain_0',np.array([[1.,0.]]))]
    rows=[];derivative_checks=[];all_results=[]
    for label,W in models:
        clean_bias,clean_loss,clean_candidates=optimal_biases(W,states,P,[1.,1.])
        model_folder=output/label;model_folder.mkdir()
        write_json(model_folder/'supplied_geometry.json',{'W':W.tolist(),'energy':float(np.sum(W*W)),
                  'clean_optimal_bias':clean_bias.tolist(),'clean_loss':clean_loss,
                  'clean_bias_candidates':clean_candidates})
        offsets=states@(W.T@W)
        for sigma in SETTINGS['sigmas']:
            case=model_folder/f'sigma_{sigma:.2f}';case.mkdir()
            frozen=exact_decoder_mse(W,clean_bias,states,P,sigma)
            if sigma==0:
                calibrated_bias=clean_bias.copy();calibrated=frozen.copy()
                global_lower=calibrated.copy();global_upper=calibrated.copy();results=[]
            else:
                results=[]
                for feature in range(2):
                    feature_folder=case/f'feature_{feature}';feature_folder.mkdir()
                    sd=float(sigma*abs(W[0,feature]))
                    if sd>0:
                        for beta in [float(clean_bias[feature]),0.]:
                            loss,g=scalar_objective_gradient(beta,offsets[:,feature],states[:,feature],P,sd)
                            h=1e-6
                            lp=scalar_objective_gradient(beta+h,offsets[:,feature],states[:,feature],P,sd)[0]
                            lm=scalar_objective_gradient(beta-h,offsets[:,feature],states[:,feature],P,sd)[0]
                            difference=abs(g-(lp-lm)/(2*h))
                            derivative_checks.append({'label':label,'sigma':sigma,'feature':feature,'beta':beta,
                                                      'analytic_gradient':g,'central_difference':(lp-lm)/(2*h),
                                                      'absolute_discrepancy':difference})
                            if difference>1e-6:
                                write_json(output/'derivative_checks.json',derivative_checks)
                                raise AssertionError('Gradient check failed; diagnostic values saved')
                    result=calibrate_feature(offsets[:,feature],states[:,feature],P,sd,float(clean_bias[feature]),feature_folder)
                    results.append(result)
                    if not result['resolved']:
                        write_json(output/'failure.json',{'label':label,'sigma':sigma,'feature':feature,
                                   'reason':'unresolved global calibration gap; stopped without changing settings',
                                   'feature_result':result})
                        raise RuntimeError('Unresolved global calibration; raw failure retained')
                calibrated_bias=np.array([r['beta'] for r in results])
                calibrated=exact_decoder_mse(W,calibrated_bias,states,P,sigma)
                global_lower=np.array([r['global_lower'] for r in results]);global_upper=np.array([r['global_upper'] for r in results])
            resolved=all(r['resolved'] for r in results)
            row={'label':label,'sigma':sigma,'frozen_clean_bias_0':float(clean_bias[0]),
                 'frozen_clean_bias_1':float(clean_bias[1]),'calibrated_bias_0':float(calibrated_bias[0]),
                 'calibrated_bias_1':float(calibrated_bias[1]),'frozen_sum_mse':float(frozen.sum()),
                 'calibrated_sum_mse':float(calibrated.sum()),'calibrated_global_lower':float(global_lower.sum()),
                 'calibrated_global_upper':float(global_upper.sum()),
                 'calibrated_sum_gap':float((global_upper-global_lower).sum()),'resolved':resolved}
            for i in range(2):row.update({f'frozen_mse_{i}':float(frozen[i]),f'calibrated_mse_{i}':float(calibrated[i])})
            rows.append(row);all_results.append({'label':label,'sigma':sigma,'features':results})
            np.savez_compressed(case/'outputs.npz',W=W,clean_bias=clean_bias,calibrated_bias=calibrated_bias,
                                frozen_mse=frozen,calibrated_mse=calibrated,global_lower=global_lower,global_upper=global_upper)
            print(json.dumps(row),flush=True)
    write_csv(output/'outcomes.csv',rows);write_json(output/'all_calibration_results.json',all_results)
    write_json(output/'derivative_checks.json',derivative_checks)
    write_json(output/'timings.json',{'seconds':time.perf_counter()-start})
    manifest={str(path.relative_to(output)):hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(output.rglob('*')) if path.is_file()}
    write_json(output/'sha256_manifest.json',manifest)
    print('Stopped after the three supplied codes and sigma0/.30/.60:',output,flush=True)


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        if ACTIVE_OUTPUT is not None:
            failure_path=ACTIVE_OUTPUT/'failure.json'
            if not failure_path.exists():write_json(failure_path,{'exception':type(exc).__name__,'message':str(exc)})
            manifest={str(path.relative_to(ACTIVE_OUTPUT)):hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in sorted(ACTIVE_OUTPUT.rglob('*')) if path.is_file() and path.name!='sha256_manifest.json'}
            write_json(ACTIVE_OUTPUT/'sha256_manifest.json',manifest)
        raise
