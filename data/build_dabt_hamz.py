# يبني mushaf/dmap.json: ربط كلمات المصحف بأبيات باب ضبط الهمز (ورش) آليًا من الرسم المكتوب
import json,re,sys,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json'))
V='َُِ'          # فتحة ضمة كسرة
MK='[ً-ٰٟۖ-ۭ]'  # كل العلامات
def toks(text): return [p for p in text.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
def ends_hamza(t):
    t=re.sub('[ ٠-٩ۖۗۘۙۚۛۜ]','',t); t=re.sub(MK,'',t)
    return t[-1:] in 'ءأإؤئ' or t.endswith('ـ')
CAT=collections.Counter(); EX=collections.defaultdict(list)
D={}
def add(key,ti,ids,cat,s,a,tok):
    d=D.setdefault(key,{}).setdefault(str(ti),[])
    for n in ids:
        if n not in d: d.append(n)
    CAT[cat]+=1
    if len(EX[cat])<25: EX[cat].append(f'{s}:{a} {tok}')
for s,a,t,*_ in q['a']:
    key=f'{s}:{a}'; T=toks(t)
    for ti,tok in enumerate(T):
        prev=T[ti-1] if ti else None
        w=re.sub('([۪۬۟])([َُِْ])',r'\2\1',tok.strip('\u00a0')).replace('آ','آ')
        cats=[]
        # ١) النقل: كلمة تبدأ بألف مجردة محركة بلا علامة وصل، أو «ال» بعدها لام محركة فألف
        if re.match(r'^ا[َُِ](?![۪۬۟])',w) or re.match(r'^اٰ',w):
            if prev and ends_hamza(prev): cats.append(('two-words-naql?',[529]))
            else: cats.append(('naql',[529]))
        elif re.match('^[وفبلك]?ا[َُِ]?۬?ل[َُِ]ا(?!ٓ)',w):
            cats.append(('naql-article',[529]))
        # ٢) همزتان من كلمتين: الثانية مبدلة حرفا متحركا (اَ۬ + حرف متحرك) أو مسهلة/مبدلة مدا (ا بلا حركة)
        if prev and ends_hamza(prev):
            if re.match(r'^ا[َُِ]۬[^\s][َُِ]',w) and not re.match(r'^ا[َُِ]۬ل[َُِ]ا(?!ٓ)',w): cats.append(('two-words-ibdal-mutaharrik',[508]))
            elif re.match(r'^ا(?![َُِٰ۪۬۟])[ء-ي]',w): cats.append(('two-words-agreed',[505]))
        # ٣) همزتان في كلمة: الثانية مسهلة (ءَآ)
        if 'ءَآ' in w:
            if re.search('ءَآمّ',w): cats.append(('hamza-then-alif',[515,504]))   # ءامّين: همزة واحدة
            elif re.search('ءَآللّ',w): cats.append(('aalaan',[533]))       # ءالله
            else: cats.append(('two-in-word-tasheel',[518,521,534]))
        # ٤) «ءالآن» وبابه مع الإبدال (آٰ)
        if 'آٰ' in w or 'آٰ' in w:
            if re.search('[ا][ٰٓ]{2}ل',w): cats.append(('aalaan',[533,529]))
            else: cats.append(('two-in-word-tasheel',[518,521,534,529]))
        # ٥) الهمز المتحرك المبدل واوا أو ياء (مؤجلا، يؤاخذ، لئلا)
        if re.search(r'[وي]َ۬',w): cats.append(('ibdal-mutaharrik',[506]))
        # ٦) همزة في أول الكلمة بعدها ألف (ءامنوا، ءادم، ءايات)
        if re.match('^(?:[وفبلك][َُِ]?){0,2}(?:ءَ|ـَٔ)ا(?![ٰٓ۬])',w): cats.append(('hamza-then-alif',[515,504]))
        if re.match('^(?:[وفبلك][َُِ]?){0,2}ءَا[ٰ۬]{2}م',w): cats.append(('aamantum-istifham',[525,526]))
        if re.match('^(?:[وفبلك][َُِ]?){0,2}ءَا[ٰ۬]{2}ل',w): cats.append(('aalihatuna',[524]))
        if re.match('^(?:[وفبلك][َُِ]?){0,2}(?:أَ۟|[أا]َوْ۟)',w) : cats.append(('two-in-word-mukhtalif',[518,522,523]))
        if re.match('^(?:[وفبلك][َُِ]?){0,2}أَ(?:ئِ|ي۪)',w) : cats.append(('two-in-word-mukhtalif',[518,522,524]))
        # ٧) همزة لا صورة لها: ء مفردة (غير ما سبق) أو على كرسي ـ
        rest=re.sub('^(?:[وفبلك][َُِ]?){0,2}(?:ءَ|ـَٔ)ا(?![ٓ])','',w).replace('ءَآ','')
        if 'ء' in rest or re.search('ـ[َُِْ]?[ٕٔ]',rest): cats.append(('no-image',[511,504]))
        # ٨) همزة لها صورة: أ إ ؤ ئ ۓ ي+ٔ
        if re.match('^أَلَٓ',w): continue   # فواتح السور
        if re.search(r'[أإؤئۓ]|[يے][َُِْ]?ٔ',w): cats.append(('image',[512,504]))
        for c,ids in cats: add(key,ti,ids,c,s,a,tok)
for c,n in CAT.most_common(): print(n,c,EX[c][:12])
json.dump(D,open('/home/claude/work/dmap_hamz.json','w'),ensure_ascii=False,separators=(',',':'))
print('words linked',sum(len(v) for v in D.values()))
json.dump(EX,open('/home/claude/work/ex.json','w'),ensure_ascii=False)
