"""Deliver the completed frequency calculation and its existing dependencies.

No scientific calculation is rerun. Frozen run manifests are verified before
packaging, and every delivered byte is checked against a SHA-256 manifest.
Existing delivery archives are never overwritten.
"""
from pathlib import Path
import hashlib
import json
import zipfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = HERE.parent / "focused_bridge_2026-10-06"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    frozen_checks = {}
    for directory in [
        HERE / "toy" / "run_v1",
        PRIOR / "toy" / "run_v1",
        PRIOR / "toy" / "run_angle_diagnostic_v1",
    ]:
        saved = json.loads((directory / "sha256_manifest.json").read_text(encoding="utf-8"))
        for name, expected in saved.items():
            if digest(directory / name) != expected:
                raise AssertionError(f"Frozen archive mismatch: {directory / name}")
        frozen_checks[directory.relative_to(ROOT).as_posix()] = len(saved)

    target = ROOT / "output" / "Project1_Frequency_Transition_Code_and_Results_2026-10-06.zip"
    sidecar = target.with_suffix(".sha256.json")
    if target.exists() or sidecar.exists():
        raise FileExistsError("Refusing to overwrite an existing delivery artifact")
    target.parent.mkdir(parents=True, exist_ok=True)
    files = [
        p for base in [HERE, PRIOR] for p in base.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    ]
    files += [ROOT / "AGENTS.md", ROOT / "project1_toy" / "plan.md"]
    files += [
        ROOT / "project1_toy" / "literature_review" / name
        for name in ["novelty_audit.md", "search_ledger.md", "source_index.md"]
    ]
    files = sorted(set(files))
    manifest = {p.relative_to(ROOT).as_posix(): digest(p) for p in files}
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            archive.write(p, p.relative_to(ROOT).as_posix())
        archive.writestr("DELIVERY_MANIFEST.json", json.dumps(manifest, indent=2))
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise AssertionError("ZIP integrity check failed")
        if json.loads(archive.read("DELIVERY_MANIFEST.json")) != manifest:
            raise AssertionError("Delivered manifest differs from source manifest")
        for name, expected in manifest.items():
            if hashlib.sha256(archive.read(name)).hexdigest() != expected:
                raise AssertionError(f"Delivered file hash mismatch: {name}")
    summary = {
        "archive": str(target),
        "archive_sha256": digest(target),
        "file_count_excluding_manifest": len(manifest),
        "bytes": target.stat().st_size,
        "frozen_manifest_files_verified": frozen_checks,
        "all_delivered_files_verified": True,
        "files_sha256": manifest,
        "scope": (
            "Frequency-transition proof, fixed noisy-risk calculation, raw records, "
            "independent reviews and preserved failures; previous focused bridge "
            "included because the verifier imports its reviewed backend. Living plan "
            "and literature audit/index included; archived literature PDFs remain "
            "in the workspace. No new training or real-model experiment."
        ),
    }
    sidecar.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "files_sha256"}, indent=2))


if __name__ == "__main__":
    main()
