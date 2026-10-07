"""Bounded metadata-only check. No feature fitting or risk/pair selection."""
from pathlib import Path
import csv, hashlib, io, json, tarfile, time, urllib.request
import pymupdf as fitz

ROOT = Path(__file__).resolve().parent
CACHE = Path.home() / '.cache' / 'monosemanticity_semantic_resource_20261006'
COMMIT = '39dff5bd6dea67fc3ef350bc7b2312e5fcfc1493'
BASE = f'https://raw.githubusercontent.com/ExplainableML/sae-for-vlm/{COMMIT}/'
PAPER = 'https://proceedings.neurips.cc/paper_files/paper/2025/file/89e83382abeee53b932a6df62edbf9cc-Paper-Conference.pdf'

def get(url, name, cap):
    dest = CACHE / name
    if not dest.exists():
        data = bytearray()
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'research-resource-audit'}), timeout=40) as r:
            while block := r.read(1024 * 1024):
                data.extend(block)
                if len(data) > cap:
                    raise RuntimeError('Download cap exceeded')
        dest.write_bytes(data)
    data = dest.read_bytes()
    if len(data) > cap:
        raise RuntimeError('Cached download cap exceeded')
    return dest, {'url':url, 'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()}

def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    out = ROOT / 'resource_gate_v1'
    out.mkdir(exist_ok=True)
    start=time.monotonic()
    archive, archive_meta=get(BASE+'metric_benchmark.tar.gz','metric_benchmark.tar.gz',30_000_000)
    rows=[]
    with tarfile.open(archive,'r:gz') as tf:
        members=tf.getmembers()
        if sum(m.size for m in members)>250_000_000:
            raise RuntimeError('Decompressed cap exceeded')
        for m in members:
            path=Path(m.name)
            if path.is_absolute() or '..' in path.parts or m.issym() or m.islnk():
                raise RuntimeError('Unsafe archive member')
            item={'name':m.name,'bytes':m.size}
            if path.name.startswith('._'):
                item['ignored_reason']='MacOS AppleDouble metadata, not a CSV'
            elif m.isfile() and m.name.endswith('.csv'):
                stream=io.TextIOWrapper(tf.extractfile(m),encoding='utf-8')
                reader=csv.reader(stream)
                header=next(reader)
                item.update(column_count=len(header),first_columns=header[:20])
                # Only top-image and preference metadata. Do not read activation outcomes.
                if 'top16' in m.name:
                    item['first_top_image_row']=next(reader)
                elif 'pairs' in m.name:
                    item['first_pair_metadata']=next(reader)[:3]
                stream.close()
            rows.append(item)
    source_meta={}
    for name in ['README.md','save_activations.py','find_hai_indices.py','visualize_neurons.py']:
        dest,meta=get(BASE+name,name,200_000)
        source_meta[name]=meta
        (out/name.replace('.py','_source.txt')).write_text(dest.read_text(encoding='utf-8'),encoding='utf-8')
    pdf,pdf_meta=get(PAPER,'pach_neurips2025.pdf',20_000_000)
    doc=fitz.open(pdf)
    relevant=[]
    for i,page in enumerate(doc):
        text=page.get_text()
        if 'Benchmark' in text or 'benchmark' in text and ('participant' in text or 'annotation' in text):
            relevant.append({'page':i+1,'text':text})
    # Full primary text stays in external cache; only metadata retained in project.
    (CACHE/'paper.txt').write_text('\n'.join(p.get_text() for p in doc),encoding='utf-8')
    report={'commit':COMMIT,'archive':archive_meta,'members':rows,'sources':source_meta,'paper':pdf_meta,'relevant_pages':[p['page'] for p in relevant],'elapsed_seconds':time.monotonic()-start,'risk_evaluated':False}
    (out/'resource_metadata.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    for p in relevant:
        if p['page']>=15:
            print('PAPER PAGE',p['page'],p['text'][:18000])

if __name__=='__main__':
    main()
