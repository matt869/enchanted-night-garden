/* Enchanted Night Garden — service worker.
 *
 * Makes the garden installable and fully usable offline. Bump CACHE whenever
 * a precached file changes; the old cache is dropped on activate.
 */
const CACHE = 'night-garden-v7';

/* Everything the garden needs to open with no network at all. Audio is left
 * out on purpose — it can be large, and it is cached on first play instead. */
const SHELL = [
    './',
    './index.html',
    './manifest.webmanifest',
    './vendor/three.min.js',
    './icons/icon-192.png',
    './icons/icon-512.png',
    './icons/icon-maskable-512.png',
    './icons/apple-touch-icon.png'
];

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(CACHE)
            // addAll is all-or-nothing, so add individually: one missing
            // optional file must not fail the whole install
            .then(function (cache) {
                return Promise.all(SHELL.map(function (url) {
                    return cache.add(url).catch(function () {});
                }));
            })
            .then(function () { return self.skipWaiting(); })
    );
});

self.addEventListener('activate', function (event) {
    event.waitUntil(
        caches.keys()
            .then(function (keys) {
                return Promise.all(keys.map(function (k) {
                    return k === CACHE ? null : caches.delete(k);
                }));
            })
            .then(function () { return self.clients.claim(); })
    );
});

self.addEventListener('message', function (event) {
    if (event.data === 'SKIP_WAITING') self.skipWaiting();
});

function isAudio(url, request) {
    return request.destination === 'audio' || /\/audio\/[^/]+\.(mp3|m4a|ogg|wav|aac|flac)$/i.test(url.pathname);
}

/* Media is fetched with Range headers (Safari always does), and handing a
 * browser a full 200 response to a Range request breaks playback. So cache the
 * whole file once, then answer each range out of it. */
async function serveAudio(request, url) {
    const cache = await caches.open(CACHE);
    const key = url.pathname;
    let full = await cache.match(key);

    if (!full) {
        try {
            // deliberately a fresh, range-less request so we store the whole file
            const net = await fetch(url.toString(), { credentials: 'same-origin' });
            if (!net.ok) return net;
            await cache.put(key, net.clone());
            full = net;
        } catch (err) {
            return new Response('', { status: 504, statusText: 'Offline' });
        }
    }

    const range = request.headers.get('range');
    if (!range) return full;

    const buf = await full.arrayBuffer();
    const total = buf.byteLength;
    const m = /^bytes=(\d*)-(\d*)$/.exec(range.trim());
    if (!m) return full;

    const start = m[1] ? parseInt(m[1], 10) : 0;
    const end = m[2] ? Math.min(parseInt(m[2], 10), total - 1) : total - 1;

    if (isNaN(start) || start > end || start >= total) {
        return new Response('', {
            status: 416,
            statusText: 'Range Not Satisfiable',
            headers: { 'Content-Range': 'bytes */' + total }
        });
    }

    const slice = buf.slice(start, end + 1);
    return new Response(slice, {
        status: 206,
        statusText: 'Partial Content',
        headers: {
            'Content-Type': full.headers.get('Content-Type') || 'audio/mpeg',
            'Content-Length': String(slice.byteLength),
            'Content-Range': 'bytes ' + start + '-' + end + '/' + total,
            'Accept-Ranges': 'bytes'
        }
    });
}

/* Network first, so a redeploy is picked up as soon as there is a connection,
 * with the cached copy standing in when there is not. */
async function serveDocument(request) {
    const cache = await caches.open(CACHE);
    try {
        const net = await fetch(request);
        if (net && net.ok) cache.put('./index.html', net.clone());
        return net;
    } catch (err) {
        return (await cache.match(request))
            || (await cache.match('./index.html'))
            || Response.error();
    }
}

/* Cache first for the static shell — instant paint — while quietly refreshing
 * the copy in the background for next launch. */
async function serveAsset(request) {
    const cache = await caches.open(CACHE);
    const hit = await cache.match(request);

    const refresh = fetch(request).then(function (net) {
        if (net && net.ok) cache.put(request, net.clone());
        return net;
    }).catch(function () { return null; });

    return hit || (await refresh) || Response.error();
}

self.addEventListener('fetch', function (event) {
    const request = event.request;
    if (request.method !== 'GET') return;

    const url = new URL(request.url);
    if (url.origin !== self.location.origin) return;   // let anything external through

    if (request.mode === 'navigate') {
        event.respondWith(serveDocument(request));
    } else if (isAudio(url, request)) {
        event.respondWith(serveAudio(request, url));
    } else {
        event.respondWith(serveAsset(request));
    }
});
