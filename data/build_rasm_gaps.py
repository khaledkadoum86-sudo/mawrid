# يملأ أبيات الرسم (44–454) التي لها كلمات في الفهرس ولم تُربط بأي موضع من المصحف
import json,re,collections,sys
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json'));M=json.load(open(R+'mushaf/mawrid.json'))['m']
W=json.load(open(R+'mushaf/wmap.json'));WI=json.load(open(R+'mushaf/winfo.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
def nk(w):   # مفتاح مطابقة متسامح: بلا حركات ولا ألف صغيرة ولا ياء/واو صغيرة، والهمزات كلها ألف
    w=re.sub('[ً-ٟۖ-ۭـ ٠-٩ٰٓ«»:،.()\\[\\]]','',w)
    w=re.sub('[إأآٱءؤئ]','ا',w).replace('ے','ي').replace('ى','ي').replace('ة','ه')
    w=re.sub('ا+','ا',w)
    return w
def strip_pre(k):
    out={k}
    for p in ['وال','فال','بال','لل','ال','و','ف','ب','ل']:
        if k.startswith(p) and len(k)-len(p)>=2: out.add(k[len(p):])
    return out
cnt=collections.Counter(n for d in W.values() for l in d.values() for n in l)
IDX={}
for line in open(R+'data/index.tsv',encoding='utf-8'):
    if '\t' in line:
        n,v=line.rstrip('\n').split('\t',1); IDX[int(n)]=[t.strip() for t in v.split('،') if t.strip()]
gap=[n for n in range(44,455) if cnt[n]==0 and n in IDX]
A=[(s,a,toks(t)) for s,a,t,*_ in q['a']]
res=collections.defaultdict(list)
for n in gap:
    for term in IDX[n]:
        parts=[nk(x) for x in term.split()]
        for s,a,T in A:
            K=[nk(x) for x in T]
            for i in range(len(K)-len(parts)+1):
                ok = parts[0] in strip_pre(K[i]) or K[i]==parts[0]
                ok = ok and all(K[i+j]==parts[j] or parts[j] in strip_pre(K[i+j]) for j in range(1,len(parts)))
                if ok: res[n].append((s,a,i,len(parts),' '.join(T[i:i+len(parts)]),term))
for n in gap:
    r=res[n]; print(n,len(r),'|',' — '.join(M[n-1]),'|',[x[4]+' '+str(x[0])+':'+str(x[1]) for x in r[:6]])
json.dump({n:res[n] for n in gap},open('/home/claude/work/gaps.json','w'),ensure_ascii=False)
