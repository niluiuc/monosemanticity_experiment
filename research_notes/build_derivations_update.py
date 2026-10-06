"""Compile only Volume II, render all pages, and export a portable TeX project.

Uses the already installed pdflatex for this multi-file book with figures.
No TeX installation or research experiment is performed.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile

import pymupdf as fitz
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = ROOT / "tmp/pdfs/derivations_update_20261006"
OUTPUT = ROOT / "output/pdf/Superposition_Recursive_Training_Derivations.pdf"
PORTABLE = ROOT / "output/overleaf/research_derivations"


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    for iteration in range(3):
        completed = subprocess.run([
            "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
            "-output-directory=" + str(WORK), "volume2.tex"
        ], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (WORK / f"build_{iteration+1}.log").write_text(completed.stdout, encoding="utf-8")
        if completed.returncode:
            raise RuntimeError(completed.stdout[-6000:])
    warnings = [line for line in completed.stdout.splitlines()
                if "Overfull" in line or "undefined" in line or "multiply defined" in line]
    if warnings:
        raise RuntimeError("LaTeX layout/reference checks failed:\n" + "\n".join(warnings))
    pdf_path = WORK / "volume2.pdf"
    pdf = fitz.open(pdf_path)
    qa = WORK / "qa"
    qa.mkdir(exist_ok=True)
    texts = []
    thumbnails = []
    issues = []
    short_pages = []
    for number, page in enumerate(pdf, 1):
        page_text = page.get_text()
        texts.append(page_text)
        if len(page_text.strip()) < 350:
            short_pages.append(number)
        page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False).save(qa / f"page_{number:02}.png")
        thumbnail = Image.open(qa / f"page_{number:02}.png").convert("RGB")
        thumbnail.thumbnail((225, 318))
        tile = Image.new("RGB", (245, 345), "#eeeeee")
        tile.paste(thumbnail, ((245-thumbnail.width)//2, 22))
        ImageDraw.Draw(tile).text((8, 5), str(number), fill="black")
        thumbnails.append(tile)
        for block in page.get_text("blocks"):
            if block[0] < 25 or block[2] > page.rect.width-25:
                issues.append({"page": number, "box": list(block[:4]), "text": block[4][:100]})
    for start in range(0, len(thumbnails), 16):
        montage = Image.new("RGB", (980, 1380), "white")
        for offset, tile in enumerate(thumbnails[start:start+16]):
            montage.paste(tile, ((offset % 4)*245, (offset // 4)*345))
        montage.save(qa / f"contact_{start//16}.png")
    text = "\n\n".join(texts)
    (qa / "text.txt").write_text(text, encoding="utf-8")
    if issues:
        raise RuntimeError("Text boundary issues: " + str(issues))
    required = ["clean training selects", "two crossings", "Machin", "importance", "frequency"]
    if not all(term.lower() in text.lower() for term in required):
        raise AssertionError("Expected integrated content absent from compiled PDF")
    report = {
        "pages": len(pdf), "page_boundary_issues": issues,
        "short_pages_for_visual_review": short_pages,
        "latex_layout_or_reference_warnings": warnings,
        "source": str(HERE / "volume2.tex"), "pdf": str(OUTPUT),
        "compiled_pdf_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
        "visual_review_status": "pending",
    }
    pdf.close()
    (WORK / "qa_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    # Final PDF copied only after compilation and structural checks pass.
    shutil.copy2(pdf_path, OUTPUT)
    PORTABLE.mkdir(parents=True, exist_ok=True)
    source = (HERE / "volume2.tex").read_text(encoding="utf-8")
    preamble = (HERE / "preamble.tex").read_text(encoding="utf-8")
    portable_source = source.replace("\\input{preamble.tex}", preamble, 1)
    (PORTABLE / "main.tex").write_text(portable_source, encoding="utf-8")
    figures = PORTABLE / "figures"
    figures.mkdir(exist_ok=True)
    for path in (HERE / "figures").glob("*.png"):
        shutil.copy2(path, figures / path.name)
    readme = (
        "# Updated research derivations\n\n"
        "Upload main.tex and the figures/ folder to Overleaf; select main.tex "
        "as the main document and pdfLaTeX as the compiler. The preamble is "
        "included in main.tex, so no additional .tex inputs are needed. "
        "Run compilation twice to settle contents and references.\n\n"
        "The source continues the existing derivation volume. Project 1 additions "
        "contain full clean-selection and noise proofs; Project 2 remains "
        "background. Mathematical correctness, publication novelty and "
        "real-model transfer are distinct claims.\n"
    )
    (PORTABLE / "README.md").write_text(readme, encoding="utf-8")
    archive_path = ROOT / "output/overleaf/Superposition_Recursive_Training_Derivations_Source.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PORTABLE.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PORTABLE).as_posix())
    print(json.dumps(report, indent=2))
    print("Portable source project:", archive_path)


if __name__ == "__main__":
    main()
