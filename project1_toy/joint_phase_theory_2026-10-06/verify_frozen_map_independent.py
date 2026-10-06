"""Direct quadrature check; does not import the map's Gaussian moment code."""
import argparse,csv, hashlib, json, math
from pathlib import Path
from scipy.integrate import quad

HERE=Path(__file__).resolve().parent
FOLDER=HERE/'frozen_run_v1'
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=HERE/'frozen_independent_review_v1')
out=parser.parse_args().output
out.mkdir(parents=True,exist_ok=False)
manifest=json.loads((FOLDER/'sha256_manifest.json').read_text())
for rel,digest in manifest.items():
    assert hashlib.sha256((FOLDER/rel).read_bytes()).hexdigest()==digest,rel
saved=json.loads((FOLDER/'results.json').read_text())
with (FOLDER/'population_map.csv').open() as f: rows=list(csv.DictReader(f))
# Three fixed map points, prescribed by case/grid indices; no outcome selection.
chosen=[(0,60),(2,40),(5,20)]
checks=[]
for case_index,grid_index in chosen:
    case=saved['cases'][case_index];p=float(case['p']);row=rows[case_index*122+grid_index]
    sigma=float(row['sigma'])
    for name,w,beta in [('sharing',[float(v) for v in case['weights']],[float(v) for v in case['bias']]),
                        ('mono',[1.,0.],[0.,p])]:
        total=0.;bound=0.;quad_error=0.
        tail=math.erfc(12/math.sqrt(2));density=math.exp(-72)/math.sqrt(2*math.pi)
        second_tail=24*density+tail
        for x in [(0,0),(0,1),(1,0),(1,1)]:
            P=math.prod(p if b else 1-p for b in x);h=sum(wi*xi for wi,xi in zip(w,x))
            for i,I in enumerate([1.,.5]):
                mu=w[i]*h+beta[i];sd=sigma*abs(w[i]);target=x[i]
                if sd==0:
                    value=(max(mu,0)-target)**2;err=0.
                else:
                    def integrand(z):
                        return (max(mu+sd*z,0)-target)**2*math.exp(-z*z/2)/math.sqrt(2*math.pi)
                    gate=-mu/sd;points=[gate] if -12<gate<12 else None
                    value,err=quad(integrand,-12,12,points=points,epsabs=1e-14,epsrel=1e-12,limit=100)
                    bound+=P*I*(2*(abs(mu)+target)**2*tail+2*sd*sd*second_tail)
                total+=P*I*value;quad_error+=P*I*err
        delta=abs(total-float(row[name]))
        checks.append(dict(epsilon=case['epsilon'],grid_index=grid_index,sigma=sigma,model=name,
                           saved_risk=float(row[name]),quadrature_risk=total,absolute_difference=delta,
                           omitted_tail_bound=bound,quadrature_reported_error=quad_error,
                           passed=delta<1e-12))
assert all(c['passed'] for c in checks)
report=dict(hash_checks=len(manifest),checks=checks,max_difference=max(c['absolute_difference'] for c in checks),
            scope='Independent implementation of direct Gaussian integral, not interval-arithmetic proof or root completeness.')
(out/'results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
