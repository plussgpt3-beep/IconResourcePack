"""พืชใหม่ (2026-11-27): painters for the seven new crops of the cooking system: the produce (rice, chili,
garlic, shallot, tomato, cabbage, lemongrass), their seed pouches, and the four growth stages of each plant.

Plant stages are side views, bottom-anchored on the full 512 canvas: build.py shrinks them to a 32x32
block/crop texture without cropping (CROP = True), so the stem stands on the ground."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, noise, edge_darken, cloth
from _dishes import _col, _dome, grain

LEAF = (0.30, 0.56, 0.20)
DARK_LEAF = (0.20, 0.42, 0.14)


# ---------- shapes ----------

def _bez(p0, p1, p2, n=24):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2)


def blade_mask(p0, p1, p2, w0, w1=0.0, belly=0.0):
    """A tapering leaf blade along a quadratic curve: width w0 at the base, w1 at the tip. belly > 0 swells
    the middle (a broad leaf) instead of a straight taper (a grass blade)."""
    pts = _bez(p0, p1, p2)
    d = np.gradient(pts, axis=0); d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-6
    nrm = np.stack([-d[:, 1], d[:, 0]], axis=1)
    t = np.linspace(0, 1, len(pts))
    w = w0 + (w1 - w0) * t + belly * np.sin(t * np.pi)
    left = pts + nrm * w[:, None] / 2; right = pts - nrm * w[:, None] / 2
    outline = [tuple(p) for p in left] + [tuple(p) for p in right[::-1]]
    return blur(poly(outline), 1.0), pts


def blade(c, rng, p0, p1, p2, w0, w1=0.0, belly=0.0, color=LEAF, vein=True, k=1.0):
    m, pts = blade_mask(p0, p1, p2, w0, w1, belly)
    col = _col(color, rng, 0.3, 24)
    shade = 0.35 * pillow(m, max(2, w0 * 0.3), 0.7)
    c.over(light(shade, col, depth=30, spec=0.25, gloss=25) * edge_darken(m, 4, 0.25), m * k)
    if vein and w0 > 10:
        v = blur(poly([tuple(p) for p in pts[:-3]], width=max(2, int(w0 * 0.12))), 0.8) * m
        c.over(np.zeros((N, N, 3)) + np.array(color) * 1.35, np.clip(v, 0, 1) * 0.5 * k, cast=False)
    return m


def stem(c, rng, pts, w, color=(0.36, 0.52, 0.20)):
    m = blur(poly([tuple(p) for p in pts], width=int(w)), 1.0)
    c.over(light(0.3 * pillow(m, w * 0.4), _col(color, rng, 0.2), depth=25, spec=0.2), m)
    return m


def _ball(c, rng, cx, cy, rx, ry, rgb, spec=0.5, gloss=35, k=0.22, depth=60):
    m = blur(ellipse([cx - rx, cy - ry, cx + rx, cy + ry]), 1.1)
    c.over(light(_dome(cx, cy, rx, ry) * m, _col(rgb, rng, k), depth=depth, spec=spec, gloss=gloss) * edge_darken(m, 6, 0.3), m)
    return m


# ---------- produce ----------

def tomato(c, rng, cx, cy, r=120):
    """A ripe vine tomato: slightly flattened, deep red with an orange blush near the stalk, two highlights,
    faint shoulders, and a curly green calyx."""
    m = blur(ellipse([cx - r, cy - r * 0.82, cx + r, cy + r * 0.86]), 1.2)
    ang = np.arctan2(yy - (cy - r * 0.55), xx - cx)
    d = np.hypot((xx - cx) / r, (yy - cy + r * 0.55) / r)
    shoulders = 0.025 * np.cos(ang * 6) * np.exp(-((d - 0.35) / 0.25) ** 2)
    col = _col((0.78, 0.09, 0.05), rng, 0.08, 18)
    blush = np.exp(-(d / 0.45) ** 2)[..., None]
    col = col * (1 - blush) + np.array([0.90, 0.36, 0.08]) * blush
    under = np.clip((yy - cy) / r, 0, 1)[..., None]
    col = col * (1 - 0.35 * under)
    pores = 0.03 * noise(rng, 60, 1)
    c.over(light((_dome(cx, cy, r, r * 0.84) + shoulders + pores) * m, np.clip(col, 0, 1), depth=70, spec=0.55, gloss=25) * edge_darken(m, 12, 0.4), m)
    hl = blur(ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.18, cy - r * 0.28]), 10) * m
    c.over(np.ones((N, N, 3)), hl * 0.35, cast=False)
    hl2 = blur(ellipse([cx - r * 0.48, cy - r * 0.47, cx - r * 0.36, cy - r * 0.40]), 2) * m
    c.over(np.ones((N, N, 3)), hl2 * 0.7, cast=False)
    rim = blur(np.clip(m - blur(m, 6) * 1.0, 0, 1), 3)   # a little sky light on the lower edge
    c.over(np.zeros((N, N, 3)) + np.array([0.95, 0.45, 0.35]), rim * 0.25 * (yy > cy), cast=False)
    for i in range(6):   # the calyx: six thin curling sepals
        a = i * np.pi / 3 + 0.2
        tip = (cx + np.cos(a) * r * 0.55, cy - r * 0.60 + np.sin(a) * r * 0.24)
        ctrl = (cx + np.cos(a + 0.5) * r * 0.32, cy - r * 0.66 + np.sin(a + 0.5) * r * 0.16 - r * 0.05)
        blade(c, rng, (cx, cy - r * 0.64), ctrl, tip, r * 0.12, 1, color=(0.24, 0.44, 0.14), vein=False)
    s_ = blur(poly([(cx, cy - r * 0.64), (cx + r * 0.04, cy - r * 0.80), (cx + r * 0.12, cy - r * 0.95)], width=int(r * 0.10)), 1)
    c.over(light(0.4 * pillow(s_, 4), _col((0.32, 0.48, 0.18), rng, 0.2), depth=25), s_)
    return m


def chili(c, rng, p0, p1, p2, w=44, rgb=(0.80, 0.06, 0.04)):
    """A long glossy chili pepper from the stalk end p0 to the curled tip p2: a long reflection along its length,
    creases near the cap, darker on its shaded side, a green cap and a crooked stalk."""
    m, pts = blade_mask(p0, p1, p2, w, w * 0.12, belly=w * 0.22)
    col = _col(rgb, rng, 0.10, 20)
    # shade across the pod: the far side darker, so it reads round
    dist = np.full((N, N), 1e9, np.float32); side = np.zeros((N, N), np.float32)
    for i in range(0, len(pts), 2):
        dd = (xx - pts[i][0]) ** 2 + (yy - pts[i][1]) ** 2
        upd = dd < dist
        dist = np.where(upd, dd, dist)
        side = np.where(upd, (xx - pts[i][0]) * 0.7 + (yy - pts[i][1]) * 0.7, side)
    col = col * (1 - 0.35 * np.clip(side / (w * 0.5), 0, 1))[..., None]
    c.over(light(pillow(m, w * 0.5, 0.55), np.clip(col, 0, 1), depth=50, spec=0.9, gloss=70) * edge_darken(m, 6, 0.35), m)
    gl = blur(poly([(p[0] - w * 0.16, p[1] - w * 0.16) for p in pts[2:-6]], width=max(2, int(w * 0.10))), 2) * m
    c.over(np.ones((N, N, 3)), gl * 0.55, cast=False)
    for k in range(3):   # creases by the cap
        q = pts[1 + k]
        cr = blur(poly([(q[0] - w * 0.3, q[1] + w * 0.05 * k), (q[0] + w * 0.3, q[1] + w * 0.1 + w * 0.05 * k)], width=2), 1) * m
        c.over(np.zeros((N, N, 3)) + np.array(rgb) * 0.4, cr * 0.5, cast=False)
    d = np.array(p1) - np.array(p0); d = d / np.linalg.norm(d)
    cap = blur(ellipse([p0[0] - w * 0.6, p0[1] - w * 0.42, p0[0] + w * 0.6, p0[1] + w * 0.42]), 1)
    c.over(light(0.5 * pillow(cap, 6) + 0.1 * noise(rng, 30, 1) * cap, _col((0.26, 0.46, 0.16), rng, 0.25), depth=35, spec=0.35), cap)
    s_ = blur(poly([tuple(p0), (p0[0] - d[0] * w * 0.5 + w * 0.15, p0[1] - d[1] * w * 0.5), (p0[0] - d[0] * w * 0.9 + w * 0.35, p0[1] - d[1] * w * 0.9 - w * 0.25)], width=int(w * 0.2)), 1)
    c.over(light(0.4 * pillow(s_, 3), _col((0.34, 0.48, 0.20), rng, 0.2), depth=20), s_)


def garlic(c, rng, cx, cy, r=130):
    body = blur(np.maximum(ellipse([cx - r, cy - r * 0.8, cx + r, cy + r * 0.85]),
                           poly([(cx - r * 0.35, cy - r * 0.5), (cx, cy - r * 1.35), (cx + r * 0.35, cy - r * 0.5)])), 1.2)
    # the cloves bulge: a height made of several lobes
    h = np.zeros((N, N), np.float32)
    for dx in (-0.62, -0.22, 0.22, 0.62):
        h = np.maximum(h, _dome(cx + dx * r, cy, r * 0.42, r * 0.85))
    alb = _col((0.93, 0.90, 0.84), rng, 0.12)
    streak = np.clip(np.sin((xx - cx) / r * 9) * 0.5 + 0.5, 0, 1) * np.clip((yy - cy + r * 0.2) / r, 0, 1)
    alb = alb * (1 - 0.25 * streak[..., None]) + np.array([0.55, 0.25, 0.45]) * 0.25 * streak[..., None]
    fib = 0.06 * noise(rng, 70, 1)
    c.over(light(h * body * 0.9 + 0.15 * pillow(body, 20) + fib * body, alb, depth=55, spec=0.35, gloss=25) * edge_darken(body, 10, 0.35), body)
    for dx in (-0.42, 0.0, 0.42):   # seams between the cloves, curving up to the neck
        seam = blur(poly([tuple(p) for p in _bez((cx + dx * r * 0.5, cy + r * 0.78), (cx + dx * r * 1.25, cy), (cx + dx * r * 0.15, cy - r * 0.9), 16)], width=3), 1.2) * body
        c.over(np.zeros((N, N, 3)) + np.array([0.62, 0.55, 0.48]), seam * 0.55, cast=False)
    neck = blur(poly([(cx - r * 0.08, cy - r * 0.9), (cx, cy - r * 1.33), (cx + r * 0.08, cy - r * 0.9)]), 1) * body
    c.over(_col((0.80, 0.72, 0.56), rng, 0.25), neck * 0.6, cast=False)
    roots = blur(rect([cx - r * 0.3, cy + r * 0.78, cx + r * 0.3, cy + r * 0.92], 8), 1)
    c.over(_col((0.60, 0.50, 0.36), rng, 0.3), roots)
    for dx in np.linspace(-0.25, 0.25, 6):
        rt = blur(poly([(cx + dx * r, cy + r * 0.86), (cx + dx * r * 1.6, cy + r * 1.05)], width=4), 0.8)
        c.over(np.zeros((N, N, 3)) + np.array([0.70, 0.60, 0.44]), rt)


def shallot(c, rng, cx, cy, r=80):
    """A single red shallot: a teardrop bulb, coppery papery skin with fine veins running tip to root, a paler
    flake of skin peeling, a dry tip and a tuft of roots."""
    m = blur(np.maximum(ellipse([cx - r, cy - r * 0.9, cx + r, cy + r]),
                        poly([(cx - r * 0.45, cy - r * 0.55), (cx, cy - r * 1.55), (cx + r * 0.45, cy - r * 0.55)])), 1.2)
    nx = (xx - cx) / r
    veins = np.clip(np.sin(np.arcsin(np.clip(nx, -0.99, 0.99)) * 16 + noise(rng, 8, 2) * 1.5) * 0.5 + 0.5, 0, 1) ** 3
    alb = _col((0.62, 0.24, 0.24), rng, 0.12, 14) * (0.92 + 0.12 * veins[..., None])
    alb = alb + np.array([0.18, 0.10, 0.04]) * np.clip((yy - cy) / r, 0, 1)[..., None]   # coppery near the root
    c.over(light(_dome(cx, cy, r, r) * m * 0.9 + 0.1 * pillow(m, 10), np.clip(alb, 0, 1), depth=55, spec=0.5, gloss=35) * edge_darken(m, 8, 0.35), m)
    flake = blur(poly([(cx + r * 0.2, cy - r * 0.2), (cx + r * 0.75, cy + r * 0.05), (cx + r * 0.55, cy + r * 0.55), (cx + r * 0.25, cy + r * 0.3)]), 2) * m
    c.over(_col((0.85, 0.60, 0.45), rng, 0.2), blur(flake, 6) * 0.22, cast=False)
    tip = blur(poly([(cx, cy - r * 1.45), (cx + r * 0.08, cy - r * 1.7), (cx + r * 0.2, cy - r * 1.9)], width=int(r * 0.14)), 1)
    c.over(light(0.3 * pillow(tip, 3), _col((0.66, 0.50, 0.32), rng, 0.3), depth=20), tip)
    for dx in np.linspace(-0.25, 0.25, 5):
        rt = blur(poly([(cx + dx * r, cy + r * 0.95), (cx + dx * r * 1.7, cy + r * 1.15)], width=max(2, int(r * 0.04))), 0.8)
        c.over(np.zeros((N, N, 3)) + np.array([0.72, 0.62, 0.46]), rt)


def _cabbage_leaf(c, rng, cx, cy, ang, L, W, color, clip=None, k=1.0):
    """One broad cabbage leaf fanning out from (cx, cy) along ang: a pale thick midrib, branching veins that
    raise the blade between them (the savoy puckering), and a wavy edge."""
    ca, sa = np.cos(ang), np.sin(ang)
    u = (xx - cx) * ca + (yy - cy) * sa
    v = -(xx - cx) * sa + (yy - cy) * ca
    t = np.clip(u / L, 0, 1)
    half = W * np.sin(np.clip(t, 0, 1) * np.pi * 0.85 + 0.15) * (1 + 0.06 * np.sin(v / W * 9 + u / L * 20))
    m = blur(((u > 0) & (u < L) & (np.abs(v) < half)).astype(np.float32), 1.4)
    if clip is not None:
        m = m * clip
    mid = np.exp(-(v / (W * 0.07)) ** 2) * (u > 0)
    wv = v + noise(rng, 6, 2) * W * 0.15
    branch = np.exp(-(((np.abs(wv) - (u - L * 0.1) * 0.9) % (L * 0.26)) / (W * 0.03)) ** 2) * (np.abs(v) < half * 0.9) * (np.abs(v) > W * 0.08)
    pucker = 0.12 * noise(rng, 26, 2) * (1 - branch)
    h = pillow(m, W * 0.3, 0.6) * 0.6 + pucker * m + 0.08 * branch * m
    col = _col(color, rng, 0.15, 20)
    edge = np.clip(np.abs(v) / np.maximum(half, 1), 0, 1)[..., None]
    col = col * (0.85 + 0.25 * edge) * (1 - 0.15 * t[..., None])
    c.over(light(h, np.clip(col, 0, 1), depth=55, spec=0.35, gloss=30) * edge_darken(m, 6, 0.35), m * k)
    vein_col = np.zeros((N, N, 3)) + np.clip(np.array(color) * 1.6 + 0.12, 0, 1)
    c.over(vein_col, np.clip(mid * 0.85 + branch * 0.28, 0, 1) * m * k, cast=False)
    return m


def cabbage(c, rng, cx, cy, r=170):
    """A green cabbage: big dark outer leaves spreading behind, a tight pale head, and two wrapper leaves cupping
    its lower half in front; every leaf with a thick pale midrib and veins."""
    base = (cx, cy + r * 0.75)
    for a in (np.pi * 0.92, np.pi * 0.08, np.pi * 0.75, np.pi * 0.25):   # behind: spreading wide and up
        _cabbage_leaf(c, rng, base[0], base[1], -a, r * 1.25, r * 0.6, (0.30, 0.50, 0.30))
    head = _ball(c, rng, cx, cy - r * 0.05, r * 0.78, r * 0.72, (0.72, 0.85, 0.52), spec=0.4, gloss=30, depth=70)
    for a in np.linspace(-2.5, -0.6, 4):   # the inner leaves overlapping on the head: soft arcs of shade
        ox, oy = cx + np.cos(a) * r * 0.3, cy - r * 0.05 + np.sin(a) * r * 0.25
        arc = blur(np.clip(ellipse([ox - r * 0.55, oy - r * 0.45, ox + r * 0.55, oy + r * 0.45])
                           - ellipse([ox - r * 0.50, oy - r * 0.40, ox + r * 0.50, oy + r * 0.40]), 0, 1), 3) * head
        c.over(np.zeros((N, N, 3)) + np.array([0.42, 0.58, 0.30]), arc * 0.4, cast=False)
    for a in (np.pi * 0.66, np.pi * 0.34):   # in front: two wrapper leaves up to the head's middle
        _cabbage_leaf(c, rng, base[0], base[1] + r * 0.1, -a, r * 0.95, r * 0.55, (0.38, 0.60, 0.32))


def lemongrass(c, rng, cx=256, cy=300, s=1.0):
    """A bundle of lemongrass stalks: pale bulbous bases, green tops, tied with twine."""
    for i, dx in enumerate((-90, 30, -30, 90)):
        top = (cx + dx * 1.3 * s + 40 * s, cy - 230 * s)
        base = (cx + dx * s - 40 * s, cy + 190 * s)
        mid = ((top[0] + base[0]) / 2, (top[1] + base[1]) / 2)
        m, _ = blade_mask(base, mid, top, 64 * s, 50 * s)
        t = np.clip((yy - top[1]) / (base[1] - top[1]), 0, 1)
        col = np.array([0.42, 0.62, 0.22]) * (1 - t[..., None]) + np.array([0.92, 0.88, 0.70]) * t[..., None]
        col = col * (0.85 + 0.25 * noise(rng, 20, 2))[..., None]
        d = np.array(top) - np.array(base); d = d / np.linalg.norm(d)
        across = (xx - base[0]) * d[1] - (yy - base[1]) * d[0]   # distance across the stalk: lines run along it
        stripes = 0.92 + 0.08 * np.sin(across / (3.5 * s)) + 0.05 * noise(rng, 60, 1)
        purple = np.exp(-((t - 0.88) / 0.06) ** 2)[..., None]   # the faint purple ring near a lemongrass base
        col = col * (1 - 0.35 * purple) + np.array([0.62, 0.40, 0.45]) * 0.35 * purple
        c.over(light(pillow(m, 14 * s, 0.6), np.clip(col * stripes[..., None], 0, 1), depth=40, spec=0.3) * edge_darken(m, 5, 0.3), m)
        cut = blur(ellipse([top[0] - 12 * s, top[1] - 6 * s, top[0] + 12 * s, top[1] + 6 * s]), 1) * m
        c.over(np.zeros((N, N, 3)) + np.array([0.80, 0.86, 0.60]), cut, cast=False)
        ring = blur(np.clip(cut - blur(ellipse([top[0] - 7 * s, top[1] - 3.5 * s, top[0] + 7 * s, top[1] + 3.5 * s]), 1), 0, 1), 0.8) * m
        c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.66, 0.35]), ring * 0.7, cast=False)
    tie = blur(poly([(cx - 110 * s, cy + 40 * s), (cx + 100 * s, cy + 10 * s)], width=int(26 * s)), 1)
    c.over(light(0.4 * pillow(tie, 6), _col((0.62, 0.45, 0.26), rng, 0.3), depth=30, spec=0.2), tie)


def rice_sheaf(c, rng, cx=256, cy=290, s=1.0):
    """A small sheaf of ripe rice: golden stalks tied in the middle, heads of grain drooping over."""
    stalks = []
    for dx in np.linspace(-70, 70, 9):
        p0 = (cx + dx * 0.5 * s, cy + 200 * s); p2 = (cx + dx * 1.1 * s, cy - 150 * s)
        stalks.append((p0, p2))
        stem(c, rng, _bez(p0, (cx + dx * 0.3 * s, cy), p2, 12), 9 * s, color=(0.80, 0.66, 0.30))
    for (p0, p2) in stalks:   # drooping heads: rows of plump grains along a curve
        d = 1 if p2[0] >= cx else -1
        pts = _bez(p2, (p2[0] + d * 55 * s, p2[1] - 35 * s), (p2[0] + d * 60 * s, p2[1] + 150 * s), 10)
        for j, p in enumerate(pts[1:]):
            gr = 13 * s
            for side in (-1, 1):
                gx, gy = p[0] + side * gr * 0.7, p[1] + j * 1.5
                _ball(c, rng, gx, gy, gr * 0.6, gr, (0.92, 0.74, 0.32), spec=0.5, depth=30, k=0.15)
    tie = blur(poly([(cx - 70 * s, cy + 70 * s), (cx + 70 * s, cy + 55 * s)], width=int(24 * s)), 1)
    c.over(light(0.4 * pillow(tie, 6), _col((0.55, 0.36, 0.18), rng, 0.3), depth=30), tie)


def chili_pair(c, rng, cx=256, cy=256, s=1.0):
    chili(c, rng, (cx - 90 * s, cy - 150 * s), (cx - 120 * s, cy + 40 * s), (cx + 10 * s, cy + 170 * s), 58 * s)
    chili(c, rng, (cx + 40 * s, cy - 170 * s), (cx + 40 * s, cy + 10 * s), (cx + 150 * s, cy + 120 * s), 54 * s, rgb=(0.86, 0.12, 0.05))


def shallot_trio(c, rng, cx=256, cy=290, s=1.0):
    shallot(c, rng, cx - 95 * s, cy + 20 * s, 78 * s)
    shallot(c, rng, cx + 95 * s, cy + 30 * s, 74 * s)
    shallot(c, rng, cx, cy + 60 * s, 92 * s)


PRODUCE = {
    'rice': lambda c, rng, cx, cy, s: rice_sheaf(c, rng, cx, cy, s),
    'chili': lambda c, rng, cx, cy, s: chili_pair(c, rng, cx, cy, s),
    'garlic': lambda c, rng, cx, cy, s: garlic(c, rng, cx, cy + 20 * s, 140 * s),
    'shallot': lambda c, rng, cx, cy, s: shallot_trio(c, rng, cx, cy, s),
    'tomato': lambda c, rng, cx, cy, s: tomato(c, rng, cx, cy + 20 * s, 150 * s),
    'cabbage': lambda c, rng, cx, cy, s: cabbage(c, rng, cx, cy + 20 * s, 180 * s),
    'lemongrass': lambda c, rng, cx, cy, s: lemongrass(c, rng, cx, cy, s),
}

SEED_RGB = {
    'rice': (0.86, 0.72, 0.38), 'chili': (0.92, 0.80, 0.50), 'garlic': (0.94, 0.90, 0.80),
    'shallot': (0.68, 0.36, 0.30), 'tomato': (0.90, 0.80, 0.52), 'cabbage': (0.30, 0.22, 0.16),
    'lemongrass': (0.70, 0.62, 0.40),
}


def produce_icon(crop, seed):
    rng = np.random.default_rng(seed)
    c = Canvas()
    PRODUCE[crop](c, rng, 256, 256, 1.0)
    return c.image()


def _seed(c, rng, kind, x, y, r, a):
    """One seed of a kind at (x, y), size r, turned by angle a."""
    ca, sa = np.cos(a), np.sin(a)
    u = (xx - x) * ca + (yy - y) * sa
    v = -(xx - x) * sa + (yy - y) * ca
    if kind == 'shallot':     # a small seed bulb, copper skin, dry tip
        shallot(c, rng, x, y, r)
        return
    if kind == 'cabbage':     # tiny dark round seeds
        _ball(c, rng, x, y, r, r * 0.95, (0.30, 0.18, 0.12), spec=0.6, gloss=45, depth=35, k=0.2)
        return
    if kind == 'lemongrass':  # a slip: a short pale stalk cutting with a green top
        m, _ = blade_mask((x - ca * r * 2, y - sa * r * 2), (x, y), (x + ca * r * 2, y + sa * r * 2), r * 0.9, r * 0.7)
        t = np.clip((u + r * 2) / (r * 4), 0, 1)[..., None]
        col = np.array([0.92, 0.88, 0.70]) * (1 - t) + np.array([0.48, 0.66, 0.26]) * t
        c.over(light(pillow(m, r * 0.4, 0.6), np.clip(col * (0.9 + 0.2 * noise(rng, 20, 2))[..., None], 0, 1), depth=35, spec=0.3) * edge_darken(m, 4, 0.3), m)
        return
    # chili and tomato: flat teardrop seeds; garlic: a clove, the same teardrop, big and ivory
    rgb = {'chili': (0.96, 0.86, 0.52), 'tomato': (0.92, 0.84, 0.62), 'garlic': (0.95, 0.92, 0.84)}[kind]
    m = blur((((u / r) ** 2 + (v / (r * 0.72 * (1 - 0.25 * u / r))) ** 2) < 1).astype(np.float32), 1.0)
    c.over(light(0.5 * pillow(m, r * 0.5, 0.6), _col(rgb, rng, 0.12), depth=30, spec=0.5, gloss=35) * edge_darken(m, 4, 0.35), m)
    if kind == 'garlic':   # a clove: pointed tip, faint lengthwise lines, a brown root end
        tipm = blur(poly([(x + ca * r * 0.7 - sa * r * 0.35, y + sa * r * 0.7 + ca * r * 0.35), (x + ca * r * 1.45, y + sa * r * 1.45),
                          (x + ca * r * 0.7 + sa * r * 0.35, y + sa * r * 0.7 - ca * r * 0.35)]), 1)
        c.over(light(0.3 * pillow(tipm, 4), _col((0.90, 0.84, 0.70), rng, 0.15), depth=25, spec=0.3), tipm)
        lines = np.clip(np.sin(v / r * 9) * 0.5 + 0.5, 0, 1) ** 4 * m
        c.over(np.zeros((N, N, 3)) + np.array([0.70, 0.62, 0.50]), lines * 0.35, cast=False)
        root = blur(ellipse([x - ca * r * 0.95 - r * 0.25, y - sa * r * 0.95 - r * 0.25, x - ca * r * 0.95 + r * 0.25, y - sa * r * 0.95 + r * 0.25]), 1) * m
        c.over(np.zeros((N, N, 3)) + np.array([0.62, 0.48, 0.30]), root * 0.9, cast=False)
        return
    hilum = blur(ellipse([x - ca * r * 0.8 - r * 0.15, y - sa * r * 0.8 - r * 0.15, x - ca * r * 0.8 + r * 0.15, y - sa * r * 0.8 + r * 0.15]), 1) * m
    c.over(np.zeros((N, N, 3)) + np.array(rgb) * 0.6, hilum, cast=False)


SEED_SIZE = {'chili': 34, 'tomato': 28, 'garlic': 52, 'shallot': 50, 'cabbage': 22, 'lemongrass': 34}
SEED_COUNT = {'chili': 16, 'tomato': 18, 'garlic': 6, 'shallot': 6, 'cabbage': 26, 'lemongrass': 6}


def seed_icon(crop, seed):
    """Only the seeds (the user, 2026-11-27: "แก้ภาพเมล็ดพืชให้มีแค่เมล็ด"): a small heap of them, the back ones first."""
    rng = np.random.default_rng(seed)
    c = Canvas()
    r = SEED_SIZE[crop]
    n = SEED_COUNT[crop]
    pts = []
    for i in range(n):   # a mound: wider at the bottom, the top seeds higher up
        t = rng.uniform(0, 1)
        y = 360 - (120 if r < 30 else 170) * t ** 1.3 + rng.uniform(-10, 10)
        w = (120 if r < 30 else 170) * (1 - 0.6 * t)
        pts.append((rng.uniform(256 - w, 256 + w), y, rng.uniform(0, np.pi * 2)))
    for (x, y, a) in sorted(pts, key=lambda p: p[1]):
        s = r * rng.uniform(0.85, 1.15)
        _seed(c, rng, crop, x, y, s, a if crop != 'shallot' else rng.uniform(-0.5, 0.5))
    return c.image()


# ---------- plant stages (side view, bottom anchored) ----------

G = 500   # ground line on the 512 canvas


def _soil_tuft(c, rng):
    m = blur(ellipse([150, G - 18, 362, G + 30]) * (yy < G + 12), 1.5)
    c.over(light(0.3 * pillow(m, 8), grain(rng, (0.36, 0.24, 0.14), 4, 0.5), depth=20, spec=0.05), m)


def _grass_clump(c, rng, n, height, spread, w, color, droop=0.25, cx=256):
    for i in range(n):
        t = (i + 0.5) / n - 0.5
        base = (cx + t * spread * 0.4, G)
        tip = (cx + t * spread * 1.6 + rng.uniform(-15, 15), G - height * rng.uniform(0.8, 1.05))
        mid = ((base[0] + tip[0]) / 2 - t * 20, (base[1] + tip[1]) / 2 - height * 0.1)
        end = (tip[0] + np.sign(t + 1e-3) * height * droop, tip[1] + height * droop * 0.8)
        blade(c, rng, base, mid, end, w, 2, color=color, vein=w > 12)


def plant_rice(stage, rng):
    c = Canvas()
    h = (120, 230, 350, 400)[stage - 1]
    _grass_clump(c, rng, 5 + stage * 2, h, 60 + stage * 30, 14 + stage, (0.34, 0.62, 0.22) if stage < 4 else (0.62, 0.66, 0.26), 0.15 + 0.05 * stage)
    if stage >= 3:
        for dx in (-80, -20, 40, 100)[:stage - 1]:
            top = (256 + dx, G - h * 0.95)
            gold = (0.88, 0.72, 0.30) if stage == 4 else (0.62, 0.72, 0.30)
            d = 1 if dx >= 0 else -1
            pts = _bez(top, (top[0] + d * 50, top[1] - 30), (top[0] + d * 80, top[1] + 90), 8)
            stem(c, rng, _bez((256 + dx * 0.3, G - 60), (256 + dx * 0.7, G - h * 0.6), top, 8), 18, color=(0.55, 0.62, 0.25))
            for p in pts[1:]:
                _ball(c, rng, p[0], p[1], 16, 20, gold, spec=0.5, depth=25, k=0.15)
    _soil_tuft(c, rng)
    return c.image()


def _leafy_stem(c, rng, h, leaves, leaf_len, leaf_w, color=LEAF, cx=256, compound=False):
    """A stem with leaves on alternate sides, each a little different: longer low down, drooping at the tip,
    turned at its own angle. compound: a tomato's leaf, a stalk with paired serrated leaflets."""
    pts = _bez((cx, G), (cx + 18, G - h * 0.5), (cx - 8, G - h), 16)
    stem(c, rng, pts, max(16, leaf_w * 0.32), color=(0.36, 0.50, 0.22))
    nodes = []
    for i in range(leaves):
        f = 0.18 + 0.78 * i / max(1, leaves - 1)
        p = pts[int(f * (len(pts) - 1))]
        side = -1 if i % 2 else 1
        L = leaf_len * (1.15 - 0.45 * f) * rng.uniform(0.85, 1.1)
        rise = rng.uniform(0.15, 0.55)
        droop = rng.uniform(0.0, 0.35)
        tip = (p[0] + side * L, p[1] - L * (rise - droop))
        ctrl = (p[0] + side * L * 0.45, p[1] - L * (rise + 0.2))
        shade = tuple(np.clip(np.array(color) * rng.uniform(0.85, 1.12), 0, 1))
        if compound:
            stem(c, rng, _bez(tuple(p), ctrl, tip, 10), max(8, leaf_w * 0.14), color=(0.34, 0.50, 0.22))
            q = _bez(tuple(p), ctrl, tip, 7)
            for j in range(2, 7):   # paired leaflets along the leaf stalk, the end one alone
                d = q[min(j, 6)] - q[j - 1]; d = d / (np.linalg.norm(d) + 1e-6)
                for sgn in ((-1, 1) if j < 6 else (0,)):
                    nrm = np.array([-d[1], d[0]]) * sgn
                    dirv = d * 0.5 + nrm if sgn else d
                    ll = L * 0.32 * (1.2 if j == 6 else 1)
                    t2 = (q[j][0] + dirv[0] * ll, q[j][1] + dirv[1] * ll + ll * 0.15)
                    blade(c, rng, tuple(q[j]), ((q[j][0] + t2[0]) / 2, (q[j][1] + t2[1]) / 2 - ll * 0.15), t2, 6, 0,
                          belly=leaf_w * 0.45, color=shade, vein=True)
        else:
            blade(c, rng, tuple(p), ctrl, tip, 10, 0, belly=leaf_w * rng.uniform(0.85, 1.1), color=shade)
        nodes.append((p, side, L))
    return pts, nodes


def plant_chili(stage, rng):
    c = Canvas()
    h = (110, 210, 320, 380)[stage - 1]
    pts, nodes = _leafy_stem(c, rng, h, 2 + stage * 2, 70 + stage * 20, 30 + stage * 4, color=(0.24, 0.50, 0.18))
    if stage >= 3:   # slender pods hanging from the leaf joints, in ones and twos
        for i, (p, side, L) in enumerate(nodes[1:-1]):
            for k in range(1 + (i % 2)):
                x, y = p[0] + side * (L * 0.45 + 26 * k), p[1] + 4
                rgb = ((0.86, 0.10, 0.05) if (i + k) % 3 else (0.92, 0.40, 0.06)) if stage == 4 else (0.38, 0.64, 0.20)
                chili(c, rng, (x, y), (x + side * 6, y + 50), (x + side * (14 + 6 * k), y + 92 - 10 * k), 26, rgb=rgb)
    _soil_tuft(c, rng)
    return c.image()


def plant_garlic(stage, rng):
    c = Canvas()
    h = (110, 200, 290, 330)[stage - 1]
    if stage >= 3:
        r = (0, 0, 45, 70)[stage - 1]
        garlic(c, rng, 256, G - r * 0.55, r)
    _grass_clump(c, rng, 3 + stage, h, 40 + stage * 20, 18 + stage * 2, (0.36, 0.58, 0.28) if stage < 4 else (0.52, 0.58, 0.30), 0.25)
    _soil_tuft(c, rng)
    return c.image()


def plant_shallot(stage, rng):
    c = Canvas()
    h = (100, 180, 260, 300)[stage - 1]
    if stage >= 3:
        r = (0, 0, 34, 48)[stage - 1]
        for dx in (-50, 50, 0):
            shallot(c, rng, 256 + dx, G - r * 0.7, r)
    n = 3 + stage
    for i in range(n):   # hollow round leaves: thin, straight, fanned out
        t = (i + 0.5) / n - 0.5
        base = (256 + t * 50, G - 20); tip = (256 + t * 380, G - h * (0.8 + 0.2 * np.cos(t * 3)))
        blade(c, rng, base, ((base[0] + tip[0]) / 2, (base[1] + tip[1]) / 2 - 20), tip, 18, 8, color=(0.36, 0.60, 0.30), vein=False)
    _soil_tuft(c, rng)
    return c.image()


def plant_tomato(stage, rng):
    c = Canvas()
    h = (120, 230, 350, 420)[stage - 1]
    pts, nodes = _leafy_stem(c, rng, h, 2 + stage, 90 + stage * 22, 34 + stage * 4, color=(0.26, 0.48, 0.18), compound=True)
    if stage >= 3:   # trusses: three or four fruits hanging together off the stem
        for i, (p, side, L) in enumerate(nodes[:-1]):
            if i % 2:
                continue
            bx, by = p[0] - side * 30, p[1] + 20
            for k, (dx, dy, r) in enumerate(((0, 0, 40), (-side * 46, 26, 36), (side * 26, 50, 38), (-side * 12, 82, 30))[: 3 + (i % 3 == 0)]):
                if stage == 4:
                    rgb = (0.84, 0.14, 0.06) if k < 2 else (0.92, 0.42, 0.10)
                else:
                    rgb = (0.52, 0.72, 0.28)
                _ball(c, rng, bx + dx, by + dy, r, r * 0.92, rgb, spec=0.7, gloss=45)
    _soil_tuft(c, rng)
    return c.image()


def plant_cabbage(stage, rng):
    c = Canvas()
    n = 3 + stage
    for i in range(n):   # spreading outer leaves, broad and wavy
        t = (i + 0.5) / n - 0.5
        L = (90, 130, 170, 200)[stage - 1]
        tip = (256 + t * L * 3.2, G - L * (0.7 + 0.3 * np.cos(t * 3)))
        blade(c, rng, (256 + t * 40, G), (256 + t * L * 1.2, G - L * 0.9), tip, 14, 6, belly=L * 0.45,
              color=(0.38, 0.62, 0.30) if stage < 4 else (0.34, 0.56, 0.28))
    if stage >= 2:
        r = (0, 70, 110, 140)[stage - 1]
        cabbage(c, rng, 256, G - r * 0.8, r * 0.85)
    _soil_tuft(c, rng)
    return c.image()


def plant_lemongrass(stage, rng):
    c = Canvas()
    h = (140, 260, 380, 450)[stage - 1]
    if stage >= 3:
        for dx in (-30, 0, 30)[: stage - 1]:
            m = blur(rect([256 + dx - 16, G - h * 0.35, 256 + dx + 16, G], 10), 1)
            c.over(light(pillow(m, 8), _col((0.88, 0.86, 0.66), rng, 0.15), depth=30, spec=0.3), m)
    _grass_clump(c, rng, 6 + stage * 2, h, 80 + stage * 30, 14 + stage, (0.42, 0.64, 0.26), 0.3)
    _soil_tuft(c, rng)
    return c.image()


PLANT = {'rice': plant_rice, 'chili': plant_chili, 'garlic': plant_garlic, 'shallot': plant_shallot,
         'tomato': plant_tomato, 'cabbage': plant_cabbage, 'lemongrass': plant_lemongrass}


def plant_icon(crop, stage, seed):
    return PLANT[crop](stage, np.random.default_rng(seed))
