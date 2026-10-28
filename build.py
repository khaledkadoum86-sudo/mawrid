import json,shutil,os

data=open('data/data.json').read()
h=open('src/index.html').read().replace('/*DATA*/null',data)
open('index.html','w').write(h)
for f in ['sw.js','manifest.webmanifest','icon-180.png','icon-192.png','icon-512.png']: shutil.copy('src/'+f,f)
open('.nojekyll','w').close()
print('built',len(h))
