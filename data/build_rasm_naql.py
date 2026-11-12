import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json'));W=json.load(open(R+'mushaf/wmap.json'));WI=json.load(open(R+'mushaf/winfo.json'))
toks=lambda t:[p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
def key(w):
    w=re.sub('[ً-ٟۖ-ۭـ ٠-٩ٰٓ]','',w)
    w=re.sub('^([وفبلك]?)[اأإآء]+','\\1ا',w)          # الهمزة الأولى أو النقل
    w=re.sub('^(و?ال)[اأإآء]','\\1ا',w)              # نقل لام التعريف
    return re.sub('[أإآٱ]','ا',w)
L=collections.defaultdict(collections.Counter); INFO={}
occ=[]
for s,a,t,*_ in q['a']:
    for i,w in enumerate(toks(t)):
        k=key(w); l=tuple(sorted(n for n in W.get(f'{s}:{a}',{}).get(str(i),[]) if n<=454))
        if l: L[k][l]+=1; INFO.setdefault((k,l),WI[f'{s}:{a}'][str(i)])
        else: occ.append((s,a,i,w,k))
prop=[]
for s,a,i,w,k in occ:
    x=re.sub('([۪۬۟])([َُِ])',r'\2\1',w)
    naql=bool(re.match('^[وفبلك]?[َُِ]?ا(?:[َُِ](?![۪۬۟])|ٰ)',x)) or bool(re.match('^[وفبلك]?[َِ]?ا[َُِ]?۬?ل[َُِ]ا',x))
    if not naql or k not in L: continue
    l,c=L[k].most_common(1)[0]
    if c/sum(L[k].values())>=0.8 and sum(L[k].values())>=2:
        prop.append((s,a,i,w,list(l),INFO[(k,l)]))
print('naql-spelled unlinked words that match a consistently linked form:',len(prop))
cc=collections.Counter((p[3],tuple(p[4])) for p in prop)
for x,n in cc.most_common(40): print(n,x)
json.dump(prop,open('/home/claude/work/naql_prop.json','w'),ensure_ascii=False)
