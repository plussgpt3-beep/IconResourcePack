"""Evolved gear tier 5 แดนอเวจี (2026-11-20). The user wanted new shapes ("อยากได้รูปทรงใหม่"), not tier 4 recoloured:
weapons and armour reforged as demon-work in obsidian with hell-gold, the element burning through them.
sword a: a split abyss greatblade with a hooked tip, demon-wing guard and a skull pommel
sword b: a curved reaver with a saw-toothed back and a crescent guard
axe a:   a double crescent axe with a demon eye and a spear spike
axe b:   one huge jagged bit with a bone hook behind
bow a:   bat-wing limbs with membrane            bow b: two great horns meeting at a skull grip
armour:  a horned demon helm, a spiked ribcage cuirass, plated legs with knee spikes, clawed sabatons.
Finished by _abyss5.abyssify(recolour_metal=False): runes, element rim, aura and sparks."""
import zlib
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, rect, chrome, noise, leather_col
from _gear import ELEMENTS
import _abyss5

METAL = {'fire': (0.58, 0.22, 0.15), 'ice': (0.42, 0.60, 0.82), 'storm': (0.46, 0.38, 0.72), 'venom': (0.32, 0.54, 0.28)}
HELLGOLD = (0.92, 0.58, 0.26)


def _glowpaint(c, mask, col, k=1.0, halo=6):
    c.over(np.ones((N, N, 3)) * np.array(col), np.clip(blur(mask, halo) * 0.9 * k, 0, 0.9), cast=False)
    c.over(np.ones((N, N, 3)) * np.clip(np.array(col) * 0.5 + 0.5, 0, 1), np.clip(mask, 0, 1), cast=False)


_TEX = {}


def _texture(seed):
    """Hammered metal with fine scratches (the user, 2026-11-20: "ขอดูสมจริงกว่านี้")."""
    if seed not in _TEX:
        rng = np.random.default_rng(seed)
        t = 0.80 + 0.22 * noise(rng, 34, 3) + 0.08 * noise(rng, 140, 2)
        sc = np.zeros((N, N), np.float32)
        for _ in range(70):
            x, y = rng.uniform(0, N, 2); a = rng.uniform(0, np.pi); l = rng.uniform(10, 40)
            sc = np.maximum(sc, poly([(x, y), (x + np.cos(a) * l, y + np.sin(a) * l)], width=1))
        _TEX[seed] = np.clip(t - 0.18 * blur(sc, 0.6), 0, 1.2)
    return _TEX[seed]


def _metal(c, m, elem, r=10, k=0.8, tint=None):
    base = np.array(tint or METAL[elem])
    steel = base * 0.45 + np.array((0.42, 0.42, 0.45)) * 0.55          # mostly steel, the element as a lustre
    h = pillow(m, r) * k
    tex = _texture(7)[..., None]
    lit = light(h, np.clip(steel * tex, 0, 1), depth=55, spec=0.55, gloss=40)
    shine = chrome(h, np.clip(steel * 1.15, 0, 1), depth=50, sky=1.0, ground=0.12)
    c.over(np.clip(lit * 0.55 + shine * 0.45, 0, 1), m)


def _gold(c, m, r=6):
    tex = _texture(11)[..., None]
    c.over(np.clip(chrome(pillow(m, r) * 0.8, (0.70, 0.50, 0.26), depth=40) * (0.85 + 0.15 * tex), 0, 1), m)


def _horn(c, root, ctrl, tip, r0, elem):
    """A curved horn: tapering, ridged rings, dark at the root and pale at the tip."""
    ts = np.linspace(0, 1, 48)
    pts = [((1 - t) ** 2 * root[0] + 2 * (1 - t) * t * ctrl[0] + t * t * tip[0], (1 - t) ** 2 * root[1] + 2 * (1 - t) * t * ctrl[1] + t * t * tip[1]) for t in ts]
    m = np.zeros((N, N), np.float32); rings = np.zeros((N, N), np.float32)
    for i, (x, y) in enumerate(pts):
        r = r0 * (1 - i / len(pts)) ** 0.8 + 3
        m = np.maximum(m, ellipse([x - r, y - r, x + r, y + r]))
        if i % 4 == 2 and i < len(pts) - 6:
            rings = np.maximum(rings, ellipse([x - r, y - r * 0.35, x + r, y + r * 0.35]) - ellipse([x - r + 3, y - r * 0.35 + 2, x + r - 3, y + r * 0.35 - 2]))
    m = blur(m, 1.2)
    along = np.zeros((N, N), np.float32)
    for i, (x, y) in enumerate(pts):
        along = np.maximum(along, ellipse([x - 6, y - 6, x + 6, y + 6]) * (i / len(pts)))
    g = np.clip(blur(along, 30) * 2.2, 0, 1)[..., None]
    col = np.array((0.16, 0.10, 0.08)) * (1 - g) + np.array((0.86, 0.80, 0.68)) * g
    c.over(light(pillow(m, 10) * 0.9, col * _texture(13)[..., None], depth=60, spec=0.4, gloss=30), m)
    c.over(np.zeros((N, N, 3)) + 0.06, np.clip(rings, 0, 1) * m * 0.5, cast=False)


def _gem(c, x, y, r, glow):
    g = blur(ellipse([x - r, y - r, x + r, y + r]), 1.2)
    c.over(chrome(pillow(g, 8, 0.7), glow, depth=60, sky=1.15, ground=0.25), g)
    pupil = blur(ellipse([x - r * 0.25, y - r * 0.7, x + r * 0.25, y + r * 0.7]), 1)
    c.over(np.zeros((N, N, 3)) + 0.02, pupil * 0.9, cast=False)      # a slit like a demon's eye


class Frame:
    """Local coordinates along a straight item: u 0 (butt) .. 1 (tip) from p0 to p1, v across in px."""
    def __init__(self, p0, p1):
        self.p0 = np.array(p0, np.float32); d = np.array(p1, np.float32) - self.p0
        self.L = float(np.hypot(*d)); self.d = d / self.L; self.n = np.array([-self.d[1], self.d[0]])

    def P(self, u, v):
        q = self.p0 + self.d * u * self.L + self.n * v
        return (float(q[0]), float(q[1]))

    def poly(self, pts, width=None):
        return poly([tuple(round(a) for a in self.P(u, v)) for u, v in pts], width)


def _motif(c, rng, elem, F, u0, u1, vmax, glow, big=1.0):
    """The element along a blade: flame tongues, frost shards, lightning or venom drips."""
    m = np.zeros((N, N), np.float32)
    if elem == 'fire':
        for i, u in enumerate(np.linspace(u0, u1, 7)):
            s = 1 if i % 2 else -1
            m = np.maximum(m, F.poly([(u - 0.03, s * vmax * 0.6), (u + 0.04, s * (vmax + 34 * big)), (u + 0.05, s * vmax * 0.5)]))
        _glowpaint(c, blur(m, 2), (1.0, 0.55, 0.12), 0.9, 8)
    elif elem == 'ice':
        for i, u in enumerate(np.linspace(u0, u1, 8)):
            s = 1 if i % 2 else -1
            m = np.maximum(m, F.poly([(u - 0.02, s * vmax * 0.6), (u + 0.05, s * (vmax + 44 * big)), (u + 0.02, s * vmax * 0.6)]))
        m = blur(m, 1.3)
        c.over(np.ones((N, N, 3)) * np.array((0.6, 0.86, 1.0)), np.clip(blur(m, 8) * 0.7, 0, 0.8), cast=False)
        c.over(chrome(pillow(m, 6) * 0.9, (0.78, 0.94, 1.0), depth=50, sky=1.1, ground=0.35), m)
    elif elem == 'storm':       # thin forked lightning crawling off the edges
        for k in range(5):
            u = rng.uniform(u0, u1); sd = 1 if k % 2 else -1
            pts = [(u, sd * vmax * 0.9)]; uu, vv = u, sd * vmax * 0.9
            for j in range(9):
                uu += rng.uniform(-0.02, 0.02); vv += sd * rng.uniform(4, 9) * big; pts.append((uu, vv + rng.uniform(-5, 5)))
                if j == 4:
                    br = [(uu, vv)] + [(uu + rng.uniform(-0.03, 0.03), vv + sd * 8 * (q + 1)) for q in range(3)]
                    m = np.maximum(m, F.poly(br, width=2))
            m = np.maximum(m, F.poly(pts, width=3))
        _glowpaint(c, blur(m, 0.7), (1.0, 0.96, 0.6), 0.9, 6)
    else:
        for k in range(6):
            u = rng.uniform(u0, u1)
            x, y = F.P(u, -vmax * rng.uniform(0.2, 0.9))
            m = np.maximum(m, poly([(x - 5, y), (x + 5, y), (x, y + 26 * big)]))
        _glowpaint(c, blur(m, 1), (0.5, 1.0, 0.3), 0.9, 4)


def sword(path):
    elem, way = path.split('_')
    glow = ELEMENTS[elem][1]
    rng = np.random.default_rng(zlib.crc32(repr(('sword5', path)).encode()))
    c = Canvas()
    F = Frame((70, 446), (452, 60))
    g0 = 0.26
    if way == 'a':      # split abyss greatblade, hooked tip
        us = np.linspace(g0, 0.9, 30)
        w = lambda u: 44 + 14 * np.sin((u - g0) / (0.9 - g0) * np.pi * 0.8)
        top = [(u, w(u)) for u in us] + [(0.97, 30), (1.0, -6), (0.93, -18), (0.95, -40)]
        bot = [(u, -w(u)) for u in us[::-1]]
        blade = blur(F.poly(top + bot), 1.3)
        teeth = np.zeros((N, N), np.float32)
        for u in np.linspace(g0 + 0.06, 0.86, 9):
            teeth = np.maximum(teeth, F.poly([(u - 0.02, -w(u) + 2), (u + 0.01, -w(u) - 16), (u + 0.025, -w(u) + 2)]))
        blade = np.maximum(blade, blur(teeth, 1))
        slot = blur(F.poly([(g0 + 0.05, 7), (0.84, 5), (0.86, 0), (0.84, -5), (g0 + 0.05, -7)]), 1)
        _metal(c, blade, elem, 14)
        c.over(np.zeros((N, N, 3)) + 0.02, slot, cast=False)
        _glowpaint(c, slot * 0.9, glow, 1.0, 8)
        _motif(c, rng, elem, F, g0 + 0.08, 0.86, 62, glow)
        edge = np.clip(blade - np.clip((blur(blade, 3) - 0.6) * 4, 0, 1), 0, 1)
        _gold(c, edge * 0.9, 2)
        # demon-wing guard, swept back, with horns
        wing = np.maximum(F.poly([(g0 + 0.02, 0), (g0 + 0.01, 70), (g0 - 0.10, 120), (g0 - 0.05, 80), (g0 - 0.03, 20)]),
                          F.poly([(g0 + 0.02, 0), (g0 + 0.01, -70), (g0 - 0.10, -120), (g0 - 0.05, -80), (g0 - 0.03, -20)]))
        horns = np.maximum(F.poly([(g0 + 0.01, 40), (g0 + 0.09, 66), (g0 + 0.03, 50)]), F.poly([(g0 + 0.01, -40), (g0 + 0.09, -66), (g0 + 0.03, -50)]))
        _metal(c, blur(wing, 1.2), elem, 8, tint=tuple(np.array(METAL[elem]) * 0.8))
        _gold(c, blur(horns, 1))
    else:               # curved reaver, saw back
        us = np.linspace(g0, 0.98, 40)
        off = lambda u: 52 * np.sin(np.clip((u - g0) / (1 - g0), 0, 1) * np.pi * 0.85)
        w = lambda u: 30 * np.clip((1.0 - u) / 0.12, 0, 1) ** 0.5
        top = [(u, off(u) + w(u)) for u in us]
        bot = [(u, off(u) - w(u)) for u in us[::-1]]
        blade = blur(F.poly(top + bot), 1.3)
        saw = np.zeros((N, N), np.float32)
        for u in np.linspace(g0 + 0.05, 0.85, 12):
            saw = np.maximum(saw, F.poly([(u - 0.02, off(u) + w(u) - 2), (u + 0.015, off(u) + w(u) + 14), (u + 0.025, off(u) + w(u) - 2)]))
        blade = np.maximum(blade, blur(saw, 1))
        _metal(c, blade, elem, 12)
        vein = blur(F.poly([(u, off(u) - w(u) * 0.35) for u in np.linspace(g0 + 0.04, 0.9, 30)], width=6), 1)
        _glowpaint(c, vein, glow, 1.0, 7)
        _motif(c, rng, elem, F, g0 + 0.1, 0.86, 40, glow, 0.8)
        cres = blur(F.poly([(g0 + 0.03, -64), (g0 - 0.04, -30), (g0 - 0.05, 0), (g0 - 0.04, 30), (g0 + 0.03, 64), (g0 + 0.0, 30), (g0 - 0.01, 0), (g0 + 0.0, -30)]), 1.2)
        _gold(c, cres, 8)
    gx, gy = F.P(g0, 0)
    _gem(c, gx, gy, 18, glow)
    grip = blur(F.poly([(0.06, 11), (g0 - 0.03, 11), (g0 - 0.03, -11), (0.06, -11)]), 1)
    wrap = 0.7 + 0.3 * np.sin(((xx - F.p0[0]) * F.d[0] + (yy - F.p0[1]) * F.d[1]) / 4.0)
    c.over(light(pillow(grip, 5) * 0.6, leather_col(rng, (0.10, 0.05, 0.10)) * wrap[..., None], depth=30, spec=0.25), grip)
    for u in (0.10, 0.17):
        _gold(c, blur(F.poly([(u, 13), (u + 0.012, 13), (u + 0.012, -13), (u, -13)]), 1))
    px, py = F.P(0.03, 0)
    skull = blur(np.maximum(ellipse([px - 24, py - 22, px + 24, py + 20]), ellipse([px - 14, py + 4, px + 14, py + 28])), 1.2)
    _metal(c, skull, elem, 8, tint=(0.80, 0.74, 0.62))
    for ex in (-9, 9):
        _glowpaint(c, blur(ellipse([px + ex - 5, py - 6, px + ex + 5, py + 4]), 0.8), glow, 1.0, 4)
    return c


def axe(path):
    elem, way = path.split('_')
    glow = ELEMENTS[elem][1]
    rng = np.random.default_rng(zlib.crc32(repr(('axe5', path)).encode()))
    c = Canvas()
    F = Frame((70, 460), (400, 120))
    haft = blur(F.poly([(0.0, 15), (1.05, 13), (1.05, -13), (0.0, -15)]), 1.2)
    _metal(c, haft, elem, 6, tint=(0.18, 0.10, 0.14))
    for u in np.linspace(0.12, 0.6, 5):
        _gold(c, blur(F.poly([(u, 14), (u + 0.015, 14), (u + 0.015, -14), (u, -14)]), 1))
    hu = 0.84
    if way == 'a':      # two crescents and a spear spike
        head = np.zeros((N, N), np.float32)
        for s in (1, -1):
            pts = [(hu - 0.07, s * 14), (hu - 0.16, s * 95), (hu - 0.08, s * 178), (hu + 0.03, s * 203), (hu + 0.11, s * 178),
                   (hu + 0.17, s * 95), (hu + 0.08, s * 14), (hu + 0.05, s * 81), (hu, s * 135), (hu - 0.04, s * 81)]
            head = np.maximum(head, F.poly(pts))
        spike = F.poly([(hu + 0.06, 16), (1.12, 0), (hu + 0.06, -16)])
        head = blur(np.maximum(head, spike), 1.3)
        _metal(c, head, elem, 14)
        edge = np.clip(head - np.clip((blur(head, 3) - 0.6) * 4, 0, 1), 0, 1)
        _gold(c, edge * 0.9, 2)
        _motif(c, rng, elem, F, hu - 0.1, hu + 0.12, 190, glow, 0.6)
        ex, ey = F.P(hu, 0)
        _gem(c, ex, ey, 28, glow)
    else:               # one huge jagged bit, bone hook behind
        pts = [(hu - 0.08, -13), (hu - 0.20, -122), (hu - 0.12, -230), (hu + 0.06, -256), (hu + 0.16, -202), (hu + 0.12, -81), (hu + 0.07, -13)]
        bit = F.poly(pts)
        jag = np.zeros((N, N), np.float32)
        for k in range(7):
            t = k / 6.0
            u = hu - 0.12 + 0.28 * t; v = -230 + 10 * np.sin(t * 3) - 10
            jag = np.maximum(jag, F.poly([(u - 0.03, v + 12), (u, v - 22), (u + 0.03, v + 12)]))
        bit = blur(np.maximum(bit, jag), 1.3)
        _metal(c, bit, elem, 14)
        hook = blur(F.poly([(hu - 0.04, 14), (hu - 0.02, 81), (hu - 0.12, 149), (hu - 0.04, 95), (hu + 0.04, 14)]), 1.2)
        _metal(c, hook, elem, 8, tint=(0.82, 0.76, 0.64))
        _motif(c, rng, elem, F, hu - 0.1, hu + 0.1, 200, glow, 0.6)
        vein = blur(F.poly([(hu - 0.1, -81), (hu - 0.02, -162), (hu + 0.08, -148), (hu + 0.04, -81)], width=7), 1)
        _glowpaint(c, vein, glow, 1.0, 7)
        ex, ey = F.P(hu, -40)
        _gem(c, ex, ey, 18, glow)
    return c


def bow(path):
    elem, way = path.split('_')
    glow = ELEMENTS[elem][1]
    rng = np.random.default_rng(zlib.crc32(repr(('bow5', path)).encode()))
    c = Canvas()
    gx, gy = 150, 150                      # grip near the upper left, limbs reaching to top-right and bottom-left
    A, Bt = (440, 64), (64, 440)
    if way == 'a':      # bat wings
        for tip, mid in ((A, (300, 70)), (Bt, (70, 300))):
            limb = blur(poly([(gx, gy), mid, tip], width=22), 1.2)
            _metal(c, limb, elem, 6)
            # finger bones and membrane hanging toward the string
            fingers = [((gx + mid[0]) / 2, (gy + mid[1]) / 2), mid, ((mid[0] + tip[0]) / 2, (mid[1] + tip[1]) / 2)]
            mem = np.zeros((N, N), np.float32)
            for (fx, fy) in fingers:
                inner = (fx + (tip[0] + gx) * 0.0 + 60 if tip == A else fx + 40, fy + 40 if tip == A else fy + 60)
                mem = np.maximum(mem, poly([(fx, fy), inner, (gx + 30, gy + 30)]))
                _metal(c, blur(poly([(fx, fy), inner], width=8), 1), elem, 4, tint=(0.82, 0.76, 0.64))
            c.over(np.ones((N, N, 3)) * np.array(METAL[elem]) * 1.6, blur(mem, 1.5) * 0.75, cast=False)
            _glowpaint(c, blur(poly([(gx, gy), mid, tip], width=4), 1), glow, 0.8, 5)
    else:               # two great horns meeting at a skull
        for tip, ctrl in ((A, (320, 20)), (Bt, (20, 320))):
            ts = np.linspace(0, 1, 40)
            pts = [((1 - t) ** 2 * gx + 2 * (1 - t) * t * ctrl[0] + t * t * tip[0], (1 - t) ** 2 * gy + 2 * (1 - t) * t * ctrl[1] + t * t * tip[1]) for t in ts]
            horn = np.zeros((N, N), np.float32)
            for i in range(len(pts) - 1):
                r = 26 * (1 - i / len(pts)) + 5
                x, y = pts[i]
                horn = np.maximum(horn, ellipse([x - r, y - r, x + r, y + r]))
            horn = blur(horn, 1.2)
            _metal(c, horn, elem, 10, tint=(0.70, 0.62, 0.52))
            rings = np.zeros((N, N), np.float32)
            for i in range(4, len(pts) - 4, 5):
                x, y = pts[i]; r = 26 * (1 - i / len(pts)) + 5
                rings = np.maximum(rings, poly([(x - r, y + r * 0.3), (x + r, y - r * 0.3)], width=3))
            c.over(np.zeros((N, N, 3)) + 0.1, rings * horn * 0.7, cast=False)
            _glowpaint(c, blur(poly([(round(x), round(y)) for x, y in pts[::4]], width=3), 1), glow, 0.7, 5)
    string = blur(poly([A, Bt], width=5), 0.8)
    _glowpaint(c, string, glow, 0.9, 6)
    skull = blur(np.maximum(ellipse([gx - 34, gy - 30, gx + 34, gy + 28]), ellipse([gx - 20, gy + 8, gx + 20, gy + 40])), 1.2)
    _metal(c, skull, elem, 8, tint=(0.82, 0.76, 0.64))
    for ex in (-12, 12):
        _glowpaint(c, blur(ellipse([gx + ex - 7, gy - 8, gx + ex + 7, gy + 5]), 0.8), glow, 1.0, 5)
    for hx in (-1, 1):
        _gold(c, blur(poly([(gx + hx * 26, gy - 18), (gx + hx * 44, gy - 52), (gx + hx * 34, gy - 16)]), 1))
    return c


def _spikes(c, elem, pts, h, w=14):
    m = np.zeros((N, N), np.float32)
    for (x, y, a) in pts:
        tip = (x + np.cos(a) * h, y + np.sin(a) * h)
        m = np.maximum(m, poly([(x - np.sin(a) * w, y + np.cos(a) * w), tip, (x + np.sin(a) * w, y - np.cos(a) * w)]))
    _gold(c, blur(m, 1.2))


def armour(kind, elem):
    glow = ELEMENTS[elem][1]
    rng = np.random.default_rng(zlib.crc32(repr(('armour5', kind, elem)).encode()))
    c = Canvas()
    up = -np.pi / 2
    if kind == 'helmet':      # a horned close helm: ridged dome, narrow visor slit, breaths, riveted rim, curling horns
        for sd in (-1, 1):
            _horn(c, (256 + sd * 104, 168), (256 + sd * 220, 150), (256 + sd * 176, 36), 30, elem)
        dome = ellipse([138, 70, 374, 320])
        face = poly([(146, 210), (366, 210), (356, 380), (306, 440), (206, 440), (156, 380)])
        shell = blur(np.maximum(dome, face), 1.2)
        _metal(c, shell, elem, 26, 0.9)
        keel = blur(poly([(256, 66), (256, 436)], width=14), 1.2)
        _metal(c, keel, elem, 6, 0.9)
        slit = blur(poly([(168, 246), (344, 246), (338, 262), (174, 262)]), 1)
        c.over(np.zeros((N, N, 3)) + 0.02, slit, cast=False)
        _glowpaint(c, slit * 0.55, glow, 0.6, 5)
        holes = np.zeros((N, N), np.float32)
        for row, y in enumerate((310, 334, 358)):
            for x in range(196 + row * 8, 324 - row * 8, 18):
                if abs(x - 256) > 12: holes = np.maximum(holes, ellipse([x - 4, y - 4, x + 4, y + 4]))
        c.over(np.zeros((N, N, 3)) + 0.03, blur(holes, 0.8), cast=False)
        rim = np.clip(shell - np.clip((blur(shell, 4) - 0.7) * 5, 0, 1), 0, 1)
        _gold(c, rim * 0.95, 3)
        rivets = np.zeros((N, N), np.float32)
        for a in np.linspace(0.15, np.pi - 0.15, 9):
            x, y = 256 - np.cos(a) * 112, 200 - np.sin(a) * 118
            rivets = np.maximum(rivets, ellipse([x - 5, y - 5, x + 5, y + 5]))
        _gold(c, blur(rivets, 0.8), 3)
        _gem(c, 256, 150, 16, glow)
    elif kind == 'chest':     # a real cuirass: ridged breastplate, gorget, layered spaulders with spikes, lames at the waist
        for sd in (-1, 1):            # spaulders: three overlapping lames each side, outermost first
            for k in range(3):
                cx, cy = 256 + sd * (150 - k * 22), 128 + k * 26
                lame = poly([(cx - sd * 70, cy - 22), (cx + sd * 54, cy - 30), (cx + sd * 76, cy + 6), (cx + sd * 60, cy + 40), (cx - sd * 64, cy + 30)])
                _metal(c, blur(lame, 1.2), elem, 10, 0.85)
                _gold(c, np.clip(blur(lame, 1.2) - np.clip((blur(lame, 3) - 0.7) * 5, 0, 1), 0, 1) * 0.9, 2)
            _spikes(c, elem, [(256 + sd * 170, 104, -np.pi / 2 + sd * 0.7), (256 + sd * 132, 92, -np.pi / 2 + sd * 0.35)], 42, 9)
        torso = poly([(176, 150), (336, 150), (366, 300), (340, 400), (172, 400), (146, 300)])
        plate = blur(torso, 1.2)
        nx = (xx - 256) / 150
        h = pillow(torso, 30) * 0.8 + 0.25 * np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * torso
        base = np.array(METAL[elem]) * 0.45 + np.array((0.42, 0.42, 0.45)) * 0.55
        lit = light(h, np.clip(base * _texture(7)[..., None], 0, 1), depth=55, spec=0.55, gloss=40)
        c.over(np.clip(lit * 0.55 + chrome(h, np.clip(base * 1.15, 0, 1), depth=50, ground=0.12) * 0.45, 0, 1), plate)
        ridge = blur(poly([(256, 156), (256, 396)], width=6), 1)
        c.over(np.zeros((N, N, 3)) + 0.92, ridge * 0.35, cast=False)
        for y in (404, 430, 456):     # lames at the waist
            lame = blur(poly([(170 + (y - 404) * 0.2, y - 10), (342 - (y - 404) * 0.2, y - 10), (338, y + 14), (174, y + 14)]), 1.2)
            _metal(c, lame, elem, 6, 0.8)
            _gold(c, blur(poly([(176, y + 12), (336, y + 12)], width=3), 0.8), 2)
        gorget = blur(poly([(196, 120), (316, 120), (330, 156), (182, 156)]), 1.2)
        _metal(c, gorget, elem, 8, 0.85)
        _gold(c, np.clip(plate - np.clip((blur(plate, 3) - 0.7) * 5, 0, 1), 0, 1) * 0.9, 2)
        etch = np.zeros((N, N), np.float32)        # a faint etched motif glowing through the breastplate
        for sd in (-1, 1):
            etch = np.maximum(etch, poly([(256 + sd * 14, 210), (256 + sd * 70, 250), (256 + sd * 60, 330), (256 + sd * 20, 360)], width=3))
        _glowpaint(c, blur(etch, 0.8) * 0.7, glow, 0.5, 4)
        _gem(c, 256, 206, 20, glow)
    elif kind == 'legs':      # plate legs: a fauld, cuisses, fan-winged knee cops with spikes, greaves
        def edge(m):
            return np.clip(m - np.clip((blur(m, 3) - 0.7) * 5, 0, 1), 0, 1)
        for y0 in (56, 84):           # fauld lames
            lame = blur(poly([(150, y0), (362, y0), (366, y0 + 30), (146, y0 + 30)]), 1.2)
            _metal(c, lame, elem, 6, 0.8); _gold(c, edge(lame) * 0.9, 2)
        for sd in (-1, 1):
            cx = 256 + sd * 62
            cuisse = blur(poly([(cx - 52, 116), (cx + 52, 116), (cx + 44, 268), (cx - 44, 268)]), 1.2)
            _metal(c, cuisse, elem, 14, 0.85)
            greave = blur(poly([(cx - 40, 330), (cx + 40, 330), (cx + 36, 468), (cx - 34, 468)]), 1.2)
            _metal(c, greave, elem, 12, 0.85)
            c.over(np.zeros((N, N, 3)) + 0.9, blur(poly([(cx, 336), (cx, 462)], width=4), 1) * 0.3, cast=False)
            fan = blur(poly([(cx - sd * 40, 270), (cx + sd * 66, 252), (cx + sd * 70, 300), (cx + sd * 40, 334), (cx - sd * 40, 330)]), 1.2)
            _metal(c, fan, elem, 8, 0.8); _gold(c, edge(fan) * 0.9, 2)
            cop = blur(ellipse([cx - 38, 268, cx + 38, 334]), 1.2)
            _metal(c, cop, elem, 12, 0.95, tint=tuple(np.array(METAL[elem]) * 1.2)); _gold(c, edge(cop) * 0.9, 2)
            _spikes(c, elem, [(cx, 300, -np.pi / 2 + sd * 1.2)], 34, 8)
            for g in (cuisse, greave): _gold(c, edge(g) * 0.9, 2)
            _glowpaint(c, blur(poly([(cx - 24, 196), (cx + 24, 196)], width=3), 0.8) * 0.7, glow, 0.5, 4)
        _gem(c, 256, 70, 14, glow)
    else:                     # sabatons: a greave cuff, ankle plates, overlapping toe lames ending in claws, a spur
        def edge(m):
            return np.clip(m - np.clip((blur(m, 3) - 0.7) * 5, 0, 1), 0, 1)
        for sd in (-1, 1):
            cx = 256 + sd * 104
            greave = blur(poly([(cx - 52, 110), (cx + 52, 110), (cx + 48, 300), (cx - 48, 300)]), 1.2)
            _metal(c, greave, elem, 14, 0.85); _gold(c, edge(greave) * 0.9, 2)
            c.over(np.zeros((N, N, 3)) + 0.9, blur(poly([(cx, 116), (cx, 294)], width=4), 1) * 0.3, cast=False)
            cuff = blur(rect([cx - 56, 104, cx + 56, 140], 8), 1.2)
            _gold(c, cuff, 6)
            ankle = blur(ellipse([cx - 56, 284, cx + 56, 352]), 1.2)
            _metal(c, ankle, elem, 12, 0.9, tint=tuple(np.array(METAL[elem]) * 1.2)); _gold(c, edge(ankle) * 0.9, 2)
            for k in range(4):          # toe lames stepping down and out
                y = 340 + k * 26; w = 60 + k * 10
                lame = blur(poly([(cx - w, y), (cx + w, y), (cx + w + 6, y + 30), (cx - w - 6, y + 30)]), 1.2)
                _metal(c, lame, elem, 6, 0.8); _gold(c, edge(lame) * 0.9, 2)
            claws = np.zeros((N, N), np.float32)
            for kx in (-1, 0, 1):
                bx = cx + kx * 46
                claws = np.maximum(claws, poly([(bx - 13, 446), (bx + kx * 12, 494), (bx + 13, 446)]))
            _gold(c, blur(claws, 1))
            _spikes(c, elem, [(cx - sd * 52, 318, np.pi if sd > 0 else 0.0)], 30, 8)
            _gem(c, cx, 122, 12, glow)
            _glowpaint(c, blur(poly([(cx - 30, 220), (cx + 30, 220)], width=3), 0.8) * 0.7, glow, 0.5, 4)
    return c


def draw(kind, path):
    elem = path.split('_')[0]
    if kind == 'sword': c = sword(path)
    elif kind == 'axe': c = axe(path)
    elif kind == 'bow': c = bow(path)
    else: c = armour(kind, elem)
    return _abyss5.abyssify(c.image(), elem, ('g5', kind, path), recolour_metal=False)
