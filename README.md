# 🌙 Enchanted Night Garden

An interactive 3D night garden that blooms in your browser. Fourteen hand-crafted procedural flowers rest under a starlit sky — tap one open, watch moths drift through in colors that echo the petals, change the weather, and dream up flowers that have never existed.

It also installs. On an iPhone or an Android phone you can add it to your home screen and it opens full-screen, with no browser chrome and no network — the whole garden is cached on the device.

*Built with [Three.js](https://threejs.org/). No build step, no package manager, nothing to compile — it's static files all the way down.*

---

## ✨ Features

- **14 procedural flowers** — Peony, Rose, Dahlia, Orchid, Lotus, Sunflower, Cherry Blossom, Morning Glory, Night Cereus, Bleeding Heart, Tulip, Lily, Anemone, and Ranunculus. Each is generated from scratch in code — petal shape, curl, texture, and glow are all procedural, so no two frames look quite the same.
- **✨ Dream flowers** — a generator that invents a brand-new flower every time you tap it: its own palette, petal count, luminous heart, made-up name, and faux-Latin species. Endlessly different.
- **Tap to bloom** — click or tap a flower to gently open or furl its petals closed, with a soft burst of stardust when it reopens.
- **Living moths** — luna-style moths drift through the garden on time-warped wingbeats, and their wings shift color to harmonize with whatever flower is on screen.
- **Weather** — cycle through **Midnight**, **Aurora**, **Snowfall**, and **Rainfall**, each with its own sky, fog, light, and atmosphere (falling snow, rain, shimmering aurora curtains, lightning).
- **A soundtrack** — a looping night-time audio track plays at the touch of the ♪ button. Drop your own into [`public/audio/`](public/audio/) and it is picked up automatically.
- **Installs like an app** — add it to the home screen on iOS or Android and it launches full-screen, offline, with its own icon.
- **Cinematic look** — real multi-pass bloom post-processing, drifting fireflies, shooting stars, a Milky Way band, mist, and a glowing heart-glint at the center of every flower.
- **Photo mode** — capture the current view as a PNG to your downloads.
- **A hidden keepsake** — somewhere in the garden, something is written for the curious. You'll have to look very closely to find it. 🤍

---

## 🎮 Controls

| Action | Mouse | Touch |
|---|---|---|
| Rotate the view | Click + drag | One-finger drag |
| Zoom in / out | Scroll wheel | Pinch |
| Open / close the flower | Click the flower | Tap the flower |
| Recenter the camera | Double-click | Double-tap |
| Switch flowers | Tap a name at the top | Tap a name at the top |

**Toolbar (top-right):**

| Button | What it does |
|---|---|
| ▶ | Auto-tour through all the flowers |
| 🎲 | Jump to a random flower |
| ✨ | Grow a brand-new dream flower |
| ☾ | Change the weather |
| 📷 | Save a photo |
| ♪ | Turn the soundtrack on / off |
| ⤓ | Install the garden to your home screen *(appears only when it can be installed)* |
| ✧ | Hide the interface for a clean view |

**Keyboard:** `←` / `→` wander between flowers · `W` change weather

> 🔊 **A note on sound:** browsers only allow audio to start *after* you interact with the page. Tap the ♪ button and the soundtrack fades in.

---

## 📲 Installing it on a phone

The garden is a Progressive Web App, so it installs straight from the browser — no App Store, no Play Store, no account.

**iPhone / iPad** — open the site in **Safari** (this only works in Safari), tap the **Share** button, scroll down to **Add to Home Screen**, then **Add**.

**Android** — open it in Chrome and either tap the **⤓** button in the garden's toolbar or choose **Install app** from the browser menu.

Either way you get an icon on the home screen that opens full-screen. After the first visit everything but the soundtrack is cached on the device, so it opens in airplane mode too; the soundtrack is cached the first time you press ♪.

> Installing requires **HTTPS** (or `localhost`). Opening `index.html` straight off the disk with `file://` will not offer it.

---

## 🚀 Running it

There is no build step — serve the `public/` folder and you're done.

- **Locally:** from the repo root, run `python -m http.server 8000 --directory public`, then open <http://localhost:8000>. A plain web server is needed rather than opening the file directly, because service workers refuse to run over `file://`.
- **On the web:** upload the contents of `public/` to any static host.

### Deploying to Cloudflare

`wrangler.jsonc` configures a static-assets Worker pointed at `public/`:

```bash
npx wrangler deploy
```

If instead you connect the repository through the Cloudflare dashboard as a **Pages** project, leave the build command **empty** and set the output directory to **`public`**.

> ⚠️ Pages and Workers are two different products. If the site is served from a Pages project, a `wrangler deploy` will not update it — and vice versa. Whichever one is live, confirm a change actually landed by loading the site rather than trusting the push.

### After you deploy an update

The service worker serves the cached copy first for speed. Bump the `CACHE` constant at the top of [`public/sw.js`](public/sw.js) whenever you change a cached file, so returning visitors are guaranteed the new version rather than yesterday's.

---

## 🗂️ What's in here

```
public/
  index.html            the whole garden — markup, styles, and all the logic
  manifest.webmanifest  name, colours and icons for the installed app
  sw.js                 service worker: offline caching + audio range requests
  audio/                your soundtrack goes here (see its README)
  icons/                app icons, generated by tools/make-icons.py
  vendor/three.min.js   Three.js r128, vendored so the app works offline
tools/
  make-icons.py         redraws the icons; standard library only
wrangler.jsonc          Cloudflare static-assets config
```

---

## 🛠️ How it works

- **Every flower is procedural** — petals are built from parametric geometry (length, curl, ruffle, recurve, fold, cup) and painted with canvas-generated textures, then arranged in rings. Nothing is a pre-made 3D model.
- **Three.js (r128)** does the 3D rendering. It is committed into `public/vendor/` rather than pulled from a CDN, because an installed app has to keep working with no network at all.
- **The soundtrack is a real file** served from `public/audio/`, played through a plain `<audio>` element and faded in and out with script. It deliberately avoids the Web Audio API: iOS suspends audio contexts aggressively, and a single looping track has no need for one.
- **The service worker** caches the shell on install so the garden opens instantly and offline. Audio is cached separately on first play, and served back with proper HTTP range handling — Safari always asks for media in ranges, and answering a range request with a whole file breaks playback.
- **Post-processing** adds the cinematic glow: the scene is rendered to a texture, its bright areas are extracted and blurred, then composited back with a soft highlight roll-off so nothing blows out to flat white.

It is all static files: tiny to host, fast to load, with no server, no database and no framework to break.

---

## 💛 About

A small, quiet thing made to be wandered through rather than *used*. Move slowly, zoom in, change the weather, and see what blooms.

Made with care. 🌸
