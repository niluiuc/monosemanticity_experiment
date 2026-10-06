"""Package the working record and immutable run artifacts, excluding bytecode caches."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile


def package(destination):
    root = Path(__file__).resolve().parent
    destination = Path(destination).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError('Refusing to replace an existing experiment package')
    files = [p for p in sorted(root.rglob('*')) if p.is_file()
             and not any(part in ('__pycache__', '.venv') for part in p.relative_to(root).parts)
             and p.suffix != '.pyc']
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=5) as archive:
        for path in files:
            archive.write(path, Path('project1_toy') / path.relative_to(root))
    checked = 0
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise AssertionError('ZIP integrity failure')
        for manifest in root.rglob('manifest.json'):
            entries = json.loads(manifest.read_text())['files']
            for entry in entries:
                path = manifest.parent / entry['path']
                archived_path = (Path('project1_toy') / path.relative_to(root)).as_posix()
                data = archive.read(archived_path)
                if hashlib.sha256(data).hexdigest() != entry['sha256']:
                    raise AssertionError(f'Archived hash mismatch: {archived_path}')
                checked += 1
    audit = {'zip': str(destination), 'files': len(files), 'bytes': destination.stat().st_size,
             'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
             'manifest_entries_verified_in_zip': checked}
    destination.with_suffix('.sha256.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination')
    args = parser.parse_args()
    package(args.destination)
