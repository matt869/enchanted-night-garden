# 🌙 Enchanted Night Garden

An interactive 3D night garden that blooms in your browser. Fourteen hand-crafted procedural flowers rest under a starlit sky — tap one open, watch moths drift through in colors that echo the petals, change the weather, and dream up flowers that have never existed. A single self-contained HTML file, with its own looping soundtrack baked in.

*Built with [Three.js](https://threejs.org/). No build step, no dependencies to install — just open the file.*

---

## ✨ Features

- **14 procedural flowers** — Peony, Rose, Dahlia, Orchid, Lotus, Sunflower, Cherry Blossom, Morning Glory, Night Cereus, Bleeding Heart, Tulip, Lily, Anemone, and Ranunculus. Each is generated from scratch in code — petal shape, curl, texture, and glow are all procedural, so no two frames look quite the same.
- **✨ Dream flowers** — a generator that invents a brand-new flower every time you tap it: its own palette, petal count, luminous heart, made-up name, and faux-Latin species. Endlessly different.
- **Tap to bloom** — click or tap a flower to gently open or furl its petals closed, with a soft burst of stardust when it reopens.
- **Living moths** — luna-style moths drift through the garden on time-warped wingbeats, and their wings shift color to harmonize with whatever flower is on screen.
- **Weather** — cycle through **Midnight**, **Aurora**, **Snowfall**, and **Rainfall**, each with its own sky, fog, light, and atmosphere (falling snow, rain, shimmering aurora curtains, lightning).
- **A soundtrack** — a looping night-time audio track plays at the touch of the ♪ button.
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
| ✧ | Hide the interface for a clean view |

**Keyboard:** `←` / `→` wander between flowers · `W` change weather

> 🔊 **A note on sound:** browsers only allow audio to start *after* you interact with the page. Tap the ♪ button and the soundtrack fades in.

---

## 🚀 Running it

It's one file. There is nothing to install.

- **Locally:** just open `index.html` in any modern browser (Chrome, Firefox, Safari, Edge).
- **On the web:** upload the single HTML file to any static host and you're done.

### Deploying to Cloudflare Pages (via GitHub)

1. Create a GitHub repository and add this file, renamed to **`index.html`**.
2. In the [Cloudflare dashboard](https://dash.cloudflare.com/) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
3. Pick your repository. Leave the build command **empty** and set the output directory to **`/`** (root) — there is no build step.
4. **Save and Deploy.** Your garden goes live at `your-project.pages.dev`.

Any push to the repository automatically redeploys.

---

## 🛠️ How it works

Everything lives in one HTML file:

- **Three.js (r128)** is loaded from a CDN and does the 3D rendering.
- **Every flower is procedural** — petals are built from parametric geometry (length, curl, ruffle, recurve, fold, cup) and painted with canvas-generated textures, then arranged in rings. Nothing is a pre-made 3D model.
- **The soundtrack is embedded** directly inside the file as data, so the page is fully self-contained and works offline once loaded — the only external request is the Three.js library.
- **Post-processing** adds the cinematic glow: the scene is rendered to a texture, its bright areas are extracted and blurred, then composited back with a soft highlight roll-off so nothing blows out to flat white.

Because it's a single static file, it's tiny to host, loads fast, and can't break — there's no server, no database, no framework.

---

## 💛 About

A small, quiet thing made to be wandered through rather than *used*. Move slowly, zoom in, change the weather, and see what blooms.

Made with care. 🌸
