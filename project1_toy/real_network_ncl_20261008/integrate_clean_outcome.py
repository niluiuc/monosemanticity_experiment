from pathlib import Path
import shutil
base=Path(__file__).parent; root=base.resolve().parents[1]
source=root/'research_notes/volume2.tex'
shutil.copy2(base/'outputs/figures/clean_gates.png',root/'research_notes/figures/native_clean_gates_20261008.png')
text=source.read_text(encoding='utf-8'); start='% BEGIN NATIVE CLEAN PREREQUISITES'; end='% END NATIVE CLEAN PREREQUISITES'
section=start+'\n'+(base/'clean_outcome.tex').read_text(encoding='utf-8')+'\n'+end+'\n\n'
if start in text:
    a=text.index(start); b=text.index(end,a)+len(end); text=text[:a]+section.rstrip()+text[b:]
else:
    a=text.index('\\chapter{Project 2'); text=text[:a]+section+text[a:]
source.write_text(text,encoding='utf-8'); print('Integrated failed clean prerequisites with evidence and limitations.')
