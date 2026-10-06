"""Package the completed focused experiment without altering raw run files."""
from pathlib import Path
import hashlib
import json
import zipfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    # Validate that the original scientific outputs still match their run hashes.
    for run in ['run_v1', 'run_angle_diagnostic_v1']:
        directory = HERE / 'toy' / run
        saved = json.loads((directory / 'sha256_manifest.json').read_text(encoding='utf-8'))
        for name, expected in saved.items():
            assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected, name
    target = ROOT / 'output' / 'Project1_Focused_Bridge_2026-10-06.zip'
    sidecar = target.with_suffix('.sha256.json')
    if target.exists() or sidecar.exists():
        raise FileExistsError('Refusing to overwrite an existing delivery artifact')
    target.parent.mkdir(parents=True, exist_ok=True)
    files = [p for p in HERE.rglob('*')
             if p.is_file() and '__pycache__' not in p.parts]
    files += [ROOT / 'project1_toy' / 'plan.md']
    files += [ROOT / 'project1_toy' / 'literature_review' / name
              for name in ['novelty_audit.md', 'search_ledger.md', 'source_index.md']]
    manifest = {p.relative_to(ROOT).as_posix():
                hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(set(files))}
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(set(files)):
            archive.write(p, p.relative_to(ROOT).as_posix())
        archive.writestr('DELIVERY_MANIFEST.json', json.dumps(manifest, indent=2))
    # Verify the bytes actually delivered, including the manifest contents.
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert json.loads(archive.read('DELIVERY_MANIFEST.json')) == manifest
        for name, expected in manifest.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected, name
    summary = {'archive': str(target),
               'archive_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
               'file_count_excluding_manifest': len(manifest),
               'bytes': target.stat().st_size,
               'files_sha256': manifest,
               'all_delivered_files_verified': True,
               'scope': 'Focused code/raw outputs/reviews and living plan; literature audit/index included, archived literature PDFs remain in the workspace.'}
    sidecar.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'files_sha256'}, indent=2))


if __name__ == '__main__':
    main()
