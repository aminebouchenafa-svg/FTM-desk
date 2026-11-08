import json,re,unicodedata,collections,difflib,datetime,sys
T=sys.argv[1] if len(sys.argv)>1 else '2026-11-08'
def norm(s):
    s=unicodedata.normalize('NFD',str(s)); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'\s+',' ',re.sub(r'[^A-Z0-9 ]',' ',s.upper())).strip()
PRE=('EL','AIT','BEN','OULD','SABER','HADJ','AHMED','NAIT','SAID','BRAHAM','LABBACI','LAMINE')
def split(n):
    w=norm(n).split()
    if not w: return '',''
    if w[0] in PRE and len(w)>2: return w[0]+' '+w[1], ' '.join(w[2:])
    if w[0] in PRE and len(w)==2: return w[0]+' '+w[1], ''
    return w[0], ' '.join(w[1:])
reg=json.load(open('w/pilotes.json'))['rows']
idx=collections.defaultdict(list)
for p in reg: sn,g=split(p['nom']); idx[sn].append((p,g))
keys=list(idx)
def cands(sn):
    C=idx.get(sn,[])
    if C: return C
    pref=[k for k in keys if k.startswith(sn+' ') or sn.startswith(k+' ')]
    if len(pref)==1: return idx[pref[0]]
    close=difflib.get_close_matches(sn,keys,n=2,cutoff=0.86)
    if len(close)==1: return idx[close[0]]
    return []
ev=json.load(open('ev.json'))
res={}; unk=collections.Counter(); amb=collections.Counter()
for n,date,sheet,kind in ev:
    sn,g=split(n)
    if sn in ('RECURRENT','DMRA'): continue
    C=cands(sn)
    if len(C)>1:
        g0=g.split(' ')[0] if g else ''
        C2=[c for c in C if g0 and c[1].startswith(g0[:3])] or [c for c in C if g0 and c[1][:1]==g0[:1]]
        if len(C2)!=1: amb[n]+=1; continue
        C=C2
    if not C: unk[sn]+=1; continue
    p=C[0][0]; r=res.setdefault(p['id'],{'id':p['id'],'nom':p['nom'],'dates':set(),'src':{}})
    r['dates'].add(date); r['src'][date]=sheet
rows=[]
for r in res.values():
    ds=sorted(r['dates']); past=[d for d in ds if d<=T]; fut=[d for d in ds if d>T]
    rows.append({'id':r['id'],'nom':r['nom'],'last':past[-1] if past else '','next':fut[0] if fut else '','n':len(ds),'lastSrc':r['src'].get(past[-1],'') if past else ''})
rows.sort(key=lambda x:norm(x['nom']))
json.dump(rows,open('simuhist_rows.json','w'),ensure_ascii=False)
print('pilotes',len(rows),'ambigus',sum(amb.values()),'inconnus (hors annuaire)',len(unk))
print(sorted(unk)[:80])
# échéances
def add6(d):
    y,m,dd=map(int,d.split('-')); m+=6; y+=(m-1)//12; m=(m-1)%12+1
    import calendar; dd=min(dd,calendar.monthrange(y,m)[1]); return f'{y}-{m:02d}-{dd:02d}'
c=collections.Counter()
for x in rows:
    if not x['last']: c['jamais (seulement futur)']+=1; continue
    e=add6(x['last']); cov = x['next'] and x['next']<=e
    days=(datetime.date.fromisoformat(e)-datetime.date.fromisoformat(T)).days
    c['expiré non programmé' if days<0 and not x['next'] else 'expiré mais programmé' if days<0 else '<30j non programmé' if days<=30 and not cov else 'ok']+=1
print(c)
