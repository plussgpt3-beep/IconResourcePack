"""Evolved axes, bows and armour (โรงตีบวก, 2026-11-14), in the family of the evolved swords (_gear.py):
tier 2 the element shows in the metal; tier 3 its marks (flames, frost spikes, lightning, a serpent) and a
gem; tier 4 dark metal, big marks, floating sparks and gold. Ways (a/b) only for weapons."""
import zlib
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, rect, chrome, band, noise, wood, leather_col, gold_tint, mask_from
from _gear import ELEMENTS, _glowpaint
from lib import steel_tint

DARK = {'fire': (0.42, 0.16, 0.10), 'ice': (0.62, 0.82, 1.0), 'storm': (0.34, 0.34, 0.48), 'venom': (0.20, 0.30, 0.20)}


def _split(path):
    e = path.split('_')[0]
    return e, (path.split('_')[1] if '_' in path else '')


def _metal_tint(elem, tier):
    return DARK[elem] if tier == 4 else ELEMENTS[elem][0]


def _halo(c, mask, glow, tier):
    if tier >= 3:
        h = np.clip(blur(mask, 16 if tier == 4 else 10) * (1.5 if tier == 4 else 1.0), 0, 0.85)
        c.over(np.ones((N, N, 3)) * np.array(glow), np.clip(h - mask, 0, 1), cast=False)


def _sparks(c, rng, elem, mask, n):
    ys, xs = np.nonzero(blur(mask, 30) > 0.05)
    glow = ELEMENTS[elem][1]
    for _ in range(n):
        i = rng.integers(len(xs)); x, y = xs[i], ys[i]; r = rng.uniform(3, 7)
        if elem == 'ice':
            m = poly([(x, y - r * 2), (x + r, y), (x, y + r * 2), (x - r, y)])
        else:
            m = blur(ellipse([x - r, y - r, x + r, y + r]), 1)
        _glowpaint(c, m, glow, 0.9, 4)


def _marks(c, rng, elem, tier, area, axis_ang=-0.8):
    """Element marks painted inside a mask: flame licks, frost cracks, lightning veins, scale spots."""
    glow = ELEMENTS[elem][1]
    k = 0.5 if tier == 3 else 0.8
    if elem == 'fire':
        n = np.sin((xx + yy) / 10.0 + 6 * noise(rng, 4, 2))
        m = np.clip((n - 0.55) * 5, 0, 1) * area
    elif elem == 'ice':
        n = np.abs(np.sin((xx * 0.9 + yy * 0.4) / 9.0) * np.sin((xx * -0.3 + yy) / 11.0))
        m = np.clip((0.12 - n) * 10, 0, 1) * area
    elif elem == 'storm':
        n = np.abs(np.sin(xx / 13.0 + 3 * np.sin(yy / 19.0)))
        m = np.clip((0.10 - n) * 12, 0, 1) * area
    else:
        n = np.sin(xx / 9.0) * np.sin(yy / 9.0)
        m = np.clip((np.abs(n) - 0.8) * 6, 0, 1) * area
    _glowpaint(c, blur(m, 0.8), glow, k, 5)


def _gem(c, x, y, r, glow):
    g = blur(ellipse([x - r, y - r, x + r, y + r]), 1.2)
    c.over(chrome(pillow(g, 8, 0.7), glow, depth=60, sky=1.1, ground=0.25), g)


def _trim(c, mask, tier, guard_t, width=7):
    edge = np.clip(mask - blur(mask, width) * 1.15, 0, 1) * 2
    edge = np.clip(edge, 0, 1)
    c.over(chrome(pillow(edge, 3) * 0.6, gold_tint() if tier == 4 else guard_t, depth=30), edge * mask)


# ===== weapons =====

def axe(path, tier):
    elem, way = _split(path)
    blade_t, glow, guard_t, grip = ELEMENTS[elem]
    metal = _metal_tint(elem, tier)
    rng = np.random.default_rng(zlib.crc32(repr(('axe', path, tier)).encode()))
    c = Canvas()
    p0, p1 = (110, 470), (340, 52)
    s, t = band(p0, p1, 0)
    haft = blur(((s > 0) & (s < 1.02) & (np.abs(t) < 16)).astype(np.float32), 1)
    # blade shape
    big = 1.0 + 0.15 * (tier - 2)
    cx, cy = 312, 120
    def P(pts): return [(cx - (x - cx) * big, cy + (y - cy) * big) for x, y in pts]   # blade faces left, as the game's axes do
    if way == 'b' or tier == 2:      # bearded single bit, long lower hook
        pts = [(300, 70), (410, 30), (452, 120), (440, 230), (380, 290), (360, 200), (300, 170)]
        blade = poly(P(pts))
    else:                            # double bit
        blade = np.maximum(poly(P([(300, 60), (420, 20), (455, 120), (420, 220), (300, 180)])),
                           poly(P([(330, 70), (215, 30), (180, 120), (215, 215), (330, 180)])))
    if tier >= 3:   # notched / spiked edge by element
        if elem in ('fire', 'ice'):
            for k in range(5):
                a = -0.9 + k * 0.45
                bx, by = cx - 135 * big * np.cos(a), cy + 135 * big * np.sin(a)
                blade = np.maximum(blade, poly([(bx + 14, by - 6), (bx - 34 * np.cos(a), by + 34 * np.sin(a)), (bx - 8, by + 14)]))
    blade = blur(blade, 1.3)
    _halo(c, blade, glow, tier)
    c.over(light(np.clip(1 - np.abs(t) / 16, 0, 1) ** 0.5 * haft,
                 leather_col(rng, grip) if tier == 4 else wood(rng, (0.42, 0.26, 0.14), angle=-1.2, rings=4), depth=30, spec=0.3), haft)
    edge = np.clip((np.hypot(xx - cx, yy - cy) - 95 * big) / 40, 0, 1) * blade
    c.over(chrome(0.45 * pillow(blade, 16) + 0.25 * edge, metal, depth=50, sky=0.95, ground=0.12), blade)
    if tier >= 3: _marks(c, rng, elem, tier, blade * np.clip(1 - edge, 0, 1))
    if tier == 4: _trim(c, blade, tier, guard_t, 8)
    # socket and gem
    sock = blur(rect([cx - 22, cy - 40, cx + 22, cy + 70], 8), 1.2)
    c.over(chrome(pillow(sock, 8) * 0.7, gold_tint() if tier == 4 else guard_t, depth=40), sock)
    if tier >= 3: _gem(c, cx, cy + 15, 15 if tier == 3 else 19, glow)
    if tier == 4: _sparks(c, rng, elem, blade, 14)
    return c.image()


def bow(path, tier):
    elem, way = _split(path)
    blade_t, glow, guard_t, grip = ELEMENTS[elem]
    metal = _metal_tint(elem, tier)
    rng = np.random.default_rng(zlib.crc32(repr(('bow', path, tier)).encode()))
    c = Canvas()
    recurve = way == 'a'
    # limbs as a polyline arc from top-right to bottom-left, bulging to the upper left
    ts = np.linspace(0, 1, 60)
    ax, ay, bx2, by2 = 420, 60, 60, 450
    mx, my = (40, 40) if way == 'b' else (90, 90)
    pts = [((1 - u) ** 2 * ax + 2 * (1 - u) * u * mx + u * u * bx2, (1 - u) ** 2 * ay + 2 * (1 - u) * u * my + u * u * by2) for u in ts]
    if recurve:
        pts = [(ax + 55, ay + 45), (ax + 30, ay + 5)] + pts + [(bx2 - 5, by2 - 30), (bx2 + 45, by2 + 55)]
    limb = blur(poly([(round(x), round(y)) for x, y in pts], width=34 if tier < 4 else 40), 1.2)
    _halo(c, limb, glow, tier)
    col = wood(rng, (0.38, 0.22, 0.12), rings=4) if tier == 2 else np.ones((N, N, 3)) * np.array(metal)
    if tier == 2:
        c.over(light(0.5 * pillow(limb, 6), col, depth=40, spec=0.3), limb)
        tips = np.maximum(blur(ellipse([ax - 18, ay - 18, ax + 18, ay + 18]), 1), blur(ellipse([bx2 - 18, by2 - 18, bx2 + 18, by2 + 18]), 1))
        c.over(chrome(pillow(tips, 6) * 0.7, blade_t, depth=40), tips)
    else:
        c.over(chrome(0.5 * pillow(limb, 8), metal, depth=50), limb)
        _marks(c, rng, elem, tier, limb)
        if tier == 4: _trim(c, limb, tier, guard_t, 6)
    # string
    sx = [pts[0], pts[-1]]
    string = blur(poly(sx, width=4 if tier < 4 else 6), 0.8)
    if tier >= 3: _glowpaint(c, string, glow, 0.8, 5)
    else: c.over(np.zeros((N, N, 3)) + 0.9, string, cast=False)
    # grip
    gx, gy = pts[len(pts) // 2]
    gripm = blur(ellipse([gx - 22, gy - 40, gx + 22, gy + 40]), 1.2)
    c.over(light(pillow(gripm, 6) * 0.6, leather_col(rng, grip), depth=30, spec=0.2), gripm)
    if tier >= 3: _gem(c, gx, gy, 13 if tier == 3 else 17, glow)
    if tier == 4: _sparks(c, rng, elem, limb, 14)
    return c.image()


# ===== armour (front views) =====

def _helmet():
    dome = ellipse([126, 60, 386, 330])
    face = rect([136, 190, 376, 440], 40)
    cheeks = np.maximum(poly([(136, 300), (200, 300), (220, 430), (150, 440)]), poly([(376, 300), (312, 300), (292, 430), (362, 440)]))
    shell = np.maximum(np.maximum(dome, face), cheeks)
    shell = np.clip(shell - poly([(226, 330), (286, 330), (276, 445), (236, 445)]), 0, 1)   # open chin
    ridge = rect([246, 56, 266, 300], 8)
    slit = np.maximum(rect([160, 238, 244, 258], 6), rect([268, 238, 352, 258], 6))
    breaths = np.zeros((N, N), np.float32)
    for y in (300, 324):
        for x in (170, 200, 312, 342):
            breaths = np.maximum(breaths, ellipse([x - 6, y - 6, x + 6, y + 6]))
    return blur(shell, 1.2), blur(np.maximum(slit, breaths), 1), blur(ridge, 1.2), [((0, 1), (200, 200))]


def _chest():
    torso = poly([(160, 120), (352, 120), (372, 300), (340, 440), (172, 440), (140, 300)])
    pl = ellipse([60, 90, 210, 230]); pr = ellipse([302, 90, 452, 230])
    neck = ellipse([210, 70, 302, 150])
    body = np.clip(np.maximum(torso, np.maximum(pl, pr)) - neck, 0, 1)
    lames = np.zeros((N, N), np.float32)
    for y in (330, 372, 412):
        lames = np.maximum(lames, rect([160, y, 352, y + 6], 3) * torso)
    keel = rect([250, 150, 262, 320], 4)
    return blur(body, 1.2), blur(lames, 1), blur(keel, 1.2), []


def _legs():
    m = poly([(150, 60), (362, 60), (372, 460), (284, 460), (262, 200), (250, 200), (228, 460), (140, 460)])
    belt = rect([146, 60, 366, 104], 8)
    knees = np.maximum(ellipse([150, 250, 232, 330]), ellipse([280, 250, 362, 330]))
    lames = np.zeros((N, N), np.float32)
    for y in (150, 196, 370, 412):
        lames = np.maximum(lames, rect([140, y, 372, y + 6], 3) * m)
    return blur(m, 1.2), blur(lames, 1), blur(np.maximum(belt, knees), 1.2), []


def _boots():
    l = poly([(90, 120), (210, 120), (215, 340), (250, 380), (250, 450), (50, 450), (60, 380), (85, 340)])
    r = poly([(302, 120), (422, 120), (427, 340), (452, 380), (462, 450), (262, 450), (262, 380), (297, 340)])
    body = np.maximum(l, r)
    lames = np.zeros((N, N), np.float32)
    for y in (360, 395, 425):
        lames = np.maximum(lames, rect([40, y, 470, y + 6], 3) * body)
    cuff = np.maximum(rect([80, 120, 220, 164], 8), rect([292, 120, 432, 164], 8))
    return blur(body, 1.2), blur(lames, 1), blur(cuff, 1.2), []


SHAPES = {'helmet': _helmet, 'chest': _chest, 'legs': _legs, 'boots': _boots}


def armour(kind, path, tier):
    elem, _ = _split(path)
    blade_t, glow, guard_t, grip = ELEMENTS[elem]
    metal = _metal_tint(elem, tier)
    rng = np.random.default_rng(zlib.crc32(repr((kind, path, tier)).encode()))
    c = Canvas()
    body, detail, plate, _ = SHAPES[kind]()
    if tier >= 3:   # element crest: spikes on top / shoulders
        spikes = np.zeros((N, N), np.float32)
        ys, xs = np.nonzero(body > 0.5)
        top = ys.min()
        cols = np.linspace(xs.min() + 30, xs.max() - 30, 5 if tier == 4 else 3)
        for x in cols:
            col_ys = ys[np.abs(xs - x) < 2]
            if len(col_ys) == 0: continue
            y = col_ys.min()
            h = (55 if tier == 4 else 32) * (1.2 if abs(x - 256) < 40 else 0.8)
            if elem == 'storm':
                spikes = np.maximum(spikes, poly([(x - 10, y + 6), (x + 6, y - h * 0.5), (x - 4, y - h * 0.5), (x + 10, y - h), (x + 2, y + 6)]))
            elif elem == 'venom':
                spikes = np.maximum(spikes, poly([(x - 12, y + 6), (x + 2, y - h), (x + 12, y + 6)]))
            else:
                spikes = np.maximum(spikes, poly([(x - 14, y + 8), (x + (6 if elem == 'fire' else 0), y - h), (x + 14, y + 8)]))
        spikes = blur(spikes, 1.2)
        body = np.maximum(body, spikes)
    _halo(c, body, glow, tier)
    nx = (xx - 256) / 200
    shade = 0.45 * pillow(body, 18) + 0.15 * np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * body
    c.over(chrome(shade, metal, depth=50, sky=0.95, ground=0.12), body)
    if tier >= 3: _marks(c, rng, elem, tier, body * np.clip(blur(noise(rng, 5, 2) > 0.45, 6), 0, 1))
    trim_t = gold_tint() if tier == 4 else (guard_t if tier == 3 else steel_tint())
    c.over(chrome(pillow(plate, 6) * 0.8, trim_t, depth=45), plate)
    dark = 0.06 if kind == 'helmet' else 0.0
    c.over(np.zeros((N, N, 3)) + 0.05, detail * (1.0 if kind == 'helmet' else 0.55), cast=False)
    _trim(c, body, tier, guard_t, 8 if tier == 4 else 6)
    if tier >= 3:
        ys, xs = np.nonzero(body > 0.5)
        gy = {'helmet': 150, 'chest': 230, 'legs': 82, 'boots': 142}[kind]
        if kind == 'boots':
            _gem(c, 140, gy, 12 if tier == 3 else 15, glow); _gem(c, 372, gy, 12 if tier == 3 else 15, glow)
        else:
            _gem(c, 256, gy, 16 if tier == 3 else 21, glow)
    if tier == 4: _sparks(c, rng, elem, body, 16)
    return c.image()
