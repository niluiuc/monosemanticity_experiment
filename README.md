# monosemanticity_experiment
Research paper on monosemanticity

This branch contains the Project 1 research record: mathematical assumptions,
controlled toy-model code, saved numerical outputs, independent checks, and
the current evidence and publication assessment. Proved statements, numerical
findings, and unresolved questions are distinguished in the linked records.

## Start here

- [Living research plan and experiment log](project1_toy/plan.md)
- [Latest decision and calibration-control overview](project1_toy/paper_decision_2026-10-06/README.md)
- [Calibration-control results and limitations](project1_toy/paper_decision_2026-10-06/calibration_results.md)
- [Senior research assessment](project1_toy/paper_decision_2026-10-06/professor_decision.md)
- [Exact-claim literature comparison](project1_toy/paper_decision_2026-10-06/exact_claim_comparison.md)
- [Full mathematical derivations (PDF)](output/pdf/Superposition_Recursive_Training_Derivations.pdf)

## Reproduce and inspect

Use Python 3.12. Each experiment directory documents its settings, stopping
criteria, dependencies, and immutable recorded run. Run reproductions in a
fresh output directory; do not overwrite archived results.

The initial toy experiment uses the pinned dependencies in
[project1_toy/requirements.txt](project1_toy/requirements.txt):

```sh
python -m pip install -r project1_toy/requirements.txt
```

Additional mathematical and toy checks have their own dependency lists:

- [Focused clean-training bridge](project1_toy/focused_bridge_2026-10-06/README.md)
- [Frequency-dependent storage transition](project1_toy/frequency_boundary_2026-10-06/README.md)
- [Original toy protocol and saved outputs](project1_toy/README.md)
- [Literature audit and preserved source provenance](project1_toy/literature_review/novelty_audit.md)
- [Research-note build utilities and verification records](research_notes/README.md)

For example, the latest calibration control can be reproduced with a new output
directory using the existing approval record:

```sh
cd project1_toy/paper_decision_2026-10-06
python run_calibration_control.py --senior-review professor_decision.md --output run_reproduction
```

This publication snapshot intentionally excludes personal discussion archives,
payment information, LaTeX source/build files, and all PDFs except the linked
derivations volume. Code, notes, scientific figures and recorded experiment
outputs remain available. Links inside archived historical documents may refer
to locally retained source files excluded from this public snapshot.

The repository's existing [license](LICENSE) is retained.

The two external HTML wrappers containing embedded website tokens were omitted
after GitHub push protection rejected them. Their extracted article text and
provenance are retained. Archived research bytes are preserved with Git text
conversion disabled, so recorded SHA-256 hashes survive cloning.

See [the publication snapshot manifest](upload_audit/manifest.json) for exact
included paths, file sizes, hashes and exclusion counts.
