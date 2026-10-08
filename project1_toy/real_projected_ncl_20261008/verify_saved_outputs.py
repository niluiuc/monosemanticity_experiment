"""Independent NumPy checks of saved outputs, without loading any checkpoint."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np

def read(path): return json.loads(path.read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--root',type=Path,required=True)
    root=parser.parse_args().root; clean=root/'clean_run_v1'
    report={}; results=read(clean/'results.json'); split=np.load(clean/'split_indices.npz')
    fit=split['fit']; val=split['validation']
    assert len(fit)==45000 and len(val)==5000
    assert len(np.unique(np.r_[fit,val]))==50000
    report['fit_validation_disjoint']=True
    predictions={}
    for method in ('CL','NCL'):
        data=np.load(clean/method/'validation_predictions.npz')
        errors=data['logits'].argmax(1)!=data['labels']
        assert np.array_equal(errors,data['errors'])
        value=float(errors.mean())
        assert abs(value-results['models'][method]['validation_error'])<1e-7
        report[method+'_validation_error']=value; predictions[method]=errors
    delta=float((predictions['NCL'].astype(float)-predictions['CL'].astype(float)).mean())
    assert abs(delta-results['delta_error'])<1e-7
    bootstrap=np.load(clean/'bootstrap_draws.npz')
    error_ci=np.quantile(bootstrap['error_difference'],[.025,.975])
    sc_ci=np.quantile(bootstrap['consistency_difference'],[.025,.975])
    assert np.allclose(error_ci,results['error_difference_ci95'],rtol=0,atol=1e-12)
    assert np.allclose(sc_ci,results['consistency_difference_ci95'],rtol=0,atol=1e-12)
    assert bool(error_ci[0]>0 and sc_ci[0]>0)==results['clean_gates_passed']
    report.update(delta_error=delta,clean_gates_passed=results['clean_gates_passed'],
                  scope='Error decisions, split integrity and interval/gate recomputation from saved arrays. Does not independently establish bootstrap assumptions or representation causality.')
    pred=root/'prediction_run_v1/prediction.json'
    if pred.exists():
        frozen=read(pred.parent/'frozen_prediction_hash.json'); assert digest(pred)==frozen['sha256']
        prediction=read(pred)
        subset_errors=[]
        for method in ('CL','NCL'):
            data=np.load(pred.parent/(method+'_validation.npz'))
            subset_errors.append(data['affine_errors'].mean(1)-data['clean_errors'][:,None])
        curve=delta+(subset_errors[1]-subset_errors[0]).mean(0)
        assert np.allclose(curve,prediction['delta_error_prediction'],rtol=0,atol=1e-7)
        report['prediction_curve_verified']=True
    test=root/'test_run_v1/results.json'
    if test.exists():
        result=read(test); model_errors=[]
        for method in ('CL','NCL'):
            data=np.load(test.parent/(method+'_test_scores.npz'))
            model_errors.append(data['errors'].mean(1))
            assert np.allclose(model_errors[-1].mean(0),result[method+'_error'],rtol=0,atol=1e-12)
        curve=(model_errors[1]-model_errors[0]).mean(0)
        assert np.allclose(curve,result['delta_NCL_minus_CL'],rtol=0,atol=1e-12)
        draws=np.load(test.parent/'bootstrap_curves.npz')['curves']; k=len(curve)
        bands=np.quantile(draws,[.025/k,1-.025/k],axis=0)
        assert np.allclose(bands[0],result['simultaneous_lower'],rtol=0,atol=1e-12)
        assert np.allclose(bands[1],result['simultaneous_upper'],rtol=0,atol=1e-12)
        assert bool(bands[0,0]>0 and (bands[1,1:]<0).any())==result['resolved_reversal']
        report['test_curve_and_reversal_decision_verified']=True
    target=root/'independent_output_verification.json'
    target.write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))

if __name__=='__main__': main()
