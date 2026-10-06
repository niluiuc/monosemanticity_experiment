"""Independent numerical checks for the two teaching volumes.

Runs small CPU calculations, not a reproduction of the paper's trained models.
Every generated figure is original and every random experiment has a fixed seed.
"""
from pathlib import Path
import json
import itertools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import ndtr
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
FIG = ROOT / 'figures'
FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
 'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160,
 'axes.labelcolor':'#22344a','text.color':'#22344a'})
COL = ['#235789','#D17A22','#3D806A','#AC4568']
rng = np.random.default_rng(20260921)
results = {'seed':20260921,'description':'Independent analytical checks; no large-model training'}

def moments(s):
    """Conditional moments for paper's y=1{x1>x2}, including zero-zero tie."""
    mu_m=np.array([(1-s)**2/(3*(1+s*s)),(2+s)/(3*(1+s))])
    e2_m=np.array([(1-s)**2/(6*(1+s*s)),(3+s)/(6*(1+s))])
    mu_p=np.array([-(1-s)*(1+2*s)/(3*(1+s*s)),(1+2*s)/(3*(1+s))])
    e2_p=np.array([(1-s)*(1+3*s)/(6*(1+s*s)),(1+3*s)/(6*(1+s))])
    return mu_m,e2_m-mu_m**2,mu_p,e2_p-mu_p**2

def J(mu,v): return (mu[1]-mu[0])/np.sqrt(v[0]*v[1])

def noisy_moments(s,eta,mu,v):
    pi=np.array([(1+s*s)/2,(1-s*s)/2])
    T=np.array([[1-eta,eta],[eta,1-eta]])
    joint=T*pi[None,:]
    weights=joint/joint.sum(axis=1,keepdims=True)
    assert np.max(np.abs(weights.sum(axis=1)-1))<1e-12
    m=weights@mu
    var=weights@(v+mu**2)-m**2
    return m,var

s=.2
mm,vm,mp,vp=moments(s)
N=1500000
x=(rng.random((N,2))>=s)*rng.random((N,2))
y=(x[:,0]>x[:,1]).astype(int)
z=[x[:,0],x[:,0]-x[:,1]]
emp=[]
for v,mt,vt in zip(z,[mm,mp],[vm,vp]):
    me=np.array([v[y==c].mean() for c in [0,1]])
    ve=np.array([v[y==c].var() for c in [0,1]])
    assert np.max(np.abs(me-mt))<.002
    assert np.max(np.abs(ve-vt))<.002
    emp.append({'mean':me.tolist(),'variance':ve.tolist()})
etas=np.linspace(0,.499,300)
jm=[];jp=[]
for eta in etas:
    jm.append(J(*noisy_moments(s,eta,mm,vm)))
    jp.append(J(*noisy_moments(s,eta,mp,vp)))
root=brentq(lambda e:J(*noisy_moments(s,e,mm,vm))-J(*noisy_moments(s,e,mp,vp)),.001,.49)
noise_root=brentq(lambda sig:J(mm,vm+sig**2)-J(mp,vp+2*sig**2),.001,4)
results['paper_moments']={'S':s,'mono_mean':mm.tolist(),'mono_variance':vm.tolist(),
 'poly_mean':mp.tolist(),'poly_variance':vp.tolist(),'J_mono':J(mm,vm),'J_poly':J(mp,vp),
 'MC_N':N,'MC':emp,'corrected_label_J_crossing':root,'input_noise_J_crossing':noise_root,
 'J_at_eta_025':[J(*noisy_moments(s,.25,mm,vm)),J(*noisy_moments(s,.25,mp,vp))]}

fig,ax=plt.subplots(1,2,figsize=(9,3.3))
ax[0].plot(etas,jm,label='Mono',color=COL[0]);ax[0].plot(etas,jp,label='Poly',color=COL[1])
ax[0].axvline(root,ls=':',color='#777777',label=f'Crossing {root:.3f}')
ax[0].set(xlabel='Label flip probability',ylabel='Paper score J',title='Corrected mixture probabilities');ax[0].legend()
sig=np.linspace(0,1.5,300)
ax[1].plot(sig,[J(mm,vm+t*t) for t in sig],label='Mono',color=COL[0])
ax[1].plot(sig,[J(mp,vp+2*t*t) for t in sig],label='Poly',color=COL[1])
ax[1].axvline(noise_root,ls=':',color='#777777',label=f'Crossing {noise_root:.3f}')
ax[1].set(xlabel='Input noise standard deviation',ylabel='Paper score J',title='Independent Gaussian input noise');ax[1].legend()
fig.tight_layout();fig.savefig(FIG/'paper_J.png');plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(9,3.3))
for k in range(2):
    for c in [0,1]:
        ax[k].hist(z[k][y==c],bins=50,density=True,alpha=.5,color=COL[c],label=f'Class {c}')
    ax[k].set(xlabel='Representation value',ylabel='Histogram density',title=['Mono: x1','Poly: x1 - x2'][k]);ax[k].legend()
fig.tight_layout();fig.savefig(FIG/'conditional_distributions.png');plt.close(fig)

# Input-noise classification risk with an optimally chosen scalar threshold,
# estimated on independent validation data (not paper J).
train_x=(rng.random((200000,2))>=s)*rng.random((200000,2))
train_y=train_x[:,0]>train_x[:,1]
test_x=(rng.random((400000,2))>=s)*rng.random((400000,2))
test_y=test_x[:,0]>test_x[:,1]
noise_levels=[0,.1,.3,.6,1.0]
threshold_errors=[]
for noise in noise_levels:
    xx=train_x+noise*rng.normal(size=train_x.shape)
    tt=test_x+noise*rng.normal(size=test_x.shape)
    row={'sigma':noise}
    for label,a in [('mono',np.array([1.,0.])),('poly',np.array([1.,-1.]))]:
        h=xx@a;ht=tt@a
        thresholds=np.unique(np.r_[np.quantile(h,np.linspace(0,1,501)),0])
        errors=np.array([np.mean((h>t)!=train_y) for t in thresholds])
        best=thresholds[np.argmin(errors)]
        row[label]={'threshold':float(best),'test_error':float(np.mean((ht>best)!=test_y))}
    threshold_errors.append(row)
results['threshold_classification']=threshold_errors

# Exact Project 1 binary-feature model: same one-dimensional code noise.
def pair_risk(p1,p2,I1,I2,sigma,poly_amplitude=1.,mono_amplitude=1.):
    q=ndtr(-.5*poly_amplitude/sigma) if sigma>0 else 0.
    q3=ndtr(-1.5*poly_amplitude/sigma) if sigma>0 else 0.
    qm=ndtr(-.5*mono_amplitude/sigma) if sigma>0 else 0.
    P00=(1-p1)*(1-p2);P10=p1*(1-p2);P01=(1-p1)*p2;P11=p1*p2
    poly=(I1+I2)*P00*q+P10*(I1*q+I2*q3)+P01*(I1*q3+I2*q)+P11*(I1+I2)*(1-q)
    mono1=I1*qm+I2*p2
    mono2=I2*qm+I1*p1
    return np.array([poly,mono1,mono2])

phase_root=brentq(lambda t:pair_risk(.2,.2,1,1,t)[0]-pair_risk(.2,.2,1,1,t)[1],.05,3)
checks=[]
for p1,p2,i1,i2,noise in [(.2,.2,1,1,.3),(.1,.4,1,.3,.7),(.6,.3,1,2,1.)]:
    b=(rng.random((500000,2))<np.array([p1,p2])).astype(float)
    eta=noise*rng.normal(size=len(b))
    hp=b[:,0]-b[:,1]+eta
    pred=np.column_stack([hp>.5,hp<-.5])
    empirical=np.mean(np.sum((pred!=b)*[i1,i2],axis=1))
    theoretical=pair_risk(p1,p2,i1,i2,noise)[0]
    assert abs(empirical-theoretical)<.005
    checks.append([p1,p2,i1,i2,noise,float(theoretical),float(empirical)])
results['pair_phase']={'p_equal_02_sigma_crossing':phase_root,'checks':checks}
energy_root=brentq(lambda t:pair_risk(.2,.2,1,1,t,1/np.sqrt(2))[0]-pair_risk(.2,.2,1,1,t,1/np.sqrt(2))[1],.05,3)
results['pair_phase']['equal_energy_p02_sigma_crossing']=energy_root
ps=np.linspace(.01,.8,150);ns=np.linspace(.01,1.5,160)
delta=np.array([[pair_risk(p,p,1,1,t)[0]-pair_risk(p,p,1,1,t)[1] for p in ps] for t in ns])
fig,ax=plt.subplots(figsize=(6.8,4.2))
im=ax.pcolormesh(ps,ns,delta,cmap='RdBu_r',shading='auto',vmin=-.25,vmax=.25)
ax.contour(ps,ns,delta,levels=[0],colors='black',linewidths=1.5)
ax.set(xlabel='Activation probability p = 1 - s',ylabel='Code-noise standard deviation',title='Exact binary pair: risk(poly) - risk(mono)')
fig.colorbar(im,ax=ax,label='Negative: superposed pair has lower weighted error')
fig.tight_layout();fig.savefig(FIG/'pair_phase.png');plt.close(fig)

delta_energy=np.array([[pair_risk(p,p,1,1,t,1/np.sqrt(2))[0]-pair_risk(p,p,1,1,t,1/np.sqrt(2))[1] for p in ps] for t in ns])
fig,ax=plt.subplots(figsize=(6.8,4.2))
im=ax.pcolormesh(ps,ns,delta_energy,cmap='RdBu_r',shading='auto',vmin=-.25,vmax=.25)
ax.contour(ps,ns,delta_energy,levels=[0],colors='black',linewidths=1.5)
ax.set(xlabel='Activation probability p = 1 - s',ylabel='Code-noise standard deviation',title='Equal encoder energy: risk(poly) - risk(mono)')
fig.colorbar(im,ax=ax,label='Negative: superposed pair has lower weighted error')
fig.tight_layout();fig.savefig(FIG/'pair_phase_equal_energy.png');plt.close(fig)

# Pair's exact 4-state transition kernel. Column probabilities sum to one.
states=np.array(list(itertools.product([0,1],repeat=2)))
def pair_K(sig):
    K=np.zeros((4,4))
    for j,b in enumerate(states):
        d=b[0]-b[1]
        K[1,j]=ndtr((-.5-d)/sig) # 01
        K[2,j]=ndtr((d-.5)/sig)  # 10
        K[0,j]=1-K[1,j]-K[2,j]
    assert np.max(np.abs(K.sum(axis=0)-1))<1e-12
    return K
P0=np.prod(np.where(states==1,.2,.8),axis=1)
K=pair_K(.35)
histories=[]
for alpha in [0,.2]:
    P=P0.copy();hist=[P.copy()]
    for t in range(20):
        err=np.sum(K*(np.sum(np.abs(states[:,None,:]-states[None,:,:]),axis=2))*P[None,:])
        marg=P@states
        new=K@P
        assert np.max(np.abs(new@states-marg))<=err+1e-12
        P=alpha*P0+(1-alpha)*new
        hist.append(P.copy())
    histories.append(np.array(hist))
results['pair_kernel']={'states':states.tolist(),'K_sigma_035':K.tolist(),
 'P0':P0.tolist(),'history_alpha0':histories[0].tolist(),'history_alpha02':histories[1].tolist()}
fig,ax=plt.subplots(1,2,figsize=(9,3.3))
for k,H in enumerate(histories):
    for i in range(4): ax[k].plot(H[:,i],color=COL[i],label=''.join(map(str,states[i])))
    ax[k].set(xlabel='Generation',ylabel='Probability',title=['No real-data mixing','20% real-data mixing'][k]);ax[k].legend(ncol=2)
fig.tight_layout();fig.savefig(FIG/'pair_recursion.png');plt.close(fig)

# Linear identities and spectrum counterexample.
W=rng.normal(size=(3,6));G=W.T@W
C=rng.normal(size=(6,6));C=C@C.T
Ct=C.copy()
for t in range(5):
    assert np.allclose(Ct,np.linalg.matrix_power(G,t)@C@np.linalg.matrix_power(G,t))
    Ct=G@Ct@G
counter=[]
for c in [.5,1,2]:
    G=c*.5*np.ones((2,2));M=np.diag(G)/np.linalg.norm(G,axis=1)
    covariance=np.eye(2);tr=[]
    for _ in range(5):
        tr.append(float(np.trace(covariance)));covariance=G@covariance@G
    counter.append({'c':c,'M':M.tolist(),'eigenvalues':np.linalg.eigvalsh(G).tolist(),'trace':tr})
results['same_M_counterexample']=counter

# Gaussian denoising recursion: fitted denoiser vs posterior sampling.
c=1.;sig2=.2;seq=[c]
for _ in range(10): c=c*c/(c+sig2);seq.append(c)
results['gaussian_denoising']={'noise_variance':sig2,'mean_only_covariance':seq,
 'posterior_sampling_covariance':[1.]*11}
fig,ax=plt.subplots(figsize=(6.8,3.4))
ax.semilogy(seq,'o-',color=COL[0],label='Posterior mean used as generated data')
ax.semilogy(np.ones(11),'--',color=COL[1],label='Exact posterior sampling')
ax.set(xlabel='Retraining generation',ylabel='Variance',title='A precisely specified Gaussian training loop');ax.legend()
fig.tight_layout();fig.savefig(FIG/'gaussian_recursion.png');plt.close(fig)

# Geometry picture.
fig,ax=plt.subplots(1,2,figsize=(8,3.5))
for k,angles in enumerate([[0,np.pi/2],[0,2*np.pi/3,4*np.pi/3]]):
    for j,a in enumerate(angles):
        ax[k].arrow(0,0,np.cos(a),np.sin(a),width=.015,length_includes_head=True,color=COL[j])
        ax[k].text(1.15*np.cos(a),1.15*np.sin(a),f'feature {j+1}',ha='center',fontsize=9)
    ax[k].set(xlim=(-1.55,1.55),ylim=(-1.4,1.4),aspect='equal',title=['Two isolated feature directions','Three features in two dimensions'][k]);ax[k].axhline(0,c='#cccccc',lw=.6);ax[k].axvline(0,c='#cccccc',lw=.6)
fig.tight_layout();fig.savefig(FIG/'geometry.png');plt.close(fig)

# Verify capacity benchmark for an equal-norm tight frame.
angles=np.arange(3)*2*np.pi/3
W=np.array([np.cos(angles),np.sin(angles)]);F=W.T@W
v=.2;noisevar=.1;g=v/((v+noisevar)*1.5);Gs=g*F
risk=np.trace(v*(np.eye(3)-Gs)@(np.eye(3)-Gs).T+noisevar*Gs@Gs.T)
mono=3*v-2*v*v/(v+noisevar)
assert abs(risk-mono)<1e-12
results['linear_tight_frame_risk']={'distributed':risk,'mono':mono}

(ROOT/'verification_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in results.items() if k not in ['pair_kernel']},indent=2))
