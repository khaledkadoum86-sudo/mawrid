# يضيف إلى mushaf/dmap.json: إلحاق المحذوف (544–563)، المزيد في الهجاء (565–572)، لام ألف (573–578)
import json,re,collections
R='/home/claude/mawrid/'
q=json.load(open(R+'quran.json')); D=json.load(open(R+'mushaf/dmap.json'))
def toks(t): return [p for p in t.split(' ') if p and re.search('[ء-ي]',re.sub('[٠-٩]','',p))]
CAT=collections.Counter(); EX=collections.defaultdict(list)
def add(key,ti,ids,cat,ref):
    d=D.setdefault(key,{}).setdefault(str(ti),[])
    for n in ids:
        if n not in d: d.append(n)
    CAT[cat]+=1
    if len(EX[cat])<10: EX[cat].append(ref)
H='[ً-ْٰۥۦ۪ٕ۬۟ٓٔ]*'
SA='ٰ'; SUK='ْ'
for s,a,t,*_ in q['a']:
    key=f'{s}:{a}'
    for ti,tok in enumerate(toks(t)):
        ref=f'{s}:{a} {tok}'; w=re.sub('[ۖ-ۜ ٠-٩]','',tok)
        # ---------- اسم الله
        if re.search('ل[َِّ]*ل?[َِّ]*ه[َُِ]', w) and re.search('(^|[وفبلت]?[َِ]?)(ا[^ء-ي]*)?لل?[^ء-ي]*ه[َُِ](مَّ)?$',w) and not re.search('[ء-ي]ل[^ء-ي]*ل[^ء-ي]*ه',re.sub('^[وفبلت][َِ]?','',re.sub('^ا[^ء-ي]*','',w))[1:] if False else ''):
            if re.fullmatch('(?:[وفبت][َُِ]?)?(?:ا[^ء-ي]*)?(?:ل[^ء-ي]*)?ل[^ء-ي]*ه[َُِ](?:مَّ)?',w): add(key,ti,[557],'allah',ref)
        if re.fullmatch('(?:[وفب][َُِ]?)?(?:ا[^ء-ي]*)?ل[^ء-ي]*لَٰ?تَ',w): add(key,ti,[557],'allat',ref)
        # ---------- الألف المحذوفة الملحقة (ٰ)
        for m in re.finditer(SA,w):
            i=m.start(); before=re.sub(H+'$','',w[:i])[-1:] if i else ''
            final = not re.search('[ء-ي]',w[i+1:])
            if before in 'ىيے': add(key,ti,[553,554] if final else [553],'alif-on-ya',ref)
            elif before=='و': add(key,ti,[553],'alif-on-waw',ref)
            elif before=='ل': add(key,ti,[555,556],'alif-with-lam',ref)
            elif before: add(key,ti,[552],'alif-dropped-middle',ref)
        # ---------- إلحاق أول المثلين وما بني عليه اللفظ
        if 'ۧ' in w: add(key,ti,[544,545,546],'ya-mulhaqa-nabiyyin',ref)
        if re.search('وُ'+'ۥ',w): add(key,ti,[547] if re.search('يَلْو',w) else [549],'waw-mulhaqa',ref)
        if re.search('ٰٓءَا$',w): add(key,ti,[546],'taraa',ref)
        if 'ۨ' in w: add(key,ti,[559],'nunji',ref)
        if re.search('إِۦلَ',w): add(key,ti,[558],'ilaf',ref)
        if re.search('يِ'+'ۦ',w): add(key,ti,[559],'hayiya',ref)
        if re.search('أَوْلِيَآ[ؤئ]',w): add(key,ti,[560,561],'awliya-mudmar',ref)
        if re.search('جَزَٰ?ٓ?ؤُهُ',w): add(key,ti,[562],'jazauhu',ref)
        # ---------- المزيد في الهجاء (الدارة)
        zaid=False
        for m in re.finditer('ا'+SUK,w):
            zaid=True; pre=w[:m.start()]
            if re.search('م[\u0651\u0650]*$',pre): add(key,ti,[567,571],'zaid-alif-miah',ref)
            elif re.search('[تي]َ$',pre) and re.search('يْـ?[َٔ]*س',w): add(key,ti,[567,571],'zaid-alif-tayasu',ref)
            elif re.search('ل[َِ][أإ][َِ]?$',pre): add(key,ti,[565,566,571],'zaid-alif-laadhbahanna',ref)
            elif w[m.end():m.end()+1] and w[m.end():m.end()+1] in 'يے': add(key,ti,[567,571],'zaid-alif-jai',ref)
            elif re.search('ؤ[\u064b-\u065f]*$',pre): add(key,ti,[568,571],'zaid-alif-after-hamza-waw',ref)
            elif re.search('و'+H+'$',pre): add(key,ti,[568,571],'zaid-alif-after-waw',ref)
            else: add(key,ti,[571],'zaid-alif-other',ref)
        if re.search('ُو'+SUK,w): zaid=True; add(key,ti,[569,571],'zaid-waw',ref)
        if re.search('يْيْ|ي'+SUK+'ي'+SUK,w): zaid=True; add(key,ti,[570,571],'zaid-ya-bi-ayd',ref)
        elif re.search('[ِ][يے]'+SUK,w): zaid=True; add(key,ti,[569,571],'zaid-ya',ref)
        if re.search('يِّيكُمُ',w) and re.search('بِأَ',w): add(key,ti,[572],'bi-ayyikum',ref)
        # إن لم يكن في الكلمة سكون حقيقي فلا يُربط بباب السكون
        if zaid:
            real=re.sub('ا'+SUK+'|ُو'+SUK+'|[ِ][يے]'+SUK+'|يْيْ','',w)
            if SUK not in real and key in D and str(ti) in D[key] and 483 in D[key][str(ti)] and 'ّ' not in w:
                D[key][str(ti)].remove(483); CAT['removed-483']+=1
        # ---------- لام ألف
        if re.search('ل'+'[َُِّ]*'+'[اأإآ]',w) and not re.search('ل[^ء-ي]*'+SA,w):
            ids=[573]
            if re.search('ل[^ء-ي]*[أإ]',w): ids+=[574,577]
            if re.search('ل[^ء-ي]*(?:آ|آ)',w): ids+=[575,576]
            if re.search('ل[^ء-ي]*(?:آ|ا)ٓ?ء',w): ids+=[578]
            add(key,ti,ids,'lam-alif',ref)
# الحركات (460–461) تبقى فقط للكلمة التي لا بيت لها غيرها
for k,d in D.items():
    for ti,l in d.items():
        if set(l)-{460,461} and (460 in l or 461 in l):
            d[ti]=[n for n in l if n not in (460,461)]; CAT['harakat-removed']+=1
for c,n in CAT.most_common(): print(n,c,EX[c][:8])
json.dump(D,open(R+'mushaf/dmap.json','w'),ensure_ascii=False,separators=(',',':'))
