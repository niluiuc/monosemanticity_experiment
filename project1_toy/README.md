# Project 1 controlled toy experiment

Read **[plan.md](plan.md)** first. It records the motivation, definitions, hypotheses,
fixed settings, results interpretation, limitations and next decision. This README
only explains running and inspecting the experiment.

The first saved experiment is `runs/protocol_v1_2026-10-05`. Read its
[generated results](runs/protocol_v1_2026-10-05/results.md) alongside the
[post-run review](reviews/protocol_v1_2026-10-05/review.md), which includes the
unfavorable findings and a documented plotting correction. The complete living
plan retains the pre-run protocol and appends the outcomes after it.

## Run a new experiment

Use Python 3.12 or later (the pinned SciPy version requires it). The recorded run
used Python 3.12.14. From this directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python checks.py
python run_experiments.py
```

The runner prints its new output directory. A normal CPU is sufficient. There is
no pretrained model download or GPU requirement. Every run has a fresh directory;
an existing directory is refused rather than overwritten. To choose its name:

```powershell
python run_experiments.py --output runs/my_independent_run
```

The locally bundled NumPy/SciPy/Matplotlib environment also works without creating
a virtual environment. `environment.json` records the actual versions and CPU/BLAS
configuration. Pinning Python and package versions improves numerical repeatability;
different BLAS implementations can produce small floating-point differences.

## Verify a saved run

```powershell
python -B verify_results.py runs/RUN_DIRECTORY --retrain
```

This checks file hashes, replays raw predictions from saved inputs/noise/weights,
checks CSV counts and exact risks, and (with `--retrain`) reruns every training seed
from initialization. It does not refit, tune or replace saved results. You can run
the archived copy of `source/verify_results.py` instead of the current working copy
to use the precise mathematical code preserved with that run.

To save the audit separately from the immutable run artifacts:

```powershell
python -B verify_results.py runs/RUN_DIRECTORY --retrain --report audits/my_audit.json
```

## Files to read

- `plan.md`: living narrative and append-only experiment log.
- `config.json`: all prespecified settings.
- `toy_math.py`: population construction, explicit tied gradient, exact risk,
  bound, optimizer, mono baseline, and rectified-Gaussian reconstruction moments.
- `checks.py`: finite-difference gradient and independent pair/enumeration checks.
- `run_experiments.py`: simulation, storage and experiment orchestration.
- `plot_results.py`: factual report and plots, with all seeds retained.
- `verify_results.py`: verification without changing saved artifacts.
- `runs/<run>/results.md`: generated outcomes for that specific run.
- `runs/<run>/summary.json`: machine-readable outcomes; no hand-edited table.
- `runs/<run>/trained_feature_metrics.csv`: error, FP/FN, thresholds, geometry,
  confidence intervals, bound and reconstruction errors for every feature.
- `runs/<run>/paired_comparisons.csv`: learned-minus-mono differences using common
  samples; uncertainty includes test sampling, not initialization variation.
- `runs/<run>/trained/p*/`: saved inputs, noise, models, predictions and full traces.
- `runs/<run>/source/`: code/config snapshot; `plan_before_run.md` fixes the protocol.
- `runs/<run>/manifest.json`: SHA-256 integrity list.

## Read compressed raw predictions

```python
import numpy as np

data = np.load("runs/RUN_DIRECTORY/trained/p0.15_seed0/test_predictions.npz")
shape = tuple(data["shape"])
name = "learned_matched_s3"  # s3 indexes sigma=0.30 in config.json
prediction = np.unpackbits(data[name], count=int(np.prod(shape))).reshape(shape).astype(bool)
inputs = np.load("runs/RUN_DIRECTORY/trained/p0.15_seed0/test_inputs.npz")["inputs"]
print((prediction != inputs).mean(axis=0))
```

Bit packing is lossless; standard Gaussian noise is saved as float64 without
rounding. The same test examples/noise are reused across models and sigma, making
comparisons paired. They are not independent repetitions across noise levels.

`-B` prevents Python from adding bytecode caches when verifying an archived code
snapshot. Such caches are not measurement artifacts and are excluded from the ZIP.

## Corrected visualization of the first run

The original risk plot has a documented shared-axis upper-limit bug. It is preserved
with its original source. Use the corrected images in
`reviews/protocol_v1_2026-10-05/plots/`; no CSV or raw prediction was modified.
To regenerate views separately from an archived run with the current plotting code:

```powershell
python plot_results.py runs/protocol_v1_2026-10-05 --plots-only-to reviews/my_views/plots
```

`review_saved_run.py` also writes a factual review and post-run descriptive geometry
summary from existing files; it performs no additional experiment. Those descriptive
measurements must not be presented as preregistered hypothesis tests.

## Maintain the record

Never edit a saved run to improve a conclusion. Change the code or configuration
for a justified question, append its motivation and settings to `plan.md` **before**
running, and write a new run folder. Report failed checks and unfavorable outcomes.
The current runner is specific to uniform-importance independent binary concepts;
do not label a changed distribution as covered by this protocol.
