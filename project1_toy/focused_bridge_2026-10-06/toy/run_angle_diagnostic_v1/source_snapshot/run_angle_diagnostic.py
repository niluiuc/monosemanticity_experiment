"""Two preregistered profiled-angle Armijo diagnostics, without broadening v1."""
import csv
import hashlib
import json
import platform
import shutil
import sys
import time
from pathlib import Path
import numpy as np
import scipy
from bridge_math import optimal_biases, weighted_loss_gradient
from run_bridge import angle_encoder
from toy_math_snapshot import binary_population, exact_detection, exact_decoder_mse, geometry

CONFIG={'n':2,'m':1,'encoder_energy':1.,'p':[.05,.20],'importance':[1.,.5],
        'theta_start':-np.pi/4,'initial_trial_step':.1,'maximum_halvings':30,
        'armijo_coefficient':1e-4,'gradient_tolerance':1e-8,'maximum_iterations':4000,
        'sigmas':[0.,.05,.15,.30,.60],
        'noise':'Gaussian code noise h+sigma*epsilon, epsilon N(0,1)',
        'purpose':'local solver diagnostic; no global-optimality claim',
        'bias_tie_policy':'retain all numerical ties; smallest finite tied bias chosen',
        'gradient':'weighted tied W gradient contracted with (-sin(theta),cos(theta)); envelope only on differentiable minimizing branches'}


def save_json(path,data):
    path.write_text(json.dumps(data,indent=2,allow_nan=True),encoding='utf-8')


def save_csv(path,rows):
    if not rows:
        return
    with path.open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def profile(theta,states,probabilities):
    W=angle_encoder(theta)
    bias,loss,details=optimal_biases(W,states,probabilities,CONFIG['importance'])
    checked_loss,gW,gb=weighted_loss_gradient(W,bias,states,probabilities,CONFIG['importance'])
    if abs(loss-checked_loss)>1e-12:
        raise AssertionError('Profile loss and independently evaluated weighted loss disagree')
    angle_gradient=float(gW[0]@np.array([-np.sin(theta),np.cos(theta)]))
    z=states@(W.T@W)+bias
    branch={'active_masks':(z>0).T.tolist(),
            'minimum_absolute_preactivation':float(np.min(abs(z))),
            'exact_zero_preactivations':np.argwhere(z==0).tolist(),
            'numerically_near_kinks_1e_12':np.argwhere(abs(z)<=1e-12).tolist(),
            'tied_finite_minimizers':[d['tied_finite_minimizers'] for d in details],
            'all_off_plateau_tied':[d['all_off_plateau_tied'] for d in details],
            'bias_gradient_norm':float(np.linalg.norm(gb)),
            'chosen_bias':bias.tolist()}
    return W,bias,loss,angle_gradient,branch,details


def main():
    base=Path(__file__).resolve().parent
    output=base/'run_angle_diagnostic_v1'
    output.mkdir(exist_ok=False)
    snapshot=output/'source_snapshot';snapshot.mkdir()
    for name in ['run_angle_diagnostic.py','run_bridge.py','bridge_math.py','toy_math_snapshot.py']:
        shutil.copy2(base/name,snapshot/name)
    shutil.copy2(base.parent/'followup_protocol.md',snapshot/'followup_protocol.md')
    save_json(output/'settings.json',CONFIG)
    save_json(output/'environment.json',{'python':sys.version,'executable':sys.executable,
             'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()})
    summaries=[];risk_rows=[];geometry_rows=[]
    start=time.perf_counter()
    for p in CONFIG['p']:
        case=f'p_{p:.2f}';folder=output/case;folder.mkdir()
        states,probabilities=binary_population(2,p)
        theta=CONFIG['theta_start']; trace=[];branches=[];candidate_trials=[]
        before=time.perf_counter();stop_reason=None; accepted_updates=0
        for iteration in range(CONFIG['maximum_iterations']+1):
            W,bias,loss,g,branch,details=profile(theta,states,probabilities)
            row={'iteration':iteration,'theta':float(theta),'loss':loss,'angle_gradient':g,
                 'bias_0':float(bias[0]),'bias_1':float(bias[1]),
                 'W_0':float(W[0,0]),'W_1':float(W[0,1]),'energy':float(np.sum(W**2)),
                 'accepted_step':None,'halvings':None,'next_theta':None,'next_loss':None,
                 'bias_gradient_norm':branch['bias_gradient_norm'],
                 'minimum_absolute_preactivation':branch['minimum_absolute_preactivation'],
                 'finite_bias_tie_count_0':len(branch['tied_finite_minimizers'][0]),
                 'finite_bias_tie_count_1':len(branch['tied_finite_minimizers'][1]),
                 'near_kink_count':len(branch['numerically_near_kinks_1e_12'])}
            branches.append({'iteration':iteration,**branch,'scalar_bias_details':details})
            if abs(g)<=CONFIG['gradient_tolerance']:
                stop_reason='angle_gradient_tolerance';trace.append(row);break
            if iteration==CONFIG['maximum_iterations']:
                stop_reason='maximum_iterations';trace.append(row);break
            accepted=False
            for halvings in range(CONFIG['maximum_halvings']+1):
                step=CONFIG['initial_trial_step']*2.**(-halvings)
                next_theta=theta-step*g
                _,_,next_loss,_,next_branch,_=profile(next_theta,states,probabilities)
                rhs=loss-CONFIG['armijo_coefficient']*step*g*g
                passes=next_loss<=rhs
                candidate_trials.append({'iteration':iteration,'halvings':halvings,
                                         'step':step,'theta':float(next_theta),'loss':next_loss,
                                         'armijo_rhs':rhs,'accepted':bool(passes),
                                         'near_kink_count':len(next_branch['numerically_near_kinks_1e_12'])})
                if passes:
                    accepted=True
                    row.update({'accepted_step':step,'halvings':halvings,
                                'next_theta':float(next_theta),'next_loss':next_loss})
                    theta=next_theta;accepted_updates+=1;break
            trace.append(row)
            if not accepted:
                stop_reason='armijo_failure';break
        save_csv(folder/'trace.csv',trace)
        save_csv(folder/'armijo_trials.csv',candidate_trials)
        save_json(folder/'bias_branches.json',branches)
        np.savez_compressed(folder/'final.npz',theta=theta,W=W,bias=bias,
                            states=states,probabilities=probabilities)
        v1_landscape=np.load(base/'run_v1'/f'p_{p:.2f}_importance_0.50'/'landscape.npz')
        grid_min=float(v1_landscape['losses'].min())
        ambiguity_iterations=[b['iteration'] for b in branches
                              if any(len(x)>1 for x in b['tied_finite_minimizers'])
                              or any(b['all_off_plateau_tied'])
                              or b['numerically_near_kinks_1e_12']]
        branch_changes=[branches[i]['iteration'] for i in range(1,len(branches))
                        if branches[i]['active_masks']!=branches[i-1]['active_masks']]
        # Local finite-difference agreement is diagnostic, not an extra optimizer.
        fd_checks=[]
        for theta_check,label in [(CONFIG['theta_start'],'start'),(theta,'final')]:
            _,_,_,analytic,_,_=profile(theta_check,states,probabilities)
            h=1e-6
            lp=profile(theta_check+h,states,probabilities)[2]
            lm=profile(theta_check-h,states,probabilities)[2]
            fd_checks.append({'point':label,'theta':float(theta_check),
                              'analytic':analytic,'central_difference':(lp-lm)/(2*h),
                              'absolute_discrepancy':abs(analytic-(lp-lm)/(2*h))})
        summary={'p':p,'importance':CONFIG['importance'],'stop_reason':stop_reason,
                 'accepted_updates':accepted_updates,'recorded_iterates':len(trace),
                 'initial_loss':trace[0]['loss'],'initial_gradient':trace[0]['angle_gradient'],
                 'final_theta':float(theta),'final_loss':loss,'final_gradient':g,
                 'seconds':time.perf_counter()-before,'previous_grid_minimum_loss':grid_min,
                 'final_minus_previous_grid_minimum':loss-grid_min,
                 'ambiguous_or_near_kink_iterations':ambiguity_iterations,
                 'active_mask_change_iterations':branch_changes,'finite_difference_checks':fd_checks}
        summaries.append(summary);save_json(folder/'summary.json',summary)
        models=[('angle_profile_final',W,bias)]
        for label,mono_W in [('mono_retain_0',np.array([[1.,0.]])),
                            ('mono_retain_1',np.array([[0.,1.]]))]:
            mono_bias,_,_=optimal_biases(mono_W,states,probabilities,CONFIG['importance'])
            models.append((label,mono_W,mono_bias))
        for label,model_W,model_bias in models:
            G,d,V,B,M,midpoint=geometry(model_W,p)
            actual=.5-model_bias
            mse0=exact_decoder_mse(model_W,model_bias,states,probabilities,0.)
            geometry_rows.append({'p':p,'label':label,'W_0':float(model_W[0,0]),
                                  'W_1':float(model_W[0,1]),'bias_0':float(model_bias[0]),
                                  'bias_1':float(model_bias[1]),'G_00':float(d[0]),
                                  'G_11':float(d[1]),'G_01':float(G[0,1]),
                                  'M_0':float(M[0]),'M_1':float(M[1]),
                                  'clean_weighted_sum_mse':float(np.asarray(CONFIG['importance'])@mse0)})
            for sigma in CONFIG['sigmas']:
                per_mse=exact_decoder_mse(model_W,model_bias,states,probabilities,sigma)
                for detector,threshold in [('actual_decoder',actual),('centered_midpoint',midpoint)]:
                    risk,fp,fn,_=exact_detection(model_W,states,probabilities,threshold,sigma)
                    row={'p':p,'label':label,'sigma':sigma,'detector':detector,
                         'weighted_sum_error':float(np.asarray(CONFIG['importance'])@risk),
                         'unweighted_sum_error':float(risk.sum()),
                         'weighted_sum_mse':float(np.asarray(CONFIG['importance'])@per_mse),
                         'unweighted_sum_mse':float(per_mse.sum())}
                    for i in range(2):
                        row.update({f'error_{i}':float(risk[i]),f'fp_{i}':float(fp[i]),
                                    f'fn_{i}':float(fn[i]),f'decoder_mse_{i}':float(per_mse[i])})
                    risk_rows.append(row)
        print(json.dumps(summary),flush=True)
    save_json(output/'summaries.json',summaries)
    save_csv(output/'risks.csv',risk_rows)
    save_csv(output/'geometry.csv',geometry_rows)
    save_json(output/'timings.json',{'total_seconds':time.perf_counter()-start})
    manifest={str(path.relative_to(output)):hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(output.rglob('*')) if path.is_file()}
    save_json(output/'sha256_manifest.json',manifest)
    print('Stopped after two prescribed deterministic diagnostics:',output,flush=True)


if __name__=='__main__':
    main()
