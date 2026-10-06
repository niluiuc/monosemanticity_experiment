"""Integrate reviewed Project 1 chapters into the existing derivation volume.

Preserves the preceding source and PDF once; does not run experiments.
"""
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = HERE / "volume2.tex"
PDF = ROOT / "output" / "pdf" / "Superposition_Recursive_Training_Derivations.pdf"
BEGIN = "% BEGIN REVIEWED PROJECT 1 UPDATE 2026-10-06"
END = "% END REVIEWED PROJECT 1 UPDATE 2026-10-06"


def main():
    archive = ROOT / "tmp" / "pdfs" / "derivations_before_20261006"
    archive.mkdir(parents=True, exist_ok=True)
    for source in [SOURCE, PDF]:
        destination = archive / source.name
        if not destination.exists():
            shutil.copy2(source, destination)
    content = SOURCE.read_text(encoding="utf-8")
    chapters = "\n".join((HERE / name).read_text(encoding="utf-8") for name in [
        "project1_clean_update_20261006.tex", "project1_noise_update_20261006.tex"
    ])
    block = BEGIN + "\n" + chapters + "\n" + END + "\n\n"
    if BEGIN in content:
        before, remainder = content.split(BEGIN, 1)
        _, after = remainder.split(END, 1)
        content = before + block + after.lstrip("\r\n")
    else:
        marker = "\\chapter{Project 2: the correct meaning of the covariance recursion}"
        if content.count(marker) != 1:
            raise ValueError("Cannot locate unique Project 1 / Project 2 chapter boundary")
        content = content.replace(marker, block + marker)
        content = content.replace(
            "Chapters 1--3 establish definitions and repair the earlier formulas. Chapters 4--6 derive Project 1 results. Chapters 7--10 derive Project 2 and the mathematical connection. Chapters 11--13 explain diffusion, controlled validation and the eight-week execution plan.",
            "Chapters 1--3 establish definitions and operational interpretations. Chapters 4--6 derive fixed-geometry Project 1 results and a general interference bound. Chapters 7--8 derive clean-selected geometry, the global frequency transition and the certified nonmonotone noise comparison. Chapters 9--12 derive Project 2 and the mathematical connection. Chapters 13--15 explain diffusion, controlled validation and the original eight-week execution outline."
        )
        content = content.replace("as in Chapter 10.", "as in Chapter 12.")
        content = content.replace("Under the kernel of Chapter 8,", "Under the kernel of Chapter 10,")
        content = content.replace("fixed-point series in Chapter 8.", "fixed-point series in Chapter 10.")
        content = content.replace(
            "\\section{Recovering the old expression}",
            "\\section{A normalized matched-readout example}"
        ).replace(
            "\\section{Why this differs from the earlier proposed boundary}",
            "\\section{Distinguishing geometric overlap from statistical interference}"
        ).replace(
            "\\section{Answers to the earlier conceptual questions}",
            "\\section{Interpreting isolation, rarity and signed overlap}"
        )
        content = content.replace(
            "\\textbf{Prepared:} 20 September 2026.",
            "\\textbf{Prepared:} 20 September 2026; Project 1 derivations updated 6 October 2026."
        )
        content = content.replace(
            "\\hypersetup{pdftitle=",
            "\\fancyfoot[L]{\\small Research derivations | Updated October 2026}\n\\hypersetup{pdftitle=",
            1
        )
        contribution_note = r"""
\section*{Project 1 update: exact scope of the completed mathematics}
The added clean-training and noise chapters derive the finite bias profiles,
dense-case optima, a certified low-frequency geometry, the global clean
frequency transition, and the at-least-two noise-crossing result. They preserve
the distinction between reconstruction-selected representations and downstream
binary detection. All new mathematics remains in this volume rather than only
in working Markdown files. The arbitrary-load/importance target and real-model
transfer are not complete; the original Project 2 material is preserved as
background, with no new recursive-training experiment introduced.
"""
        content = content.replace("\\section*{The scientific question in plain language}",
                                  contribution_note + "\n\\section*{The scientific question in plain language}")
        content = content.replace(
            "\\section{It is a matched readout, not always the optimal readout}",
            r"""The squared alignment score also equals the established per-feature
capacity in Scherlis et al., \emph{Polysemanticity and Capacity in Neural Networks},
Equation (3):
\begin{equation}
C_i=\frac{(w_i^\top w_i)^2}{\sum_j(w_i^\top w_j)^2}=M_i^2.
\end{equation}
This identity prevents treating the score itself as a new contribution.
A dropped feature requires a separate convention because the ratio is undefined.

\section{It is a matched readout, not always the optimal readout}"""
        )
        content = content.replace(
            "\\chapter{An eight-week program that preserves both projects}",
            r"""\chapter{An eight-week program that preserves both projects}
\section{Status of this execution outline}
This is the original September planning outline, retained as background rather
than a renewed eight-week allowance. The October Project 1 results appear in
Chapters 7--8. The current stop decision is to consolidate the established
claims, compare their exact assumptions with the direct prior literature, and
specify one bounded real-model transfer. Broad grids, additional toy families
and recursive diffusion retraining are not automatically authorized by this
historical outline. The full variable-load/importance boundary remains open."""
        )
        content = content.replace(
            "\\item Shumailov et al.",
            "\\item Scherlis et al. \\emph{Polysemanticity and Capacity in Neural Networks} (2022). \\url{https://arxiv.org/abs/2210.01892}. Its per-feature capacity, Equation (3), is exactly the squared geometric alignment used here; capacity allocation has prior analytic theory.\n\\item Shumailov et al."
        )
    SOURCE.write_text(content, encoding="utf-8")
    for source, name in [
        (ROOT / "project1_toy/frequency_boundary_2026-10-06/toy/run_v1/storage_transition.png", "project1_storage_transition.png"),
        (ROOT / "project1_toy/frequency_boundary_2026-10-06/report/actual_risk_difference.png", "project1_actual_risk_difference.png"),
    ]:
        shutil.copy2(source, HERE / "figures" / name)
    print(f"Integrated reviewed Project 1 derivations into {SOURCE}")


if __name__ == "__main__":
    main()
