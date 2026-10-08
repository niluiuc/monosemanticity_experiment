"""One prospective controlled image model. Train/test stages prevent holdout peeking.

This file prepares an experiment; do not execute training before joint review.
Soft scores feed a separately reviewed compressor; this is not native vision transfer.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np

SEED = 20261008
CONFIG = dict(seed=SEED, train_backgrounds=256, calibration_backgrounds=64,
              test_backgrounds=256, max_epochs=80, train_seconds=180,
              batch_size=128, learning_rate=.005, recovery_rms_gate=5e-4,
              threads=4, factor_probability=.5, importance=[1., 1.],
              prescribed_sigmas=[0., .3], no_thresholding=True,
              model='conv3x8_k5_s2_p2_relu_conv8x16_k3_s2_p1_relu_flat_linear1024x32_relu_linear32x2')
STATES = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float64)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def manifest(out):
    write(out / 'sha256.json', {p.relative_to(out).as_posix(): sha(p)
                              for p in out.rglob('*') if p.is_file() and p.name != 'sha256.json'})


def render(data, indices, nuisance_seed):
    """All four states per background, with identical nuisance within each group."""
    rng = np.random.default_rng(nuisance_seed)
    images, labels, ids, nuisance = [], [], [], []
    yy, xx = np.mgrid[:32, :32]
    for index in indices:
        grey = data[int(index)].astype(np.float32).mean(axis=2) / 255.
        base = np.repeat((.05 + .20 * grey)[..., None], 3, axis=2)
        dx1, dy1, dx2, dy2 = rng.integers(-2, 3, size=4)
        intensity1, intensity2 = rng.uniform(.75, .95, size=2)
        disk = (xx - (8 + dx1)) ** 2 + (yy - (16 + dy1)) ** 2 <= 9
        bar = (np.abs(xx - (24 + dx2)) <= 2) & (np.abs(yy - (16 + dy2)) <= 3)
        for state in STATES:
            image = base.copy()
            if state[0]:
                image[disk] = intensity1
            if state[1]:
                image[bar] = intensity2
            images.append(np.moveaxis(image, 2, 0))
            labels.append(state)
            ids.append(int(index))
            nuisance.append([int(dx1), int(dy1), int(dx2), int(dy2), intensity1, intensity2])
    return dict(images=np.stack(images).astype(np.float32),
                labels=np.asarray(labels, dtype=np.float64), background_ids=np.asarray(ids),
                nuisance=np.asarray(nuisance, dtype=np.float64))


def model_class(torch):
    return torch.nn.Sequential(torch.nn.Conv2d(3, 8, 5, stride=2, padding=2), torch.nn.ReLU(),
                               torch.nn.Conv2d(8, 16, 3, stride=2, padding=1), torch.nn.ReLU(),
                               torch.nn.Flatten(), torch.nn.Linear(1024, 32), torch.nn.ReLU(),
                               torch.nn.Linear(32, 2))


def infer(torch, model, images):
    values = []
    model.eval()
    with torch.inference_mode():
        for begin in range(0, len(images), CONFIG['batch_size']):
            values.append(model(torch.from_numpy(images[begin:begin + CONFIG['batch_size']])).numpy())
    logits = np.concatenate(values).astype(np.float64)
    # Stable sigmoid evaluated in float64; no hard labels, snapping, or temperature.
    scores = np.empty_like(logits)
    positive = logits >= 0
    scores[positive] = 1 / (1 + np.exp(-logits[positive]))
    exp_negative = np.exp(logits[~positive])
    scores[~positive] = exp_negative / (1 + exp_negative)
    return logits, scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['train', 'test'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--trained', type=Path)
    parser.add_argument('--prediction', type=Path)
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=False)
    write(out / 'config.json', CONFIG)
    (out / 'source_snapshot.py').write_bytes(Path(__file__).read_bytes())
    import torch
    import torchvision
    torch.set_num_threads(CONFIG['threads'])
    torch.set_num_interop_threads(1)
    torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True)
    data = torchvision.datasets.CIFAR10(str(args.cache / 'data'), train=True, download=False)
    selection = np.random.default_rng(SEED).permutation(len(data.data))[:576]
    splits = dict(train=selection[:256], calibration=selection[256:320], test=selection[320:576])
    np.savez_compressed(out / 'split_background_ids.npz', **splits)
    provenance = dict(torch=torch.__version__, torchvision=torchvision.__version__,
                      numpy=np.__version__, source_sha256=sha(__file__),
                      cifar_archive_sha256=sha(args.cache / 'data' / data.filename),
                      dataset_class_labels_used=False, controlled_semisynthetic=True,
                      status='started', stage=args.stage)
    write(out / 'provenance.json', provenance)
    model = model_class(torch)
    try:
        if args.stage == 'train':
            train = render(data.data, splits['train'], SEED + 1)
            cal = render(data.data, splits['calibration'], SEED + 2)
            np.savez_compressed(out / 'train_images.npz', **train)
            np.savez_compressed(out / 'calibration_images.npz', **cal)
            optimizer = torch.optim.Adam(model.parameters(), lr=CONFIG['learning_rate'])
            criterion = torch.nn.BCEWithLogitsLoss()
            images = torch.from_numpy(train['images'])
            labels = torch.from_numpy(train['labels'].astype(np.float32))
            shuffle = torch.Generator().manual_seed(SEED + 4)
            start = time.monotonic()
            history = []
            completed = 0
            timed_out = False
            model.train()
            for epoch in range(CONFIG['max_epochs']):
                order = torch.randperm(len(images), generator=shuffle)
                total = 0.
                seen = 0
                for begin in range(0, len(images), CONFIG['batch_size']):
                    if time.monotonic() - start >= CONFIG['train_seconds']:
                        timed_out = True
                        break
                    ids = order[begin:begin + CONFIG['batch_size']]
                    optimizer.zero_grad(set_to_none=True)
                    loss = criterion(model(images[ids]), labels[ids])
                    if not torch.isfinite(loss):
                        raise FloatingPointError('Nonfinite training loss')
                    loss.backward()
                    optimizer.step()
                    total += float(loss.detach()) * len(ids)
                    seen += len(ids)
                history.append(dict(epoch=epoch + 1, examples=seen, mean_bce=total / max(1, seen),
                                    elapsed_seconds=time.monotonic() - start, completed=not timed_out))
                write(out / 'training_history.json', history)
                if timed_out:
                    break
                completed += 1
            torch.save(model.state_dict(), out / 'model.pt')
            recovery = {}
            for split, records in [('train', train), ('calibration', cal)]:
                logits, scores = infer(torch, model, records['images'])
                np.savez_compressed(out / f'{split}_scores.npz', logits=logits, scores=scores,
                                    labels=records['labels'], background_ids=records['background_ids'])
                recovery[split] = dict(rms=float(np.sqrt(np.mean(np.sum((scores - records['labels']) ** 2, axis=1)))),
                                       coordinate_mse=np.mean((scores - records['labels']) ** 2, axis=0).tolist(),
                                       maximum_absolute_error=float(np.max(np.abs(scores - records['labels']))))
            passed = not timed_out and all(v['rms'] <= CONFIG['recovery_rms_gate'] for v in recovery.values())
            write(out / 'recovery_gate.json', dict(passed=passed, values=recovery, threshold=CONFIG['recovery_rms_gate'],
                                                  completed_epochs=completed, timed_out=timed_out,
                                                  training_elapsed_seconds=time.monotonic() - start))
            provenance.update(status='complete' if passed else 'quality_gate_failed',
                              model_sha256=sha(out / 'model.pt'), test_images_not_constructed=True)
        else:
            if args.trained is None or args.prediction is None:
                raise ValueError('Test requires trained artifact and pre-recorded approved prediction')
            gate = json.loads((args.trained / 'recovery_gate.json').read_text())
            prediction = json.loads(args.prediction.read_text())
            if not gate['passed'] or not prediction.get('approved_for_heldout', False):
                raise RuntimeError('Prediction/recovery prerequisites not approved')
            if prediction.get('model_sha256') != sha(args.trained / 'model.pt'):
                raise RuntimeError('Prediction is not bound to this final image model')
            if json.loads((args.trained / 'config.json').read_text()) != CONFIG:
                raise RuntimeError('Do not change the model configuration after training')
            model.load_state_dict(torch.load(args.trained / 'model.pt', map_location='cpu', weights_only=True))
            test = render(data.data, splits['test'], SEED + 3)
            np.savez_compressed(out / 'test_images.npz', **test)
            logits, scores = infer(torch, model, test['images'])
            np.savez_compressed(out / 'test_scores.npz', logits=logits, scores=scores,
                                labels=test['labels'], background_ids=test['background_ids'])
            error = float(np.sqrt(np.mean(np.sum((scores - test['labels']) ** 2, axis=1))))
            write(out / 'recovery_gate.json', dict(passed=error <= CONFIG['recovery_rms_gate'], rms=error,
                                                  threshold=CONFIG['recovery_rms_gate'],
                                                  no_thresholding=True, outcome_exclusion=False))
            provenance.update(status='complete', prediction_sha256=sha(args.prediction),
                              model_sha256=sha(args.trained / 'model.pt'),
                              prospective_recovery_gate_passed=error <= CONFIG['recovery_rms_gate'])
    except Exception as exc:
        provenance.update(status='failed', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        write(out / 'provenance.json', provenance)
        manifest(out)


if __name__ == '__main__':
    main()
