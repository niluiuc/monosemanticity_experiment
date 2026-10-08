# Official CIFAR-100 checkpoint feasibility

Date: 8 October 2026. No training, feature extraction, image scoring, corrupted test evaluation, or model selection was performed.

## Motivation and smallest check

Project 1 asks when sharing's clean task advantage reverses under corruption. The proposed native-network experiment needs two actual pretrained representation models, not a two-feature compressor fitted to their outputs. This check lists the official release, downloads only its two CIFAR-100 checkpoints, inspects them safely, and reads the associated evaluation source. Stop after determining what the available artifacts actually support.

## Confirmed files

Official repository: https://github.com/PKU-ML/non_neg

Inspected source commit: `880b3ceace102d1b04132ca371eb773faffdf54e`.

Official CIFAR-100 folder: https://drive.google.com/drive/folders/1EbF9oKFu9rjsfRj_hv-Q-GVYKUSVxIkP

| Release subfolder | File | Drive file ID |
|---|---|---|
| CIFAR100-CL | cifar100-simclr-e200-3a7937mb-ep=199.ckpt | 146YDJ8C0P4DCBYOiC-8qPrM6A0r2hcbE |
| CIFAR100-NCL | cifar100-simclr-e200-gelu_relu-jt2gegkm-ep=199.ckpt | 1b0k2rBs2EYvbq9q0shNY7LrtqRKzwtia |

Each file is 102,467,009 bytes. Both load with `torch.load(..., map_location='cpu', weights_only=True)`. Actual checkpoint metadata reports epoch 199 and global step 39000, rather than relying only on filenames. Tensor shapes match between checkpoints. The first convolution is 64-by-3-by-3-by-3, consistent with the official CIFAR ResNet adaptation. Both contain 100-by-512 online classifier weights and the projection head.

Checksums, all tensor keys/shapes and pinned source hashes are in `checkpoint_inventory.json`. The external model files are cached at `C:/Users/indra/.cache/monosemanticity_ncl_20261008/checkpoints/`; source snapshots are in the adjacent `official_source/` folder. They are not copied into the research repository. Original model files were not modified.

## What must be resolved in the frozen protocol

- **Checkpoint identity:** these are the predecessor paper's official releases. Neither filenames nor inspected checkpoint metadata establish that they are the identical trained runs behind the anchor paper's numerical table. Its published clean gap must not be assumed for these files.
- **Heads:** `classifier.*` is the online supervised classifier trained during pretraining on detached backbone features. This is not the anchor's separately fitted clean linear probe. One must explicitly choose the evaluation head or fit the clean probes as planned; switching after seeing performance is inappropriate.
- **Representation:** the inspected `main_eval.py` evaluates `h['z']`, the 256-dimensional projection output, and applies ReLU when the checkpoint path contains `relu`. The stored online classifier instead consumes the 512-dimensional backbone representation. Calling the former's class consistency a property directly measured on the latter would be a mismatch. Specify the representation(s), head and operational meaning of consistency before evaluation.
- **Execution:** `main_eval.py` calls `.cuda()` directly and runs extra retrieval analysis. It is not an immediately CPU-compatible minimal test. A faithful restricted implementation or an appropriate cluster runtime is needed; reproducing its metric conventions must be documented.
- **Prediction:** squared logit/margin changes per noise variance are not classification-error growth coefficients. Their units and decision event differ. The proposed square-root crossing expression is not yet justified for this task. Do not freeze it as an established theoretical forecast or compare it against test data without a task-specific argument and declared applicability checks.
- **Claim scope:** CL versus NCL changes the training procedure, not monosemanticity in isolation. Association is appropriate; these two checkpoints alone cannot identify a causal monosemanticity effect or training-seed uncertainty.

## Cluster access

The user completed password plus Duo authentication in Git Bash, but the configured ControlMaster connection resets every new shell request. `ssh -O check ncsa` reports a living master; a batch command through it still fails. Therefore successful authentication is not yet usable autonomous cluster access.

The command `ssh -o ControlMaster=no -o ControlPath=none ncsa` avoids this failing local multiplexing path for an ordinary interactive login. It does not establish agent-reusable access. No job has been submitted, no cluster files uploaded, and no SSH settings or keys were changed.

## Next action

Give Claude this exact inventory so the frozen protocol uses the correct files, representation and head. Correct the unsupported classification crossing predictor before evaluating corrupted test images. Keep the dataset, checkpoint pair and corruption family fixed; do not replace this prerequisite check with another parameter search.
