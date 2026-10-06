# Monosemanticity research course and derivations

Read **Volume I** first for the source paper and **Volume II** for the two-project derivation program. Final PDFs are in `../output/pdf/`.

The notes preserve the superposition-to-robustness phase diagram and the recursive-training/monosemanticity question. They distinguish exact conditional mathematics, independently checked toy calculations, standard mathematical tools, and research claims that still require novelty checks and real-model evidence.

## Contents

- `volume1.tex`: graduate lecture course, including source-version differences, detailed derivations, experiment explanations and worked exercises.
- `volume2.tex`: operational robustness formulas, exact nonlinear pair tradeoff, general error bound, recursive kernels, retraining derivative, coupling bounds, diffusion explanation and eight-week research protocol.
- `preamble.tex`: shared print layout and mathematical notation.
- `verify_math.py`: original numerical calculations and figures; fixed seed 20260921.
- `verify_additional.py`: generalized risk checks, Bernstein-bound checks, equal-energy pair simulation and exact symbolic algebra verification. This is symbolic simplification, **not symbolic regression or equation fitting**.
- `verification_results.json` and `additional_verification.json`: recorded numerical results.
- `build_notes.py`: compile both PDFs and render pages for visual review.

## Rebuild

With Python containing NumPy, SciPy, Matplotlib, SymPy, PyMuPDF and Pillow, and a LaTeX distribution providing `pdflatex`:

```text
python research_notes/verify_math.py
python research_notes/verify_additional.py
python research_notes/build_notes.py
```

LaTeX is used here for native vector equations and searchable mathematical text. The build checks for overfull lines and out-of-page text and renders every page to `../tmp/pdfs/qa/`; visual review is still necessary.

These calculations are not a reproduction of the source paper's neural-network training, nor a completed diffusion experiment. Source references, precise assumptions and the remaining research work are documented in the PDFs. The source paper and later proceedings PDF are retained under `../tmp/paper_audit/` for provenance.
