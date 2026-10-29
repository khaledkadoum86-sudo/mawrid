# يبني data/quran.json من نص مجمع الملك فهد برواية ورش (الإصدار 10)
# المصدر: https://github.com/thetruetruth/quran-data-kfgqpc  (warsh/data/warshData_v10.json)
import json,sys
src=sys.argv[1] if len(sys.argv)>1 else '/home/claude/kfgqpc/warsh/data/warshData_v10.json'
d=json.load(open(src))
names={}
out=[]
for r in d:
    names[r['sura_no']]=r['sura_name_ar'].strip()
    out.append([r['sura_no'],r['aya_no'],r['aya_text'].replace('‏','').strip(),r['page'].split('-')[0].strip()])
json.dump({'n':[names[i] for i in range(1,115)],'a':out},open('quran.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(out))
