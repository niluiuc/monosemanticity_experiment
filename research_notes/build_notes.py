"""Build both PDF volumes with native, searchable LaTeX mathematics.

Requires pdflatex on PATH; uses PyMuPDF and Pillow for local QA renders.
Run verify_math.py and verify_additional.py before building after math edits.
"""
from pathlib import Path
import subprocess, shutil, json
import pymupdf as fitz
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parent
scratch=root.parent/'tmp'/'pdfs'
out=root.parent/'output'/'pdf'
qa=scratch/'qa'
for d in [scratch,out,qa]:d.mkdir(parents=True,exist_ok=True)
names={'volume1':'Monosemanticity_Robustness_Lecture_Course.pdf',
       'volume2':'Superposition_Recursive_Training_Derivations.pdf'}
report={}
for stem,name in names.items():
    for run in range(3):
        result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
            '-output-directory='+str(scratch),stem+'.tex'],cwd=root,capture_output=True,text=True)
        (scratch/(stem+'_build.log')).write_text(result.stdout,encoding='utf8')
        if result.returncode:raise RuntimeError(result.stdout[-4000:])
    bad=[l for l in result.stdout.splitlines() if 'Overfull' in l or 'undefined' in l]
    if bad:raise RuntimeError('\n'.join(bad))
    pdf=fitz.open(scratch/(stem+'.pdf'))
    thumbs=[];bounds=[];text=[];sparse=[]
    for i,page in enumerate(pdf):
        text.append(page.get_text())
        if len(text[-1])<550 and i>1:sparse.append(i+1)
        pix=page.get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False)
        pix.save(qa/f'{stem}_{i+1:02}.png')
        image=Image.open(qa/f'{stem}_{i+1:02}.png').convert('RGB')
        image.thumbnail((190,269))
        tile=Image.new('RGB',(210,295),'#dddddd')
        tile.paste(image,((210-image.width)//2,18))
        ImageDraw.Draw(tile).text((7,3),str(i+1),fill='black');thumbs.append(tile)
        for b in page.get_text('blocks'):
            if b[0]<28 or b[2]>page.rect.width-25:
                bounds.append({'page':i+1,'box':list(b[:4]),'text':b[4][:80]})
    for start in range(0,len(thumbs),20):
        sheet=Image.new('RGB',(1050,1180),'white')
        for j,tile in enumerate(thumbs[start:start+20]):sheet.paste(tile,((j%5)*210,(j//5)*295))
        sheet.save(qa/f'{stem}_contact_{start//20}.png')
    (qa/(stem+'_text.txt')).write_text('\n'.join(text),encoding='utf8')
    report[stem]={'pages':len(pdf),'bounds_issues':bounds,'short_pages_to_review':sparse,'output':name}
    if bounds:raise RuntimeError(str(bounds))
    pdf.close()
    shutil.copyfile(scratch/(stem+'.pdf'),out/name)
(qa/'qa_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
