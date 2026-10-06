"""One prescribed all-five tangent-gradient repair; no noise calibration."""
import argparse,csv,hashlib,json,platform,shutil,sys,time
from pathlib import Path
import numpy as np
import scipy

HERE=Path(__file__).resolve().parent
INPUT=HERE/'clean_run_v1'
SETTINGS=dict(seeds=list(range(5)),maximum_accepted_updates=2000,initial_alpha=.01,armijo_coefficient=1e-4,
              maximum_halvings=20,selected_joint_gradient_stop=1e-5,total_seconds_budget=120,
              n=8,m=4,p=.2,encoder_energy=4.,importance=[2**(-i/4) for i in range(8)],
              checkpoint_interval=100,convergence_window=100,convergence_absolute_tolerance=1e-5,
              input_policy='All five immutable original final iterates; no Adam moments or checkpoint selection',
              scope='Single optimizer-blocker diagnostic, not globally optimal training')

def dump(path,data):path.write_text(json.dumps(data,indent=2,allow_nan=True))
def csvwrite(path,fields,rows):
    with path.open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(fields);writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'repair_run_v1');args=parser.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=False);snap=out/'source_snapshot';snap.mkdir()
    for path in [Path(__file__),HERE/'repair_protocol.md',HERE/'repair_derivation.tex',HERE/'professor_decision.md',
                 INPUT/'source_snapshot/bridge_math.py',INPUT/'source_snapshot/toy_math_snapshot.py']:
        shutil.copy2(path,snap/path.name)
    shutil.copy2(INPUT/'settings.json',snap/'original_training_settings.json')
    shutil.copy2(INPUT/'sha256_manifest.json',snap/'original_training_manifest.json')
    inputs=out/'input_snapshot';inputs.mkdir()
    for seed in SETTINGS['seeds']:
        dst=inputs/f'seed_{seed}';dst.mkdir()
        for name in ['final.npz','results.json']:shutil.copy2(INPUT/f'seed_{seed}'/name,dst/name)
    shutil.copy2(INPUT/'population.npz',inputs/'population.npz');shutil.copy2(INPUT/'mono.json',inputs/'mono.json')
    dump(out/'settings.json',SETTINGS);dump(out/'environment.json',dict(python=sys.version,executable=sys.executable,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__))
    sys.path.insert(0,str(snap));from bridge_math import weighted_loss_gradient,optimal_biases
    from toy_math_snapshot import exact_decoder_mse
    population=np.load(inputs/'population.npz');X=population['states'];P=population['probabilities'];I=population['importance'];mono=json.loads((inputs/'mono.json').read_text())['clean_loss']
    started=time.perf_counter();deadline=started+120;results=[]
    for seed in SETTINGS['seeds']:
        folder=out/f'seed_{seed}';folder.mkdir();original=np.load(inputs/f'seed_{seed}/final.npz');W=original['W'].copy();bias=original['bias'].copy()
        history=[];trials=[];ck_steps=[0];ck_W=[W.copy()];ck_bias=[bias.copy()];accepted=0;reason=None
        def current():
            loss,gW,gb=weighted_loss_gradient(W,bias,X,P,I);T=gW-np.sum(gW*W)/4*W
            nT=np.linalg.norm(T);nb=np.linalg.norm(gb);distance=np.min(abs(X@(W.T@W)+bias))
            return loss,T,gb,float(nT),float(nb),float(distance)
        while True:
            loss,T,gb,nT,nb,distance=current();joint=float(np.hypot(nT,nb))
            history.append([accepted,loss,np.sum(W*W),nT,nb,joint,distance,time.perf_counter()-started])
            if not np.isfinite(loss) or not np.all(np.isfinite(T)) or not np.all(np.isfinite(gb)):reason='nonfinite';break
            if time.perf_counter()>=deadline:reason='total_wallclock_budget';break
            if joint<=1e-5:reason='selected_gradient_threshold';break
            if accepted>=2000:reason='maximum_accepted_updates';break
            got=False
            for halving in range(21):
                if time.perf_counter()>=deadline:reason='total_wallclock_budget';break
                alpha=.01/2**halving;V=W-alpha*T;norm=np.linalg.norm(V);valid=bool(np.isfinite(norm) and norm>0)
                if valid:
                    new_W=2*V/norm;new_bias=bias-alpha*gb;new_loss=weighted_loss_gradient(new_W,new_bias,X,P,I)[0]
                else:new_loss=float('nan')
                target=loss-1e-4*alpha*joint**2;passes=bool(valid and np.isfinite(new_loss) and new_loss<=target)
                trials.append([accepted,halving,alpha,loss,new_loss,target,passes,time.perf_counter()-started])
                if passes:
                    W,bias=new_W,new_bias;accepted+=1;got=True
                    if accepted%100==0:ck_steps.append(accepted);ck_W.append(W.copy());ck_bias.append(bias.copy())
                    break
            if not got:
                reason=reason or 'backtracking_failed';break
        if ck_steps[-1]!=accepted:ck_steps.append(accepted);ck_W.append(W.copy());ck_bias.append(bias.copy())
        history=np.asarray(history);loss,T,gb,nT,nb,distance=current()
        profile_bias,profile_loss,profile_ledger=optimal_biases(W,X,P,I)
        change=abs(history[-100:,1].mean()-history[-200:-100,1].mean()) if len(history)>=200 else None
        individual=exact_decoder_mse(W,bias,X,P,0.);assert abs(I@individual-loss)<1e-11
        np.savez_compressed(folder/'final.npz',W=W,bias=bias,history=history,clean_profile_bias=profile_bias)
        np.savez_compressed(folder/'checkpoints.npz',steps=np.array(ck_steps),W=np.stack(ck_W),bias=np.stack(ck_bias))
        csvwrite(folder/'history.csv',['accepted_step','loss','encoder_energy','tangent_gradient_norm','bias_gradient_norm','joint_gradient_norm','minimum_absolute_preactivation','total_elapsed_seconds'],history)
        csvwrite(folder/'backtracking_trials.csv',['accepted_step_before_trial','halving','alpha','current_loss','proposal_loss','armijo_target','accepted','total_elapsed_seconds'],trials)
        dump(folder/'clean_bias_profiles.json',profile_ledger)
        old=json.loads((inputs/f'seed_{seed}/results.json').read_text())
        norms=np.linalg.norm(W,axis=0);stored=norms>0;mono_stored=np.arange(8)<4
        support_penalty=float(.2**2*np.sum(I*(stored.astype(int)-mono_stored.astype(int))))
        Q=float(4/(3*np.sqrt(2*np.pi))*np.sum(I[stored]*.2/norms[stored]))
        record=dict(seed=seed,accepted_updates=accepted,stop_reason=reason,backtracking_trials=len(trials),
                    original_clean_loss=old['raw_clean_loss'],final_clean_loss=float(loss),clean_bias_profiled_loss=profile_loss,
                    mono_clean_loss=mono,delta_vs_mono=float(loss-mono),tangent_gradient_norm=nT,bias_gradient_norm=nb,
                    joint_gradient_norm=float(np.hypot(nT,nb)),minimum_absolute_preactivation=distance,
                    window_mean_loss_change=change,loss_stability_pass=bool(change is not None and change<=1e-5),
                    selected_gradient_threshold_pass=bool(np.hypot(nT,nb)<=1e-5),
                    near_kink_warning=bool(distance<=1e-8),encoder_energy=float(np.sum(W*W)),
                    column_norms=norms.tolist(),support_penalty_P=support_penalty,bound_constant_Q=Q,
                    bound_noise_Q_over_P=Q/support_penalty if support_penalty>0 else None,
                    interpretation='Local/nonsmooth optimization diagnostic only; no global training claim')
        dump(folder/'results.json',record);results.append(record);dump(out/'results.json',dict(cases=results,mono_clean_loss=mono,total_seconds=time.perf_counter()-started))
        print(json.dumps(record),flush=True)
    dump(out/'timing.json',dict(seconds=time.perf_counter()-started))
    dump(out/'sha256_manifest.json',{str(path.relative_to(out)):hashlib.sha256(path.read_bytes()).hexdigest() for path in out.rglob('*') if path.is_file()})

if __name__=='__main__':main()
