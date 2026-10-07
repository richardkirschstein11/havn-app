#!/usr/bin/env python3
"""Build the HAVN demo app: src/app.html + src/images.json -> dist/artifact.html (body only, for the Claude artifact) and dist/index.html (full document for hosting / download)."""
import json, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
tpl = open('src/app.html').read()
imgs = json.load(open('src/images.json'))
import segno
qrs = {}
for room in ['S-01','S-02','S-03','S-04','S-05','D-01','D-02','D-03','D-04','H-01','H-02']:
    q = segno.make('https://havn.rest/key/' + room + '/7F2K-DEMO', error='m')
    qrs[room] = q.svg_inline(scale=4, border=0, dark='#141414', light=None)
body = tpl.replace('{{IMAGES}}', json.dumps(imgs)).replace('{{QRS}}', json.dumps(qrs))
os.makedirs('dist', exist_ok=True); os.makedirs('docs', exist_ok=True)
open('dist/artifact.html', 'w').write(body)
head = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="HAVN">
<meta name="theme-color" content="#141414">
<meta name="description" content="HAVN — Rest, on demand. Private recovery rooms by the hour. Investor demo of the guest journey.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" sizes="180x180" href="icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<style>html{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box;background:#F4F2EE}html:has(body.dark){background:#141414}</style>
<script>if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register('./sw.js').catch(function(){})})}</script>
'''
# move <title> and the Google Fonts <link> into <head>
m_title = re.search(r'<title>.*?</title>\n', body); m_link = re.search(r'<link rel="stylesheet"[^>]*>\n', body)
rest = body.replace(m_title.group(0), '').replace(m_link.group(0), '')
full = head + m_title.group(0) + m_link.group(0) + '</head>\n<body>\n' + rest + '\n</body>\n</html>\n'
open('dist/index.html', 'w').write(full)
open('docs/index.html', 'w').write(full)
import shutil
for f in ('icon-180.png', 'icon-192.png', 'icon-512.png'):
    shutil.copy('dist/' + f, 'docs/' + f)
json.dump({"name": "HAVN", "short_name": "HAVN", "id": "./", "description": "Rest, on demand. Private recovery rooms by the hour.", "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait", "background_color": "#141414", "theme_color": "#141414", "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, open('docs/manifest.webmanifest', 'w'), indent=1)
open('docs/sw.js', 'w').write('''const C = 'havn-' + %s;
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(['./', './index.html', './icon-180.png', './icon-192.png', './icon-512.png', './manifest.webmanifest']))); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const cp = r.clone(); caches.open(C).then(c => c.put(e.request, cp)); return r; }).catch(() => caches.match(e.request).then(m => m || caches.match('./index.html'))));
});
''' % repr(__import__('time').strftime('%%Y%%m%%d%%H%%M')))
print('artifact.html', len(body)//1024, 'KB ·', 'index.html', len(full)//1024, 'KB')
