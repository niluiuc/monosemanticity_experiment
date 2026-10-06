"""Five prespecified n8/m4 clean population trainings; no noisy calibration."""
import argparse,csv,hashlib,json,platform,shutil,sys,time
from pathlib import Path
import numpy as np
import scipy

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'focused_bridge_2026-10-06/toy'
SETTINGS=dict(n=8,m=4,p=.2,encoder_energy=4.,importance=[2**(-i/4) for i in range(8)],seeds=list(range(5)),
              steps=5000,learning_rate=.01,adam_beta1=.9,adam_beta2=.999,adam_epsilon=1e-8,
              convergence_window=100,convergence_absolute_tolerance=1e-5,
              outcome='Sum importance-weighted exact population reconstruction MSE',
              support_policy='Actual nonzero column norms, no thresholding',
              selection='Every final iterate, no retry or checkpoint selection',
              scope='Local projected-Adam trained dictionaries, not global geometry optima')

def dump(path,data):path.write_text(json.dumps(data,indent=2,allow_nan=True))
def write_csv(path,fields,rows):
    with path.open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(fields);writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'clean_run_v1');args=parser.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=False);snap=out/'source_snapshot';snap.mkdir()
    for src in [Path(__file__),HERE/'protocol.md',SOURCE/'bridge_math.py',SOURCE/'toy_math_snapshot.py']:
        shutil.copy2(src,snap/src.name)
    dump(out/'settings.json',SETTINGS)
    dump(out/'environment.json',dict(python=sys.version,executable=sys.executable,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__))
    sys.path.insert(0,str(snap))
    from bridge_math import train_weighted,weighted_loss_gradient,optimal_biases
    from toy_math_snapshot import binary_population,mono_baseline,exact_decoder_mse
    states,probs=binary_population(8,.2);I=np.array(SETTINGS['importance']);np.savez_compressed(out/'population.npz',states=states,probabilities=probs,importance=I)
    rng=np.random.default_rng(2026100608);W=rng.normal(size=(4,8));W*=2/np.linalg.norm(W);bias=np.full(8,.137)
    z=states@(W.T@W)+bias;minimum_score_distance=float(np.min(abs(z)))
    assert minimum_score_distance>1e-5,'Prescribed gradient point too near kink; no retry'
    _,gW,gb=weighted_loss_gradient(W,bias,states,probs,I);packed=np.r_[W.ravel(),bias];analytic=np.r_[gW.ravel(),gb]
    numeric=[];h=1e-6
    for j in range(40):
        plus=packed.copy();minus=packed.copy();plus[j]+=h;minus[j]-=h
        numeric.append((weighted_loss_gradient(plus[:32].reshape(4,8),plus[32:],states,probs,I)[0]-weighted_loss_gradient(minus[:32].reshape(4,8),minus[32:],states,probs,I)[0])/(2*h))
    Wmono,bmono=mono_baseline(8,4,.2,4.);mono_individual=exact_decoder_mse(Wmono,bmono,states,probs,0.)
    mono_loss=float(I@mono_individual);expected_mono=float(.2*.8*I[4:].sum())
    gradient_error=float(np.max(abs(analytic-numeric)))
    checks=dict(population_states=len(states),probability_sum=float(probs.sum()),gradient_test_seed=2026100608,
                minimum_score_distance=minimum_score_distance,gradient_finite_difference_h=h,gradient_absolute_max_error=gradient_error,
                mono_loss=mono_loss,expected_mono_loss=expected_mono,mono_energy=float(np.sum(Wmono**2)),
                passed=bool(gradient_error<1e-6 and abs(mono_loss-expected_mono)<1e-12))
    dump(out/'prechecks.json',checks);assert checks['passed'],checks
    np.savez_compressed(out/'mono.npz',W=Wmono,bias=bmono,individual_clean_mse=mono_individual)
    dump(out/'mono.json',dict(clean_loss=mono_loss,individual_clean_mse=mono_individual.tolist(),stored_columns=list(range(4)),energy=float(np.sum(Wmono**2))))
    results=[];started=time.perf_counter();mono_support=np.linalg.norm(Wmono,axis=0)>0
    for seed in SETTINGS['seeds']:
        folder=out/f'seed_{seed}';folder.mkdir();before=time.perf_counter()
        W,bias,history,checkpoints,diagnostics=train_weighted(SETTINGS,.2,I,seed)
        np.savez_compressed(folder/'final.npz',W=W,bias=bias,history=history)
        np.savez_compressed(folder/'checkpoints.npz',**checkpoints)
        write_csv(folder/'history.csv',['step','loss','encoder_energy','tangent_gradient_norm','bias_gradient_norm'],history)
        bias_profile,profile_loss,profile_details=optimal_biases(W,states,probs,I)
        dump(folder/'clean_bias_profiles.json',profile_details)
        raw_individual=exact_decoder_mse(W,bias,states,probs,0.)
        profile_individual=exact_decoder_mse(W,bias_profile,states,probs,0.)
        norms=np.linalg.norm(W,axis=0);stored=norms>0
        P=float(.2**2*np.sum(I*(stored.astype(int)-mono_support.astype(int))))
        Q=float(4/(3*np.sqrt(2*np.pi))*np.sum(I[stored]*.2/norms[stored]))
        clean_raw=float(I@raw_individual);assert abs(clean_raw-diagnostics['final_loss'])<1e-11
        assert abs(float(I@profile_individual)-profile_loss)<1e-11
        record=dict(seed=seed,seconds=time.perf_counter()-before,diagnostics=diagnostics,
                    raw_clean_loss=clean_raw,clean_bias_profiled_loss=profile_loss,mono_clean_loss=mono_loss,
                    raw_delta_vs_mono=clean_raw-mono_loss,profiled_delta_vs_mono=profile_loss-mono_loss,
                    raw_individual_mse=raw_individual.tolist(),profiled_individual_mse=profile_individual.tolist(),
                    clean_profile_bias=bias_profile.tolist(),column_norms=norms.tolist(),stored_columns=np.flatnonzero(stored).tolist(),
                    support_penalty_P=P,bound_constant_Q=Q,bound_noise_Q_over_P=Q/P if P>0 else None,
                    bound_noise_2Q_over_P=2*Q/P if P>0 else None,encoder_energy=float(np.sum(W**2)),
                    history_rows=len(history),checkpoint_count=len(checkpoints['steps']),
                    interpretation='Fixed-step local training only; loss stability is not a stationarity/global-optimality certificate')
        dump(folder/'results.json',record);results.append(record);dump(out/'results.json',dict(stage='clean training only',cases=results,mono_clean_loss=mono_loss))
        print(json.dumps(dict(seed=seed,loss=clean_raw,profiled=profile_loss,mono=mono_loss,tangent_gradient=diagnostics['final_tangent_gradient_norm'],bias_gradient=diagnostics['final_bias_gradient_norm'],loss_stable=diagnostics['convergence_diagnostic_pass'],P=P,Q=Q,Q_over_P=Q/P if P>0 else None,failure=diagnostics['failure'])),flush=True)
    dump(out/'timing.json',dict(seconds=time.perf_counter()-started))
    dump(out/'sha256_manifest.json',{str(path.relative_to(out)):hashlib.sha256(path.read_bytes()).hexdigest() for path in out.rglob('*') if path.is_file()})

if __name__=='__main__':main()
