"""Finite certificate/noisy-risk checks after independent mathematics approval.

No training, dense frequency scan or new encoder family. Reuses the reviewed
finite branch/root-isolation implementation with exact rational probabilities.
"""
import argparse
import csv
import hashlib
import itertools
import json
import platform
import shutil
import sys
import time
from pathlib import Path
import numpy as np
import scipy
import sympy as s
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import certificate_backend_snapshot as backend
from toy_math_snapshot import binary_population,exact_detection,exact_decoder_mse,geometry

CONFIG={'frequencies':['1/20','1/5','7/20','3/8','2/5'],
        'importance':['1','1/2'],'n':2,'m':1,'encoder_energy':1,
        'pc_expression':'(3-sqrt(5))/2',
        'primary_sigmas':[0.,.05,.15,.30,.60],
        'display_sigmas_count':240,'display_sigmas_min':.001,'display_sigmas_max':4.,
        'brent_sign_magnitude_min':1e-12,'brent_xtol':1e-12,'brent_rtol':1e-12,
        'brent_maxiter':100,'algebraic_root_isolation_epsilon':'1e-35',
        'noise':'Gaussian code noise h+sigma*epsilon, epsilon N(0,1)',
        'actual_decoder':'strict reconstruction>0.5',
        'midpoint':'separately labeled centered matched midpoint',
        'scope':'five fixed frequencies; no training; finite certificates and CDF evaluation',
        'risk_root_claim':'numerical display crossings, not a completeness theorem'}


def write_json(path,data):
    path.write_text(json.dumps(data,indent=2,allow_nan=True),encoding='utf-8')


def write_csv(path,rows):
    if rows:
        with path.open('w',newline='',encoding='utf-8') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def encode_root(root):
    return {'polynomial':str(root['poly'].as_expr()),'isolating_interval':[str(x) for x in root['ab']],
            'key':root['key']}


def finite_certificate(p,folder):
    """Exact global candidate calculation for one supplied rational frequency.

    This uses the same four geometry sign/order regions and fixed-bias kink and
    stationary candidates as the independently reviewed p=1/5 backend. Each
    candidate's feasible stationary/domain-boundary roots is checked exactly.
    """
    backend.P=[(1-p)**2,p*(1-p),p*(1-p),p*p]
    start=time.perf_counter()
    t=backend.t
    regions=[(None,-1,s.Rational(-2)),(-1,0,s.Rational(-1,2)),
             (0,1,s.Rational(1,2)),(1,None,s.Rational(2))]
    feasible=[]; branches=[]; raw_roots=[]
    for rid,(left,right,sample) in enumerate(regions):
        first=backend.feature_candidates(0,sample);second=backend.feature_candidates(1,sample)
        region_constraints=[]
        if left is not None:region_constraints.append(s.Poly(t-left,t))
        if right is not None:region_constraints.append(s.Poly(right-t,t))
        for c1,c2 in itertools.product(first,second):
            objective=s.cancel(c1['loss']+c2['loss']/2)
            constraints=region_constraints+c1['constraints']+c2['constraints']
            derivative=backend.positive_numerator(s.diff(objective,t))
            branch_index=len(branches)
            branches.append({'region':rid,'left':None if left is None else str(left),
                             'right':None if right is None else str(right),
                             'interior_sample':str(sample),'bias_candidates':[c1['name'],c2['name']],
                             'bias_formulas':[str(c1['bias']),str(c2['bias'])],
                             'objective':str(objective),'derivative_numerator':str(derivative.as_expr()),
                             'feasibility_numerators':[str(poly.as_expr()) for poly in constraints]})
            roots={}
            for poly in constraints+[derivative]:
                for root in backend.roots_of_expression(poly.as_expr()):
                    roots[root['key']]=root
            for root in roots.values():
                signs=[backend.sign_at(poly,root) for poly in constraints]
                valid=all(sign>=0 for sign in signs)
                item={'branch_index':branch_index,'root':encode_root(root),
                      'constraint_signs':signs,'feasible':valid}
                raw_roots.append(item)
                if not valid:
                    continue
                bounds=backend.value_interval(objective,root)
                candidate={'region':rid,'branch_index':branch_index,'branches':[c1['name'],c2['name']],
                           'objective':objective,'root':root,'bounds':bounds,
                           'bias':[c1['bias'],c2['bias']]}
                feasible.append(candidate)
        print('certificate',str(p),'region',rid,'feasible candidates',len(feasible),flush=True)
    unique={}
    for candidate in feasible:
        key=(str(candidate['objective']),candidate['root']['key'])
        if key not in unique:unique[key]=candidate
    candidates=list(unique.values())
    if not candidates:
        raise RuntimeError('No feasible algebraic candidates')
    winner=min(candidates,key=lambda c:c['bounds'][1])
    competitors=[c for c in candidates if c is not winner]
    unresolved=[c for c in competitors if c['bounds'][0]<=winner['bounds'][1]]
    mono_first=p*(1-p)/2;mono_second=p*(1-p)
    # t=0 occurs among algebraic boundaries above. Explicit infinity endpoints
    # complete the rational chart and correspond to retention of feature 1.
    endpoints=[{'geometry':'t=0; retain feature0','bias':['0',str(p)],'loss':str(mono_first)},
               {'geometry':'t=+infinity; retain feature1','bias':[str(p),'0'],'loss':str(mono_second)},
               {'geometry':'t=-infinity; retain feature1','bias':[str(p),'0'],'loss':str(mono_second)}]
    certified=not unresolved and winner['bounds'][1]<min(mono_first,mono_second)
    chosen_t=(winner['root']['ab'][0]+winner['root']['ab'][1])/2
    bias=np.array([float(s.N(expr.subs(t,chosen_t),40)) for expr in winner['bias']])
    tf=float(s.N(chosen_t,40));W=np.array([[1.,tf]])/np.sqrt(1+tf*tf)
    serial=[]
    for c in candidates:
        serial.append({'region':c['region'],'branch_index':c['branch_index'],
                       'bias_candidates':c['branches'],'objective':str(c['objective']),
                       'root':encode_root(c['root']),'loss_interval':[str(x) for x in c['bounds']],
                       'bias_formulas':[str(x) for x in c['bias']]})
    summary={'p':str(p),'branch_count':len(branches),'raw_root_count':len(raw_roots),
             'feasible_before_deduplication':len(feasible),'distinct_feasible_candidates':len(candidates),
             'strict_global_sharing_certificate':bool(certified),'unresolved_competitors':len(unresolved),
             'winner':{'region':winner['region'],'branches':winner['branches'],
                       'objective':str(winner['objective']),'root':encode_root(winner['root']),
                       'loss_interval':[str(x) for x in winner['bounds']],
                       't_approx':str(s.N(chosen_t,25)),
                       'loss_approx':str(s.N(sum(winner['bounds'])/2,25)),
                       'bias_formulas':[str(x) for x in winner['bias']]},
             'minimum_other_candidate_lower_bound':str(min(c['bounds'][0] for c in competitors)),
             'mono_first_loss':str(mono_first),'mono_second_loss':str(mono_second),
             'seconds':time.perf_counter()-start}
    write_json(folder/'all_branches.json',branches)
    write_json(folder/'all_root_feasibility_checks.json',raw_roots)
    write_json(folder/'feasible_candidates.json',serial)
    write_json(folder/'chart_endpoints.json',endpoints)
    write_json(folder/'certificate_summary.json',summary)
    return W,bias,summary


def evaluate(W,bias,p,sigma,detector):
    states,P=binary_population(2,float(p))
    midpoint=geometry(W,float(p))[-1]
    threshold=.5-bias if detector=='actual_decoder' else midpoint
    errors,fp,fn,_=exact_detection(W,states,P,threshold,sigma)
    per_mse=exact_decoder_mse(W,bias,states,P,sigma)
    return errors,fp,fn,per_mse


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--math-review',required=True,help='Saved independent mathematical approval file; required before execution.')
    parser.add_argument('--output',default='run_v1',help='Fresh output directory; existing directories refused.')
    args=parser.parse_args()
    base=Path(__file__).resolve().parent
    review=Path(args.math_review).resolve()
    if not review.is_file():
        raise SystemExit('Independent mathematics approval file is missing; no cases executed.')
    output=Path(args.output).resolve()
    output.mkdir(exist_ok=False,parents=True)
    source=output/'source_snapshot';source.mkdir()
    for name in ['run_frequency_verification.py','certificate_backend_snapshot.py','toy_math_snapshot.py','bridge_math_snapshot.py']:
        shutil.copy2(base/name,source/name)
    for name in ['protocol.md','verification_protocol.md']:
        shutil.copy2(base.parent/name,source/name)
    shutil.copy2(review,source/'independent_math_review.md')
    write_json(output/'settings.json',CONFIG)
    write_json(output/'environment.json',{'python':sys.version,'executable':sys.executable,
               'platform':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__,
               'sympy':s.__version__,'math_review_file':str(review)})
    start=time.perf_counter();risks=[];geometries=[];curve_rows=[];crossings=[];summaries=[]
    sigmas=np.geomspace(CONFIG['display_sigmas_min'],CONFIG['display_sigmas_max'],CONFIG['display_sigmas_count'])
    importance=np.array([1.,.5]);pc=s.Rational(3,2)-s.sqrt(5)/2
    for frequency in CONFIG['frequencies']:
        p=s.Rational(frequency);pf=float(p);case=f'p_{pf:.3f}'
        folder=output/case;folder.mkdir()
        if p<pc:
            try:
                W,bias,certificate=finite_certificate(p,folder)
            except Exception as exc:
                write_json(folder/'failure.json',{'error':str(exc),'case':frequency})
                raise
            if not certificate['strict_global_sharing_certificate']:
                write_json(folder/'failure.json',{'error':'Global value intervals not strictly separated; no automatic extra cases/refinement.',
                                                 'case':frequency})
                raise RuntimeError('Unresolved global sharing certificate at '+frequency)
            selected_type='strict computer-assisted global sharing certificate'
        else:
            W=np.array([[1.,0.]]);bias=np.array([0.,pf])
            certificate={'p':frequency,'selection':'reviewed theorem: mono above pc',
                         'mono_first_loss':str(p*(1-p)/2),'mono_second_loss':str(p*(1-p)),
                         'no_new_branch_enumeration_above_transition':True}
            write_json(folder/'theorem_selection.json',certificate)
            selected_type='reviewed global mono theorem above pc'
        models=[('clean_selected',W,bias),('mono_retain_0',np.array([[1.,0.]]),np.array([0.,pf])),
                ('mono_retain_1',np.array([[0.,1.]]),np.array([pf,0.]))]
        write_json(folder/'selected_models.json',[{'label':label,'W':w.tolist(),'bias':b.tolist()} for label,w,b in models])
        np.savez_compressed(folder/'selected.npz',W=W,bias=bias,p=pf)
        for label,w,b in models:
            G,d,V,B,M,midpoint=geometry(w,pf)
            mse=evaluate(w,b,p,0.,'actual_decoder')[-1]
            geometries.append({'p':pf,'p_rational':frequency,'label':label,'selection':selected_type if label=='clean_selected' else 'mono control',
                               'W_0':float(w[0,0]),'W_1':float(w[0,1]),'bias_0':float(b[0]),'bias_1':float(b[1]),
                               'd_0':float(d[0]),'d_1':float(d[1]),'G_01':float(G[0,1]),
                               'M_0':float(M[0]),'M_1':float(M[1]),'energy':float(np.sum(w*w)),
                               'clean_weighted_sum_mse':float(importance@mse)})
            for sigma in CONFIG['primary_sigmas']:
                for detector in ['actual_decoder','centered_midpoint']:
                    error,fp,fn,mse=evaluate(w,b,p,sigma,detector)
                    row={'p':pf,'p_rational':frequency,'label':label,'sigma':sigma,'detector':detector,
                         'weighted_sum_error':float(importance@error),'unweighted_sum_error':float(error.sum()),
                         'weighted_sum_mse':float(importance@mse),'unweighted_sum_mse':float(mse.sum())}
                    for i in range(2):
                        row.update({f'error_{i}':float(error[i]),f'fp_{i}':float(fp[i]),f'fn_{i}':float(fn[i]),f'mse_{i}':float(mse[i])})
                    risks.append(row)
        def difference(sigma):
            chosen=evaluate(W,bias,p,sigma,'actual_decoder')[0]
            mono=evaluate(models[1][1],models[1][2],p,sigma,'actual_decoder')[0]
            return float(importance@(chosen-mono))
        differences=[]
        for sigma in sigmas:
            selected_error=evaluate(W,bias,p,float(sigma),'actual_decoder')[0]
            mono_error=evaluate(models[1][1],models[1][2],p,float(sigma),'actual_decoder')[0]
            delta=float(importance@(selected_error-mono_error));differences.append(delta)
            curve_rows.append({'p':pf,'p_rational':frequency,'sigma':float(sigma),
                               'selected_weighted_error':float(importance@selected_error),
                               'mono_retaining0_weighted_error':float(importance@mono_error),'difference':delta})
        for lo,hi,flo,fhi in zip(sigmas[:-1],sigmas[1:],differences[:-1],differences[1:]):
            if abs(flo)<=1e-12 or abs(fhi)<=1e-12 or flo*fhi>=0:
                continue
            try:
                root,info=brentq(difference,float(lo),float(hi),xtol=1e-12,rtol=1e-12,maxiter=100,full_output=True,disp=False)
                crossings.append({'p':pf,'p_rational':frequency,'lower_sigma':float(lo),'upper_sigma':float(hi),
                                  'lower_difference':flo,'upper_difference':fhi,'root_sigma':float(root),
                                  'root_residual':difference(root),'converged':bool(info.converged),
                                  'iterations':int(info.iterations),'function_calls':int(info.function_calls)})
            except Exception as exc:
                crossings.append({'p':pf,'p_rational':frequency,'lower_sigma':float(lo),'upper_sigma':float(hi),
                                  'lower_difference':flo,'upper_difference':fhi,'failure':str(exc)})
        summaries.append({'p_rational':frequency,'selection_type':selected_type,'certificate':certificate})
        print('Completed frequency',frequency,selected_type,flush=True)
    write_csv(output/'geometry.csv',geometries);write_csv(output/'primary_risks.csv',risks)
    write_csv(output/'display_risk_curves.csv',curve_rows);write_json(output/'display_crossings.json',crossings)
    write_json(output/'summaries.json',summaries)
    # Discrete geometry/loss points are not interpolated into a geometry theorem.
    selected=[g for g in geometries if g['label']=='clean_selected'];pc_float=float(pc)
    fig,axes=plt.subplots(1,2,figsize=(11,4.2))
    axes[0].scatter([g['p'] for g in selected],[g['d_0'] for g in selected],label='selected energy: concept 0',marker='o')
    axes[0].scatter([g['p'] for g in selected],[g['d_1'] for g in selected],label='selected energy: concept 1',marker='s')
    axes[1].scatter([g['p'] for g in selected],[g['clean_weighted_sum_mse'] for g in selected],label='selected clean weighted MSE')
    mono=[g for g in geometries if g['label']=='mono_retain_0']
    axes[1].scatter([g['p'] for g in mono],[g['clean_weighted_sum_mse'] for g in mono],label='mono retaining 0',marker='x')
    for ax in axes:
        ax.axvline(pc_float,color='black',linestyle='--',label=r'proved $p_c=(3-\sqrt{5})/2$')
        ax.set_xlabel('concept activation probability p');ax.grid(alpha=.2);ax.legend(fontsize=8)
    axes[0].set_ylabel('squared encoder column norm');axes[0].set_ylim(-.04,1.04)
    axes[1].set_ylabel('clean importance-weighted sum MSE')
    fig.suptitle('Fixed-load storage transition: five certified points; no geometry interpolation')
    fig.tight_layout();fig.savefig(output/'storage_transition.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(2,3,figsize=(12,7),sharex=True)
    for ax,p in zip(axes.ravel(),[float(s.Rational(q)) for q in CONFIG['frequencies']]):
        rows=[r for r in curve_rows if r['p']==p]
        ax.semilogx([r['sigma'] for r in rows],[r['difference'] for r in rows],label='actual decoder: selected minus mono')
        ax.axhline(0,color='black',linewidth=.7)
        points=[r for r in risks if r['p']==p and r['label']=='clean_selected' and r['detector']=='actual_decoder' and r['sigma']>0]
        controls={r['sigma']:r['weighted_sum_error'] for r in risks if r['p']==p and r['label']=='mono_retain_0' and r['detector']=='actual_decoder'}
        ax.scatter([r['sigma'] for r in points],[r['weighted_sum_error']-controls[r['sigma']] for r in points],color='darkorange',label='primary noise settings')
        ax.set_title(f'p={p:g}');ax.set_xlabel('Gaussian code-noise sigma');ax.set_ylabel('weighted error difference');ax.grid(alpha=.2)
    axes.ravel()[-1].axis('off');axes.ravel()[0].legend(fontsize=7)
    fig.suptitle('Actual-decoder comparison: below zero favors sharing; numerical display interval only')
    fig.tight_layout();fig.savefig(output/'actual_risk_difference.png',dpi=180);plt.close(fig)
    write_json(output/'timings.json',{'seconds':time.perf_counter()-start})
    manifest={str(path.relative_to(output)):hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(output.rglob('*')) if path.is_file()}
    write_json(output/'sha256_manifest.json',manifest)
    print('Stopped after the five prescribed cases:',output,flush=True)


if __name__=='__main__':main()
