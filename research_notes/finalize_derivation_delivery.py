"""Check the portable TeX project and record completed delivery checks."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

import pymupdf as fitz

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "tmp/pdfs/derivations_update_20261006"
PORTABLE = ROOT / "output/overleaf/research_derivations"
PDF = ROOT / "output/pdf/Superposition_Recursive_Training_Derivations.pdf"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    check = WORK / "portable_check"
    check.mkdir(parents=True, exist_ok=True)
    for run in range(3):
        completed = subprocess.run([
            "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
            "-output-directory=" + str(check), "main.tex"
        ], cwd=PORTABLE, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (check / f"build_{run+1}.log").write_text(completed.stdout, encoding="utf-8")
        if completed.returncode:
            raise RuntimeError(completed.stdout[-5000:])
    warnings = [line for line in completed.stdout.splitlines()
                if "Overfull" in line or "undefined" in line or "multiply defined" in line]
    if warnings:
        raise AssertionError(warnings)
    with fitz.open(PDF) as original, fitz.open(check / "main.pdf") as portable:
        if len(original) != len(portable):
            raise AssertionError("Portable PDF page count differs")
        normalize = lambda text: " ".join(text.split())
        for number, (page, other) in enumerate(zip(original, portable), 1):
            if normalize(page.get_text()) != normalize(other.get_text()):
                raise AssertionError(f"Portable typeset page text differs at page {number}")
    archive_path = ROOT / "output/overleaf/Superposition_Recursive_Training_Derivations_Source.zip"
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise AssertionError("Portable ZIP integrity error")
        for name in archive.namelist():
            if hashlib.sha256(archive.read(name)).hexdigest() != digest(PORTABLE / name):
                raise AssertionError(f"Portable ZIP differs from source: {name}")
    report_path = WORK / "qa_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report.update({
        "visual_review_status": "passed",
        "visual_review_scope": "All-page contact sheets, full-size new mathematical pages, introduction and figures inspected; final figure reflow pages inspected separately.",
        "portable_compilation": "passed; normalized typeset text agrees page by page",
        "portable_zip_integrity_and_source_hashes": "passed",
        "math_teacher_review": str(ROOT / "project1_toy/frequency_boundary_2026-10-06/math/teacher_document_review.md"),
        "math_teacher_review_sha256": digest(ROOT / "project1_toy/frequency_boundary_2026-10-06/math/teacher_document_review.md"),
        "source_sha256": digest(ROOT / "research_notes/volume2.tex"),
        "portable_source_sha256": digest(PORTABLE / "main.tex"),
        "final_pdf_sha256": digest(PDF),
        "portable_zip_sha256": digest(archive_path),
        "new_scientific_experiments": {"frozen_population_rows": 732, "calibrated_endpoint_comparisons": 12, "original_larger_toy_seeds": 5, "bounded_repair_seeds": 5},
        "current_independent_repair_audit_sha256": digest(ROOT / "project1_toy/broader_toy_20261006/independent_repair_review_v2/results.json"),
        "current_calibration_audit_sha256": digest(ROOT / "project1_toy/joint_phase_theory_2026-10-06/calibrated_professor_check_results.json"),
        "calibration_math_review": str(ROOT / "project1_toy/paper_decision_2026-10-06/professor_calibration_review.md"),
        "calibration_math_review_sha256": digest(ROOT / "project1_toy/paper_decision_2026-10-06/professor_calibration_review.md"),
        "calibration_independent_verification_sha256": digest(ROOT / "project1_toy/paper_decision_2026-10-06/independent_review/results.json"),
    })
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (ROOT / "output/pdf/Superposition_Recursive_Training_Derivations.verification.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
