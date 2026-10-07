"""One fixed frozen-vision pass. No bottleneck fitting or risk comparisons."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import time
import sys

DEFAULT_CACHE = Path('C:/Users/indra/.cache/monosemanticity_vision_20261006')
HERE = Path(__file__).resolve().parent


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=DEFAULT_CACHE)
    parser.add_argument('--output', type=Path, default=HERE / 'extraction_run_v1')
    parser.add_argument('--protocol', type=Path, required=True)
    parser.add_argument('--max-seconds', type=float, default=600)
    args = parser.parse_args()
    assert args.protocol.is_file(), 'A reviewed prospective protocol is required before extraction.'
    started = time.monotonic()
    args.output.mkdir(parents=True, exist_ok=False)
    args.cache.mkdir(parents=True, exist_ok=True)
    snapshot = args.output / 'source_snapshot'
    snapshot.mkdir()
    shutil.copy2(Path(__file__), snapshot / Path(__file__).name)
    shutil.copy2(args.protocol, snapshot / args.protocol.name)
    os.environ['TORCH_HOME'] = str(args.cache / 'weights')
    try:
        import numpy as np
        import torch
        import torchvision
        from torchvision.datasets import CIFAR10
        from torchvision.models import ResNet18_Weights, resnet18
    except Exception as error:
        failure = dict(status='dependency_import_failed', error_type=type(error).__name__,
                       error=str(error), source_sha256=sha256(Path(__file__)),
                       elapsed_seconds=time.monotonic() - started)
        (args.output / 'provenance.json').write_text(json.dumps(failure, indent=2), encoding='utf-8')
        (args.output / 'sha256.json').write_text(json.dumps({
            str(p.relative_to(args.output)): sha256(p) for p in args.output.rglob('*')
            if p.is_file() and p.name != 'sha256.json'}, indent=2), encoding='utf-8')
        raise

    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    weights = ResNet18_Weights.IMAGENET1K_V1
    transform = weights.transforms()
    metadata = {
        'protocol': 'fixed frozen extraction; no training, class selection or risk outcomes',
        'seed': 20261006, 'device': 'cpu', 'batch_size': 32, 'threads': 4,
        'split_sizes': {'train': 256, 'calibration': 256, 'test': 512},
        'checkpoint': weights.name, 'checkpoint_url': weights.url,
        'dataset_url': CIFAR10.url, 'dataset_archive_md5': CIFAR10.tgz_md5,
        'transform_repr': repr(transform),
        'transform_fields': {key: getattr(transform, key, None) for key in
                             ['crop_size', 'resize_size', 'mean', 'std', 'antialias']},
        'feature_location': 'post-ReLU layer4 output; spatial cell [height//2,width//2]',
        'channel_rule': 'first two by index with train variance>0 and train mean!=0',
        'normalization': 'divide by channel train RMS; no centering',
        'max_seconds': args.max_seconds,
        'python': sys.version, 'torch': torch.__version__, 'torchvision': torchvision.__version__,
        'numpy': np.__version__, 'source_sha256': sha256(Path(__file__)),
        'cache': str(args.cache.resolve()), 'status': 'started',
    }
    (args.output / 'provenance.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    try:
        dataset = CIFAR10(root=str(args.cache / 'data'), train=True, download=True)
        if time.monotonic() - started > args.max_seconds:
            raise TimeoutError('Budget exhausted during data acquisition; no feature pass.')
        model = resnet18(weights=weights, progress=False).eval()
        if time.monotonic() - started > args.max_seconds:
            raise TimeoutError('Budget exhausted during checkpoint acquisition; no feature pass.')
        for parameter in model.parameters():
            parameter.requires_grad_(False)
        indices = np.random.default_rng(20261006).permutation(len(dataset))[:1024]
        np.save(args.output / 'image_indices.npy', indices)
        all_features = []
        coordinates = []
        def capture(_module, _inputs, output):
            height, width = output.shape[-2:]
            coordinates.append([int(height), int(width), int(height // 2), int(width // 2)])
            all_features.append(output[:, :, height // 2, width // 2].detach().cpu().numpy().copy())
        hook = model.layer4.register_forward_hook(capture)
        labels = []
        try:
            with torch.inference_mode():
                for begin in range(0, len(indices), 32):
                    if time.monotonic() - started > args.max_seconds:
                        raise TimeoutError('Budget exhausted; partial feature batches preserved.')
                    samples = [dataset[int(i)] for i in indices[begin:begin + 32]]
                    labels.extend([int(label) for _, label in samples])
                    image_batch = torch.stack([transform(image) for image, _ in samples])
                    model(image_batch)
        finally:
            hook.remove()
            if all_features:
                np.save(args.output / 'features_raw.npy', np.concatenate(all_features, axis=0))
                np.save(args.output / 'labels_for_audit_only.npy', np.asarray(labels, dtype=np.int64))
        features = np.concatenate(all_features, axis=0)
        assert features.shape == (1024, 512) and np.isfinite(features).all()
        assert (features >= 0).all(), 'Expected post-ReLU nonnegative activations.'
        train = features[:256].astype(np.float64)
        means = train.mean(axis=0)
        variances = train.var(axis=0)
        channels = np.flatnonzero((variances > 0) & (means != 0))[:2]
        if len(channels) != 2:
            raise RuntimeError('Two predeclared eligible channels unavailable; no pair scan.')
        rms = np.sqrt((train[:, channels] ** 2).mean(axis=0))
        normalized = features[:, channels].astype(np.float64) / rms
        np.savez(args.output / 'selected_features.npz', channels=channels, train_rms=rms,
                 train=normalized[:256], calibration=normalized[256:512], test=normalized[512:],
                 train_indices=indices[:256], calibration_indices=indices[256:512],
                 test_indices=indices[512:])
        zero_fractions = (train[:, channels] == 0).mean(axis=0)
        active = train[:, channels] > 0
        archive = args.cache / 'data' / CIFAR10.filename
        checkpoint = args.cache / 'weights' / 'hub' / 'checkpoints' / Path(weights.url).name
        metadata.update({
            'channels': channels.tolist(), 'train_rms': rms.tolist(),
            'train_zero_fractions': zero_fractions.tolist(),
            'normalized_pair_noise_reference_sqrt_mean_variance':
                float(np.sqrt(normalized[:256].var(axis=0).mean())),
            'train_coactivation_fraction': float(np.logical_and(active[:, 0], active[:, 1]).mean()),
            'train_state_fractions_00_01_10_11': [float(((active[:, 0] == i) &
                      (active[:, 1] == j)).mean()) for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]],
            'noise_reference': 'sigma is scalar bottleneck-code SD after train-RMS feature normalization; energy=1',
            'layer4_spatial_coordinates_per_batch': coordinates,
            'dataset_archive_sha256': sha256(archive),
            'checkpoint_sha256': sha256(checkpoint),
            'status': 'stop_no_exact_zero_mass' if np.all(zero_fractions == 0) else 'extraction_complete',
            'both_selected_channels_have_exact_zero_mass': bool(np.all(zero_fractions > 0)),
            'downstream_execution': 'none; professor review required',
        })
        metadata['elapsed_seconds_at_activation_save'] = time.monotonic() - started
        np.savez(args.output / 'vision_activations.npz',
                 train=features[:256], calibration=features[256:512], test=features[512:],
                 train_indices=indices[:256], calibration_indices=indices[256:512],
                 test_indices=indices[512:],
                 metadata_json=np.asarray(json.dumps(metadata, sort_keys=True)))
    except Exception as error:
        metadata.update(status='failed', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        metadata['elapsed_seconds'] = time.monotonic() - started
        (args.output / 'provenance.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
        manifest = {str(path.relative_to(args.output)): sha256(path) for path in
                    sorted(args.output.rglob('*')) if path.is_file() and path.name != 'sha256.json'}
        (args.output / 'sha256.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
