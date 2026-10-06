# Monosemanticity and Robustness: Reading Notes

Upload this ZIP as a new Overleaf project. Use **pdfLaTeX** and select **main.tex** as the main document. No custom fonts, external templates, shell escape or bibliography processor is needed.

Files:
- `main.tex`: complete editable document.
- `figures/`: the three figures included in the notes.
- `supplement/verify_math.py`: source of the numerical checks and figures.
- `supplement/verification_results.json`: saved results of those checks.

The document retains the technical content, equations, tables, examples, questions and references of the lecture-note version, with a conventional article layout and neutral research-note wording. The numerical checks are small simulations, not a reproduction of the paper's ResNet or Llama training.

To run the optional verification script locally, install NumPy, SciPy and Matplotlib, then run `python supplement/verify_math.py`. It writes generated figures to `supplement/figures/` and a results JSON beside the script. Compilation on Overleaf does not run Python; the required figures are already included.
