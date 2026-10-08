"""Append the reviewed controlled-image coupling proof and unchanged run outcome."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'research_notes/volume2.tex'
REVIEW = ROOT / 'project1_toy/professor_bridge_review_20261007'
RUN = ROOT / 'project1_toy/controlled_image_phase_20261007'
BEGIN = '% BEGIN CONTROLLED VISION COUPLING'
END = '% END CONTROLLED VISION COUPLING'


def main():
    text = SOURCE.read_text(encoding='utf-8')
    proof = (REVIEW / 'controlled_vision_coupling.tex').read_text(encoding='utf-8')
    outcome_path = RUN / 'outcome_section.tex'
    outcome = outcome_path.read_text(encoding='utf-8') if outcome_path.exists() else ''
    section = BEGIN + '\n' + proof + '\n' + outcome + '\n' + END + '\n\n'
    if BEGIN in text:
        start = text.index(BEGIN)
        finish = text.index(END, start) + len(END)
        text = text[:start] + section.rstrip() + text[finish:]
    else:
        anchor = '\\chapter{Project 2'
        start = text.index(anchor)
        text = text[:start] + section + text[start:]
    SOURCE.write_text(text, encoding='utf-8')
    print('Integrated controlled-image proof and available outcome in existing Volume II.')


if __name__ == '__main__':
    main()
