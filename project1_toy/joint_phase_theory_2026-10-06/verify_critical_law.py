"""Prespecified high-precision population checks; no fitted laws or training."""
from pathlib import Path
import json
import argparse
import mpmath as mp

mp.mp.dps = 70
pc = (3-mp.sqrt(5))/2
qc = 1-pc
Dc = 1-pc+pc**2
K = mp.sqrt(5)/(6*pc*qc)
C = 5*mp.sqrt(5)/(216*Dc*pc*qc)
B = qc*(1-2*pc)/2
cross = mp.sqrt(C/B)
phi = lambda z: mp.exp(-z*z/2)/mp.sqrt(2*mp.pi)
Phi = lambda z: mp.erfc(-z/mp.sqrt(2))/2

def moments(mu, sd):
    if sd == 0:
        return max(mu,0), max(mu,0)**2
    z = mu/sd
    return sd*phi(z)+mu*Phi(z), (mu*mu+sd*sd)*Phi(z)+mu*sd*phi(z)

def difference(k,p):
    q=1-p; D=1-p+p*p
    c=k*k/(1+k*k); r=k/(1+k*k)
    return p*q*c/D*(p-D/2+(1-2*p)*c+2*p*q*r)

def risk(k,p,sigma,mono=False):
    q=1-p; D=1-p+p*p
    if mono:
        w=[mp.mpf(1),mp.mpf(0)]; beta=[mp.mpf(0),p]
    else:
        a=1/(1+k*k); c=1-a; r=k/(1+k*k)
        w=[mp.sqrt(a),-mp.sqrt(c)]
        beta=[p*(c+p*r)/D,p*(a+r)]
    result=mp.mpf(0)
    for x in [(0,0),(0,1),(1,0),(1,1)]:
        prob=mp.fprod([p if b else q for b in x])
        h=sum(wi*xi for wi,xi in zip(w,x))
        for i,weight in enumerate([mp.mpf(1),mp.mpf('.5')]):
            m1,m2=moments(w[i]*h+beta[i],sigma*abs(w[i]))
            result+=prob*weight*(m2-2*x[i]*m1+x[i]**2)
    return result

rows=[]
for raw in ['.02','.01','.005','.0025']:
    eps=mp.mpf(raw); p=pc-eps
    k=mp.findroot(lambda v: mp.diff(lambda u:difference(u,p),v)/v,
                  (K*eps*mp.mpf('.8'),K*eps*mp.mpf('1.2')))
    row={'epsilon':raw,'k':str(k),'k_over_epsilon':str(k/eps),
         'clean_gain_over_epsilon_cubed':str(-difference(k,p)/eps**3),'checks':[]}
    for scale,t in [('critical',cross/2),('critical',2*cross),('gate',mp.mpf('.05')),('gate',mp.mpf('10'))]:
        sigma=t*eps**mp.mpf('1.5') if scale=='critical' else k*t
        delta=risk(k,p,sigma)-risk(k,p,sigma,True)
        row['checks'].append({'scale':scale,'multiplier':str(t),'sigma':str(sigma),'delta':str(delta)})
    rows.append(row)
z=mp.findroot(lambda z:pc*z+qc*(z*Phi(z)+phi(z)),-.4)
v=pc*(1+z*z)+qc*moments(z,mp.mpf(1))[1]
output={'precision_digits':mp.mp.dps,'pc':str(pc),'K':str(K),'C':str(C),'B_frozen':str(B),
        'crossing_coefficient_frozen':str(cross),'mono_calibration_z':str(z),
        'B_calibrated':str(Dc-v),'crossing_coefficient_calibrated':str(mp.sqrt(C/(Dc-v))),
        'rows':rows,'scope':'Local stationarity and exact frozen population risk; no global numerical certificate or calibrated toy run.'}
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('verification_results.json'))
path=parser.parse_args().output
if path.exists():
    raise RuntimeError('Preserve prior output: choose a fresh output name before reproducing.')
path.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
for row in rows:
    print(row['epsilon'], 'k/eps=',float(row['k_over_epsilon']),
          'gain/eps^3=',float(row['clean_gain_over_epsilon_cubed']),
          'signs=',[mp.sign(mp.mpf(c['delta'])) for c in row['checks']])
print('Constants',float(K),float(C),float(cross),float(mp.sqrt(C/(Dc-v))))
