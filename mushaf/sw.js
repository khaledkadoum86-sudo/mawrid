const CACHE="mushaf-core-v32";
const PAGES="mushaf-pages"; // صور الصفحات لا تتغير
const CORE=["./","index.html","mawrid.json","wmap.json","vmap.json","boxes.json","winfo.json","thumn.json","mg.json","khilaf.json","tiraz.json","dmap.json","manifest.webmanifest","../quran.json","../warsh.woff2","icon-180.png","icon-192.png","icon-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE.map(u=>new Request(u,{cache:"reload"})))).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("mushaf-core")&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{
  const req=e.request;if(req.method!=="GET")return;
  const url=new URL(req.url);
  if(/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)){
    e.respondWith(caches.open(CACHE).then(c=>c.match(req).then(r=>r||fetch(req).then(res=>{c.put(req,res.clone());return res}))));return;}
  if(url.origin!==location.origin)return;
  if(/\/mushaf\/(qp|mp)\/|\/pg\/tiraz\//.test(url.pathname)){
    e.respondWith(caches.open(PAGES).then(c=>c.match(req,{ignoreSearch:true}).then(r=>r||fetch(req).then(res=>{if(res.ok)c.put(req,res.clone());return res}))));return;}
  // الصفحة نفسها: من الشبكة أولًا (فيصل كل تحديث فورًا)، ومن الكاش عند انقطاع الإنترنت
  if(req.mode==="navigate"||/\/mushaf\/(index\.html)?$/.test(url.pathname)){
    e.respondWith(caches.open(CACHE).then(c=>{
      const net=fetch(req,{cache:"no-cache"}).then(res=>{if(res.ok)c.put(req,res.clone());return res});
      const late=new Promise(r=>setTimeout(r,4000)).then(()=>c.match(req,{ignoreSearch:true}));
      return Promise.race([net.catch(()=>c.match(req,{ignoreSearch:true})),late.then(r=>r||net)]);
    }));return;}
  // البيانات: من الكاش فورًا، وتُحدَّث في الخلفية
  e.respondWith(caches.open(CACHE).then(c=>c.match(req,{ignoreSearch:true}).then(r=>{
    const net=fetch(req).then(res=>{if(res.ok)c.put(req,res.clone());return res}).catch(()=>r);
    return r||net;})));
});
