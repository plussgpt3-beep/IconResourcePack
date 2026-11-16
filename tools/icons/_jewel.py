"""เครื่องประดับ (ร่าง 2026-11-16): rings, necklaces, earrings, bracelets, belts and charms.
Each piece is one icon; its grade (zone 1-4) shows in the item's name colour, not in the picture."""
import numpy as np
from lib import (N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, rect, chrome, gold_tint, steel_tint,
                 noise, leather_col, stone, cloth, wood)
from lib import poly as _poly


def poly(points, width=None):
    return _poly(points, None if width is None else max(1, int(round(width))))

COL = {'fire': (1.00, 0.36, 0.10), 'ice': (0.55, 0.88, 1.00), 'storm': (1.00, 0.84, 0.20), 'venom': (0.40, 0.90, 0.26),
       'ruby': (0.85, 0.08, 0.12), 'emerald': (0.10, 0.75, 0.35), 'sky': (0.70, 0.90, 1.0), 'soul': (0.62, 0.30, 1.0)}
SILVER = (0.86, 0.88, 0.92)
IRON = (0.55, 0.57, 0.60)
DARK = (0.38, 0.36, 0.42)


def metal_ring(c, box, thick, tint):
    """A band seen at a slight angle: an ellipse with a hole."""
    x0, y0, x1, y1 = box
    outer = blur(ellipse(box), 1.5)
    inner = blur(ellipse([x0 + thick, y0 + thick * 0.75, x1 - thick, y1 - thick * 0.75]), 1.5)
    m = np.clip(outer - inner, 0, 1)
    c.over(chrome(0.5 * pillow(m, thick * 0.45), tint, depth=60), m)


def glow(c, box, colour, a=0.6, r=12):
    c.over(np.zeros((N, N, 3)) + np.array(colour), blur(ellipse(box), r) * a, cast=False)


def stone_cab(c, box, colour, bezel=gold_tint()):
    """A round cabochon in a metal bezel."""
    if isinstance(colour, str): colour = COL[colour]
    x0, y0, x1, y1 = box
    bm = blur(ellipse([x0 - 12, y0 - 12, x1 + 12, y1 + 12]), 1.5)
    c.over(chrome(0.6 * pillow(bm, 10), bezel, depth=50), bm)
    m = blur(ellipse(box), 1.5)
    d = np.hypot(xx - (x0 + (x1 - x0) * 0.38), yy - (y0 + (y1 - y0) * 0.35)) / ((x1 - x0) * 0.7)
    cc = (np.zeros((N, N, 3)) + np.array(colour)) * (1.25 - 0.7 * np.clip(d, 0, 1))[..., None]
    c.over(light(0.9 * pillow(m, (x1 - x0) * 0.4), np.clip(cc, 0, 1), depth=80, spec=0.9, gloss=60), m)
    gx, gy = x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.28
    glow(c, [gx - 9, gy - 9, gx + 9, gy + 9], (1, 1, 1), 0.85, 3)


def ring(c, tint, gem=None, gem_r=62, notches=False, rng=None):
    metal_ring(c, [110, 200, 402, 440], 46, tint)
    if notches:
        for t in np.linspace(0.15, 0.85, 7):
            ang = np.pi * (0.1 + t * 0.8)
            x, y = 256 + 146 * np.cos(ang), 320 + 120 * np.sin(ang)
            m = blur(poly([(x - 5, y - 10), (x + 5, y - 10), (x + 5, y + 10), (x - 5, y + 10)]), 1)
            c.over(np.zeros((N, N, 3)) + 0.25, m * 0.6, cast=False)
    if gem:
        stone_cab(c, [256 - gem_r, 210 - gem_r, 256 + gem_r, 210 + gem_r], COL[gem] if isinstance(gem, str) else gem, tint)


def chain(c, pts, tint, link=16):
    """A chain of interlocking oval links along a polyline: flat links face us, edge links are thin bars."""
    pts = np.array(pts, np.float32)
    seg = np.diff(pts, axis=0); lens = np.hypot(seg[:, 0], seg[:, 1]); acc = np.cumsum(lens); tot = lens.sum()
    n = int(tot / (link * 1.05))
    for i in range(n + 1):
        s = i / max(1, n) * tot
        k = min(np.searchsorted(acc, s, side='right'), len(seg) - 1)
        s0 = s - (acc[k] - lens[k])
        p = pts[k] + seg[k] * (s0 / max(lens[k], 1e-3))
        d = seg[k] / max(lens[k], 1e-3); nrm = np.array([-d[1], d[0]])
        if i % 2 == 0:
            L, W = link * 1.15, link * 0.72
            q = [tuple(p + d * L * np.cos(a) + nrm * W * np.sin(a)) for a in np.linspace(0, 2 * np.pi, 24)]
            qi = [tuple(p + d * (L - 6) * np.cos(a) + nrm * (W - 6) * np.sin(a)) for a in np.linspace(0, 2 * np.pi, 24)]
            m = np.clip(blur(poly(q), 0.8) - blur(poly(qi), 0.8), 0, 1)
            c.over(chrome(0.6 * pillow(m, 3), tint, depth=50, spec=1.0), m, cast=True)
        else:
            m = blur(poly([tuple(p - d * link * 1.1), tuple(p + d * link * 1.1)], width=7), 0.8)
            c.over(chrome(0.6 * pillow(m, 3), tint, depth=50, spec=1.0), m, cast=True)


def cord(c, pts, colour, width=12, rng=None):
    m = blur(poly(pts, width=width), 1.5)
    tex = np.zeros((N, N, 3)) + np.array(colour)
    tex = tex * (0.85 + 0.2 * np.sin((xx + yy) / 4.0))[..., None]
    c.over(light(0.4 * pillow(m, 5), np.clip(tex, 0, 1), depth=40, spec=0.1), m)


def loop_pts(top, bottom, half):
    """The two sides of a necklace hanging in a U, from the top corners to the pendant."""
    t = np.linspace(0, 1, 14)
    left = [(256 - half * np.cos(a * np.pi / 2), top + (bottom - top) * np.sin(a * np.pi / 2)) for a in t]
    right = [(256 + half * np.cos(a * np.pi / 2), top + (bottom - top) * np.sin(a * np.pi / 2)) for a in t]
    return left, right


def necklace(c, tint, kind='chain'):
    left, right = loop_pts(60, 290, 175)
    if kind == 'chain':
        chain(c, left, tint); chain(c, right, tint)
    else:
        cord(c, left, tint); cord(c, right, tint)


def flat_metal(c, pts, tint, depth=50, r=8):
    m = blur(poly(pts), 1.3)
    c.over(chrome(0.55 * pillow(m, r), tint, depth=depth), m)
    return m


def leather(c, rng, pts, colour=(0.42, 0.24, 0.12), r=14):
    m = blur(poly(pts), 1.5)
    tex = leather_col(rng, colour)
    c.over(light(0.4 * pillow(m, r), np.clip(tex, 0, 1), depth=45, spec=0.15), m)
    return m


def stitches(c, p0, p1, n=9, colour=(0.85, 0.78, 0.6)):
    for t in np.linspace(0.05, 0.95, n):
        x = p0[0] + (p1[0] - p0[0]) * t; y = p0[1] + (p1[1] - p0[1]) * t
        m = blur(ellipse([x - 6, y - 2.5, x + 6, y + 2.5]), 0.8)
        c.over(np.zeros((N, N, 3)) + np.array(colour), m, cast=False)


def stud(c, x, y, r, tint=steel_tint()):
    m = blur(ellipse([x - r, y - r, x + r, y + r]), 1)
    c.over(chrome(0.7 * pillow(m, r * 0.7), tint, depth=60), m)


def belt(c, rng, buckle=IRON, colour=(0.40, 0.23, 0.11)):
    """A belt strap across, curving slightly, with a square buckle."""
    leather(c, rng, [(40, 250), (472, 210), (472, 290), (40, 330)], colour)
    stitches(c, (60, 262), (460, 224), 14)
    stitches(c, (60, 318), (460, 278), 14)
    o = blur(rect([196, 196, 316, 346], 14), 1.2)
    h = blur(rect([222, 222, 290, 320], 8), 1.2)
    m = np.clip(o - h, 0, 1)
    c.over(chrome(0.6 * pillow(m, 10), buckle, depth=60), m)
    flat_metal(c, [(250, 230), (262, 230), (262, 312), (250, 312)], buckle, r=4)


# ---------- realism pass (2026-11-16 "ทำให้สมจริงขึ้น") ----------
def worn(rgb, rng, amount=0.18, scratches=True):
    """Metal that has been worn: soft tarnish blotches and fine scratches."""
    t = noise(rng, 7, 4)
    out = rgb * (1 - amount * 0.5 + amount * t)[..., None]
    if scratches:
        s = np.zeros((N, N), np.float32)
        for _ in range(26):
            x0, y0 = rng.uniform(60, 450, 2); ang = rng.uniform(0, np.pi); L = rng.uniform(15, 60)
            s = np.maximum(s, poly([(x0, y0), (x0 + L * np.cos(ang), y0 + L * np.sin(ang))], width=1.2) * rng.uniform(0.3, 0.8))
        out = out + 0.10 * blur(s, 0.6)[..., None]
    return np.clip(out, 0, 1)


def metal_real(c, m, tint, rng, r=10, depth=60, amount=0.18):
    c.over(worn(chrome(0.55 * pillow(m, r), tint, depth=depth), rng, amount), m)


def facet_gem(c, cx, cy, rx, ry, colour, rng=None):
    """An oval brilliant cut seen from above: table, star and kite facets, darker toward the girdle."""
    if isinstance(colour, str): colour = COL[colour]
    col = np.array(colour)
    dx = (xx - cx) / rx; dy = (yy - cy) / ry
    r = np.hypot(dx, dy); a = np.arctan2(dy, dx)
    m = blur((r <= 1).astype(np.float32), 1.2)
    k = 8
    sector = np.floor((a + np.pi) / (2 * np.pi) * k)
    shade = 0.55 + 0.45 * np.cos((sector + 0.5) * 2 * np.pi / k - np.pi * 1.25)   # facets facing the light are bright
    table = (r < 0.48).astype(np.float32)
    ring2 = ((r >= 0.48) & (r < 0.78)).astype(np.float32)
    sector2 = np.floor((a + np.pi + np.pi / k) / (2 * np.pi) * k)
    shade2 = 0.5 + 0.5 * np.cos((sector2 + 0.5) * 2 * np.pi / k - np.pi * 1.25)
    v = table * (0.95 + 0.25 * (0.5 - dy * 0.5)) + ring2 * (0.45 + 0.6 * shade2) + (1 - table - ring2) * (0.30 + 0.55 * shade)
    rgb = np.clip(col[None, None, :] * v[..., None] * 1.15, 0, 1)
    # inner fire: a few pale sparkles
    rgb = rgb + 0.35 * (np.clip(1 - np.hypot(dx + 0.25, dy + 0.3) / 0.25, 0, 1) ** 2)[..., None]
    c.over(np.clip(rgb, 0, 1), m)
    edges = np.zeros((N, N), np.float32)
    for i in range(k):
        ang = i * 2 * np.pi / k - np.pi
        edges = np.maximum(edges, poly([(cx + 0.48 * rx * np.cos(ang), cy + 0.48 * ry * np.sin(ang)), (cx + rx * np.cos(ang), cy + ry * np.sin(ang))], width=1.5))
    edges = np.maximum(edges, np.clip(1 - np.abs(r - 0.48) * 60, 0, 1))
    c.over(np.zeros((N, N, 3)) + col * 0.30, blur(edges, 0.6) * m * 0.7, cast=False)
    girdle = np.clip(1 - np.abs(r - 0.97) * 40, 0, 1)
    c.over(np.zeros((N, N, 3)) + col * 0.25, blur(girdle, 0.6) * 0.8, cast=False)
    glow(c, [cx - rx * 0.55, cy - ry * 0.6, cx - rx * 0.15, cy - ry * 0.2], (1, 1, 1), 0.7, 5)


def set_gem(c, cx, cy, rx, ry, colour, tint, rng, prongs=6):
    """A faceted stone in a collet with claw prongs."""
    coll = blur(ellipse([cx - rx - 14, cy - ry - 14, cx + rx + 14, cy + ry + 14]), 1.3)
    metal_real(c, coll, tint, rng, r=10)
    facet_gem(c, cx, cy, rx, ry, colour, rng)
    for i in range(prongs):
        ang = i * 2 * np.pi / prongs + np.pi / prongs
        px, py = cx + (rx + 2) * np.cos(ang), cy + (ry + 2) * np.sin(ang)
        pm = blur(ellipse([px - 9, py - 11, px + 9, py + 11]), 1)
        metal_real(c, pm, tint, rng, r=6)


def engraved_band(c, box, thick, tint, rng, pattern='scroll'):
    """A ring band with milgrain edges and an engraved pattern."""
    x0, y0, x1, y1 = box
    outer = blur(ellipse(box), 1.5)
    inner = blur(ellipse([x0 + thick, y0 + thick * 0.75, x1 - thick, y1 - thick * 0.75]), 1.5)
    m = np.clip(outer - inner, 0, 1)
    metal_real(c, m, tint, rng, r=thick * 0.45)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rxo, ryo = (x1 - x0) / 2, (y1 - y0) / 2
    rxi, ryi = rxo - thick, ryo - thick * 0.75
    eng = np.zeros((N, N), np.float32)
    for t in np.linspace(0.06, 0.94, 22):          # milgrain beads along both edges, front half only
        ang = np.pi * t
        for f, rr in ((0.95, (rxo, ryo)), (1.0, (rxi, ryi))):
            px = cx + rr[0] * f * np.cos(ang) * (0.97 if f < 1 else 1.03); py = cy + rr[1] * f * np.sin(ang) * (0.97 if f < 1 else 1.03)
            eng = np.maximum(eng, blur(ellipse([px - 3, py - 3, px + 3, py + 3]), 0.6))
    if pattern == 'scroll':
        for t in np.linspace(0.12, 0.88, 9):
            ang = np.pi * t
            rmid = ((rxo + rxi) / 2, (ryo + ryi) / 2)
            px, py = cx + rmid[0] * np.cos(ang), cy + rmid[1] * np.sin(ang)
            s = np.linspace(0, 1.6 * np.pi, 12)
            pts = [(px + 9 * np.cos(u) * (1 - u / 6), py + 7 * np.sin(u) * (1 - u / 6)) for u in s]
            eng = np.maximum(eng, poly(pts, width=2.2))
    groove = np.clip(1 - np.abs(np.hypot((xx - cx) / ((rxo + rxi) / 2), (yy - cy) / ((ryo + ryi) / 2)) - 1) * 90, 0, 1) * (yy > cy)
    if pattern != 'scroll':
        eng = np.maximum(eng, groove)
    c.over(np.zeros((N, N, 3)) + np.array(tint) * 0.22, blur(eng, 0.6) * m * 0.9, cast=False)
    hi = np.clip(1 - np.abs(np.hypot((xx - cx) / (rxo - 6), (yy - cy) / (ryo - 5)) - 1) * 70, 0, 1) * (yy > cy) * (xx < cx + 40)
    c.over(np.zeros((N, N, 3)) + 1.0, blur(hi, 1) * m * 0.35, cast=False)
    return m


def braid(c, pts, colour, width=18, rng=None):
    """A braided cord: alternating diagonal strands along the path."""
    m = blur(poly(pts, width=width), 1.3)
    p = np.array(pts, np.float32)
    seg = np.diff(p, axis=0); L = np.hypot(seg[:, 0], seg[:, 1])
    along = np.zeros((N, N), np.float32)
    # approximate the position along the path with the nearest vertex index (good enough for texture)
    d = np.full((N, N), 1e9, np.float32)
    acc = np.concatenate([[0], np.cumsum(L)])
    for i, (x, y) in enumerate(p):
        dd = (xx - x) ** 2 + (yy - y) ** 2
        sel = dd < d; d = np.where(sel, dd, d); along = np.where(sel, acc[i], along)
    strand = 0.5 + 0.5 * np.sin(along / 5.0 + (xx - yy) / 6.0)
    tex = np.zeros((N, N, 3)) + np.array(colour)
    tex = tex * (0.65 + 0.45 * strand)[..., None]
    c.over(light(0.45 * pillow(m, width * 0.35), np.clip(tex, 0, 1), depth=45, spec=0.12), m)
