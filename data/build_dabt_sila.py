# يضيف إلى mushaf/dmap.json ربط همزات الوصل وجرة النقل بأبيات الصلة والابتداء والنقل (536–542)
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json')); D=json.load(open(R+'mushaf/dmap.json'))
def toks(t): return [p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
TAN='ًٌٍٖٗٞ'
CAT=collections.Counter(); EX=collections.defaultdict(list)
def add(key,ti,ids,cat,ref):
    d=D.setdefault(key,{}).setdefault(str(ti),[])
    for n in ids:
        if n not in d: d.append(n)
    CAT[cat]+=1
    if len(EX[cat])<10: EX[cat].append(ref)
JARRA={'َ':536,'ِ':537,'ُ':537}
for s,a,t,*_ in q['a']:
    key=f'{s}:{a}'; T=toks(t)
    for ti,tok in enumerate(T):
        ref=f'{s}:{a} {tok}'; prev=T[ti-1] if ti else ''
        m=re.match('^ا([َُِ])?([۪۬۟])?',tok)
        mm=re.match('^ا([۪۬۟])([َُِ])',tok)   # العلامتان بترتيب آخر
        if mm: v,x=mm.group(2),mm.group(1)
        elif m: v,x=m.group(1),m.group(2)
        else: v=x=None
        body=re.sub('^ا[\u064e\u064f\u0650\u06ec\u06ea\u06df]*','',tok)
        is_wasl=bool(re.match('ل(?:\u0652|[ء-ي]|[\u064e\u064f\u0650]ا(?!\u0653))|[ء-ي][\u0652\u0651]|[ء-ي]\u0651',body))
        art_naql=bool(re.match('ل[\u064e\u064f\u0650]ا(?!\u0653)',body))
        if v and x and not is_wasl: v=x=None; continue
        if v and x:                      # همزة وصل: الحركة موضع الجرة، والعلامة موضع نقطة الابتداء
            ids=[JARRA[v]]
            if re.search('['+TAN+']',prev): ids.append(538)
            ids+= [539,540]
            if x=='۟': ids.append(538)
            if art_naql: ids.append(541)
            add(key,ti,ids,'wasl',ref); continue
        if v and not x:                  # النقل: جرة النقل كجرة الوصل
            add(key,ti,[541],'naql-jarra',ref); continue
        p=re.match('^([وفبلك])([َِ])ا(?=ل[ْء-ي]|[ء-ي][ّْ])',tok)
        if p:                            # همزة وصل بعد حرف متصل
            add(key,ti,[JARRA[p.group(2)]],'wasl-after-prefix',ref); continue
        if re.match('^[وفبلك][َِ]?ال[َُِ]ا',tok) or re.match('^[وفبلك][َِ]ا[َُِ]',tok):
            add(key,ti,[541],'naql-jarra-after-prefix',ref)
for c,n in CAT.most_common(): print(n,c,EX[c])
json.dump(D,open(R+'mushaf/dmap.json','w'),ensure_ascii=False,separators=(',',':'))
print('words linked',sum(len(v) for v in D.values()))
