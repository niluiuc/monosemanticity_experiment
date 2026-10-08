# Independent audit script (does not import author modules). Loads only train, cal, P rows.
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
F="/sessions/gracious-eloquent-goodall/mnt/algoverse/project1_toy/head_transfer_20261007/extraction_run_v1/raw_logits.npy"
M=np.load(F,mmap_mode='r')
pool=np.arange(1024,4608); perm=np.random.default_rng(20261008).permutation(pool); P=np.sort(perm[896:1792])
cols=[700,890]; eta=np.array([1.0,0.5])
def rows(idx): return np.maximum(np.asarray(M[idx][:,cols],dtype=np.float64),0)
Xtr=rows(np.arange(0,256)); Xca=rows(np.arange(256,512)); XP=rows(P)
rms=np.sqrt((Xtr**2).mean(0)); Xtr/=rms; Xca/=rms; XP/=rms
def out_loss(u,x,wi,b,sig):  # per-image E[(ReLU(wi*u+b+wi*sig*Z)-x)^2]
    mu=wi*u+b; s=abs(wi)*sig
    if s==0:
        r=np.maximum(mu,0); return (r-x)**2
    a=mu/s; Ph=norm.cdf(a); ph=norm.pdf(a)
    ER=mu*Ph+s*ph; ER2=(mu**2+s**2)*Ph+mu*s*ph
    return ER2-2*x*ER+x**2
def fit_b(u,x,wi,sig):
    lo,hi=-6.0,6.0
    g=np.linspace(lo,hi,1201); L=np.array([out_loss(u,x,wi,b,sig).mean() for b in g])
    k=int(np.argmin(L)); a,c=g[max(k-1,0)],g[min(k+1,len(g)-1)]
    r=minimize_scalar(lambda b: out_loss(u,x,wi,b,sig).mean(),bounds=(a,c),method='bounded',options={'xatol':1e-10})
    return r.x if r.fun<=L[k] else g[k]
def fit(w,X,sig):
    u=X@w; return [fit_b(u,X[:,i],w[i],sig) for i in range(2)]
def loss_img(w,bs,X,sig):
    u=X@w; return sum(eta[i]*out_loss(u,X[:,i],w[i],bs[i],sig) for i in range(2))
def tr_loss(t):
    w=np.array([np.cos(t),np.sin(t)]); return loss_img(w,fit(w,Xtr,0.0),Xtr,0.0).mean()
ts=np.linspace(-np.pi/2,np.pi/2,721,endpoint=False); Lt=np.array([tr_loss(t) for t in ts])
order=np.argsort(Lt)[:5]; best=None
for k in order:
    r=minimize_scalar(tr_loss,bounds=(ts[k]-np.pi/720,ts[k]+np.pi/720),method='bounded',options={'xatol':1e-8})
    if best is None or r.fun<best[1]: best=(r.x,r.fun)
t=best[0]; ws=np.array([np.cos(t),np.sin(t)])
print("t*=%.5f trainloss=%.6f; top grid t:"%best, ts[order], Lt[order])
m1=loss_img(np.array([1.,0]),fit(np.array([1.,0]),Xtr,0),Xtr,0).mean()
m2=loss_img(np.array([0.,1]),fit(np.array([0.,1]),Xtr,0),Xtr,0).mean()
wm=np.array([1.,0]) if m1<=m2 else np.array([0.,1]); ret=0 if m1<=m2 else 1
print("mono train loss keep1=%.6f keep2=%.6f -> retain feature %d"%(m1,m2,ret+1))
sigs=np.round(np.arange(0,1.01,0.1),2); D=np.zeros((len(XP),len(sigs)))
for j,s in enumerate(sigs):
    bS=fit(ws,Xca,s); bM=fit(wm,Xca,s)
    if j==0: bS0=bS
    D[:,j]=loss_img(ws,bS,XP,s)-loss_img(wm,bM,XP,s)
d=D.mean(0); print("Delta_P(sigma):",dict(zip(sigs,np.round(d,5))))
def cross(c):
    if not c[0]<0: return np.nan
    for j in range(1,len(c)):
        if c[j]>=0:
            x=sigs[j-1]+(sigs[j]-sigs[j-1])*(-c[j-1])/(c[j]-c[j-1]); return x
    return np.nan
xc=cross(d); print("point crossing %.4f"%xc)
rng=np.random.default_rng(12345); n=len(XP)
idx=rng.integers(0,n,(2000,n)); Bc=np.stack([D[i].mean(0) for i in idx])
cr=np.array([cross(c) for c in Bc]); ok=(cr>=0.05)&(cr<=0.9)
print("frac resamples crossing in [0.05,0.9]: %.4f ; frac with Delta(0)<0: %.4f"%(ok.mean(),(Bc[:,0]<0).mean()))
print("Delta(0) quantiles 0.833%%/99.167%%: %.5f %.5f"%tuple(np.quantile(Bc[:,0],[0.00833,0.99167])))
uP=XP@ws; f=[((ws[i]*uP+bS0[i])>0).mean() for i in range(2)]; pr=(XP[:,ret]>0).mean()
def v(p): return minimize_scalar(lambda z: p*(1+z*z)+(1-p)*((z*z+1)*norm.cdf(z)+z*norm.pdf(z)),bounds=(-10,10),method='bounded').fun
B=ws[0]**2*f[0]+0.5*ws[1]**2*f[1]-v(pr); G=-d[0]
print("f1=%.4f f2=%.4f p_r=%.4f v=%.5f B=%.5f G=%.5f sqrt(G/B)=%s"%(f[0],f[1],pr,v(pr),B,G,np.sqrt(G/B) if G/B>0 else 'nan'))
