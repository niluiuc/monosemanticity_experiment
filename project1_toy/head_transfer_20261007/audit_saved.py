"""Independent saved fixed-head audit; no inference, fitting or new cases.
Run only after the supervisor confirms completion.
"""
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
        summary['extraction_manifest_files'] = manifest_check(args.extraction, 'sha256_manifest.json')
        provenance = json.loads((args.extraction / 'provenance.json').read_text())
        assert provenance['status']=='complete' and provenance['images_completed']==4608
        assert provenance['checkpoint_url']=='https://download.pytorch.org/models/resnet18-f37072fd.pth'
        assert provenance['checkpoint_sha256']=='f37072fd47e89c5e827621c5baffa7500819f7896bbacec160b1a16c560e07ec'
        assert provenance['ids']==[281,207] and provenance['names']==['tabby','golden retriever']
        assert provenance['seed']==20261007 and provenance['split_sizes']==[256,256,4096]
        assert provenance['batch_size']==32 and provenance['threads']==4 and provenance['max_seconds']==1200
        for fragment in ['crop_size=[224]', 'resize_size=[256]', 'mean=[0.485, 0.456, 0.406]', 'std=[0.229, 0.224, 0.225]']:
            assert fragment in provenance['transform'], fragment
        categories=json.loads((args.extraction/'categories.json').read_text())
        assert len(categories)==1000 and [categories[281],categories[207]]==['tabby','golden retriever']
        cache=Path('C:/Users/indra/.cache/monosemanticity_vision_20261006')
        assert digest(cache/'weights/hub/checkpoints/resnet18-f37072fd.pth')==provenance['checkpoint_sha256']
        assert digest(cache/'data/cifar-10-python.tar.gz')==provenance['dataset_archive_sha256']
        # Read cached CIFAR label records, never run model inference.
        import pickle
        labels_all=[]
        for number in range(1,6):
            with (cache/'data/cifar-10-batches-py'/f'data_batch_{number}').open('rb') as file:
                labels_all.extend(pickle.load(file,encoding='bytes')[b'labels'])
        labels_all=np.asarray(labels_all)
        fixed=np.random.default_rng(20261007).permutation(50000)[:4608]
        raw=np.load(args.extraction/'raw_logits.npy',allow_pickle=False)
        labels=np.load(args.extraction/'labels.npy',allow_pickle=False)
        assert raw.shape==(4608,1000) and raw.dtype==np.float32 and np.isfinite(raw).all()
        assert np.array_equal(labels,labels_all[fixed])
        assert np.array_equal(np.load(args.extraction/'image_indices.npy'),fixed)
        targets=np.maximum(raw[:,[281,207]],0).astype(np.float64)
        archive=np.load(args.extraction/'targets.npz',allow_pickle=False)
        arrays={}
        for key,begin,end in [('train',0,256),('calibration',256,512),('test',512,4608)]:
            assert np.array_equal(archive[key],targets[begin:end])
            assert np.array_equal(archive[key+'_indices'],fixed[begin:end])
            assert np.array_equal(archive[key+'_labels'],labels[begin:end])
            arrays[key]=archive[key]
        # Independent positive-negative pair counting, not rankdata.
        def pair_auc(y,scores):
            positive=scores[y];negative=scores[~y]
            if len(positive)==0 or len(negative)==0:return None
            comparisons=positive[:,None]-negative[None,:]
            return float((np.sum(comparisons>0)+.5*np.sum(comparisons==0))/comparisons.size)
        auc_train=[pair_auc(archive['train_labels']==c,arrays['train'][:,i]) for i,c in enumerate([3,5])]
        summary.update(ids=[281,207],names=['tabby','golden retriever'],train_auc=auc_train,
                       fixed_indices_and_raw_head_targets_verified=True,genuine_source_file_hashes_verified=True,
                       feature_inference_limit='Archived source/provenance and complete head outputs checked; no forward inference duplicated.')
        if args.evaluation:
            summary['evaluation_manifest_files']=manifest_check(args.evaluation,'sha256_manifest.json')
            input_hashes=json.loads((args.evaluation/'input_hashes.json').read_text())
            for source,expected in input_hashes.items():assert digest(Path(source))==expected
            gate=json.loads((args.evaluation/'association_gate.json').read_text())
            assert gate['threshold']==.65 and gate['target_names']==['tabby','golden retriever']
            assert gate['cifar_associations']==['cat','dog']
            assert all(a==b for a,b in zip(auc_train,gate['train_auc']))
            passes=all(a is not None and a>.65 for a in auc_train)
            assert gate['passed']==passes
            decision=json.loads((args.evaluation/'stopping_decision.json').read_text())
            summary['stopping_decision']=decision
            if not passes:
                assert decision['stop']=='class_association_gate_failed'
                assert not (args.evaluation/'clean_selection.json').exists() and not (args.evaluation/'results.json').exists()
                summary.update(passed=True,audited_scope='Extraction and failed association gate only; no risk evaluation.')
                return
            train=arrays['train'];rms=np.sqrt(np.mean(train*train,axis=0))
            if not np.all((rms>0)&(np.var(train,axis=0)>0)):
                assert decision['stop']=='nonconstant_target_gate_failed' and not (args.evaluation/'results.json').exists()
                summary.update(passed=True,audited_scope='Extraction and association/nonconstant gates only.')
                return
            x={key:value/rms for key,value in arrays.items()}
            zeros=np.mean(x['train']==0,axis=0);reference=float(np.sqrt(np.var(x['train'],axis=0).mean()))
            settings=json.loads((args.evaluation/'settings.json').read_text())
            assert settings['ids']==[281,207] and settings['names']==['tabby','golden retriever']
            assert np.array_equal(np.asarray(settings['rms']),rms) and np.array_equal(settings['zero_fractions'],zeros)
            assert settings['sigma_reference']==reference
            assert settings['coactivation']==float(np.mean(np.all(x['train']>0,axis=1)))
            assert settings['importance']==[1.,2./3.] and settings['multipliers']==[0,.05,.1,.2,.4]
            assert settings['seed']==20261007 and settings['test_images']==4096
            assert settings['primary']=='delta_calibrated_at_multiplier_.4' and settings['bootstrap_replicates']==2000
            assert settings['calibration_gap']==1e-7 and settings['slack']==1e-12
            assert settings['expansions']==20000 and settings['seconds']==300
            summary.update(train_rms=rms.tolist(),train_zero_fractions=zeros.tolist(),noise_reference=reference)
            clean = json.loads((args.evaluation/'clean_selection.json').read_text())
            normalized = np.load(args.evaluation/'normalized_targets.npz')
            for key in x:
                assert np.array_equal(normalized[key],x[key])
            for name in ['sharing','mono']:
                w=np.asarray(clean[name]['weights']); beta=np.asarray(clean[name]['biases'])
                assert abs(np.sum(w*w)-1)<1e-14
                assert abs(np.mean(losses(x['train'],w,beta,0))-clean[name]['loss'])<1e-12
            assert len(clean['histories'])==2
            for history,size in zip(clean['histories'],[256,512]):
                assert history['size']==size and len(history['grid'])==size
                for position,item in enumerate(history['grid']):
                    angle=position*np.pi/size
                    assert item['angle']==angle
                    w=np.array([np.cos(angle),np.sin(angle)])
                    assert abs(np.mean(losses(x['train'],w,np.asarray(item['biases']),0))-item['loss'])<1e-12
                for item in history['refinement_trace']:
                    assert 0<=item['angle']<np.pi and np.isfinite(item['loss'])
            assert len(clean['mono_orientations'])==2
            for i,item in enumerate(clean['mono_orientations']):
                assert np.array_equal(item['weights'],np.eye(2)[i])
                assert abs(np.mean(losses(x['train'],np.eye(2)[i],np.asarray(item['biases']),0))-item['loss'])<1e-12
            assert clean['mono_orientation']==int(np.argmin([item['loss'] for item in clean['mono_orientations']]))
            gain=clean['mono']['loss']-clean['sharing']['loss']
            agreement=abs(clean['histories'][0]['result']['loss']-clean['sharing']['loss'])
            expected_gates=dict(resolution_agreement=agreement<=1e-6,
                both_refinements_successful=all(item['refinement_success'] for item in clean['histories']),
                resolved_clean_advantage=gain>1e-6,
                mixed_geometry=bool(np.all(np.square(clean['sharing']['weights'])>1e-8)))
            assert clean['gates']==expected_gates and clean['eligible']==all(expected_gates.values())
            assert abs(clean['clean_gain']-gain)<1e-14 and abs(clean['resolution_difference']-agreement)<1e-14
            decision=json.loads((args.evaluation/'stopping_decision.json').read_text())
            summary['stopping_decision']=decision
            if not clean['eligible'] or not np.any(zeros>0):
                assert decision['stop']=='clean_mechanism_gate_failed' and not (args.evaluation/'results.json').exists()
                summary.update(passed=True,audited_scope='Extraction and clean mechanism gate; no risk evaluation.')
                return
            descriptive=json.loads((args.evaluation/'association_test_descriptive.json').read_text())
            assert descriptive['used_to_fit_or_select'] is False
            assert descriptive['auc']==[pair_auc(archive['test_labels']==c,arrays['test'][:,i]) for i,c in enumerate([3,5])]
            results_path=args.evaluation/'results.json'
            if results_path.is_file():
                results=json.loads(results_path.read_text())['cases']
                assert len(results)==5 and decision['stop']=='five_fixed_levels_completed'
                assert decision['all_calibration_resolved']==all(p['resolved'] for row in results for p in row['profiles'].values())
                stored_losses=np.load(args.evaluation/'per_image_losses.npz')
                stored_boots=np.load(args.evaluation/'bootstrap_statistics.npz')
                bootstrap=np.load(args.evaluation/'bootstrap_indices.npy')
                assert bootstrap.dtype==np.uint16 and bootstrap.shape==(2000,4096)
                assert np.array_equal(bootstrap,np.random.default_rng(20261007).integers(0,4096,size=(2000,4096)).astype(np.uint16))
                total_nodes=0;max_discrepancy=0.
                baseline={}
                for name in ['sharing','mono']:
                    profiles=json.loads((args.evaluation/f'{name}_zero_calibration.json').read_text())
                    baseline[name]=np.array([item['beta'] for item in profiles])
                    w=np.asarray(clean[name]['weights']);code=x['calibration']@w
                    for i,profile in enumerate(profiles):
                        expected=scalar(profile['beta'],w[i]*code,x['calibration'][:,i],0)[0]
                        assert abs(expected-profile['loss'])<1e-12
                        for candidate in profile['candidates']:
                            value=scalar(candidate['beta'],w[i]*code,x['calibration'][:,i],0)[0]
                            assert abs(value-candidate['loss'])<1e-12
                        assert profile['loss']==min(item['loss'] for item in profile['candidates'])
                for j, row in enumerate(results):
                    assert row['multiplier'] == [0,.05,.1,.2,.4][j]
                    assert row['sigma'] == row['multiplier']*reference
                    for name in ['sharing','mono']:
                        w=np.asarray(clean[name]['weights'])
                        assert np.array_equal(row['profiles'][name]['frozen_bias'],baseline[name])
                        for policy, key in [('frozen','frozen_bias'),('calibrated','calibrated_bias')]:
                            per=losses(x['test'],w,np.asarray(row['profiles'][name][key]),row['sigma'])
                            error=float(np.max(abs(per-stored_losses[f'noise_{j}_{name}_{policy}'])))
                            max_discrepancy=max(max_discrepancy,error)
                            assert error<1e-11
                            assert abs(per.mean()-row['risks'][name+'_'+policy])<1e-12
                        gaps=[]
                        for i, importance in enumerate([1.,2./3.]):
                            ledger=json.loads((args.evaluation/f'noise_{j}/{name}_feature_{i}.json').read_text())
                            assert ledger['beta']==row['profiles'][name]['calibrated_bias'][i]
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
                        assert row['profiles'][name]['resolved']==all(json.loads((args.evaluation/f'noise_{j}/{name}_feature_{i}.json').read_text())['resolved'] for i in range(2))
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
