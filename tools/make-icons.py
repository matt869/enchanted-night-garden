#!/usr/bin/env python3
"""Draw the app icons for the Enchanted Night Garden PWA.

Writes PNGs into public/icons/. Pure standard library -- zlib and struct are
enough to emit a PNG, so this runs anywhere without Pillow installed.

    python tools/make-icons.py

Re-run it after changing the palette or the bloom geometry below.
"""

import math
import os
import struct
import zlib

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "public", "icons")

SS = 4               # supersampling factor per axis (4 -> 16 samples/pixel)
PETALS = 8           # lobes on the bloom

# palette, lifted from the page itself
NIGHT_IN = (26, 20, 56)
NIGHT_OUT = (5, 5, 15)
PETAL_IN = (255, 226, 245)
PETAL_OUT = (168, 92, 214)
HEART = (255, 231, 170)
GLOW = (255, 138, 190)


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def sample(x, y, size, inset):
    """Colour of one sample point, in unclamped float RGB.

    x, y are pixel coordinates; inset shrinks the artwork toward the middle so
    maskable icons keep their content inside the safe zone.
    """
    cx = cy = size / 2.0
    r_ref = size / 2.0 * inset

    dx, dy = x - cx, y - cy
    d = math.hypot(dx, dy)

    # --- night sky: radial gradient, brighter toward the middle
    col = list(lerp(NIGHT_IN, NIGHT_OUT, min(1.0, (d / (size * 0.62)) ** 1.25)))

    # --- scattered stars
    for sx, sy, mag in ((0.20, 0.18, 1.0), (0.79, 0.24, 0.8), (0.13, 0.72, 0.7),
                        (0.88, 0.67, 0.9), (0.32, 0.88, 0.55), (0.66, 0.09, 0.6)):
        sd = math.hypot(x - sx * size, y - sy * size)
        tw = math.exp(-(sd / (size * 0.016)) ** 2) * mag
        for i in range(3):
            col[i] += (255 - col[i]) * min(1.0, tw)

    # --- the bloom's outer glow
    halo = math.exp(-(d / (r_ref * 0.95)) ** 2) * 0.42
    for i in range(3):
        col[i] += (GLOW[i] - col[i]) * halo

    # --- petals: a rose curve r(theta), rotated so a petal points up
    theta = math.atan2(dy, dx) + math.pi / 2
    edge = r_ref * (0.60 + 0.40 * math.cos(PETALS * theta)) * 0.92
    if d <= edge:
        t = d / max(edge, 1e-6)
        petal = lerp(PETAL_IN, PETAL_OUT, t ** 0.85)
        # soften where a petal meets its neighbour
        seam = abs(math.cos(PETALS * theta / 2.0)) ** 0.5
        shade = 0.72 + 0.28 * seam
        col = [petal[i] * shade for i in range(3)]

    # --- glowing heart of the flower
    heart = math.exp(-(d / (r_ref * 0.20)) ** 2)
    for i in range(3):
        col[i] += (HEART[i] - col[i]) * min(1.0, heart * 1.15)

    return col


def render(size, inset=1.0):
    """Render one icon as raw RGB rows."""
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            acc = [0.0, 0.0, 0.0]
            for sy in range(SS):
                for sx in range(SS):
                    c = sample(px + (sx + 0.5) / SS, py + (sy + 0.5) / SS,
                               size, inset)
                    for i in range(3):
                        acc[i] += c[i]
            n = SS * SS
            row += bytes(max(0, min(255, int(acc[i] / n + 0.5))) for i in range(3))
        rows.append(bytes(row))
    return rows


def write_png(path, size, rows):
    """Emit an 8-bit RGB PNG (no alpha: iOS flattens it onto black anyway)."""
    raw = b"".join(b"\x00" + r for r in rows)      # filter byte 0 per scanline

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


def main():
    os.makedirs(OUT, exist_ok=True)
    # (filename, pixels, inset) -- maskable art sits inside the 80% safe zone
    jobs = [
        ("icon-192.png", 192, 0.86),
        ("icon-512.png", 512, 0.86),
        ("icon-maskable-512.png", 512, 0.62),
        ("apple-touch-icon.png", 180, 0.86),
    ]
    for name, size, inset in jobs:
        path = os.path.join(OUT, name)
        n = write_png(path, size, render(size, inset))
        print("wrote {:<24} {}x{}  {:,} bytes".format(name, size, size, n))


if __name__ == "__main__":
    main()
