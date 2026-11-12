# يضيف إلى mushaf/dmap.json: الإمالة والإشمام، إذاً ونون التوكيد الخفيفة، السكون والتشديد، الإدغام، ثم الحركات لكل كلمة لم تُربط بعد
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json')); D=json.load(open(R+'mushaf/dmap.json')); W=json.load(open(R+'mushaf/wmap.json'))
def toks(t): return [p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
CAT=collections.Counter(); EX=collections.defaultdict(list)
def add(key,ti,ids,cat,ref):
    d=D.setdefault(key,{}).setdefault(str(ti),[])
    for n in ids:
        if n not in d: d.append(n)
    CAT[cat]+=1
    if len(EX[cat])<10: EX[cat].append(ref)
CONS='بتثجحخدذرزسشصضطظعغفقكلمهة'   # حروف تقبل الإدغام (دون النون وحروف المد)
for s,a,t,*_ in q['a']:
    key=f'{s}:{a}'; T=toks(t)
    for ti,tok in enumerate(T):
        ref=f'{s}:{a} {tok}'; w=re.sub('[ۖ-ۜ ٠-٩]','',tok)
        body=re.sub('^ا[َُِ۪۬۟]*','',w)
        nxt=T[ti+1] if ti+1<len(T) else ''
        if re.search('[ء-ئ][ً-ْٰ]*۪',body): add(key,ti,[480],'imala',ref)
        if 'س۬' in w: add(key,ti,[481,479],'ishmam',ref)
        if re.match('^[وف]?َ?(إِذا[ًٗ]|لَنَسْفَعا|لَيَكُونا[ًٗ])',w): add(key,ti,[467],'idhan-nun-khafifa',ref)
        # الإدغام الناقص: ساكن مصوَّر بعده تاء مشددة (بسطتّ، أحطتّ)
        if re.search('[طد]ْتّ',w): add(key,ti,[500,501],'idgham-naqis',ref)
        # الإدغام التام: حرف معرّى بعده حرف مشدد في الكلمة نفسها، أو في آخرها وأول ما بعدها مشدد
        elif re.search('['+CONS+'](?=[ء-ي]ّ)',body) or (re.search('['+CONS+']$',w) and re.match('^[ء-ي]ّ',re.sub('^ا[َُِ۪۬۟]*','',nxt) if nxt else '')):
            add(key,ti,[499],'idgham-tam',ref)
        if 'ّ' in w: add(key,ti,[483,484],'shadda',ref)
        if 'ْ' in w: add(key,ti,[483],'sukun',ref)
# كل كلمة لم تُربط بعد بشيء: حكم الحركات
for s,a,t,*_ in q['a']:
    key=f'{s}:{a}'
    for ti,tok in enumerate(toks(t)):
        if not (W.get(key,{}).get(str(ti)) or D.get(key,{}).get(str(ti))):
            add(key,ti,[460,461],'harakat-only',f'{s}:{a} {tok}')
for c,n in CAT.most_common(): print(n,c,EX[c])
json.dump(D,open(R+'mushaf/dmap.json','w'),ensure_ascii=False,separators=(',',':'))
tot=sum(1 for r in q['a'] for _ in toks(r[2])); lk=sum(len(v) for v in D.values())
print('words linked',lk,'of',tot)
