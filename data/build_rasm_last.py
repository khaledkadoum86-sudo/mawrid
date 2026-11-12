# آخر أبيات الرسم التي لم يكن لها موضع: بأييام 200، أن لن تحصوه 431، كلمة في الأعراف 447–448
import json
R='/home/claude/mawrid/'
W=json.load(open(R+'mushaf/wmap.json'));WI=json.load(open(R+'mushaf/winfo.json'))
for k,ti,ids,key in [('14:7','1',[200],'بأيام'),('73:18','20',[431],'أن'),('73:18','21',[431],'لن'),('7:136','12',[447,448],'كلمة')]:
    l=W.setdefault(k,{}).setdefault(ti,[])
    for b in ids:
        if b not in l: l.append(b)
    WI.setdefault(k,{}).setdefault(ti,[0,key])
json.dump(W,open(R+'mushaf/wmap.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(WI,open(R+'mushaf/winfo.json','w'),ensure_ascii=False,separators=(',',':'))
