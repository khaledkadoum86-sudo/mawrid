# الهمز الساكن فاءً للكلمة يبدله ورش حرف مد (يومنون، ياكلون، ياتيهم، الماوى…): يربط بالبيت 505 «سُهِّل بين بين أو بالبدل»
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json')); D=json.load(open(R+'mushaf/dmap.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
bare=lambda w: re.sub('[ً-ٟۖ-ۭ ٠-٩ٰٓ]','',w)
RX=re.compile('^(?:و|ف)?(?:ل)?(?:ال)?([يتنم])([وا])(من|كل|خذ|ت|تي|تو|مر|وي|وى|لم|ذن|ثم|جر|فك|مل|سر|سن|هل|نس|بى|لف|صد)')
NOT=re.compile('^(?:و|ف|ب|ل)?(?:ال)?(?:موت|مات|توكل|يونس)|^(?:و|ف)?ماتوا$')   # الموت، مات، توكّل، يونس: ليست من هذا الباب
C=collections.Counter(); n=0
for s,a,t,*_ in q['a']:
    k=f'{s}:{a}'
    for i,w in enumerate(toks(t)):
        b=bare(w)
        if re.search('[ءأإؤئ]',w) or not RX.match(b) or NOT.match(b): continue
        l=D.setdefault(k,{}).setdefault(str(i),[])
        l[:]=[x for x in l if x not in (460,461)]
        if 505 not in l: l.insert(0,505); n+=1; C[b]+=1
json.dump(D,open(R+'mushaf/dmap.json','w'),ensure_ascii=False,separators=(',',':'))
print('linked',n,'forms',len(C)); print(C.most_common(25))
