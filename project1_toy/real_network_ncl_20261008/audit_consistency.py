"""Independent cached-feature proxy calculation; no network or image scoring."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True); root=p.parse_args().root
clean=root/'clean_run_v1'; indices=np.load(clean/'split_indices.npz')['validation']; original=json.loads((clean/'results.json').read_text())
report={}
for method in ('CL','NCL'):
    file=clean/method/'clean_train_features.npz'; cached=np.load(file)
    features=cached['features'][indices].astype(np.float64); labels=cached['labels'][indices]
    active=np.abs(features/np.maximum(np.linalg.norm(features,axis=1,keepdims=True),1e-12))>1e-5
    counts=np.stack([active[labels==c].sum(0) for c in range(100)])
    totals=counts.sum(0); keep=totals>0
    value=float((counts[:,keep].max(0)/totals[keep]).mean())
    difference=value-original['models'][method]['semantic_consistency']
    assert abs(difference)<1e-7,(method,difference)
    h=hashlib.sha256()
    with file.open('rb') as stream:
        for b in iter(lambda:stream.read(1<<20),b''): h.update(b)
    report[method]=dict(numpy_float64_semantic_consistency=value,reported_difference=difference,
                        feature_cache_sha256=h.hexdigest(),validation_images=len(labels))
report['scope']='Independent NumPy calculation from cached validation features. No checkpoints or TEST images loaded. Float64 normalization may differ from the original float32 rounding.'
target=root/'independent_consistency_verification.json'; target.write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
