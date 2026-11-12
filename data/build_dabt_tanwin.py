# يضيف إلى mushaf/dmap.json ربط الكلمات بأبيات التنوين والنون الساكنة (462–478)
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json')); D=json.load(open(R+'mushaf/dmap.json'))
def toks(t): return [p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
TAN='ًٌٍٖٗٞ'; TARKIB='ًٌٍ'
VOW='َُِ'; SUK='ْ'; SH='ّ'; IQ='ۢ'
LMNR='لمنر'
CAT=collections.Counter(); EX=collections.defaultdict(list)
def add(key,ti,ids,cat,ref):
    d=D.setdefault(key,{}).setdefault(str(ti),[])
    for n in ids:
        if n not in d: d.append(n)
    CAT[cat]+=1
    if len(EX[cat])<10: EX[cat].append(ref)
def first_letter(tok):
    m=re.search('[ء-يے]',tok); 
    if not m: return '',False
    i=m.start(); return tok[i], SH in tok[i+1:i+3]
for s,a,t,*_ in q['a']:
    key=f'{s}:{a}'; T=toks(t)
    for ti,tok in enumerate(T):
        w=re.sub('[ۖ-ۜ ٠-٩]','',tok); ref=f'{s}:{a} {tok}'
        nxt=T[ti+1] if ti+1<len(T) else None
        nl,nsh=first_letter(re.sub('^ا[َُِ۪۬۟]*(?=ل)','',nxt)) if nxt else ('',False)
        # ---- التنوين
        tan=re.search('['+TAN+']',w); iq_t=re.search('['+VOW+']'+IQ+'$',w)
        if tan or iq_t:
            ids=[462]; cat='tanwin'
            if tan: ids.append(468)
            if re.search('ا['+TAN+']|['+TAN+']ا$',w) and re.search('[ًٗ]',w): ids.append(463)
            elif re.search('ء[ًٗ]',w): ids.append(464)
            elif re.search('ى[ًٗ]',w): ids.append(465)
            if iq_t and re.search('اَ?'+IQ+'$|َا'+IQ+'$',w): ids.append(463)
            if iq_t: ids.append(473); cat='tanwin-iqlab'
            elif nxt and nl in LMNR and nsh: ids.append(469); cat='tanwin-idgham'
            elif nxt and nl in 'وي': ids.append(470); cat='tanwin-waw-ya'
            add(key,ti,ids,cat,ref)
        # ---- النون الساكنة (لا في آخر الآية ولا في الفواتح)
        if a==1 and re.search('نٓ',w): continue
        for m in re.finditer('ن(?=['+SUK+IQ+']|[ء-يے]|$)',w):
            j=m.end(); after=w[j:j+1]
            if after==SUK:
                rest=w[j+1:]
                L2,sh2=first_letter(rest) if re.search('[ء-يے]',rest) else ((nl,nsh) if nxt else ('',False))
                if L2 in 'وي' and sh2: add(key,ti,[477],'nun-sukun-waw-ya',ref)
                elif L2 and L2 not in 'ءأإؤئهعحغخا': CAT['nun-sukun-other:'+L2]+=1; add(key,ti,[474],'nun-izhar?',ref)
                else: add(key,ti,[474],'nun-izhar',ref)
                continue
            if after==IQ: add(key,ti,[475],'nun-iqlab',ref); continue
            if after=='':   # آخر الكلمة
                if not nxt: continue
                L,shd=nl,nsh
            else:
                L=after; shd=SH in w[j+1:j+3]
            if L in 'وي' and shd: add(key,ti,[477],'nun-waw-ya',ref)
            elif shd: add(key,ti,[475,476],'nun-idgham',ref)
            else: add(key,ti,[475],'nun-ikhfa',ref)
for c,n in CAT.most_common(): print(n,c,EX[c])
json.dump(D,open(R+'mushaf/dmap.json','w'),ensure_ascii=False,separators=(',',':'))
print('words linked',sum(len(v) for v in D.values()))
