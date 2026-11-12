# يربط بأبيات الرسم التي لم يكن لها أي موضع مربوط: مطابقة بكلمات الفهرس مع ضوابط كتبتها لكل بيت
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json'));W=json.load(open(R+'mushaf/wmap.json'));WI=json.load(open(R+'mushaf/winfo.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
def clean(w): return re.sub('[ۖ-ۜ ٠-٩]','',w)
def bare(w): return re.sub('[ً-ٟۖ-ۭـ ٠-٩ٰٓ]','',w)
RULES=[ # (الأبيات، شرط على الكلمة مجردةً من الحركات، شرط على ما بعدها أو None)
 ([67],  lambda w,n: re.search('^(?:ال|ل)?خا?[طس][ـ]?ين$|^(?:ال)?خا?طـون$',w), None),
 ([72],  lambda w,n: re.search('سي[ـ]?ات',w), None),
 ([99],  lambda w,n: 'ميكئل' in w, None),
 ([116], lambda w,n: w in ('وبطل','بطل') and 'ٰ' in RAW, lambda w,n: n=='ما' ),
 ([127], lambda w,n: w=='بيدي', lambda w,n: n=='أستكبرت'),
 ([129], lambda w,n: w=='بسم', None),
 ([148], lambda w,n: w=='الـن' or w=='الان', None),
 ([185], lambda w,n: w=='فالق', lambda w,n: n and 'اصباح' in n),
 ([188], lambda w,n: re.match('^(?:و)?علم$',w), lambda w,n: n and n.endswith('لغيب')),
 ([211], lambda w,n: re.search('^[يت]ستخرون$',w), None),
 ([218], lambda w,n: re.search('ليواط[ـ]?وا',w), None),
 ([261,262,266,273], lambda w,n: re.search('^(?:[وف])?(خافون|ارهبون|اتقون|اسمعون|أطيعون|تكلمون|متاب|يسقين|تكفرون|أشركتمون|اعتزلون|تقربون|ليعبدون|تفضحون|ترجمون|نذير|نكير|تشهدون|تخزون|هدن|تفندون)$',w) and raw_ends_kasra, None),
 ([276], lambda w,n: re.search('حوارين$|حواريـن$|اميين$|اميـين$|امين$',w) and 'ۧ' in RAW, None),
 ([279], lambda w,n: re.search('ستحي$',w) and 'ۦ' in RAW, None),
 ([288], lambda w,n: re.search('يَ\u0640[\u0654\u064f]{2}وس',RAW) is not None, None),
 ([321], lambda w,n: w=='أنبؤا', None),
 ([341], lambda w,n: re.search('^(?:تايسوا|يايس|استيسوا|استيس)$',w.replace('ـ','')), None),
 ([344], lambda w,n: re.search('^(?:[وف])?إذا$',w) and 'ٗ' in RAW or re.search('ليكونا$|لاهب$|^(?:و)?كأين$',w), None),
 ([363], lambda w,n: re.search('اقصا$',w), None),
 ([381], lambda w,n: w in ('ترينے',) and '۪' in RAW, None),
 ([395], lambda w,n: w=='ربا' and 'ِ' in RAW, None),
 ([398,399,400], lambda w,n: w in ('أن','وأن','ان','وان'), lambda w,n: n and n.startswith('لا')),
 ([402], lambda w,n: w in ('من','فمن','لمن'), lambda w,n: n=='ما'),
 ([406,407], lambda w,n: w in ('أنما','انما','إنما') and n=='غنمتم', lambda w,n: True),
 ([406], lambda w,n: w in ('أنما','انما','إنما'), lambda w,n: n=='عند'),
 ([409], lambda w,n: w in ('أم','ام'), lambda w,n: n=='من'),
 ([410], lambda w,n: w=='ولات', None),
 ([411], lambda w,n: w in ('مال','فمال'), lambda w,n: n in ('هؤلاء','الذين','هذا')),
 ([412], lambda w,n: w in ('وحيث','حيث','يوم','قال'), lambda w,n: (W0 in ('وحيث','حيث') and n=='ما') or (W0=='يوم' and n=='هم') or (W0=='قال' and n=='ابن')),
 ([413], lambda w,n: w=='كل' and i>0 and bare(T[i-1])=='من', lambda w,n: n=='ما'),
 ([415,416], lambda w,n: w=='كلما', lambda w,n: n in ('ألقي','دخلت')),
 ([417], lambda w,n: w=='فے', lambda w,n: n=='ما'),
 ([426,427], lambda w,n: w=='بيسما', None),
 ([437], lambda w,n: w=='فبما', lambda w,n: n=='رحمة'),
 ([442], lambda w,n: w=='نعمة', lambda w,n: n=='ربے'),
]
CAT=collections.Counter(); ex=collections.defaultdict(list)
for s,a,t,*_ in q['a']:
    T=toks(t); k=f'{s}:{a}'
    for i,raw in enumerate(T):
        RAW=clean(raw); w=bare(raw).replace('\u0640','ـ'); W0=w; nx=bare(T[i+1]) if i+1<len(T) else None
        raw_ends_kasra=bool(re.search('\u0650[\u06e6]?$',RAW.replace('\u06d6','')))
        for ids,cw,cn in RULES:
            if not cw(w,nx): continue
            if cn and not cn(w,nx): continue
            spans=[i] if not cn else [i,i+1]
            for j in spans:
                old=W.setdefault(k,{}).get(str(j),[])
                new=old+[b for b in ids if b not in old]
                if new!=old:
                    W[k][str(j)]=new; WI.setdefault(k,{}).setdefault(str(j),[0,bare(T[j])])
                    CAT[ids[0]]+=1
                    if len(ex[ids[0]])<4: ex[ids[0]].append(f'{s}:{a} {T[j]}')
for b,n in sorted(CAT.items()): print(b,n,ex[b])
json.dump(W,open(R+'mushaf/wmap.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(WI,open(R+'mushaf/winfo.json','w'),ensure_ascii=False,separators=(',',':'))
