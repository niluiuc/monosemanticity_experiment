"""sigma=0: locate the first-order line c*(p) > 0 where the global optimum jumps from the
opposite-sign to the same-sign branch, by bisection on c (8 halvings). Compare with the
leading-order prediction c* = 9 C eps^2 / (16 eta p q K)  (README §2.3)."""
import json, sys, numpy as np
from multiprocessing import Pool
from fra2 import solve, pc_theory, K_C_theory
ETA=0.5; PC=pc_theory(ETA); K,C=K_C_theory(ETA)
def one(p):
    eps=PC-p; q=1-p; pred=9*C*eps**2/(16*ETA*p*q*K)
    lo,hi=0.0,3*pred
    for _ in range(8):
        mid=0.5*(lo+hi); r=solve(p,mid,0.0,ETA)
        if r['F_neg']<=r['F_pos']: lo=mid
        else: hi=mid
    return dict(p=p,eps=eps,c_star_bracket=[lo,hi],c_star_pred=pred)
if __name__=='__main__':
    ps=[float(x) for x in sys.argv[1].split(',')]
    with Pool(2) as pool: out=pool.map(one,ps)
    for o in out: print(o)
    fn='results/coexistence_clean.json'
    old=json.load(open(fn)) if __import__('os').path.exists(fn) else []
    json.dump(old+out,open(fn,'w'),indent=1)
