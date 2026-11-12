# يضيف إلى mushaf/dmap.json ربط الكلمات بأبيات المد من باب السكون والتشديد والمد (489–495)
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json')); D=json.load(open(R+'mushaf/dmap.json'))
def toks(t): return [p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
MD='ٓ'; HAR='[ً-ْ۪۬۟ۖ-ۜ]*'
CAT=collections.Counter(); EX=collections.defaultdict(list)
def add(key,ti,ids,cat,ref):
    d=D.setdefault(key,{}).setdefault(str(ti),[])
    for n in ids:
        if n not in d: d.append(n)
    CAT[cat]+=1
    if len(EX[cat])<12: EX[cat].append(ref)
for s,a,t,*_ in q['a']:
    key=f'{s}:{a}'
    for ti,tok in enumerate(toks(t)):
        w=tok.replace('آ','ا'+MD); ref=f'{s}:{a} {tok}'; cats=[]
        fawatih = bool(re.search('[لمسصعقكنره]'+HAR+MD,w)) and s!=0 and a==1 and len(re.sub('[^ء-ي]','',w))<=5
        if fawatih: cats.append(('fawatih',[492,493]))
        else:
            # مط على حرف مد مكتوب قبل همز أو ساكن (ما عدا الهمزتين في كلمة: ءَآ)
            w2=w.replace('ءَا'+MD,'')
            if re.search('[اويىے]'+HAR+MD,w2): cats.append(('madd-written',[490]))
            # حرف مد ساقط في الخط (ٰ ۥ ۦ) عليه مط
            if re.search('[ٰۥۦ]'+HAR+MD,w) or re.search(MD+HAR+'[ٰۥۦ]',w): cats.append(('madd-dropped',[492,493]))
            # الصلة والياء الزائدة بلا همز ولا سكون بعدها
            if re.search('[ۥۦ](?!'+HAR+MD+')',w) and not re.search('[ۥۦ]'+HAR+MD,w): cats.append(('sila-no-madd',[494]))
        # اللين قبل الهمز لورش: شَيْء، السَّوْء
        if re.search('َ[ويے]ْ'+HAR+'[ءـ]',w): cats.append(('leen-hamza',[491]))
        for c,ids in cats: add(key,ti,ids,c,ref)
for c,n in CAT.most_common(): print(n,c,EX[c])
json.dump(D,open(R+'mushaf/dmap.json','w'),ensure_ascii=False,separators=(',',':'))
print('words linked',sum(len(v) for v in D.values()))
