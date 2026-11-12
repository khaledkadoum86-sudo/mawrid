# يربط كلمات الألف المحذوفة غير المربوطة بالبيت الذي يذكرها بلفظها في نص «مورد الظمآن» (الكلمة في البيت مكتوبة بالألف الصغيرة ٰ)
import json,re,collections,csv
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json'));M=json.load(open(R+'mushaf/mawrid.json'))['m']
W=json.load(open(R+'mushaf/wmap.json'));WI=json.load(open(R+'mushaf/winfo.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
def sk(w):
    w=re.sub('[ً-ٟۖ-ۭـ ٠-٩ٰٓ«»:،.()]','',w); w=re.sub('[إأآٱء]','ا',w)
    return w.replace('ے','ي').replace('ى','ي').replace('ة','ه')
PRE=['وال','فال','بال','لل','ال','و','ف','ب','ل','ك']
SUF=['كما','هما','كم','هم','هن','نا','ها','ه','ك','ي','ا']
def stems(w):
    s=sk(w); out={s}
    for p in PRE:
        if s.startswith(p) and len(s)-len(p)>=3: out.add(s[len(p):])
    for x in list(out):
        for f in SUF:
            if x.endswith(f) and len(x)-len(f)>=3: out.add(x[:-len(f)])
    return out
B=collections.defaultdict(set)
for n,(h1,h2) in enumerate(M,1):
    if n<44 or n>254: continue
    for w in (h1+' '+h2).split():
        if 'ٰ' in w:
            for st in stems(w): B[st].add(n)
added=0; forms=collections.Counter(); done=set()
for s,a,t,*_ in q['a']:
    for i,w in enumerate(toks(t)):
        x=re.sub('[ً-ٟ۪۬۟ٓ]','',w)
        x=re.sub('^([وفبلك]?)اٰ',r'\1ا',x)   # «اٰ» في أول الكلمة نقلٌ، لا ألف محذوفة
        if not re.search('[^ىيےوٰ]ٰ',x): continue
        k=f'{s}:{a}'
        if any(n<=454 for n in W.get(k,{}).get(str(i),[])): continue
        bs=set()
        for st in stems(w): bs|=B.get(st,set())
        if len(bs)!=1 or sk(w) in ('لغيه',): continue
        old=W.setdefault(k,{}).get(str(i),[])
        W[k][str(i)]=old+[b for b in sorted(bs) if b not in old]
        WI.setdefault(k,{})[str(i)]=[1,re.sub('[ً-ٟۖ-ۭـ ٠-٩ٓ]','',w).replace('ٰ','ا')]
        added+=1; forms[(sk(w),tuple(sorted(bs)))]+=1; done.add(sk(w))
json.dump(W,open(R+'mushaf/wmap.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(WI,open(R+'mushaf/winfo.json','w'),ensure_ascii=False,separators=(',',':'))
print('linked occurrences',added,'forms',len(forms))
for f,n in forms.most_common(): print(n,f[0],f[1][0],'|',' — '.join(M[f[1][0]-1]))
json.dump(sorted(done),open('/home/claude/work/hadhf_done.json','w'),ensure_ascii=False)
