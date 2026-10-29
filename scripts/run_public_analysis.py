"""Reproduce Exec Logic XRay aggregate metrics from disclosure-safe tabulation.
No association names, financial amounts or source PDFs are distributed.
Descriptive intervals are not population/survey confidence intervals.
"""
import csv,json,math,argparse
from pathlib import Path
GROUPS=['المدن الكبرى','المحافظات الأخرى']
def wilson(k,n):
    if n<=0:return None,None
    z=1.95996398454;p=k/n;den=1+z*z/n
    mid=(p+z*z/(2*n))/den
    half=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/den
    return round(mid-half,6),round(mid+half,6)
def summarize(path):
    with open(path,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    if not rows:raise ValueError('Empty aggregated input')
    fields={'group','confirmed_red','full5','cash_crit','unres_neg','count'}
    if not fields.issubset(rows[0]):raise ValueError('Missing fields')
    seen=set()
    for row in rows:
        if row['group'] not in GROUPS:raise ValueError('Unexpected group')
        k=tuple(row[c] for c in ['group','confirmed_red','full5','cash_crit','unres_neg'])
        if k in seen:raise ValueError('Duplicate aggregate combination')
        seen.add(k)
        if any(row[f] not in ('0','1') for f in ('confirmed_red','full5','cash_crit','unres_neg')):
            raise ValueError('Binary flags required')
        row['count']=int(row['count'])
        if row['count']<=0:raise ValueError('Invalid count')
    results=[]
    for g in [*GROUPS,'الكل']:
        group=[r for r in rows if g=='الكل' or r['group']==g]
        for metric in ('confirmed_red','full5_red','cash_crit','unres_neg'):
            subset=[r for r in group if metric!='full5_red' or r['full5']=='1']
            n=sum(r['count'] for r in subset)
            flag='confirmed_red' if metric=='full5_red' else metric
            k=sum(r['count'] for r in subset if r[flag]=='1')
            results.append(dict(group=g,metric=metric,n=n,count=k,share=round(k/n,6) if n else None,wilson95=wilson(k,n)))
    return results
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',default='data_clean/aggregated_indicator_counts.csv')
    ap.add_argument('--output',default='outputs/public_metrics.json')
    args=ap.parse_args()
    results=summarize(args.input)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
