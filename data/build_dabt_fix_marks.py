# كلمات تبدأ بألف عليها علامة وحدها (۟ أو ۪) دون حركة: نقلٌ بعد ساكن أو تنوين، أو همزة ثانية مسهلة بعد همز
import json,re
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json')); D=json.load(open(R+'mushaf/dmap.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
n=0
prevtok=''
for s,a,t,*_ in q['a']:
    T=toks(t); k=f'{s}:{a}'
    for i,w in enumerate(T):
        prev=re.sub('[ۖ-ۜ ٠-٩]','',T[i-1] if i else prevtok)
        if re.match('^ا[۪۟](?![َُِ])',w):
            hamza_before=bool(re.search('[ءأإ][َُِ]?$',prev))
            ids=[505,504] if hamza_before else [529,541]
            l=D.setdefault(k,{}).setdefault(str(i),[])
            l[:]=[x for x in l if x not in (460,461)]
            for b in ids:
                if b not in l: l.insert(ids.index(b),b)
            n+=1
    prevtok=T[-1] if T else ''
json.dump(D,open(R+'mushaf/dmap.json','w'),ensure_ascii=False,separators=(',',':'))
print('fixed',n)
