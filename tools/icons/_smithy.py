"""The smithy's things (ร้านตีเหล็ก, 2026-10-24): a forged anvil, a smith's hammer, a grindstone on its
wooden frame, a sword, a red-hot blade, a water bucket with steam, sparks, iron ingots, coal, an
amethyst shard. Each painter paints onto a Canvas; icons place and combine them."""
import numpy as np
from lib import (N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, band, noise, edge_darken,
                 steel_tint, gold_tint, sword, coin_flat)

IRON = (0.36, 0.36, 0.40)


def anvil(c, cx=256, top=250, w=1.0, tint=IRON):
    """A smith's anvil: horn to the left, flat face, waist, wide foot."""
    def X(x): return cx + (x - 256) * w
    def Y(y): return top + (y - 250) * w
    pts = [(56, 250), (360, 250), (440, 236), (452, 248), (440, 268), (370, 300), (320, 312), (320, 380),
           (392, 452), (120, 452), (192, 380), (192, 312), (140, 300), (70, 284)]
    m = blur(poly([(X(x), Y(y)) for x, y in pts]), 1.2)
    face = blur(rect([X(80), Y(250), X(372), Y(268)], 3), 1) * m
    c.over(chrome(0.35 * pillow(m, 16), tint, depth=50, sky=0.8, ground=0.1) * edge_darken(m, 8, 0.25), m)
    c.over(chrome(0.6 * face, (tint[0] * 1.5, tint[1] * 1.5, tint[2] * 1.5), depth=30, sky=1.0, ground=0.2), face * 0.8, cast=False)
    return m


def hammer(c, rng, p0, p1, head_w=40, head_len=120):
    """A smith's cross-peen hammer: wooden haft from p0 (the hand) to p1, iron head across p1."""
    s, t = band(p0, p1, 0)
    haft = blur(((s > 0) & (s < 1.02) & (np.abs(t) < 13)).astype(np.float32), 1)
    ang = np.arctan2(p1[1] - p0[1], p1[0] - p0[0])
    c.over(light(np.clip(1 - np.abs(t) / 13, 0, 1) ** 0.5 * haft, wood(rng, (0.55, 0.36, 0.18), angle=ang + np.pi / 2, rings=4),
                 depth=30, spec=0.3), haft)
    d = np.array([np.cos(ang), np.sin(ang)]); n = np.array([-d[1], d[0]])
    h0 = (p1[0] - n[0] * head_len * 0.5, p1[1] - n[1] * head_len * 0.5)
    h1 = (p1[0] + n[0] * head_len * 0.5, p1[1] + n[1] * head_len * 0.5)
    s2, t2 = band(h0, h1, 0)
    head = ((s2 > 0) & (s2 < 1) & (np.abs(t2) < head_w * (0.55 + 0.45 * np.clip(s2 / 0.3, 0, 1)))).astype(np.float32)
    head = blur(head, 1.2)
    c.over(chrome(0.5 * pillow(head, 10), (0.45, 0.47, 0.50), depth=50, sky=0.8, ground=0.1), head)
    return head


def sparks(c, rng, cx, cy, n=14, spread=120, color=(1.0, 0.75, 0.25)):
    """Short bright streaks flying out from a point (hot iron struck or ground)."""
    m = np.zeros((N, N), np.float32)
    for i in range(n):
        a = rng.uniform(-np.pi, 0.15) if spread > 0 else 0
        r0 = rng.uniform(10, 30); r1 = r0 + rng.uniform(25, spread * 0.7)
        p0 = (cx + r0 * np.cos(a), cy + r0 * np.sin(a)); p1 = (cx + r1 * np.cos(a), cy + r1 * np.sin(a))
        m = np.maximum(m, poly([p0, p1], width=int(rng.uniform(4, 8))))
    m = blur(m, 1.2)
    c.over(np.zeros((N, N, 3)) + np.array(color), np.clip(blur(m, 5) * 0.8, 0, 1), cast=False)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.97, 0.8]), m, cast=False)


def hot(c, mask, k=1.0):
    """Red-hot iron: deep red at the edges to orange at its middle, glowing (barely shaded)."""
    h = np.clip(pillow(mask, 10) * 1.6, 0, 1)
    col = np.array([0.72, 0.08, 0.02])[None, None, :] * (1 - h[..., None]) + np.array([1.0, 0.52, 0.08])[None, None, :] * h[..., None]
    c.over(col, mask * k, cast=False)


def ingot(c, cx, cy, w=120, tint=(0.75, 0.76, 0.80)):
    """An iron ingot: a trapezoid bar seen from above and the front."""
    h = w * 0.42
    top = blur(poly([(cx - w * 0.38, cy - h * 0.55), (cx + w * 0.38, cy - h * 0.55), (cx + w * 0.5, cy), (cx - w * 0.5, cy)]), 1.2)
    front = blur(poly([(cx - w * 0.5, cy), (cx + w * 0.5, cy), (cx + w * 0.5, cy + h * 0.45), (cx - w * 0.5, cy + h * 0.45)]), 1.2)
    c.over(chrome(0.3 * front + 0.05, (tint[0] * 0.8, tint[1] * 0.8, tint[2] * 0.8), depth=30, sky=0.6, ground=0.1), front)
    c.over(chrome(0.4 * pillow(top, 6) + 0.2, tint, depth=30, sky=1.0, ground=0.2), top)


def coal(c, rng, cx, cy, r=60):
    """A lump of coal: black, faceted, with a dull shine."""
    ang = np.linspace(0, 2 * np.pi, 9)[:-1] + rng.uniform(0, 0.4)
    pts = [(cx + r * rng.uniform(0.75, 1.05) * np.cos(a), cy + r * rng.uniform(0.7, 1.0) * np.sin(a)) for a in ang]
    m = blur(poly(pts), 1.2)
    facets = 0.85 + 0.15 * noise(rng, 6, 1)
    c.over(light(0.5 * pillow(m, 10) * facets, np.zeros((N, N, 3)) + np.array([0.10, 0.10, 0.11]), depth=50, spec=0.5, gloss=40), m)


def amethyst(c, cx, cy, s=1.0, color=(0.60, 0.36, 0.85)):
    """A cluster of three amethyst crystals."""
    for (dx, h, w, a) in ((-50, 150, 34, -0.45), (46, 130, 32, 0.45), (0, 200, 42, 0.0)):
        p0 = (cx + dx * s, cy); p1 = (cx + dx * s + np.sin(a) * h * s, cy - np.cos(a) * h * s)
        ss, t = band(p0, p1, 0)
        ww = w * s * np.clip((1 - ss) / 0.3, 0, 1) ** 0.8
        m = blur(((ss > 0) & (ss < 1) & (np.abs(t) < ww)).astype(np.float32), 1.2)
        face = np.where(t < 0, 1.0, 0.65)
        col = np.zeros((N, N, 3)) + np.array(color)
        c.over(light(0.4 * m * face, col * face[..., None], depth=30, spec=0.8, gloss=60), m)


def bucket(c, cx=256, top=250, w=1.0, water=True):
    """An iron bucket with a handle, full of water."""
    def X(x): return cx + (x - 256) * w
    def Y(y): return top + (y - 250) * w
    handle = blur(np.clip(ellipse([X(130), Y(150), X(382), Y(370)]) - ellipse([X(146), Y(166), X(366), Y(354)]), 0, 1) * (yy < Y(262)), 1)
    c.over(chrome(0.4 * pillow(handle, 3), IRON, depth=30), handle)
    body = blur(poly([(X(130), Y(262)), (X(382), Y(262)), (X(352), Y(470)), (X(160), Y(470))]), 1.2)
    nx = (xx - cx) / (126 * w)
    c.over(chrome(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * body * 0.6, (0.50, 0.50, 0.54), depth=50, sky=0.8, ground=0.12), body)
    for y in (300, 430):
        hoop = blur((np.abs(yy - Y(y)) < 8 * w).astype(np.float32) * body, 1)
        c.over(chrome(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * hoop, (0.30, 0.30, 0.33), depth=40), hoop)
    rim = blur(ellipse([X(130), Y(244), X(382), Y(282)]), 1)
    c.over(chrome(0.3 * rim, (0.55, 0.55, 0.58), depth=20), rim)
    if water:
        wat = blur(ellipse([X(142), Y(250), X(370), Y(276)]), 1)
        c.over(light(0.2 * wat, np.zeros((N, N, 3)) + np.array([0.20, 0.42, 0.80]), depth=20, spec=0.9, gloss=60), wat)


def steam(c, rng, cx, cy, h=200, k=0.75):
    """Billows of steam rising off the water: soft white puffs, shaded from the upper left."""
    m = np.zeros((N, N), np.float32)
    for i, (dx, dy, r) in enumerate(((-40, -10, 46), (10, -40, 54), (-20, -90, 50), (30, -130, 40), (-10, -170, 30))):
        m = np.maximum(m, ellipse([cx + dx - r, cy + dy - r * 0.85, cx + dx + r, cy + dy + r * 0.85]))
    m = blur(m, 4)
    col = np.zeros((N, N, 3)) + np.array([0.90, 0.92, 0.95])
    c.over(light(0.5 * pillow(m, 20), col * (0.92 + 0.08 * noise(rng, 12, 2))[..., None], depth=40, ambient=0.6, spec=0.05), m * k)


def grindstone(c, rng, cx=256, cy=250, r=150):
    """A sandstone wheel turning on an iron axle between two wooden posts."""
    for x in (cx - r - 6, cx + r - 30):
        post = blur(rect([x, cy - 20, x + 36, 470], 6), 1)
        c.over(light(0.5 * pillow(post, 8), wood(rng, (0.50, 0.32, 0.15), angle=np.pi / 2, rings=5), depth=40, spec=0.15), post)
    rr = np.hypot(xx - cx, yy - cy) / r
    wheel = blur(ellipse([cx - r, cy - r, cx + r, cy + r]), 1.2)
    grain = 0.88 + 0.12 * noise(rng, 30, 2)
    h = 0.45 * np.clip(1 - rr, 0, 1) ** 0.25 + 0.15 * np.exp(-((rr - 0.92) / 0.05) ** 2)
    col = np.array([0.66, 0.60, 0.48])[None, None, :] * grain[..., None]
    c.over(light(h * wheel, col, depth=50, spec=0.1) * edge_darken(wheel, 8, 0.3), wheel)
    ring = blur(np.clip(ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62])
                        - ellipse([cx - r * 0.56, cy - r * 0.56, cx + r * 0.56, cy + r * 0.56]), 0, 1), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.50, 0.45, 0.36]), ring * 0.6, cast=False)
    axle = blur(ellipse([cx - 26, cy - 26, cx + 26, cy + 26]), 1)
    c.over(chrome(0.5 * pillow(axle, 8), IRON, depth=40), axle)
    return wheel


def blade(c, p0, p1, w=26, hot_from=None):
    """A bare blade (no hilt yet) from its tang p0 to its tip p1; red-hot from hot_from (0..1) on."""
    s, t = band(p0, p1, 0)
    ww = w * np.clip((1 - s) / 0.12, 0, 1) ** 0.6
    tang = ((s > -0.12) & (s <= 0) & (np.abs(t) < w * 0.35)).astype(np.float32)
    m = blur(np.maximum(((s > 0) & (s < 1) & (np.abs(t) < ww)).astype(np.float32), tang), 1.2)
    hgt = np.clip(1 - np.abs(t) / (ww + 1e-3), 0, 1) ** 0.6 * m
    c.over(chrome(hgt, steel_tint(), depth=40), m)
    if hot_from is not None:
        k = np.clip((s - hot_from) / 0.15, 0, 1) * m
        hot(c, m, k)
    return m
