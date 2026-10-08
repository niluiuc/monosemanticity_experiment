"""Independent, bounded audit. Does not import or execute Claude's research scripts.
Run from any directory with Python + numpy, scipy, sympy, mpmath.
All original inputs remain unchanged; results are written beside this file.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.special import ndtr
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "claude_agent"
REPORT = {}
mp.mp.dps = 55


def load(rel):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


def joint(p, c=0):
    X = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
    v = c*p*(1-p)
    return X, np.array([(1-p)**2+v, p*(1-p)-v, p*(1-p)-v, p*p+v])


def clean_bias(offset, target, prob):
    """Enumerate EVERY bias interval and its clipped quadratic minimizer."""
    breaks = np.unique(-offset)
    edges = np.r_[-np.inf, breaks, np.inf]
    candidates = list(breaks)
    for lo, hi in zip(edges[:-1], edges[1:]):
        mid = hi-1 if np.isneginf(lo) else lo+1 if np.isposinf(hi) else (lo+hi)/2
        active = offset+mid > 0
        if not active.any():
            continue
        b = np.sum(prob[active]*(target[active]-offset[active]))/prob[active].sum()
        candidates.append(np.clip(b, lo, hi))
    values = [np.sum(prob*(np.maximum(offset+b, 0)-target)**2) for b in candidates]
    j = int(np.argmin(values))
    return float(values[j]), float(candidates[j])


def profile(theta, p, c=0, eta=.5, sigma=0):
    X, prob = joint(p, c)
    w = np.array([np.cos(theta), np.sin(theta)])
    offsets = (X@w)[:, None]*w
    terms, bs = [], []
    for i in range(2):
        o, t = offsets[:, i], X[:, i]
        s = abs(w[i])*sigma
        if s < 1e-15:
            v, b = clean_bias(o, t, prob)
        else:
            def vals(b):
                mu = o+b; z = mu/s
                phi = np.exp(-z*z/2)/np.sqrt(2*np.pi); Phi = ndtr(z)
                m1 = mu*Phi+s*phi
                m2 = (mu*mu+s*s)*Phi+mu*s*phi
                return np.dot(prob, m2-2*t*m1+t*t), np.dot(prob, 2*m1-2*t*Phi)
            # Resolve kink neighborhoods at THEIR scale, not on a fixed coarse bias grid.
            grid = np.unique(np.r_[-4., 4., -o, t-o,
                    (-o[:, None]+s*np.array([-12,-6,-3,-1,0,1,3,6,12])).ravel(),
                    np.linspace(-2, 2, 65)])
            gradients = np.array([vals(b)[1] for b in grid])
            candidates = list(grid)
            for l, h, gl, gh in zip(grid[:-1],grid[1:],gradients[:-1],gradients[1:]):
                if gl*gh < 0:
                    candidates.append(brentq(lambda b: vals(b)[1], l,h,xtol=5e-15))
            values = [vals(b)[0] for b in candidates]
            j = int(np.argmin(values)); v, b = values[j], candidates[j]
        terms.append(v); bs.append(b)
    return terms[0]+eta*terms[1], bs


def selected(p,c=0,eta=.5,sigma=0,negative_only=False):
    grid = np.unique(np.r_[np.linspace(-np.pi/2,0 if negative_only else np.pi/2,151),
                           -np.geomspace(1e-6,.4,65), 0.,
                           [] if negative_only else np.geomspace(1e-6,.4,65)])
    vals = np.array([profile(t,p,c,eta,sigma)[0] for t in grid])
    indices = [j for j in range(1,len(grid)-1) if vals[j]<=vals[j-1] and vals[j]<=vals[j+1]]
    candidates = [(vals[j],grid[j]) for j in (0,len(grid)-1,int(np.argmin(vals)))]
    for j in indices:
        r = minimize_scalar(lambda t: profile(t,p,c,eta,sigma)[0], bounds=(grid[j-1],grid[j+1]),
                            method="bounded",options={"xatol":2e-11})
        candidates.append((float(r.fun),float(r.x)))
    return min(candidates)


def symbolic():
    p,c,e,t = sp.symbols("p c eta theta",real=True); q=1-p; D=1-p+p*p
    P=[q*q+c*p*q,p*q-c*p*q,p*q-c*p*q,p*p+c*p*q]
    a=sp.cos(t)**2; d=sp.sin(t)*sp.cos(t); z=sp.sin(t)**2
    bn=(P[1]*(1-a)+P[3]*(1-a-d))/(1-P[2])
    bp=-(P[2]*d+P[1]*(a-1)+P[3]*(a+d-1))/(1-P[0])
    var=p*q*(d*d+(z-1)**2+2*c*d*(z-1))
    Fn=P[0]*bn**2+P[1]*(a+bn-1)**2+P[3]*(a+d+bn-1)**2+e*var-e*p*q
    Fp=P[2]*(d+bp)**2+P[1]*(a+bp-1)**2+P[3]*(a+d+bp-1)**2+e*var-e*p*q
    linear=sp.simplify(sp.diff(Fn,t).subs(t,0))
    kn=sp.factor(sp.diff(Fn,t,2).subs({t:0,c:0})/2)
    kp=sp.factor(sp.diff(Fp,t,2).subs({t:0,c:0})/2)
    cubic=sp.factor(-sp.diff(Fn,t,3).subs({t:0,c:0})/6)
    assert sp.simplify(linear+2*e*c*p*q)==0
    assert sp.simplify(kn-p*q*(p-e*D)/D)==0
    assert sp.simplify(kp-p*q*(1-e*(2-p))/(2-p))==0
    assert sp.simplify(cubic-2*p*p*q*q/D)==0
    pc=(3-sp.sqrt(5))/2
    A=sp.simplify(sp.diff(kn,p).subs({p:pc,e:sp.Rational(1,2)}))
    B=sp.simplify(cubic.subs(p,pc))
    K=2*A/(3*B); C=4*A**3/(27*B**2)
    saved=load("results/analytic_A.json")
    REPORT["symbolic_clean"]={"linear":str(linear),"kappa_minus":str(kn),"kappa_plus":str(kp),
        "B":str(cubic),"correct_A":float(A),"correct_K":float(K),"correct_C":float(C),
        "saved_A":saved["A"],"saved_K_pred":saved["K_pred"],"saved_C_pred":saved["C_pred"],
        "saved_sign_error_confirmed": bool(saved["K_pred"]<0 and float(K)>0),
        "source_pdf_error":"A' is written as -d(kappa_minus)/dp, but epsilon=pc-p requires +d(kappa_minus)/dp"}
    # Crucial sign in the c<0 critical response.
    REPORT["critical_response_sign"]={"h_definition":"h=2 eta c p q",
        "printed_formula":"sqrt(h/(3B)) for c<0", "correct_formula":"sqrt(-h/(3B)) for c<0",
        "status":"printed expression has a negative radicand; saved positive coefficient uses the correct magnitude"}
    print("symbolic clean: verified; saved slope/K/C signs and printed negative-c square root WRONG",flush=True)


def clean_checks():
    rng=np.random.default_rng(20261007); rows=[]
    for _ in range(100):
        p=rng.uniform(.03,.97); lower=-min(p/(1-p),(1-p)/p)
        c=rng.uniform(.98*lower,.98); eta=rng.uniform(.1,.9)
        th=rng.choice([-1,1])*1e-5
        _,b=profile(th,p,c,eta); X,P=joint(p,c)
        a=math.cos(th)**2; d=math.sin(th)*math.cos(th)
        if th<0:
            bc=(P[1]*(1-a)+P[3]*(1-a-d))/(1-P[2])
            pat=[True,True,False,True]
        else:
            bc=-(P[2]*d+P[1]*(a-1)+P[3]*(a+d-1))/(1-P[0])
            pat=[False,True,True,True]
        offset=(X@np.array([math.cos(th),math.sin(th)]))*math.cos(th)
        rows.append({"p":p,"c":c,"theta":float(th),"bias_error":abs(b[0]-bc),
                     "predicted_pattern_valid":bool(np.array_equal(offset+bc>0,pat))})
    compare=[]
    for r in load("results/analytic_A.json")["solver_checks"]:
        nu=profile(r["theta"],r["p"],r["c"])[0]-profile(0,r["p"],r["c"])[0]
        compare.append(abs(nu-r["solver"]))
    pc=(3-math.sqrt(5))/2; field=[]
    for c in [-1e-4,1e-4,-1e-5,1e-5]:
        loss,theta=selected(pc,c)
        pred=-.7344008870614411*math.sqrt(-c) if c<0 else 4.23606797749979*c
        field.append({"c":c,"theta":theta,"leading_prediction":pred,"relative_error":abs(theta/pred-1)})
    cert=[]
    for p,c in [(.30,.002),(.34,.005),(.38,0),(.40,-.02)]:
        loss,theta=selected(p,c)
        f=BASE/f"results/certificate_v2/p{p}_c{c}.json"
        if not f.exists():
            f=next(f for f in (BASE/"results/certificate_v2").glob("p*.json") if abs(load(str(f.relative_to(BASE)))["p"]-p)<1e-10 and abs(load(str(f.relative_to(BASE)))["c"]-c)<1e-10)
        saved=json.loads(f.read_text()); lo,hi=saved["surviving_range"]
        cert.append({"p":p,"c":c,"theta":theta,"inside_saved_survivors":lo<=theta<=hi,
                     "saved_side":saved["certified_side"],"loss_diff":loss-saved["best"]})
    REPORT["clean_independent"]={"gate_cases":rows,"solver_max_abs_diff":max(compare),"field_response":field,
        "certificate_spotchecks":cert,"certificate_limit":"No interval arithmetic; agreement does not establish floating-point enclosure rigour"}
    print("clean enumeration:",len(rows),"gate cases; max saved-solver difference",max(compare),flush=True)


def compression():
    # High precision full bias enumeration along the claimed profiled donor path.
    def bias_mp(offset,target,prob):
        breaks=sorted(set(-x for x in offset)); candidates=list(breaks)
        for j in range(len(breaks)+1):
            lo=breaks[j-1] if j else mp.ninf; hi=breaks[j] if j<len(breaks) else mp.inf
            mid=hi-1 if lo==mp.ninf else lo+1 if hi==mp.inf else (lo+hi)/2
            on=[i for i in range(len(offset)) if offset[i]+mid>0]
            if not on: continue
            b=sum(prob[i]*(target[i]-offset[i]) for i in on)/sum(prob[i] for i in on)
            candidates.append(max(lo,min(hi,b)))
        scores=[sum(prob[i]*(max(0,offset[i]+b)-target[i])**2 for i in range(len(offset))) for b in candidates]
        j=min(range(len(scores)),key=scores.__getitem__); return scores[j],candidates[j]
    rows=[]
    k,p,e,u,M=sp.symbols("k p eta u m",real=True); q=1-p
    a=1+u
    for sign in [-1,1]:
        d=sign*sp.sqrt(1+u)*k
        P=[q*q,p*q,p*q,p*p]
        b=(P[1]*(1-a)+P[3]*(1-a-d))/(1-P[2]) if sign<0 else -(P[2]*d+P[1]*(a-1)+P[3]*(a+d-1))/(1-P[0])
        L=P[0]*b*b+P[1]*(a+b-1)**2+P[3]*(a+d+b-1)**2 if sign<0 else P[2]*(d+b)**2+P[1]*(a+b-1)**2+P[3]*(a+d+b-1)**2
        F=L+e*p*q*(d*d+(k*k-1)**2)+p*q*(u+k*k)**2/(M-1)-e*p*q
        H=sp.simplify(sp.hessian(F,(k,u)).subs({k:0,u:0}))
        kap=sp.factor((H[0,0]-H[0,1]**2/H[1,1])/2)
        for m in ([2,3,4] if sign<0 else [2]):
            for eta in ([.3,.5] if sign<0 else [.7]):
                pc=1-math.sqrt((1-eta)/(1+eta)) if sign<0 and m==2 else (3*eta-1)/(eta+1) if sign>0 else (m*(1+eta)-math.sqrt(m*(m*(1-eta)**2+4*eta*(1-eta))))/(2*(m+eta-1))
                for pp in [pc-.005,pc+.005]:
                    sub={p:pp,e:eta,M:m}; ust=float((-H[0,1]/H[1,1]).subs(sub))
                    kk=mp.mpf("0.0000001"); uu=mp.mpf(str(ust))*kk
                    pm=mp.mpf(str(pp)); em=mp.mpf(str(eta)); qm=1-pm
                    pr=[qm*qm,pm*qm,pm*qm,pm*pm]; x1=[0,1,0,1]; x2=[0,0,1,1]
                    aa=1+uu; dd=sign*mp.sqrt(aa)*kk
                    l1,bb=bias_mp([0,aa,dd,aa+dd],x1,pr)
                    l2,_=bias_mp([0,dd,kk*kk,dd+kk*kk],x2,pr)
                    cost=pm*qm*(uu+kk*kk)**2/(m-1)
                    exact=float((l1+em*l2+cost-em*pm*qm)/(kk*kk))
                    pred=float(kap.subs(sub))
                    rows.append({"m":m,"eta":eta,"sign":sign,"p":pp,"threshold":pc,"u_over_k":ust,
                        "curvature_exact":exact,"curvature_pred":pred,"error":exact-pred,
                        "claimed_output1_gate_valid":bool(0<bb<-dd) if sign<0 else bool(-dd<bb<0)})
    REPORT["compression_independent"]={"rows":rows,"max_abs_curvature_error":max(abs(r["error"]) for r in rows),
        "all_gate_paths_valid":all(r["claimed_output1_gate_valid"] for r in rows),
        "scope":"local instability along one-partner/equal-donor paths; NOT a proof of full global n-by-m phase diagram"}
    print("compression:",len(rows),"high-precision path checks; max error",REPORT["compression_independent"]["max_abs_curvature_error"],flush=True)


def noise():
    pc=(3-math.sqrt(5))/2; rows=[]
    for sigma in [.001,.003]:
        # Existing numerical bracket identifies a SMALL verification interval; no fitting.
        saved=next(load(str(f.relative_to(BASE))) for f in (BASE/"results/resultB").glob("bisect_*.json")
                   if abs(load(str(f.relative_to(BASE)))["sigma"]-sigma)<1e-12 and abs(load(str(f.relative_to(BASE)))["eta"]-.5)<1e-12)
        lo,hi=saved["eps_trained_bracket"]
        outcomes=[]
        for eps in [lo-.00005,hi+.00005]:
            p=pc-eps
            # Resolve the competing SHARING well, excluding the mono minimum.
            predtheta=-1.5786893258332633*eps
            grid=np.linspace(2.2*predtheta,.35*predtheta,31)
            vals=[profile(t,p,sigma=sigma)[0] for t in grid]; j=int(np.argmin(vals))
            a,b=grid[max(j-1,0)],grid[min(j+1,len(grid)-1)]
            r=minimize_scalar(lambda t:profile(t,p,sigma=sigma)[0],bounds=(a,b),method="bounded",options={"xatol":1e-11})
            gain=profile(0,p,sigma=sigma)[0]-r.fun
            outcomes.append({"eps":eps,"sharing_gain":float(gain),"theta_sharing":float(r.x)})
        rows.append({"sigma":sigma,"saved_bracket":[lo,hi],"independent_endpoints":outcomes,
            "crossing_bracket_reproduced":bool(outcomes[0]["sharing_gain"]<0<outcomes[1]["sharing_gain"]),
            "leading_prediction":.8315564147061506*sigma**(2/3)})
    curv=[]
    for p in [.28,.38]:
        z=brentq(lambda z:p*z+(1-p)*(z*ndtr(z)+np.exp(-z*z/2)/np.sqrt(2*np.pi)),-8,0)
        k0=p*(1-p)*(p+(1-p)*ndtr(z)-.5)
        for s in [.003,.01]:
            dt=s*.003
            fm=profile(-dt,p,sigma=s)[0]; f0=profile(0,p,sigma=s)[0]; fp=profile(dt,p,sigma=s)[0]
            kap=(fm+fp-2*f0)/(2*dt*dt)
            pred=k0-2*p*z*s
            curv.append({"p":p,"sigma":s,"numerical_curvature":kap,"predicted_first_order":pred,"residual":kap-pred})
    REPORT["noise_independent"]={"transition_checks":rows,"curvature_checks":curv,
        "status":"finite-noise numerical confirmation, not an asymptotic remainder proof"}
    print("noise: independent crossing endpoints",[r["crossing_bracket_reproduced"] for r in rows],flush=True)


def real_ledger():
    out={}
    for name in ["real","real_logits"]:
        P={(r["i"],r["j"]):r for r in load(f"results/{name}/pairs.json")["pairs"]}
        L=load(f"results/{name}/landscapes.json")
        c=np.array([P[(r["i"],r["j"])]["corr"] for r in L])
        theta=np.array([next(s["theta_star"] for s in r["rows"] if s["sigma"]==.005) for r in L])
        bist=np.array([any(len(s["sector_minima_theta"])>=2 for s in r["rows"]) for r in L])
        q1,q2=np.quantile(abs(c),[1/3,2/3]); low=abs(c)<=q1; high=abs(c)>q2
        shrink=[]
        for r in L:
            angles=[next(s["theta_star"] for s in r["rows"] if s["sigma"]==sig) for sig in [.005,.4]]
            ratios=[min(abs(np.cos(t)),abs(np.sin(t)))/max(abs(np.cos(t)),abs(np.sin(t))) for t in angles]
            shrink.append(ratios[1]<ratios[0])
        out[name]={"negative_sign":[int(np.sum(theta[c<-.05]<0)),int(np.sum(c<-.05))],
            "positive_sign":[int(np.sum(theta[c>.15]>0)),int(np.sum(c>.15))],
            "bistable_low":[int(bist[low].sum()),int(low.sum())],"bistable_high":[int(bist[high].sum()),int(high.sum())],
            "noise_shrink_fraction":float(np.mean(shrink)),"n":len(L)}
    for name in ["real_triples","real_triples_logits"]:
        S=load(f"results/{name}/solutions.json")
        def stored(r,j): return abs(r["w"][j])/max(abs(x) for x in r["w"])>.05
        strong=[r for r in S if abs(r["c13"])>=.05]; zero=[r for r in S if r["bin"]==[-.01,.01]]
        stored3=[r for r in strong if stored(r,2)]
        pools=[r for r in S if r["bin"] in [[-.2,-.05],[.15,.6]]]
        out[name]={"T1":[sum(np.sign(r["w"][0]*r["w"][2])==np.sign(r["c13"]) for r in stored3),len(stored3)],
            "T2":[sum(stored(r,1) for r in pools),len(pools),sum(stored(r,1) for r in zero),len(zero)],
            "T3":[len(stored3),len(strong),sum(stored(r,2) for r in zero),len(zero)]}
    REPORT["real_ledger_recomputed"]=out
    REPORT["statistical_review"]={"bootstrap_problem":"real_stats.py converts resampled channels to a set, discarding multiplicities. This is a random subset procedure, not the asserted standard cluster bootstrap. Its CI95 coverage is unestablished.",
        "fisher_problem":"pairs/triples share channels, so simple independent-observation Fisher p-values are not established inferential evidence",
        "data_split_problem":"real_pairs.load concatenates train, calibration and test; fitted empirical compressor results are not held-out/native-model robustness",
        "replication_scope":"hidden activations and logits of the SAME ResNet, not independent models"}
    print("real ledger: counts recomputed; bootstrap/dependence and native-transfer limitations confirmed",flush=True)


def gradient_check():
    # Independently finite-difference the actual tied-network training gradient.
    rng=np.random.default_rng(91); X=(rng.random((32,4))<.3).astype(float)
    W=rng.normal(size=(2,4)); b=np.array([.2,.3,.2,.1]); Z=rng.normal(size=(32,2))
    eta=np.array([1,1,.5,.5]); sig=.03
    def loss(A):
        U=(X@A.T+sig*Z)@A+b
        return np.mean(np.sum(eta*(np.maximum(U,0)-X)**2,axis=1))
    H=X@W.T+sig*Z; U=H@W+b; G=2*eta*(np.maximum(U,0)-X)*(U>0)/len(X)
    analytical=H.T@G+(G@W.T).T@X
    numerical=np.zeros_like(W); step=1e-6
    for i in range(2):
        for j in range(4):
            D=np.zeros_like(W);D[i,j]=step
            numerical[i,j]=(loss(W+D)-loss(W-D))/(2*step)
    REPORT["training_gradient"]={"max_abs_error":float(np.max(abs(analytical-numerical))),
        "interpretation":"gradient implementation checked; does not validate saved seed convergence or global optimality"}
    print("training gradient max discrepancy",REPORT["training_gradient"]["max_abs_error"],flush=True)


if __name__=="__main__":
    start=time.time()
    for task in [symbolic,clean_checks,compression,noise,real_ledger,gradient_check]:
        task()
        (HERE/"results.json").write_text(json.dumps(REPORT,indent=2,default=lambda x:x.item() if isinstance(x,np.generic) else str(x)),encoding="utf-8")
    REPORT["seconds"]=time.time()-start
    REPORT["input_hashes"]={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in BASE.glob("*.py")}
    (HERE/"results.json").write_text(json.dumps(REPORT,indent=2,default=lambda x:x.item() if isinstance(x,np.generic) else str(x)),encoding="utf-8")
    print("AUDIT COMPLETE",round(REPORT["seconds"],1),"seconds",flush=True)
