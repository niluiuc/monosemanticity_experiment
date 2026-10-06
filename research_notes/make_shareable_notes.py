"""Restyle Volume I as an Overleaf-ready article, preserving its mathematics."""
from pathlib import Path
import re, shutil, subprocess, json, zipfile
import pymupdf as fitz
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'research_notes'/'volume1.tex'
DEST=ROOT/'output'/'overleaf'/'monosemanticity_notes'
SCRATCH=ROOT/'tmp'/'pdfs'/'shareable_notes'
PDF=ROOT/'output'/'pdf'/'Monosemanticity_Robustness_Research_Notes.pdf'
for d in [DEST, DEST/'figures', DEST/'supplement', SCRATCH]: d.mkdir(parents=True,exist_ok=True)
source=SOURCE.read_text(encoding='utf8')
intro=source.split(r'\begingroup\small',1)[1].split(r'\endgroup',1)[0]
body=source.split(r'\mainmatter',1)[1]

replacements={
 'This course assumes comfort':'These notes assume familiarity',
 'but does not assume prior':'but do not assume prior',
 'The intended reader wants to understand the paper well enough to derive its toy analysis, distinguish its claims from its evidence, and build a research contribution from it.':'The aim is to derive the toy analysis, distinguish the claims from the evidence, and identify possible research extensions.',
 'The course is organized as twelve lectures, suitable for six weeks at two lectures per week. That is a teaching schedule, not a requirement to postpone research for six weeks. A fast first pass through Lectures 1--4 and 7--10 gives the foundation for Volume II; return to the remaining derivations and exercises while experiments begin.':'The twelve sections can be read over six weeks, following the outline below. This reading schedule can run alongside experimental work. Sections 1--4 and 7--10 provide the main background for the companion research derivations; the remaining sections cover the experiments, checks and extensions.',
 'Three labels matter throughout.':'Three distinctions are used throughout.',
 'I read both complete PDFs, including their appendices.':'These notes cover both versions of the paper, including their appendices.',
 'Code and numerical records accompany the volumes.':'Code and numerical records are included in the accompanying source package.',
 'What the paper is actually asking':'Research question and motivation',
 'Why this is the right starting point for your project':'Connection to the proposed research',
 'Your first project asks':'The first proposed project asks',
 'Your second asks':'The second asks',
 'This separation preserves the research direction. It tells us what the existing paper supplies and what the new work must supply: a broader quantitative mechanism and a tested connection to recursive training.':'The existing paper supplies the motivation and initial evidence. The proposed extension requires a broader quantitative mechanism and a tested connection to recursive training.',
 'For your own study,':'For the proposed study,',
 'For your research, safety may be a later application.':'Safety may be a later application of this research.',
 'You do not need to build a safety benchmark or an agent system to pursue that question.':'The question does not require a safety benchmark or an agent system.',
 'A small correction, not a dismissal of the argument':'Normalization of the label-noise mixtures',
 'What the mathematical result does and does not prove':'Interpretation and limitations of the toy theory',
 'boundary your project proposes':'boundary proposed for the extension',
 'Volume II does exactly that for a small feature-detection model, while keeping the original project objectives.':'The companion research notes develop this approach for a small feature-detection model.',
 'What the conference version adds':'Additions in the conference version',
 'Reproduction lab and worked problems':'Reproduction procedures and worked examples',
 'Turn passive reading into calculations you can independently reproduce and defend.':'Reproduce and check the calculations and experimental protocols.',
 'Lab 1: verify the distribution':'Check 1: conditional distribution and moments',
 'Lab 2: verify corruption laws':'Check 2: corruption laws',
 'Lab 3: score versus actual error':'Check 3: separability score versus prediction error',
 'Lab 4: what a trained-model reproduction needs':'Requirements for a trained-model reproduction',
 'Synthesis and the bridge to your research':'Synthesis and research extensions',
 'State the paper\'s contribution accurately and carry its motivation into the agreed two-project program.':'Summarize the contribution and connect it to the two proposed research questions.',
 'The first project remains exactly the first project':'Extension I: the superposition-to-robustness phase diagram',
 'The second project remains exactly the second project':'Extension II: model collapse and monosemanticity',
 'Volume II develops this connection':'The companion research notes develop this connection',
 'Questions you should now be able to answer':'Questions for discussion',
 "The paper's main story is taught in Lectures 1--6.":"The paper's main argument is covered in Sections 1--6.",
 'These teaching notes use':'These notes use',
 'this course':'these notes',
 'The course does not reproduce':'The notes do not reproduce',
 'next lecture':'next section',
 'Lectures':'Sections',
 'Lecture':'Section',
 r'\texttt{research\_notes/verify\_math.py}':r'\path{supplement/verify_math.py}',
 r'\texttt{verification\_results.json}':r'\path{supplement/verification_results.json}',
}
def rewrite(s):
    for old,new in replacements.items():s=s.replace(old,new)
    return s
intro=rewrite(intro)
body=rewrite(body)
# Remove the reading schedule and provenance passages requested for the shared edition.
intro=re.sub(r'The twelve sections can be read over six weeks,[\s\S]*?\\end\{center\}\s*','',intro,count=1)
intro=intro.replace('Code and numerical records are included in the accompanying source package. The derivations have been checked numerically; empirical publication novelty and large-model transfer remain separate questions.','')
body=re.sub(r'The arXiv paper is distributed under a Creative Commons Attribution license\.[\s\S]*?(?=\\end\{document\})','',body,count=1)
# Preserve the original chapter/section numbering as article sections/subsections.
body=body.replace(r'\section{',r'\subsection{').replace(r'\chapter{',r'\section{')

preamble=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage[margin=25mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{graphicx,booktabs,longtable,array}
\usepackage{enumitem,listings}
\usepackage[hidelinks,bookmarksnumbered=true]{hyperref}
\setlength{\parindent}{1.2em}
\setlength{\parskip}{3pt}
\setlength{\emergencystretch}{3em}
\setlist{itemsep=3pt,topsep=4pt}
\setcounter{tocdepth}{2}
\numberwithin{equation}{section}
\numberwithin{figure}{section}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}\newtheorem{definition}[theorem]{Definition}
\newcommand{\E}{\mathbb E}\newcommand{\Prb}{\mathbb P}
\newcommand{\R}{\mathbb R}\newcommand{\Var}{\operatorname{Var}}
\newcommand{\Cov}{\operatorname{Cov}}\newcommand{\tr}{\operatorname{tr}}
\newcommand{\ReLU}{\operatorname{ReLU}}\newcommand{\diag}{\operatorname{diag}}
\newcommand{\TV}{\operatorname{TV}}\newcommand{\rank}{\operatorname{rank}}
\newcommand{\ind}{\mathbf 1}\newcommand{\norm}[1]{\left\lVert#1\right\rVert}
\newcommand{\lesson}[1]{\par\noindent\textit{Focus: #1}\par}
\newcommand{\status}[1]{\par\noindent\textit{Result status: #1}\par}
\newcommand{\checkpoint}[1]{\par\smallskip\noindent\textit{Discussion question.} #1\par}
\newcommand{\fig}[3]{\begin{figure}[htbp]\centering\includegraphics[width=#2\textwidth]{figures/#1}\caption{#3}\end{figure}}
\newcommand{\source}[1]{\par\noindent{\small\textit{Paper reference: #1}}\par}
\lstset{basicstyle=\ttfamily\small,breaklines=true,frame=single,columns=fullflexible,keepspaces=true}
\title{Monosemanticity and Robustness\\[4pt]\large Reading Notes on Zhang et al. (ICLR 2025)}
\author{}
\date{September 2026}
\hypersetup{pdftitle={Monosemanticity and Robustness: Reading Notes},pdfsubject={Derivations, experiments and research extensions}}
\begin{document}
\maketitle
\begin{abstract}
These notes examine \emph{Beyond Interpretability: The Gains of Feature Monosemanticity on Model Robustness} by Qi Zhang, Yifei Wang, Jingyi Cui, Xiang Pan, Qi Lei, Stefanie Jegelka and Yisen Wang. They collect the relevant concepts, training objectives, experimental protocols, toy-model derivations and numerical checks, and distinguish the reported results from possible extensions to robustness and recursive training. Both arXiv:2410.21331v1 and the ICLR 2025 proceedings version are considered.
\end{abstract}
\section*{Scope}
'''
tex=preamble+intro+r'''
\begingroup\small\tableofcontents\endgroup
\clearpage
'''+body
(DEST/'main.tex').write_text(tex,encoding='utf8')

# Check preservation of every displayed and inline mathematical expression in the body.
def mathematics(s):
    return re.findall(r'\$[^$]*\$|\\begin\{(?:equation|align)\}[\s\S]*?\\end\{(?:equation|align)\}',s)
original_body=source.split(r'\mainmatter',1)[1]
assert mathematics(original_body)==mathematics(body), 'Mathematics changed during restyling'
for env in ['tabular','longtable','lstlisting']:
    pattern=r'\\begin\{'+env+r'\}[\s\S]*?\\end\{'+env+r'\}'
    assert [rewrite(s) for s in re.findall(pattern,original_body)]==re.findall(pattern,body), env+' changed'
figures=re.findall(r'\\fig\{([^}]+)\}',body)
for name in figures:shutil.copy2(ROOT/'research_notes'/'figures'/name,DEST/'figures'/name)
for name in ['verify_math.py','verification_results.json']:
    shutil.copy2(ROOT/'research_notes'/name,DEST/'supplement'/name)
(DEST/'README.md').write_text('''# Monosemanticity and Robustness: Reading Notes

Upload this ZIP as a new Overleaf project. Use **pdfLaTeX** and select **main.tex** as the main document. No custom fonts, external templates, shell escape or bibliography processor is needed.

Files:
- `main.tex`: complete editable document.
- `figures/`: the three figures included in the notes.
- `supplement/verify_math.py`: source of the numerical checks and figures.
- `supplement/verification_results.json`: saved results of those checks.

The document retains the technical content, equations, tables, examples, questions and references of the lecture-note version, with a conventional article layout and neutral research-note wording. The numerical checks are small simulations, not a reproduction of the paper's ResNet or Llama training.

To run the optional verification script locally, install NumPy, SciPy and Matplotlib, then run `python supplement/verify_math.py`. It writes generated figures to `supplement/figures/` and a results JSON beside the script. Compilation on Overleaf does not run Python; the required figures are already included.
''',encoding='utf8')

for i in range(3):
    r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(SCRATCH),'main.tex'],cwd=DEST,capture_output=True,text=True)
    (SCRATCH/'build.log').write_text(r.stdout,encoding='utf8')
    if r.returncode:raise RuntimeError(r.stdout[-4000:])
warnings=[l for l in r.stdout.splitlines() if 'Overfull' in l or 'undefined' in l]
if warnings:raise RuntimeError('\n'.join(warnings))
shutil.copy2(SCRATCH/'main.pdf',PDF)

d=fitz.open(PDF)
thumbs=[];bounds=[];short=[]
for i,p in enumerate(d):
    pix=p.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False)
    pix.save(SCRATCH/f'page_{i+1:02}.png')
    im=Image.open(SCRATCH/f'page_{i+1:02}.png').convert('RGB');im.thumbnail((190,269))
    tile=Image.new('RGB',(210,295),'#dddddd');tile.paste(im,((210-im.width)//2,18))
    ImageDraw.Draw(tile).text((7,3),str(i+1),fill='black');thumbs.append(tile)
    if len(p.get_text())<500:short.append(i+1)
    for b in p.get_text('blocks'):
        if b[0]<27 or b[2]>p.rect.width-25:bounds.append([i+1,b[:4]])
for start in range(0,len(thumbs),20):
    sheet=Image.new('RGB',(1050,1180),'white')
    for j,im in enumerate(thumbs[start:start+20]):sheet.paste(im,((j%5)*210,(j//5)*295))
    sheet.save(SCRATCH/f'contact_{start//20}.png')
(SCRATCH/'extracted.txt').write_text('\n'.join(p.get_text() for p in d),encoding='utf8')
assert not bounds,bounds
zip_path=ROOT/'output'/'overleaf'/'Monosemanticity_Robustness_Overleaf.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(DEST.rglob('*')):
        if f.is_file():z.write(f,f.relative_to(DEST))
report={'pages':len(d),'math_expressions_preserved':len(mathematics(body)),'figures_preserved':figures,'bounds_issues':bounds,'short_pages_to_review':short,'pdf':str(PDF),'tex':str(DEST/'main.tex'),'overleaf_zip':str(zip_path)}
(SCRATCH/'qa.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
