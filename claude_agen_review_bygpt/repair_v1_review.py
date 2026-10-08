"""Bounded second review: repaired optimizer counterexample and independent seed-0 subset counts.
Writes only to the GPT review folder; Claude sources/results are read-only.
"""
import sys,json,importlib.util
from pathlib import Path
import numpy as np
from scipy.stats import fisher_exact
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;BASE=HERE.parent/'claude_agent';REPAIR=BASE/'repair_v1'
sys.path.insert(0,str(REPAIR));sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('repaired_solver',REPAIR/'fra2_v2.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
load=lambda p:json.loads((BASE/p).read_text(encoding='utf-8'))
old=json.loads((HERE/'results.json').read_text())
out={}
signed=load('repair_v1/results/analytic_A_signed.json')
out['signs']={k:{'repaired':signed[k.replace('correct_','') if k=='correct_A' else k.replace('correct_','')+'_pred'],
                 'independent':old['symbolic_clean'][k]} for k in ['correct_A','correct_K','correct_C']}
pc=(3-np.sqrt(5))/2
out['optimizer_checks']=[]
cases=[(.3641344889933496,.003,'original_counterexample'),
       (pc-.017781006480572594+.00005,.003,'below_independent_epsilon_crossing'),
       (pc-.017781006480572594-.00005,.003,'above_independent_epsilon_crossing')]
for p,s,name in cases:
    r=module.solve(p,0,s,.5)
    out['optimizer_checks'].append({'case':name,**r,'sharing_gain':r['F_mono']-r['F_star']})
    print(name,'theta',r['t_star'],'gain',r['F_mono']-r['F_star'],flush=True)
out['repaired_transition_comparisons']=[]
for f in sorted((REPAIR/'results').glob('bisect_v2_*.json')):
    d=json.loads(f.read_text());row={'eta':d['eta'],'sigma':d['sigma'],'bracket':d['eps_trained_bracket']}
    if abs(d['eta']-.5)<1e-10 and d['sigma'] in [.001,.003]:
        ind=next(r['independent_eps_root'] for r in json.loads((HERE/'followup_results.json').read_text())['noise_resolution'] if r['sigma']==d['sigma'])
        row.update(independent_root=ind,midpoint_difference=np.mean(row['bracket'])-ind)
    out['repaired_transition_comparisons'].append(row)

def subset(units):
    keep=[];used=set()
    for idx in np.random.default_rng(0).permutation(len(units)):
        if all(x not in used for x in units[idx]):keep.append(idx);used.update(units[idx])
    mask=np.zeros(len(units),bool);mask[keep]=True
    flat=[c for i in keep for c in units[i]]
    assert len(flat)==len(set(flat))
    return mask
def test(values,mask,group1,group2):
    a=int((values & mask & group1).sum());n=int((mask & group1).sum())
    b=int((values & mask & group2).sum());m=int((mask & group2).sum())
    return {'counts':[a,n,b,m],'one_sided_fisher':float(fisher_exact([[a,n-a],[b,m-b]],alternative='greater')[1])}
out['disjoint_seed0_recomputed']={}
for name,d in [('layer4','real'),('logits','real_logits')]:
    P={(p['i'],p['j']):p for p in load(f'results/{d}/pairs.json')['pairs']}
    L=load(f'results/{d}/landscapes.json');units=[(r['i'],r['j']) for r in L];mask=subset(units)
    c=np.array([P[u]['corr'] for u in units]);ac=abs(c);lo,hi=np.quantile(ac,[1/3,2/3])
    bist=np.array([any(len(x['sector_minima_theta'])>=2 for x in r['rows']) for r in L])
    co=np.array([any(any(t<-.1 for t in x['sector_minima_theta']) and any(t>-.05 for t in x['sector_minima_theta']) for x in r['rows']) for r in L])
    out['disjoint_seed0_recomputed'][name]={'size':int(mask.sum()),'P2':test(bist,mask,ac<=lo,ac>hi),
                                        'asymmetry':test(co,mask,(ac<.1)&(c>0),(ac<.1)&(c<0))}
for name,d in [('layer4','real_triples'),('logits','real_triples_logits')]:
    S=load(f'results/{d}/solutions.json');units=[(r['i'],r['j'],r['k']) for r in S];mask=subset(units)
    c=np.array([r['c13'] for r in S]);bins=np.array([r['bin'] for r in S])
    st=lambda r,j:abs(r['w'][j])/max(abs(x) for x in r['w'])>.05
    v2=np.array([st(r,1) for r in S]);v3=np.array([st(r,2) for r in S])
    out['disjoint_seed0_recomputed']['triples_'+name]={'size':int(mask.sum()),
      'T3':test(v3,mask,abs(c)>=.05,(bins[:,0]==-.01)&(bins[:,1]==.01)),
      'T4':test(v2&v3,mask,c>=.05,c<=-.05),
      'T5':test(v2,mask,(bins[:,0]==.15)&(bins[:,1]==.6),(bins[:,0]==-.2)&(bins[:,1]==-.05))}
out['scope']='Seed-0 arithmetic and channel disjointness verified. Fisher independence/exchangeability is NOT established by disjointness. No proof that finite angular grid finds every possible well.'
(HERE/'repair_v1_review_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out['disjoint_seed0_recomputed'],indent=2),flush=True)
