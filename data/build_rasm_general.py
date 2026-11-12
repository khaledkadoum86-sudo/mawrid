# القواعد العامة في حذف الألف (كما في تطبيق «مورد الظمآن»): جمع المذكر 48/50، جمع المؤنث 49/50، المثنى 117، بين لامين 150، يا النداء وها التنبيه 151
# تُطبَّق فقط على كلمة فيها ألف محذوفة (ٰ) في الموضع الذي تذكره القاعدة، ولم تُربط ببيت حذف من قبل
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json'));W=json.load(open(R+'mushaf/wmap.json'));WI=json.load(open(R+'mushaf/winfo.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
P='(?:[وفبلك][َُِ]?){0,2}(?:ا[َُِ]?[۪۬]?ل[ْ]?|ال)?'
RUL=[
 ('ha-tanbih',[151], re.compile('^'+P+'هَٰ')),
 ('ya-nida',[151], re.compile('^'+P+'يَٰ')),
 ('bayna-lamayn',[150], re.compile('لَٰل')),
 ('muthanna',[117], re.compile('َٰنِ$')),
 ('jam-muannath',[49,50], re.compile('َٰتِ?[ً-ِٖٗٞ]?(?:هِ|هُ|هَا|هِمْ|هُمْ|كُمْ|نَا|ي|ے)?[ۥۦٓ]*$')),
]
C=collections.Counter(); EX=collections.defaultdict(list); left=collections.Counter()
for s,a,t,*_ in q['a']:
    k=f'{s}:{a}'
    for i,raw in enumerate(toks(t)):
        w=re.sub('[ۖ-ۜ ٠-٩]','',raw)
        x=re.sub('^([وفبلك]?)اٰ',r'\1ا',re.sub('[۪۬۟]','',w))
        if not re.search('[^ىيےوٰ]ٰ',re.sub('[ً-ْٓ]','',x)): continue
        if any(n<=254 for n in W.get(k,{}).get(str(i),[])): continue
        hit=None
        for name,ids,rx in RUL:
            if rx.search(w): hit=(name,ids); break
        if not hit: left[re.sub('[ً-ٰٟٓ]','',w)]+=1; continue
        l=W.setdefault(k,{}).setdefault(str(i),[])
        for b in hit[1]:
            if b not in l: l.append(b)
        WI.setdefault(k,{}).setdefault(str(i),[1,re.sub('[ً-ٟٓ]','',w).replace('ٰ','ا')])
        C[hit[0]]+=1
        if len(EX[hit[0]])<12: EX[hit[0]].append(f'{s}:{a} {raw}')
for n,c in C.most_common(): print(c,n,EX[n])
print('left',sum(left.values()),'forms',len(left)); print(left.most_common(50))
json.dump(W,open(R+'mushaf/wmap.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(WI,open(R+'mushaf/winfo.json','w'),ensure_ascii=False,separators=(',',':'))
