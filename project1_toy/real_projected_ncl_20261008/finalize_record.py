import datetime, hashlib, json
from pathlib import Path
import fitz
base=Path(__file__).parent; workspace=base.parents[1]
paragraph='''

## Completed native outcome and independent checks, 8 October 2026

- Both jobs completed. The native corruption computation took 12 minutes 45 seconds on Physics CPU resources. The SSH connection remains open; no original user job was changed.
- The affine prediction failed and was frozen before TEST scoring. It predicts no crossing. Its frozen hash is c643b6e46cd7f170937cd95b0bac89d7c303463a3392e3c20d3c0443664eec00. This failure is not repaired by the subsequent observation.
- On the official 10,000-image TEST set, CL wins clean: NCL-minus-CL error +0.016500, simultaneous conditional interval [0.0048246875,0.027600]. At sigma .12, NCL wins: difference -0.0122333333, interval [-0.018684375,-0.00607489583]. At sigma .20 it also wins: -0.006500, interval [-0.0108502083,-0.00211645833]. This establishes the native ordering reversal at evaluated noise levels for this checkpoint/probe pair.
- The .08 difference is unresolved. The first point-estimate crossing lies between .04 and .08; linear interpolation .078352941176 is descriptive, not a successful forecast or a crossing confidence interval. At .30 CL regains a small advantage; both accuracies are below 3%, near 1% chance. There is no evidence for a unique permanent phase transition.
- Independent NumPy checks reproduce saved errors, paired-image simultaneous bands, decisions, prediction curve and hash. Cached-feature class consistency was separately recomputed. Complete scientific arrays and logs are in outputs; large training caches and checkpoints remain on scratch.
- The earlier reconstruction theorem has a different loss, noise location and representation. Its numerical boundary and critical exponent are not validated here. Existing monosemanticity papers already show robustness gains: this one comparison is not publication novelty by itself, a causal monosemanticity intervention, or a completed ICML contribution.
- Sections 8.35 and 8.36 retain the failed backbone prerequisites, successful native ordering reversal and failed prediction. Current derivation PDF and editable source compiled successfully; new pages 96--99 were visually checked without overflow.
- The remaining paper-critical gap is a finite-noise explanatory/predictive mechanism, with independent replication. One post-outcome, validation-only gate diagnostic is registered separately: at the already failed sigma .04, compare full affine logits with affine backbone plus exact nonlinear projector. If the latter fails existing thresholds, stop projection-only repairs. No new TEST evidence or retrospective prediction success is claimed.
'''
for p in (base/'RUN_STATUS.md',workspace/'project1_toy/plan.md'):
    text=p.read_text(encoding="utf-8")
    if '## Completed native outcome and independent checks, 8 October 2026' not in text:
        p.write_text(text+paragraph,encoding='utf-8')
pdf=workspace/'output/pdf/Superposition_Recursive_Training_Derivations.pdf'
source=workspace/'research_notes/volume2.tex'
record=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pages=len(fitz.open(pdf)),
    pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    native_reversal_observed=True,predictive_claim_passed=False,visual_qa_pages=[96,97,98,99])
(base/'DELIVERY_RECORD.json').write_text(json.dumps(record,indent=2)); print(json.dumps(record))
