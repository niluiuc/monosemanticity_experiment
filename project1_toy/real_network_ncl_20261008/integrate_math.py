from pathlib import Path
root=Path(__file__).resolve().parents[2]
source=root/'research_notes/volume2.tex'
text=source.read_text(encoding='utf-8')
begin='% BEGIN NATIVE CLASSIFICATION PREDICTION'
end='% END NATIVE CLASSIFICATION PREDICTION'
section=begin+'\n'+(Path(__file__).parent/'classification_prediction.tex').read_text(encoding='utf-8')+'\n'+end+'\n\n'
if begin in text:
    a=text.index(begin); b=text.index(end,a)+len(end)
    text=text[:a]+section.rstrip()+text[b:]
else:
    a=text.index('\\chapter{Project 2')
    text=text[:a]+section+text[a:]
source.write_text(text,encoding='utf-8')
print('Integrated conditional classification derivation; no experiment results asserted.')
