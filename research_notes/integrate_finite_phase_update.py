"""Continue Project1 in the existing volume; preserve prior PDF/source."""
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
archive=ROOT/'tmp/pdfs/frozen_boundary_before_20261006';archive.mkdir(parents=True,exist_ok=True)
for path in [HERE/'volume2.tex',ROOT/'output/pdf/Superposition_Recursive_Training_Derivations.pdf']:
    if not (archive/path.name).exists():shutil.copy2(path,archive/path.name)
begin='% BEGIN FINITE JOINT PHASE UPDATE 2026-10-06';end='% END FINITE JOINT PHASE UPDATE 2026-10-06'
paths=[ROOT/'project1_toy/joint_phase_theory_2026-10-06/global_strip_certificate.tex',
       HERE/'project1_finite_validation_20261006.tex']
extra=HERE/'project1_calibrated_finite_results_20261006.tex'
if extra.exists():paths.append(extra)
paths.append(HERE/'project1_broader_clean_findings_20261006.tex')
paths.append(ROOT/'project1_toy/broader_toy_20261006/repair_derivation.tex')
for extra in [ROOT/'project1_toy/joint_phase_theory_2026-10-06/importance_interval_derivation.tex',
              HERE/'project1_importance_validation_20261006.tex',
              ROOT/'project1_toy/joint_phase_theory_2026-10-06/endpoint_calibration_derivation.tex',
              HERE/'project1_endpoint_validation_20261006.tex',
              ROOT/'project1_toy/joint_phase_theory_2026-10-06/vision_calibration_derivation.tex',
              HERE/'project1_vision_results_20261006.tex']:
    if extra.exists():paths.append(extra)
block=begin+'\n'+'\n'.join(p.read_text(encoding='utf-8') for p in paths)+'\n'+end+'\n'
p=HERE/'project1_noise_update_20261006.tex';text=p.read_text(encoding='utf-8')
if begin in text:
    before,remainder=text.split(begin,1);_,after=remainder.split(end,1);text=before+block+after
else:text+='\n'+block
p.write_text(text,encoding='utf-8')
for name in ['frozen_phase_map.png','frozen_boundary_scaling.png','calibrated_boundary_scaling.png','importance_policy_phase.png','endpoint_policy_contrast.png']:
    source=ROOT/'project1_toy/joint_phase_theory_2026-10-06'/name
    if source.exists():shutil.copy2(source,HERE/'figures'/('project1_'+name))
print('Integrated exact strip certificate and finite phase validation.')
vision=ROOT/'project1_toy/vision_transfer_20261006/plots_v2'
for source_name,target_name in [('vision_policy_risk.png','project1_vision_policy_transfer.png'),
                               ('vision_policy_contrast.png','project1_vision_policy_contrast.png')]:
    source=vision/source_name
    if source.exists():shutil.copy2(source,HERE/'figures'/target_name)
