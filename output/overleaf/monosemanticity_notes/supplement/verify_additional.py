"""Additional independent checks of the generalized risk and error bound."""
from pathlib import Path
import itertools, json
import numpy as np
from scipy.special import ndtr
import sympy as sy

root=Path(__file__).resolve().parent
rng=np.random.default_rng(20260922)
states=np.array(list(itertools.product([0.,1.],repeat=5)))
records=[]
for trial in range(8):
    W=rng.normal(size=(3,5))
    W=W/np.linalg.norm(W,axis=0)
    G=W.T@W
    p=rng.uniform(.03,.7,size=5)
    sigma=float(rng.uniform(.05,.5))
    diagonal=np.diag(G)
    off=G-np.diag(diagonal)
    theta=off@p+diagonal/2
    P=np.prod(np.where(states==1,p,1-p),axis=1)
    errors=ndtr(-(2*states-1)*(states@G.T-theta)/(sigma*np.sqrt(diagonal)))
    exact=P@errors
    V=(off**2)@(p*(1-p)); B=np.max(np.abs(off),axis=1)
    bound=np.exp(-diagonal**2/(8*(V+sigma*sigma*diagonal+B*diagonal/6)))
    assert np.all(exact <= bound+1e-12)
    samples=(rng.random((150000,5))<p).astype(float)
    h=samples@W.T+sigma*rng.normal(size=(len(samples),3))
    measured=((h@W>theta)!=samples).mean(axis=0)
    assert np.max(np.abs(exact-measured))<.005
    records.append({'exact':exact.tolist(),'empirical':measured.tolist(),'bound':bound.tolist()})

# Equal-encoder-energy pair, independently implemented conditional risk.
p=.2;a=1/np.sqrt(2);sigma=.3
q=ndtr(-a/(2*sigma));q3=ndtr(-3*a/(2*sigma))
expected=2*(1-p)**2*q+2*p*(1-p)*(q+q3)+2*p*p*(1-q)
b=(rng.random((500000,2))<p).astype(float)
h=a*(b[:,0]-b[:,1])+sigma*rng.normal(size=len(b))
estimate=np.mean(np.sum(np.column_stack([h>a/2,h<-a/2])!=b,axis=1))
assert abs(estimate-expected)<.005

# Exact symbolic sign-factor identity for the source paper's relative J loss.
S=sy.Rational(1,5);e=sy.symbols('e',real=True)
pi=sy.Matrix([(1+S*S)/2,(1-S*S)/2])
mu_m=sy.Matrix([(1-S)**2/(3*(1+S*S)),(2+S)/(3*(1+S))])
mu_p=sy.Matrix([-(1-S)*(1+2*S)/(3*(1+S*S)),(1+2*S)/(3*(1+S))])
e2_m=sy.Matrix([(1-S)**2/(6*(1+S*S)),(3+S)/(6*(1+S))])
e2_p=sy.Matrix([(1-S)*(1+3*S)/(6*(1+S*S)),(1+3*S)/(6*(1+S))])
weights=sy.Matrix([[(1-e)*pi[0],e*pi[1]],[e*pi[0],(1-e)*pi[1]]])
weights=sy.diag(*[1/sum(weights[i,:]) for i in range(2)])*weights
ratios=[]
for mu,e2 in [(mu_m,e2_m),(mu_p,e2_p)]:
    v=e2-mu.applyfunc(lambda z:z*z)
    vt=weights*e2-(weights*mu).applyfunc(lambda z:z*z)
    ratios.append(vt[0]*vt[1]/(v[0]*v[1]))
claimed=292032*e*(1-e)*(13156+65501*e*(1-e))/(15341*(13-e)**2*(12+e)**2)
assert sy.simplify(ratios[1]-ratios[0]-claimed)==0

out={'seed':20260922,'general_risk_trials':records,
     'equal_energy_pair':{'exact':float(expected),'MC':float(estimate),'N':500000},
     'relative_degradation_factorization':'symbolic identity verified'}
(root/'additional_verification.json').write_text(json.dumps(out,indent=2))
print('All additional checks passed. Equal-energy pair:',out['equal_energy_pair'])
