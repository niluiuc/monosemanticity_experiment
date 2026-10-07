"""Predeclared implementation check for continuous targets, not real transfer."""
from pathlib import Path
import argparse, hashlib, json, shutil, time
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
import vision_transfer as implementation

HOME=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=False)
    for p in [Path(__file__),HOME/'vision_transfer.py',HOME/'vision_transfer_protocol.md']:
        shutil.copy2(p,out/p.name)
    offset=np.array([-.6,.2,1.1]);y=np.array([0.,.7,1.5]);sd=.15
    implementation.write(out/'settings.json',dict(offset=offset,target=y,sd=sd,
         numerical_scope='One fixed implementation-adaptation case; no image outcomes.',
         calibration_tolerance=1e-8,independent_grid=4097,gradient_step=1e-6))
    profile=implementation.clean_profile(offset,y,True)
    assert abs(profile['beta']-.45)<1e-14 and abs(profile['loss']-1/600)<1e-14
    implementation.write(out/'clean_profile.json',profile)
    checks=[]
    for beta in [.3,.45,.6]:
        numerical=[];errors=[]
        for o,target in zip(offset,y):
            mu=o+beta;boundary=-mu/sd
            inactive=target**2*float(implementation.ndtr(boundary))
            active,error=quad(lambda z:(mu+sd*z-target)**2*np.exp(-z*z/2)/np.sqrt(2*np.pi),
                              boundary,np.inf,epsabs=1e-12,epsrel=1e-12,limit=200)
            numerical.append(inactive+active);errors.append(error)
        f,g=implementation.noisy_objective(beta,offset,y,sd)
        finite=(implementation.noisy_objective(beta+1e-6,offset,y,sd)[0]-
                implementation.noisy_objective(beta-1e-6,offset,y,sd)[0])/2e-6
        difference=abs(f-np.mean(numerical));gradient_error=abs(g-finite)
        assert difference<1e-11 and gradient_error<1e-8
        checks.append(dict(beta=beta,formula=f,quadrature_mean=np.mean(numerical),
                           absolute_difference=difference,quadrature_errors=errors,
                           derivative=g,finite_difference=finite,gradient_error=gradient_error))
    ledger=implementation.calibrate(offset,y,sd,profile['beta'],1e-8,time.monotonic()+60)
    implementation.write(out/'calibration_ledger.json',ledger)
    assert ledger['resolved']
    grid=np.linspace(ledger['left_endpoint'],ledger['right_endpoint'],4097)
    values=np.array([implementation.noisy_objective(b,offset,y,sd)[0] for b in grid]);j=int(np.argmin(values))
    independent=minimize_scalar(lambda b:implementation.noisy_objective(b,offset,y,sd)[0],
         bounds=(grid[max(0,j-1)],grid[min(len(grid)-1,j+1)]),method='bounded',options={'xatol':1e-12})
    assert independent.success and ledger['lower']-1e-11<=independent.fun<=ledger['upper']+1e-11
    np.savez_compressed(out/'independent_grid.npz',bias=grid,loss=values)
    results=dict(passed=True,clean_beta=profile['beta'],clean_loss=profile['loss'],
       gaussian_checks=checks,calibration_gap=ledger['gap'],independent_minimum=independent.fun,
       independent_beta=independent.x,
       limitations='Numerical adaptation agreement; not directed-rounding proof or a real vision result.')
    implementation.write(out/'results.json',results)
    implementation.write(out/'sha256_manifest.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                                    for p in out.iterdir() if p.is_file()})
    print(json.dumps(implementation.plain(results),indent=2))

if __name__=='__main__':main()
