"""Add the reviewed bias-calibration derivation to the existing volume."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
FRAGMENT = ROOT / 'project1_toy/paper_decision_2026-10-06/calibration_derivation.tex'
DESTINATION = ROOT / 'research_notes/project1_noise_update_20261006.tex'
START = '% BEGIN REVIEWED CALIBRATION CONTROL 2026-10-06'
END = '% END REVIEWED CALIBRATION CONTROL 2026-10-06'


def main():
    addition = FRAGMENT.read_text(encoding='utf-8')
    text = DESTINATION.read_text(encoding='utf-8')
    if START in text:
        before, remainder = text.split(START, 1)
        _, after = remainder.split(END, 1)
        text = before + START + '\n' + addition + '\n' + END + after
    else:
        anchor = '\\begin{figure}[p]'
        offset = text.index(anchor)
        text = text[:offset] + START + '\n' + addition + '\n' + END + '\n\n' + text[offset:]
    DESTINATION.write_text(text, encoding='utf-8')
    shutil.copy2(ROOT / 'project1_toy/paper_decision_2026-10-06/calibration_control.png',
                 ROOT / 'research_notes/figures/project1_calibration_mse.png')
    print('Updated existing Project 1 noise chapter and copied its control plot.')


if __name__ == '__main__':
    main()
