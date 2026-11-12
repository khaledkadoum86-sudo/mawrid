# ربط صيغ أخرى للكلمات التي يذكرها الناظم بلفظ قريب، بعد مراجعتها واحدة واحدة
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json'));W=json.load(open(R+'mushaf/wmap.json'));WI=json.load(open(R+'mushaf/winfo.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
bare=lambda w: re.sub('[ً-ٟۖ-ۭ ٠-٩ٰٓ]','',w)
RUL=[
 ([80],      lambda b,w: re.fullmatch('(?:[وف]?أ?)?ذلكم[ا]?|أذلك',b) and 'ٰ' in w),
 ([182],     lambda b,w: re.fullmatch('(?:أ|ا)?(?:ف)?ريتم?|(?:أ|ا)ف?ريتكم|أفريت|اريتكم|أريتكم',b) and 'ٰ' in w),
 ([156,158], lambda b,w: re.search('يضعف',b) and 'ٰ' in w),
 ([198,199], lambda b,w: re.search('ادبر',b) and 'ٰ' in w),
 ([163,164], lambda b,w: re.search('مبرك',b) and 'ٰ' in w),
 ([144],     lambda b,w: re.fullmatch('(?:و)?لكنا',b) and 'ٰ' in w),
 ([115],     lambda b,w: re.search('بطل',b) and 'بَٰطِل' in w),
 ([151],     lambda b,w: re.fullmatch('أهؤلاء|أهذا|اهذا|اهؤلاء',b) and 'هَٰ' in w),
 ([147],     lambda b,w: 'ءَالَٰنَ' in w),
 ([311],     lambda b,w: 'ضُّعَفَٰٓؤُاْ' in w),
]
C=collections.Counter(); EX=collections.defaultdict(list)
for s,a,t,*_ in q['a']:
    k=f'{s}:{a}'
    for i,w in enumerate(toks(t)):
        if any(n<=254 or n==311 for n in W.get(k,{}).get(str(i),[])): continue
        b=bare(w)
        for ids,f in RUL:
            if f(b,w):
                l=W.setdefault(k,{}).setdefault(str(i),[])
                for x in ids:
                    if x not in l: l.append(x)
                WI.setdefault(k,{}).setdefault(str(i),[1,re.sub('[ً-ٟٓ]','',w).replace('ٰ','ا')])
                C[ids[0]]+=1; EX[ids[0]].append(f'{s}:{a} {w}'); break
for n,c in sorted(C.items()): print(n,c,EX[n][:6])
json.dump(W,open(R+'mushaf/wmap.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(WI,open(R+'mushaf/winfo.json','w'),ensure_ascii=False,separators=(',',':'))
