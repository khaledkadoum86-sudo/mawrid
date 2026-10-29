const CACHE = "mawrid-v2";
const PAGES = "mawrid-pages"; // صور صفحات الشروح: لا تُحذف عند التحديث
const CORE = ["./","index.html","quran.json","warsh.woff2","manifest.webmanifest","icon-180.png","icon-192.png","icon-512.png"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== PAGES).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) {
    e.respondWith(caches.open(CACHE).then(c => c.match(req).then(r => r || fetch(req).then(res => { c.put(req, res.clone()); return res; }))));
    return;
  }
  if (url.origin !== location.origin) return;
  // صفحات الكتب لا تتغير: من الكاش أولًا، وتُحفظ كل صفحة تُفتح
  if (url.pathname.includes("/pg/")) {
    e.respondWith(caches.open(PAGES).then(c => c.match(req, {ignoreSearch:true}).then(r => r || fetch(req).then(res => { if (res.ok) c.put(req, res.clone()); return res; }))));
    return;
  }
  e.respondWith(fetch(req).then(res => {
    const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res;
  }).catch(() => caches.match(req).then(r => r || caches.match("index.html"))));
});
