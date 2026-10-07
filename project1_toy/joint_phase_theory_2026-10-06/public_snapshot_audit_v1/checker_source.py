"""Reuse the independently reviewed 90-digit ledger audit on new saved cases."""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json
import mpmath as mp
mp.mp.dps=90
HERE=Path(__file__).resolve().parent
SLACK=mp.mpf('1e-40');TOL=mp.mpf('1e-52');maximum=mp.mpf(0)
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


ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
ap.add_argument('--allow-excluded-latex',action='store_true',
                help='Public snapshot only: report omitted source_snapshot/*.tex hashes; never skip missing numerical/code files.')
args=ap.parse_args();RUN=args.run;out=args.output;out.mkdir(parents=True,exist_ok=False)
manifest=json.loads((RUN/'sha256_manifest.json').read_text())
omitted=[];checked=0
for rel,digest in manifest.items():
    path=RUN/rel
    if not path.is_file() and args.allow_excluded_latex and Path(rel).suffix=='.tex' and Path(rel).parts[0]=='source_snapshot':
        omitted.append(dict(path=rel,original_sha256=digest,reason='user excluded LaTeX from public upload; hash not verified'))
        continue
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,rel
    checked+=1
cases=json.loads((RUN/'results.json').read_text())['cases'];settings=json.loads((RUN/'settings.json').read_text())
states=[(0,0),(0,1),(1,0),(1,1)];feature_count=node_count=nonzero=0;report=[]
for case in cases:
    endpoint='eta' not in case
    eta=mp.mpf(2)/3 if endpoint else mp.mpf(case['eta'])
    p=mp.mpf(case['p']);probs=[mp.fprod([p if b else 1-p for b in x]) for x in states]
    folder=RUN/f"epsilon_{case['epsilon']}" if endpoint else RUN/f"eta_{case['eta']}_epsilon_{case['epsilon']}"
    total_target=mp.mpf(case['calibration_gap_target'] if endpoint else case['calibration_total_gap_target'])
    rows=[dict(sigma=case['sigma'],models=case['calibrated_models'],delta_lower=case['calibrated_delta_lower'],delta_upper=case['calibrated_delta_upper'],sign=case['calibrated_sign'])] if endpoint else case['calibrated']
    for row in rows:
        sigma=mp.mpf(row['sigma']);totals={}
        for name,w in [('sharing',[mp.mpf(t) for t in case['weights']]),('mono',[mp.mpf(1),mp.mpf(0)])]:
            lower=upper=mp.mpf(0)
            for i,importance in enumerate([mp.mpf(1),eta]):
                ledger_path=folder/f'{name}_feature_{i}.json' if endpoint else folder/f"calibration_{row['multiplier']}_{name}_feature_{i}.json"
                result=json.loads(ledger_path.read_text());feature_count+=1;s=sigma*abs(w[i]);targets=[mp.mpf(x[i]) for x in states]
                offsets=[w[i]*sum(w[j]*x[j] for j in range(2)) for x in states]
                assert result['resolved'];gap=mp.mpf(result['gap'])
                assert gap<=total_target/(1+eta)+TOL
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
            assert upper-lower<=total_target+TOL;totals[name]=(lower,upper)
        dl=totals['sharing'][0]-totals['mono'][1];du=totals['sharing'][1]-totals['mono'][0]
        close(row['delta_lower'],dl);close(row['delta_upper'],du)
        expected='positive' if dl>0 else 'negative' if du<0 else 'unresolved';assert expected==row['sign']
        report.append(dict(eta=str(eta),epsilon=case['epsilon'],sigma=str(sigma),sign=expected))
    if endpoint:
        sigma=mp.mpf(case['sigma']);totals={}
        for name,w,bias in [('sharing',[mp.mpf(t) for t in case['weights']],[mp.mpf(t) for t in case['bias']]),('mono',[mp.mpf(1),mp.mpf(0)],[mp.mpf(0),p])]:
            risk=mp.mpf(0)
            for i,I in enumerate([mp.mpf(1),eta]):
                offsets=[w[i]*sum(w[j]*x[j] for j in range(2)) for x in states]
                if w[i]==0:risk+=I*sum(P*(bias[i]-x[i])**2 for P,x in zip(probs,states))
                else:risk+=I*objective(bias[i],offsets,[mp.mpf(x[i]) for x in states],probs,sigma*abs(w[i]))[0]
            totals[name]=risk;close(case['frozen_models'][name],risk)
        close(case['frozen_delta'],totals['sharing']-totals['mono'])
        assert case['opposite_policy_orderings']==(totals['sharing']-totals['mono']<0 and mp.mpf(case['calibrated_delta_lower'])>0)
result=dict(all_passed=True,hashes_checked=checked,complete_original_manifest_verified=not omitted,
            intentionally_excluded_latex_not_verified=omitted,
            feature_ledgers_checked=feature_count,nonzero_ledgers=nonzero,nodes_recomputed=node_count,
    maximum_discrepancy=str(maximum),comparisons=report,scope='Reused independent 90-digit moment/derivative/curvature/partition/exterior/incumbent/gap audit. Not directed-rounding intervals or novelty certification.')
(out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='comparisons'},indent=2))
