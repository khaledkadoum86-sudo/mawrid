# يبني data/shuruh.json: لكل بيت صفحة بداية شرحه ونهايته في كل كتاب
# الخرائط (key_map.json) تُستخرج آليًا بمطابقة نص الأبيات مع صفحات الكتب الممسوحة (تعرّف ضوئي لا يُعرض في التطبيق)
import json,os,sys
W=sys.argv[1] if len(sys.argv)>1 else '/home/claude/work'
BOOKS={
 'dalil':{'t':'دليل الحيران على مورد الظمآن','a':'المارغني','ic':'د','dir':'pg/dalil/','n':853,'seg':[[2,1,'']],
          'src':'لإبراهيم بن أحمد المارغني التونسي (ت 1349هـ)، اعتنى به عبد العزيز بن ناصر المنصري، مركز القراءات القرآنية بالكويت، ط1، 1432هـ، ومعه «تنبيه الخلان على الإعلان».','only':'m'},
 'tanbih':{'t':'تنبيه الخلان على الإعلان','a':'المارغني','ic':'ت','dir':'pg/dalil/','n':853,'seg':[[2,1,'']],'nodl':1,
          'src':'للمارغني، شرح «الإعلان بتكميل مورد الظمآن» لابن عاشر، في آخر «دليل الحيران» من الطبعة نفسها.','only':'i','from':'dalil'},
 'fath':{'t':'فتح المنان المروي بمورد الظمآن','a':'ابن عاشر','ic':'ف','dir':'pg/fath/','n':1640,'seg':[],
          'src':'لعبد الواحد بن عاشر (ت 1040هـ)، دراسة وتحقيق د. عبد الكريم بوغزالة.','only':'m'},
 'tiraz':{'t':'الطراز في شرح ضبط الخراز','a':'التنسي','ic':'ط','dir':'pg/tiraz/','n':789,'seg':[],
          'src':'لأبي عبد الله محمد بن عبد الله التنسي (ت 899هـ)، دراسة وتحقيق د. أحمد بن أحمد شرشال، مجمع الملك فهد.','only':'m'},
}
meta=json.load(open('shuruh_meta.json')) if os.path.exists('shuruh_meta.json') else {}
books={}; mp={}
for b,B in BOOKS.items():
    src=B.get('from',b); f=f'{W}/{src}_map.json'
    if not os.path.exists(f): continue
    B=dict(B, **meta.get(b,{})); m=json.load(open(f))
    sz=sum(os.path.getsize(f'{W}/{src}/pg/{i}.png') for i in range(1,B['n']+1) if os.path.exists(f'{W}/{src}/pg/{i}.png'))
    B['mb']=round(sz/1e6)
    rng=B.pop('rng',None)
    cnt=0
    for vid,v in m.items():
        if not vid.startswith(B['only']+':'): continue
        n=int(vid.split(':')[1])
        if rng and not (rng[0]<=n<=rng[1]): continue
        mp.setdefault(vid,{})[b]=v; cnt+=1
    if cnt: books[b]={k:B[k] for k in ['t','a','ic','dir','n','seg','src','mb']+(['nodl'] if B.get('nodl') else [])}
    print(b,cnt)
json.dump({'books':books,'map':mp},open('shuruh.json','w'),ensure_ascii=False,separators=(',',':'))
