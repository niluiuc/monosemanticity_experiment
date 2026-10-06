"""Independent saved-ledger audit; no optimization or new scientific case."""
from pathlib import Path
import hashlib,json
import mpmath as mp

mp.mp.dps=90
HERE=Path(__file__).resolve().parent
RUN=HERE/'calibrated_run_v1'
SLACK=mp.mpf('1e-40')
TOL=mp.mpf('1e-52')
PARENTS=[]
maximum=mp.mpf(0)

def close(a,b):
    global maximum
    d=abs(mp.mpf(a)-mp.mpf(b));maximum=max(maximum,d)
    assert d<TOL,(str(a),str(b),str(d))

def phi(z):return mp.exp(-z*z/2)/mp.sqrt(2*mp.pi)
def cdf(z):return mp.erfc(-z/mp.sqrt(2))/2
def moments(mu,s):
    z=mu/s;F=cdf(z);d=phi(z)
    return mu*F+s*d,(mu*mu+s*s)*F+mu*s*d
def objective(beta,offsets,targets,probs,s):
    f=g=mp.mpf(0)
    for o,y,P in zip(offsets,targets,probs):
        mu=o+beta;m1,m2=moments(mu,s)
        f+=P*(m2-2*y*m1+y*y)
        g+=2*P*((mu-y)*cdf(mu/s)+s*phi(mu/s))
    return f,g

manifest=json.loads((RUN/'sha256_manifest.json').read_text())
for relative,digest in manifest.items():
    assert hashlib.sha256((RUN/relative).read_bytes()).hexdigest()==digest,relative
geometries=json.loads((RUN/'source_snapshot/frozen_geometry_results.json').read_text())
lookup={case['epsilon']:case for case in geometries['cases']}
comparisons=json.loads((RUN/'comparisons.json').read_text())
states=[(0,0),(0,1),(1,0),(1,1)]
report=[];node_count=0;feature_count=0;nonzero=0;signs=[]
for row in comparisons:
    case=lookup[row['epsilon']];p=mp.mpf(case['p']);sigma=mp.mpf(row['sigma'])
    probs=[mp.fprod([p if bit else 1-p for bit in x]) for x in states]
    total_target=mp.mpf(row['target_total_gap']);totals={}
    folder=RUN/f"epsilon_{row['epsilon']}_multiplier_{row['multiplier']}"
    for name,w in [('sharing',[mp.mpf(t) for t in case['weights']]),('mono',[mp.mpf(1),mp.mpf(0)])]:
        lower=upper=mp.mpf(0)
        for i,importance in enumerate([mp.mpf(1),mp.mpf('.5')]):
            result=json.loads((folder/f'{name}_feature_{i}.json').read_text())
            feature_count+=1;s=sigma*abs(w[i]);targets=[mp.mpf(x[i]) for x in states]
            offsets=[w[i]*sum(w[j]*x[j] for j in range(2)) for x in states]
            assert result['resolved'];gap=mp.mpf(result['gap'])
            assert gap<=total_target/mp.mpf('1.5')+TOL
            close(gap,mp.mpf(result['upper'])-mp.mpf(result['lower']))
            if s==0:
                close(result['beta'],p);close(result['lower'],p*(1-p));close(result['upper'],p*(1-p))
                assert not result['nodes'] and not result['active_heap']
            else:
                nonzero+=1;nodes=result['nodes'];node_count+=len(nodes)
                assert len(nodes)==2*result['expansions']+1
                children={};heap_ids=set()
                root_lo=-max(offsets)-12*s-1;root_hi=1-min(offsets)
                close(nodes[0]['lo'],root_lo);close(nodes[0]['hi'],root_hi)
                for index,node in enumerate(nodes):
                    assert node['id']==index
                    a,b=mp.mpf(node['lo']),mp.mpf(node['hi']);mid=(a+b)/2;h=(b-a)/2
                    close(node['mid'],mid);f,g=objective(mid,offsets,targets,probs,s)
                    close(node['f'],f);close(node['g'],g)
                    density=mp.mpf(0)
                    for o,y,P in zip(offsets,targets,probs):
                        L=o+a;U=o+b;dist=mp.mpf(0) if L<=0<=U else min(abs(L),abs(U))
                        density+=P*y*phi(dist/s)/s
                    H=2*(1+density);close(node['H'],H)
                    close(node['lower'],max(mp.mpf(0),f-abs(g)*h-H*h*h/2-SLACK))
                    assert mp.mpf(node['upper_after'])>=mp.mpf(result['upper'])-TOL
                    if node['parent'] is not None:children.setdefault(node['parent'],[]).append(index)
                for parent,ids in children.items():
                    assert len(ids)==2
                    left,right=nodes[ids[0]],nodes[ids[1]];original=nodes[parent]
                    close(left['lo'],original['lo']);close(left['hi'],original['mid'])
                    close(right['lo'],original['mid']);close(right['hi'],original['hi'])
                for bound,index,a,b in result['active_heap']:
                    assert index not in children and index not in heap_ids;heap_ids.add(index)
                    close(bound,nodes[index]['lower']);close(a,nodes[index]['lo']);close(b,nodes[index]['hi'])
                for index,node in enumerate(nodes):
                    if index not in children and index not in heap_ids:
                        assert mp.mpf(node['lower'])>=mp.mpf(result['upper'])-TOL
                f_best,_=objective(mp.mpf(result['beta']),offsets,targets,probs,s)
                close(result['upper'],f_best+SLACK)
                far_left=sum(P*y*y for P,y in zip(probs,targets))-2*sum(P*y*moments(o+root_lo,s)[0] for P,y,o in zip(probs,targets,offsets))-SLACK
                far_right=objective(root_hi,offsets,targets,probs,s)[0]-SLACK
                close(result['excluded_lower_halfline'],far_left);close(result['excluded_upper_halfline'],far_right)
                heap_min=min([mp.mpf(item[0]) for item in result['active_heap']],default=mp.mpf(result['upper']))
                close(result['lower'],min(mp.mpf(result['upper']),far_left,far_right,heap_min))
            lower+=importance*mp.mpf(result['lower']);upper+=importance*mp.mpf(result['upper'])
        close(row['models'][name]['lower'],lower);close(row['models'][name]['upper'],upper)
        assert upper-lower<=total_target+TOL
        totals[name]=(lower,upper)
    dl=totals['sharing'][0]-totals['mono'][1];du=totals['sharing'][1]-totals['mono'][0]
    close(row['delta_lower'],dl);close(row['delta_upper'],du)
    expected='positive' if dl>0 else 'negative' if du<0 else 'unresolved'
    assert row['sign']==expected
    assert expected==('negative' if row['multiplier']=='0.5' else 'positive')
    signs.append(expected)
    report.append(dict(epsilon=row['epsilon'],multiplier=row['multiplier'],delta_lower=str(dl),delta_upper=str(du),sign=expected))
assert len(comparisons)==12 and feature_count==48 and nonzero==36
out=dict(all_passed=True,precision_digits=90,tolerance=str(TOL),maximum_recomputed_discrepancy=str(maximum),
         manifest_hashes_checked=len(manifest),comparisons_checked=12,feature_ledgers_checked=feature_count,
         nonzero_feature_ledgers_checked=nonzero,nodes_recomputed=node_count,negative=signs.count('negative'),positive=signs.count('positive'),
         checks=['independent moments/derivatives/local curvature','binary partition and active/pruned leaf coverage','half-line bounds','feasible incumbent risk','per-feature and weighted model gaps','delta interval arithmetic and signs','immutable snapshot hashes'],
         comparisons=report,scope='Archived-case audit only; no new scientific cases or optimization. Numerical bounds, not directed-rounding intervals.')
(HERE/'calibrated_professor_check_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='comparisons'},indent=2))
