"""Archive exact source revisions matching existing immutable evidence hashes."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
R=B/'clean_global_certificate_v1';S=R/'source_snapshot';S.mkdir(exist_ok=True)
old=(B/'certify_strip_roots.py').read_text()
old=old.replace('import argparse,hashlib,json','import hashlib,json')
start=old.index('    parser=argparse.ArgumentParser()');stop=old.index('    p,k=s.symbols',start)
old=old[:start]+"    out=HERE/'clean_global_certificate_v1';out.mkdir(exist_ok=False)\n"+old[stop:]
(S/'certify_strip_roots.py').write_bytes(old.encode('utf-8'))
tex=(B/'global_strip_certificate.tex').read_text()
(S/'global_strip_certificate.tex').write_bytes(tex.replace('\\frac38',chr(12)+'rac38').encode('utf-8'))
for name,digest in json.loads((R/'source_sha256.json').read_text()).items():
    assert hashlib.sha256((S/name).read_bytes()).hexdigest()==digest,name
(R/'source_revision_notes.md').write_text('The original run hashes match the exact source revisions now archived in source_snapshot/. After this run the script gained a fresh-output CLI argument and a TeX form-feed typo was repaired. Neither change alters the mathematics or raw result. clean_global_certificate_reproduced/ reruns the same six exact brackets with the final source. Original results and hashes are unchanged.\n')
R=B/'clean_global_certificate_reproduced';S=R/'source_snapshot';S.mkdir(exist_ok=True)
for name,digest in json.loads((R/'source_sha256.json').read_text()).items():
    source=B/name;assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
    (S/name).write_bytes(source.read_bytes())
print('Original and reproduced exact-certificate source hashes match archived revisions.')
