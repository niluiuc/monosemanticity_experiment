"""Independent audit of saved fixed vision inputs/results; no new cases or inference."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import numpy as np
from scipy.special import ndtr


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def manifest_check(folder, name):
    values = json.loads((folder / name).read_text())
    for relative, expected in values.items():
        path = (folder / relative).resolve()
        assert path.is_relative_to(folder.resolve()) and digest(path) == expected, relative
    return len(values)


def scalar(beta, offset, y, sd):
    mu = offset + beta
    if sd == 0:
        positive = np.maximum(mu, 0)
        return float(np.mean((positive-y)**2)), 0.
    z = mu/sd
    Phi = ndtr(z)
    phi = np.exp(-z*z/2)/np.sqrt(2*np.pi)
    first = np.maximum(mu*Phi+sd*phi, 0)
    second = np.maximum((mu*mu+sd*sd)*Phi+mu*sd*phi, 0)
    return float(np.mean(second-2*y*first+y*y)), float(2*np.mean((mu-y)*Phi+sd*phi))


def losses(x, w, beta, sigma):
    code = x@w
    result = np.zeros(len(x))
    for i, importance in enumerate([1., 2./3.]):
        mu = w[i]*code+beta[i]
        sd = sigma*abs(w[i])
        if sd == 0:
            result += importance*(np.maximum(mu, 0)-x[:, i])**2
        else:
            z = mu/sd
            Phi = ndtr(z)
            phi = np.exp(-z*z/2)/np.sqrt(2*np.pi)
            first = np.maximum(mu*Phi+sd*phi, 0)
            second = np.maximum((mu*mu+sd*sd)*Phi+mu*sd*phi, 0)
            result += importance*(second-2*x[:, i]*first+x[:, i]**2)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extraction', type=Path, required=True)
    parser.add_argument('--evaluation', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(Path(__file__), args.output / Path(__file__).name)
    summary = {'scope': 'saved-artifact audit; no new image extraction, training or noise cases'}
    try:
        summary['extraction_manifest_files'] = manifest_check(args.extraction, 'sha256.json')
        provenance = json.loads((args.extraction / 'provenance.json').read_text())
        assert digest(args.extraction/'source_snapshot/vision_extract.py') == provenance['source_sha256']
        assert provenance['checkpoint'] == 'IMAGENET1K_V1'
        assert provenance['checkpoint_url'] == 'https://download.pytorch.org/models/resnet18-f37072fd.pth'
        assert provenance['dataset_url'] == 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
        assert provenance['feature_location'] == 'post-ReLU layer4 output; spatial cell [height//2,width//2]'
        cache = Path(provenance['cache'])
        assert digest(cache/'weights/hub/checkpoints/resnet18-f37072fd.pth') == provenance['checkpoint_sha256']
        assert digest(cache/'data/cifar-10-python.tar.gz') == provenance['dataset_archive_sha256']
        archive = np.load(args.extraction/'vision_activations.npz', allow_pickle=False)
        raw = np.load(args.extraction/'features_raw.npy', allow_pickle=False)
        fixed = np.random.default_rng(20261006).permutation(50000)[:1024]
        assert raw.shape == (1024, 512) and np.isfinite(raw).all() and (raw >= 0).all()
        assert raw.dtype == np.float32
        for key, begin, end in [('train',0,256), ('calibration',256,512), ('test',512,1024)]:
            assert np.array_equal(archive[key], raw[begin:end])
            assert np.array_equal(archive[key+'_indices'], fixed[begin:end])
        assert np.array_equal(np.load(args.extraction/'image_indices.npy'), fixed)
        embedded = json.loads(str(archive['metadata_json']))
        for key in ['dataset_archive_sha256', 'checkpoint_sha256', 'source_sha256', 'transform_repr', 'channels']:
            assert embedded[key] == provenance[key]
        train = raw[:256].astype(np.float64)
        channels = np.flatnonzero((train.mean(0)>0)&(train.var(0)>0))[:2]
        rms = np.sqrt((train[:,channels]**2).mean(0))
        x = {key: archive[key].astype(np.float64)[:,channels]/rms
             for key in ['train','calibration','test']}
        selected = np.load(args.extraction/'selected_features.npz', allow_pickle=False)
        assert np.array_equal(channels, selected['channels'])
        assert np.array_equal(rms, selected['train_rms'])
        for key in x:
            assert np.array_equal(x[key], selected[key])
        zeros = (x['train']==0).mean(0)
        reference = float(np.sqrt(x['train'].var(0).mean()))
        assert np.array_equal(zeros, provenance['train_zero_fractions'])
        assert reference == provenance['normalized_pair_noise_reference_sqrt_mean_variance']
        summary.update(channels=channels.tolist(), train_rms=rms.tolist(),
                       train_zero_fractions=zeros.tolist(), noise_reference=reference,
                       fixed_indices_and_raw_normalized_arrays_verified=True,
                       genuine_source_file_hashes_verified=True,
                       feature_inference_limit='Archived source/provenance checked; forward inference was not duplicated.')
        if args.evaluation:
            summary['evaluation_manifest_files'] = manifest_check(args.evaluation, 'sha256_manifest.json')
            settings = json.loads((args.evaluation/'settings.json').read_text())
            assert settings['channels'] == channels.tolist()
            assert np.array_equal(np.asarray(settings['rms']), rms)
            assert settings['sigma_reference'] == reference
            assert settings['importance'] == [1., 2./3.]
            clean = json.loads((args.evaluation/'clean_selection.json').read_text())
            normalized = np.load(args.evaluation/'normalized_targets.npz')
            for key in x:
                assert np.array_equal(normalized[key],x[key])
            for name in ['sharing','mono']:
                w=np.asarray(clean[name]['weights']); beta=np.asarray(clean[name]['biases'])
                assert abs(np.sum(w*w)-1)<1e-14
                assert abs(np.mean(losses(x['train'],w,beta,0))-clean[name]['loss'])<1e-12
            decision=json.loads((args.evaluation/'stopping_decision.json').read_text())
            summary['stopping_decision']=decision
            results_path=args.evaluation/'results.json'
            if results_path.is_file():
                results=json.loads(results_path.read_text())['cases']
                stored_losses=np.load(args.evaluation/'per_image_losses.npz')
                stored_boots=np.load(args.evaluation/'bootstrap_statistics.npz')
                bootstrap=np.load(args.evaluation/'bootstrap_indices.npy')
                assert np.array_equal(bootstrap,np.random.default_rng(20261006).integers(0,512,size=(2000,512)))
                total_nodes=0;max_discrepancy=0.
                for j, row in enumerate(results):
                    assert row['multiplier'] == [0,.05,.1,.2,.4][j]
                    assert row['sigma'] == row['multiplier']*reference
                    for name in ['sharing','mono']:
                        w=np.asarray(clean[name]['weights'])
                        for policy, key in [('frozen','frozen_bias'),('calibrated','calibrated_bias')]:
                            per=losses(x['test'],w,np.asarray(row['profiles'][name][key]),row['sigma'])
                            error=float(np.max(abs(per-stored_losses[f'noise_{j}_{name}_{policy}'])))
                            max_discrepancy=max(max_discrepancy,error)
                            assert error<1e-11
                            assert abs(per.mean()-row['risks'][name+'_'+policy])<1e-12
                        gaps=[]
                        for i, importance in enumerate([1.,2./3.]):
                            ledger=json.loads((args.evaluation/f'noise_{j}/{name}_feature_{i}.json').read_text())
                            offset=w[i]*(x['calibration']@w);y=x['calibration'][:,i]
                            sd=row['sigma']*abs(w[i]); value,_=scalar(ledger['beta'],offset,y,sd)
                            assert abs(value-ledger['upper'])<2e-12
                            assert abs(ledger['gap']-(ledger['upper']-ledger['lower']))<1e-14
                            assert ledger['resolved'] == (ledger['gap']<=ledger.get('tolerance',0))
                            nodes=ledger['nodes'];total_nodes+=len(nodes)
                            children={}
                            for node in nodes:
                                f,g=scalar(node['mid'],offset,y,sd)
                                left=offset+node['lo'];right=offset+node['hi']
                                dist=np.where((left<=0)&(right>=0),0,np.minimum(abs(left),abs(right)))
                                H=2*(1+float(np.mean(y*np.exp(-.5*(dist/sd)**2)/(sd*np.sqrt(2*np.pi)))))
                                radius=(node['hi']-node['lo'])/2
                                lower=max(0.,f-abs(g)*radius-H*radius*radius/2-1e-12)
                                assert abs(f-node['f'])<1e-11 and abs(g-node['g'])<1e-11
                                assert abs(H-node['H'])<1e-9*max(1,H)
                                assert abs(lower-node['lower'])<1e-9
                                if node['parent'] is not None:
                                    children.setdefault(node['parent'],[]).append(node)
                            for parent, siblings in children.items():
                                assert len(siblings)==2
                                siblings.sort(key=lambda n:n['lo']);original=nodes[parent]
                                assert siblings[0]['lo']==original['lo'] and siblings[1]['hi']==original['hi']
                                assert siblings[0]['hi']==siblings[1]['lo']
                            if sd:
                                heap_ids={item[1] for item in ledger['active_heap']}
                                for node in nodes:
                                    if node['id'] not in children and node['id'] not in heap_ids:
                                        assert node['lower']>=ledger['upper']-1e-12
                                left_m1=offset+ledger['left_endpoint']
                                z=left_m1/sd
                                first=np.maximum(left_m1*ndtr(z)+sd*np.exp(-z*z/2)/np.sqrt(2*np.pi),0)
                                exterior=float(np.mean(y*y)-2*np.mean(y*first)-1e-12)
                                right=scalar(ledger['right_endpoint'],offset,y,sd)[0]-1e-12
                                assert abs(exterior-ledger['exterior_lower_left'])<1e-11
                                assert abs(right-ledger['exterior_lower_right'])<1e-11
                                lower=min(ledger['upper'],exterior,right,
                                          min((item[0] for item in ledger['active_heap']),default=ledger['upper']))
                                assert abs(lower-ledger['lower'])<1e-11
                            gaps.append(importance*ledger['gap'])
                        assert abs(sum(gaps)-row['profiles'][name]['total_gap'])<1e-12
                    for key, record in row['comparisons'].items():
                        values=stored_losses[f'noise_{j}_{key}']
                        prefix=f'noise_{j}_'
                        if key=='delta_frozen':
                            expected=stored_losses[prefix+'sharing_frozen']-stored_losses[prefix+'mono_frozen']
                        elif key=='delta_calibrated':
                            expected=stored_losses[prefix+'sharing_calibrated']-stored_losses[prefix+'mono_calibrated']
                        elif key=='policy_contrast':
                            expected=(stored_losses[prefix+'sharing_calibrated']-stored_losses[prefix+'mono_calibrated']
                                      -stored_losses[prefix+'sharing_frozen']+stored_losses[prefix+'mono_frozen'])
                        else:
                            name=key.replace('_calibration_improvement','')
                            expected=stored_losses[prefix+name+'_frozen']-stored_losses[prefix+name+'_calibrated']
                        assert np.allclose(values,expected,rtol=0,atol=1e-12)
                        boots=values[bootstrap].mean(1)
                        assert np.allclose(boots,stored_boots[f'noise_{j}_{key}'],rtol=0,atol=1e-12)
                        assert abs(values.mean()-record['mean'])<1e-12
                        assert np.allclose(np.quantile(boots,[.025,.975]),record['interval95'],rtol=0,atol=1e-12)
                summary.update(evaluation_cases=len(results), calibration_nodes_reviewed=total_nodes,
                               max_per_image_risk_discrepancy=max_discrepancy)
        summary['passed']=True
    except Exception as error:
        summary.update(passed=False,error_type=type(error).__name__,error=str(error))
        raise
    finally:
        (args.output/'results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
        (args.output/'sha256.json').write_text(json.dumps({p.name:digest(p) for p in args.output.iterdir()
                           if p.is_file() and p.name!='sha256.json'},indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
