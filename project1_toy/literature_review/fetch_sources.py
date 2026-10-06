"""Retrieve primary sources for a read-only novelty audit, preserving provenance."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request
import pymupdf
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ('elhang2022', '2209.10652'),
    ('scherlis2022', '2210.01892'),
    ('jermyn2022', '2211.09169'),
    ('lecomte2023', '2312.03096'),
    ('hanni2024', '2408.05451'),
    ('zhang2024', '2410.21331'),
    ('liu2025', '2505.10465'),
    ('gorton2025', '2508.17456'),
    ('bereska2025', '2512.13568'),
    ('elimadi2026', '2608.22155'),
    ('benhaim2009', '0903.4579'),
    ('sparc2014', '1403.8024'),
]


def get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (research literature audit)'})
    with urllib.request.urlopen(request, timeout=50) as response:
        return response.read(), response.geturl()


def fetch(item):
    key, arxiv = item
    directory = ROOT / 'sources' / key
    directory.mkdir(parents=True, exist_ok=True)
    record = {'key': key, 'arxiv_id': arxiv,
              'accessed_utc': datetime.now(timezone.utc).isoformat()}
    errors = []
    try:
        data, url = get('https://arxiv.org/abs/' + arxiv)
        (directory / 'abstract.html').write_bytes(data)
        soup = BeautifulSoup(data, 'html.parser')
        metadata = {tag.get('name'): tag.get('content') for tag in soup.find_all('meta') if tag.get('name')}
        record['metadata'] = {k: v for k, v in metadata.items() if k.startswith('citation_')}
        history = soup.select_one('.submission-history')
        record['submission_history'] = history.get_text(' ', strip=True) if history else None
        record['abstract_url'] = url
        pdf_url = metadata.get('citation_pdf_url', 'https://arxiv.org/pdf/' + arxiv)
    except Exception as error:
        errors.append('abstract: ' + repr(error))
        pdf_url = 'https://arxiv.org/pdf/' + arxiv
    try:
        data, url = get(pdf_url)
        if not data.startswith(b'%PDF'):
            raise ValueError('Response is not PDF')
        (directory / 'paper.pdf').write_bytes(data)
        doc = pymupdf.open(stream=data, filetype='pdf')
        pages = []
        for i, page in enumerate(doc):
            pages.append(f'\n\n===== PDF PAGE {i + 1} =====\n' + page.get_text())
        (directory / 'paper.txt').write_text(''.join(pages), encoding='utf-8')
        record.update(pdf_url=url, pages=len(doc), pdf_bytes=len(data),
                      pdf_sha256=hashlib.sha256(data).hexdigest())
    except Exception as error:
        errors.append('pdf: ' + repr(error))
    record['errors'] = errors
    (directory / 'provenance.json').write_text(json.dumps(record, indent=2) + '\n')
    return record


if __name__ == '__main__':
    records = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(fetch, item) for item in SOURCES]
        for future in as_completed(futures):
            record = future.result()
            records.append(record)
            print(record['key'], record.get('metadata', {}).get('citation_title'),
                  'pages', record.get('pages'), 'errors', record['errors'], flush=True)
    (ROOT / 'source_inventory.json').write_text(json.dumps(sorted(records, key=lambda r: r['key']), indent=2) + '\n')
