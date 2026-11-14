"""Evolved gear (โรงตีบวก, 2026-11-14): the sword a weapon becomes when it evolves at the royal smith.
Tier 2 = the element shows in the steel; tier 3 = one of two ways (a = broad greatblade, b = curved
blade); tier 4 = the masterwork, gilt and glowing. Drawn pommel at lower left, tip at upper right,
the way Minecraft holds a sword."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, chrome, band, noise, leather_col, gold_tint, steel_tint

# element: (blade tint, glow colour, guard tint, grip colour)
ELEMENTS = {
    'fire':  ((0.80, 0.52, 0.40), (1.00, 0.45, 0.10), (0.62, 0.20, 0.12), (0.30, 0.08, 0.05)),
    'ice':   ((0.70, 0.86, 0.98), (0.55, 0.85, 1.00), (0.55, 0.72, 0.88), (0.12, 0.18, 0.32)),
    'storm': ((0.80, 0.80, 0.90), (1.00, 0.92, 0.35), (0.85, 0.72, 0.30), (0.16, 0.14, 0.28)),
    'venom': ((0.55, 0.72, 0.52), (0.45, 1.00, 0.30), (0.28, 0.42, 0.22), (0.10, 0.20, 0.08)),
}


def draw(path, tier):
    elem = path.split('_')[0]
    way = path.split('_')[1] if '_' in path else ''
    blade_t, glow, guard_t, grip = ELEMENTS[elem]
    if tier == 4: blade_t = {'fire': (0.42, 0.16, 0.10), 'ice': (0.62, 0.82, 1.0), 'storm': (0.34, 0.34, 0.48), 'venom': (0.20, 0.30, 0.20)}[elem]
    rng = np.random.default_rng(hash((path, tier)) & 0xFFFF)
    c = Canvas()
    p0, p1 = (70, 442), (446, 66)
    s, t = band(p0, p1, 0)
    L = np.hypot(p1[0] - p0[0], p1[1] - p0[1])
    g0 = 0.24
    broad = way == 'a' or (tier == 4 and way == 'a')
    curved = way == 'b'
    bw = 30 if tier == 2 else (40 if broad else 30)
    if tier == 4: bw += 6
    # blade outline: taper, a curve for way b, a flame wave for fire masterworks
    off = 0.0
    if curved: off = 34 * np.sin(np.clip((s - g0) / (1 - g0), 0, 1) * np.pi * 0.9)
    tc = t - off
    w = bw * np.clip((1 - s) / (0.10 if not broad else 0.07), 0, 1) ** 0.55
    if elem == 'fire' and tier >= 3: w = w * (1 + 0.16 * np.sin(s * L / 16.0))
    if elem == 'ice' and tier >= 3: w = w * (1 + 0.10 * np.sign(np.sin(s * L / 22.0)))
    blade = blur(((s > g0) & (s < 1) & (np.abs(tc) < w)).astype(np.float32), 1.3)
    # glow behind the blade
    if tier >= 3:
        halo = np.clip(blur(blade, 16 if tier == 4 else 11) * (1.6 if tier == 4 else 1.1), 0, 0.85)
        c.over(np.ones((N, N, 3)) * np.array(glow), np.clip(halo - blade, 0, 1), cast=False)
    h = np.clip(1 - np.abs(tc) / (w + 1e-3), 0, 1) ** 0.6 * blade
    h -= 0.22 * np.exp(-(tc / 4.5) ** 2) * (s < 0.86) * blade
    c.over(chrome(h, blade_t, depth=42), blade)
    # the element running down the fuller
    vein = np.exp(-(tc / (5 if tier == 2 else 7)) ** 2) * (s > g0 + 0.04) * (s < 0.88) * blade
    if elem == 'storm':
        zig = 6 * np.sign(np.sin(s * L / 14.0))
        vein = np.exp(-((tc - zig) / 4) ** 2) * (s > g0 + 0.04) * (s < 0.9) * blade
    if elem == 'venom':
        vein = vein * (0.6 + 0.4 * (noise(rng, 18) > 0.5))
    k = 0.8 if tier == 2 else 1.0
    c.over(np.ones((N, N, 3)) * np.array(glow), np.clip(vein * k, 0, 1), cast=False)
    if tier >= 3:
        decorate(c, rng, elem, tier, p0, p1, L, g0, bw, off_fn=(lambda ss: 34 * np.sin(np.clip((ss - g0) / (1 - g0), 0, 1) * np.pi * 0.9)) if curved else (lambda ss: 0.0), glow=glow)
    # guard: plain bar, winged at tier 3, a crowned crossguard at tier 4
    gw = 66 if tier == 2 else (88 if tier == 3 else 112)
    gs = (13 if tier < 4 else 16) / L
    wing = np.clip(np.abs(t) / gw, 0, 1)
    guard = ((np.abs(s - g0) < gs * (1 + (0.8 * wing ** 2 if tier >= 3 else 0))) & (np.abs(t) < gw)).astype(np.float32)
    guard = blur(guard, 1.5)
    gt = gold_tint() if tier == 4 else guard_t
    c.over(chrome(pillow(guard, 6) * 0.8, gt, depth=40), guard)
    if tier >= 3:   # a gem where blade meets guard
        gx, gy = p0[0] + (p1[0] - p0[0]) * g0, p0[1] + (p1[1] - p0[1]) * g0
        r = 15 if tier == 3 else 19
        gem = blur(ellipse([gx - r, gy - r, gx + r, gy + r]), 1.2)
        c.over(chrome(pillow(gem, 8, 0.7), glow, depth=60, sky=1.1, ground=0.25), gem)
    # grip
    grip_m = blur(((s > 0.05) & (s < g0 - gs) & (np.abs(t) < 12)).astype(np.float32), 1.2)
    wrap = 0.72 + 0.28 * np.sin(s * L / 4.0)
    c.over(light(pillow(grip_m, 5) * 0.6, leather_col(rng, grip) * wrap[..., None], depth=30, spec=0.2), grip_m)
    # pommel
    px, py = p0[0] + (p1[0] - p0[0]) * 0.03, p0[1] + (p1[1] - p0[1]) * 0.03
    r = 21 if tier < 4 else 25
    pm = blur(ellipse([px - r, py - r, px + r, py + r]), 1.2)
    c.over(chrome(pillow(pm, 10, 0.7), gold_tint() if tier == 4 else guard_t, depth=50), pm)
    return c.image()


def _pt(p0, p1, L, ss, tt):
    d = np.array([p1[0] - p0[0], p1[1] - p0[1]]) / L
    n = np.array([-d[1], d[0]])
    q = np.array(p0) + d * ss * L + n * tt
    return (float(q[0]), float(q[1]))


def _glowpaint(c, mask, col, k=1.0, halo=6):
    c.over(np.ones((N, N, 3)) * np.array(col), np.clip(blur(mask, halo) * 0.9 * k, 0, 0.9), cast=False)
    c.over(np.ones((N, N, 3)) * np.clip(np.array(col) * 0.5 + 0.5, 0, 1), np.clip(mask, 0, 1), cast=False)


def decorate(c, rng, elem, tier, p0, p1, L, g0, bw, off_fn, glow):
    """What makes a tier 3 or 4 blade look the part: flames, frost spikes, lightning, a serpent."""
    big = tier == 4
    P = lambda ss, tt: _pt(p0, p1, L, ss, tt + off_fn(ss))
    if elem == 'fire':
        m = np.zeros((N, N), np.float32)
        for i, ss in enumerate(np.linspace(g0 + 0.08, 0.92, 7 if big else 5)):
            side = 1 if i % 2 == 0 else -1
            h = (46 if big else 30) * (1 - 0.4 * ss)
            w = bw * (1 - ss) + 8
            m = np.maximum(m, poly([P(ss - 0.035, side * w * 0.7), P(ss + 0.03, side * (w + h)), P(ss + 0.05, side * w * 0.6)]))
        m = blur(m, 2)
        _glowpaint(c, m, (1.0, 0.55, 0.12), 1.0 if big else 0.8, 8)
        if big:
            for _ in range(14):
                ss = rng.uniform(g0, 1.0); tt = rng.uniform(-90, 90)
                x, y = P(ss, tt); r = rng.uniform(4, 7)
                _glowpaint(c, blur(ellipse([x - r, y - r, x + r, y + r]), 1), (1.0, 0.75, 0.25), 0.8, 5)
    elif elem == 'ice':
        m = np.zeros((N, N), np.float32)
        for i, ss in enumerate(np.linspace(g0 + 0.06, 0.88, 8 if big else 5)):
            side = 1 if i % 2 == 0 else -1
            h = (58 if big else 34) * (1 - 0.3 * ss)
            w = bw * (1 - ss) + 6
            m = np.maximum(m, poly([P(ss - 0.025, side * w * 0.6), P(ss + 0.05, side * (w + h)), P(ss + 0.02, side * w * 0.6)]))
        m = blur(m, 1.5)
        c.over(np.ones((N, N, 3)) * np.array((0.6, 0.85, 1.0)), np.clip(blur(m, 8) * 0.7, 0, 0.8), cast=False)
        c.over(chrome(pillow(m, 6) * 0.9, (0.75, 0.92, 1.0), depth=50, sky=1.1, ground=0.35), m)
        if big:
            for _ in range(18):
                x, y = P(rng.uniform(g0, 1.0), rng.uniform(-100, 100)); r = rng.uniform(3, 6)
                _glowpaint(c, poly([(x, y - r * 2), (x + r, y), (x, y + r * 2), (x - r, y)]), (0.8, 0.95, 1.0), 0.9, 4)
    elif elem == 'storm':
        def bolt(ss0, tt0, ang, length, seg):
            pts = [P(ss0, tt0)]
            x, y = pts[0]
            for _ in range(seg):
                ang2 = ang + rng.uniform(-0.9, 0.9)
                x += np.cos(ang2) * length / seg; y += np.sin(ang2) * length / seg
                pts.append((x, y))
            return poly(pts, width=12 if big else 8)
        m = np.zeros((N, N), np.float32)
        # a bolt running the blade
        pts = [P(ss, 10 * (1 if i % 2 else -1)) for i, ss in enumerate(np.linspace(g0 + 0.04, 0.95, 12))]
        m = np.maximum(m, poly(pts, width=10 if big else 7))
        for k in range(5 if big else 2):
            ss = rng.uniform(g0 + 0.1, 0.9); side = 1 if k % 2 else -1
            d = np.array([p1[0] - p0[0], p1[1] - p0[1]]) / L
            base = np.arctan2(d[1], d[0]) + side * rng.uniform(0.9, 1.6)
            m = np.maximum(m, bolt(ss, side * bw, base, 90 if big else 55, 5))
        _glowpaint(c, blur(m, 1), (1.0, 0.95, 0.45), 1.0, 10 if big else 6)
    elif elem == 'venom':
        # a serpent coiling up the blade
        ss = np.linspace(g0 + 0.02, 0.86, 120)
        tt = (bw + 6) * np.sin(ss * (16 if big else 12))
        body = poly([P(a, b) for a, b in zip(ss, tt)], width=22 if big else 16)
        body = blur(body, 1.2)
        col = np.array((0.45, 0.85, 0.15))
        scales = 0.75 + 0.25 * (noise(rng, 6) > 0.5)
        c.over(light(pillow(body, 6) * 0.7, col * scales[..., None], depth=40, spec=0.5), body)
        hx, hy = P(0.88, tt[-1])
        r = 26 if big else 18
        head = blur(ellipse([hx - r, hy - r * 0.75, hx + r, hy + r * 0.75]), 1.2)
        c.over(light(pillow(head, 8) * 0.8, np.ones((N, N, 3)) * col, depth=40, spec=0.5), head)
        for ex in (-6, 6):
            e = blur(ellipse([hx + ex - 3, hy - 5, hx + ex + 3, hy + 1]), 0.8)
            _glowpaint(c, e, (0.85, 1.0, 0.2), 1.0, 3)
        if big:
            for _ in range(6):
                x, y = P(rng.uniform(g0 + 0.1, 0.9), rng.uniform(-30, 30))
                drip = blur(poly([(x - 5, y), (x + 5, y), (x, y + 22)]), 1)
                _glowpaint(c, drip, (0.5, 1.0, 0.3), 0.9, 4)
