"""The 22 accessory pictures (เครื่องประดับ, ร่าง 2026-11-16, รอบ 2 "ทำให้สมจริงขึ้น"), one function each."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, rect, chrome, gold_tint, steel_tint, noise, leather_col, stone, cloth, wood
from _jewel import (poly, COL, SILVER, IRON, DARK, glow, chain, cord, worn, metal_real, facet_gem, set_gem, engraved_band, braid)

OLD_GOLD = (0.95, 0.72, 0.32)
BRASS = (0.88, 0.66, 0.34)
BLACK_IRON = (0.40, 0.40, 0.44)


def _c(seed):
    return Canvas(), np.random.default_rng(seed)


def leather_real(c, rng, pts, colour=(0.42, 0.24, 0.12), r=14, width=None):
    m = blur(poly(pts, width=width) if width else poly(pts), 1.4)
    tex = leather_col(rng, colour) * (0.85 + 0.3 * noise(rng, 70, 2)[..., None])     # pebbled grain
    tex = tex * (1 - 0.18 * blur(np.clip(1 - m * 1.6, 0, 1), 4))[..., None]         # darker, burnished edges
    c.over(light(0.42 * pillow(m, r), np.clip(tex, 0, 1), depth=50, spec=0.18, gloss=20), m)
    return m


def stitch_line(c, p0, p1, n, colour=(0.86, 0.78, 0.58)):
    for t in np.linspace(0.04, 0.96, n):
        x = p0[0] + (p1[0] - p0[0]) * t; y = p0[1] + (p1[1] - p0[1]) * t
        ang = np.arctan2(p1[1] - p0[1], p1[0] - p0[0])
        dx, dy = 7 * np.cos(ang), 7 * np.sin(ang)
        m = blur(poly([(x - dx, y - dy), (x + dx, y + dy)], width=3.2), 0.7)
        c.over(np.zeros((N, N, 3)) + np.array(colour), m, cast=False)


def rivet(c, rng, x, y, r, tint=steel_tint()):
    m = blur(ellipse([x - r, y - r, x + r, y + r]), 1)
    metal_real(c, m, tint, rng, r=r * 0.8, depth=70, amount=0.25)


def metal_shape(c, rng, pts, tint, r=10, amount=0.18):
    m = blur(poly(pts), 1.3)
    metal_real(c, m, tint, rng, r=r, amount=amount)
    return m


# ---------- rings ----------
RING_BOX = [104, 214, 408, 452]


def ring_element(el, seed):
    c, rng = _c(seed)
    engraved_band(c, RING_BOX, 48, OLD_GOLD, rng)
    set_gem(c, 256, 196, 74, 62, el, OLD_GOLD, rng)
    glow(c, [196, 140, 316, 252], COL[el], 0.22, 26)
    return c.image()


def ring_warrior(seed=7201):
    c, rng = _c(seed)
    engraved_band(c, RING_BOX, 52, BLACK_IRON, rng, pattern='none')
    # a flat shield-shaped bezel with a garnet, flanked by two small blades
    metal_shape(c, rng, [(186, 128), (326, 128), (336, 220), (256, 292), (176, 220)], BLACK_IRON, r=16, amount=0.3)
    set_gem(c, 256, 196, 44, 44, 'ruby', SILVER, rng, prongs=4)
    for s in (-1, 1):
        x0 = 256 + s * 98
        metal_shape(c, rng, [(x0 - 6, 286), (x0 + 6, 286), (x0 + 4 * s + 2, 150), (x0 + 4 * s - 2, 146)], SILVER, r=4)
        metal_shape(c, rng, [(x0 - 18, 280), (x0 + 18, 280), (x0 + 18, 290), (x0 - 18, 290)], BRASS, r=4)
    return c.image()


def ring_hunter(seed=7202):
    c, rng = _c(seed)
    # a carved horn band: warm bone with growth lines
    x0, y0, x1, y1 = RING_BOX
    outer = blur(ellipse(RING_BOX), 1.5); inner = blur(ellipse([x0 + 50, y0 + 38, x1 - 50, y1 - 38]), 1.5)
    m = np.clip(outer - inner, 0, 1)
    tex = (np.zeros((N, N, 3)) + np.array((0.86, 0.78, 0.60))) * (0.82 + 0.18 * np.sin(np.hypot(xx - 256, yy - 333) / 3.5))[..., None]
    tex = tex * (0.85 + 0.25 * noise(rng, 20, 3))[..., None]
    c.over(light(0.5 * pillow(m, 22), np.clip(tex, 0, 1), depth=55, spec=0.35, gloss=30), m)
    from _wild import fang
    fang(c, rng, 256, 170, 256, 60, 30, (0.95, 0.92, 0.82))
    set_gem(c, 256, 206, 40, 36, 'emerald', BRASS, rng, prongs=4)
    return c.image()


def ring_merchant(seed=7203):
    c, rng = _c(seed)
    engraved_band(c, [104, 236, 408, 460], 46, OLD_GOLD, rng)
    face = blur(ellipse([158, 108, 354, 296]), 1.5)
    metal_real(c, face, OLD_GOLD, rng, r=22, amount=0.22)
    # an engraved signet: scales over a coin, in recessed lines
    eng = np.zeros((N, N), np.float32)
    eng = np.maximum(eng, np.clip(1 - np.abs(np.hypot((xx - 256) / 72, (yy - 202) / 66) - 1) * 40, 0, 1))
    eng = np.maximum(eng, poly([(256, 150), (256, 250)], width=3.5))
    eng = np.maximum(eng, poly([(214, 172), (298, 172)], width=3.5))
    for x in (214, 298):
        eng = np.maximum(eng, poly([(x - 18, 212), (x, 172), (x + 18, 212)], width=2.5))
        eng = np.maximum(eng, np.clip(1 - np.abs(np.hypot((xx - x) / 20, (yy - 214) / 7) - 1) * 12, 0, 1) * (yy > 212))
    c.over(np.zeros((N, N, 3)) + np.array((0.42, 0.28, 0.08)), blur(eng, 0.8) * face * 0.85, cast=False)
    return c.image()


def ring_guardian(seed=7204):
    """แหวนพิทักษ์ (2026-11-18, แทนแหวนพ่อค้า): a silver band with a raised kite shield, a cross and a sapphire."""
    c, rng = _c(seed)
    engraved_band(c, RING_BOX, 50, SILVER, rng)
    # a heater shield: flat top, sides curving to a point; blue enamel in a silver rim
    def heater(x0, x1, top, mid, tip):
        cx = (x0 + x1) / 2; half = (x1 - x0) / 2
        pts = [(x0, top), (x1, top), (x1, mid)]
        for t in np.linspace(0.15, 1, 8):
            pts.append((cx + half * np.cos(t * np.pi / 2), mid + (tip - mid) * np.sin(t * np.pi / 2)))
        for t in np.linspace(1, 0.15, 8):
            pts.append((cx - half * np.cos(t * np.pi / 2), mid + (tip - mid) * np.sin(t * np.pi / 2)))
        pts.append((x0, mid))
        return pts
    metal_shape(c, rng, heater(160, 352, 96, 170, 318), SILVER, r=14, amount=0.25)
    metal_shape(c, rng, heater(180, 332, 114, 176, 292), (0.22, 0.38, 0.78), r=10, amount=0.35)
    # a raised silver cross over the enamel
    metal_shape(c, rng, [(244, 120), (268, 120), (268, 284), (244, 284)], SILVER, r=6, amount=0.2)
    metal_shape(c, rng, [(186, 164), (326, 164), (326, 188), (186, 188)], SILVER, r=6, amount=0.2)
    rivet(c, rng, 256, 176, 12, SILVER)
    return c.image()


# ---------- necklaces ----------
def hang(c, rng, tint, kind='chain', bottom=280):
    t = np.linspace(0, 1, 16)
    left = [(256 - 178 * np.cos(a * np.pi / 2), 46 + (bottom - 46) * np.sin(a * np.pi / 2)) for a in t]
    right = [(256 + 178 * np.cos(a * np.pi / 2), 46 + (bottom - 46) * np.sin(a * np.pi / 2)) for a in t]
    if kind == 'chain':
        chain(c, left, tint, link=19); chain(c, right, tint, link=19)
    else:
        braid(c, left, tint, 16, rng); braid(c, right, tint, 16, rng)


def bail(c, rng, y, tint):
    o = blur(ellipse([232, y - 22, 280, y + 22]), 1); h = blur(ellipse([244, y - 10, 268, y + 10]), 1)
    metal_real(c, np.clip(o - h, 0, 1), tint, rng, r=6)


def neck_alpha(seed=7211):
    c, rng = _c(seed)
    hang(c, rng, SILVER)
    bail(c, rng, 286, SILVER)
    from _wild import fang
    fang(c, rng, 256, 312, 262, 480, 40, (0.96, 0.95, 0.98))
    metal_shape(c, rng, [(212, 300), (300, 300), (292, 336), (220, 336)], SILVER, r=8)
    for x in (230, 256, 282):
        rivet(c, rng, x, 318, 6, SILVER)
    glow(c, [216, 340, 300, 460], (0.85, 0.92, 1.0), 0.18, 20)
    return c.image()


def neck_heartwood(seed=7212):
    c, rng = _c(seed)
    hang(c, rng, (0.50, 0.34, 0.18), kind='cord', bottom=270)
    bail(c, rng, 276, BRASS)
    m = blur(poly([(256, 478), (140, 370), (136, 318), (176, 284), (226, 290), (256, 326), (286, 290), (336, 284), (376, 318), (372, 370)]), 2)
    c.over(light(0.6 * pillow(m, 34), wood(rng, (0.46, 0.28, 0.13), 1.2), depth=65, spec=0.2), m)
    crack = blur(poly([(256, 330), (240, 368), (268, 402), (248, 446)], width=9), 1.2)
    c.over(np.zeros((N, N, 3)) + np.array((0.55, 1.0, 0.50)), crack, cast=False)
    glow(c, [196, 320, 316, 450], (0.45, 1.0, 0.45), 0.28, 22)
    # a brass band around the heart's top
    metal_shape(c, rng, [(150, 330), (362, 330), (362, 346), (150, 346)], BRASS, r=5)
    return c.image()


def neck_crown(seed=7213):
    c, rng = _c(seed)
    hang(c, rng, OLD_GOLD, bottom=262)
    # a small royal crown hung from a ring at its tallest (centre) point
    o = blur(ellipse([238, 252, 274, 288]), 1); h = blur(ellipse([248, 262, 264, 278]), 1)
    metal_real(c, np.clip(o - h, 0, 1), OLD_GOLD, rng, r=5)
    pts = [(150, 448), (150, 360), (186, 396), (206, 334), (232, 384), (256, 304), (280, 384), (306, 334), (326, 396), (362, 360), (362, 448)]
    metal_shape(c, rng, pts, OLD_GOLD, r=18, amount=0.25)
    # velvet cap behind the points
    cap = blur(poly([(170, 420), (186, 380), (256, 356), (326, 380), (342, 420)]), 2)
    c.over(light(0.4 * pillow(cap, 16), cloth(rng, (0.55, 0.06, 0.10)), depth=40), cap * 0.0)
    for x, y in ((150, 352), (206, 326), (256, 296), (306, 326), (362, 352)):
        rivet(c, rng, x, y, 10, OLD_GOLD)
    # the band: curved front with a row of gems and pearls
    band = blur(poly([(144, 418), (368, 418), (368, 456), (256, 470), (144, 456)]), 1.3)
    metal_real(c, band, OLD_GOLD, rng, r=8, amount=0.25)
    for x, col in ((190, 'emerald'), (256, 'ruby'), (322, 'sky')):
        set_gem(c, x, 440, 15, 12, col, OLD_GOLD, rng, prongs=4)
    for x in (222, 290):
        pm = blur(ellipse([x - 7, 433, x + 7, 447]), 1)
        c.over(light(0.8 * pillow(pm, 6), np.zeros((N, N, 3)) + np.array((0.96, 0.94, 0.90)), depth=60, spec=0.9), pm)
    return c.image()


def neck_soul(seed=7214):
    c, rng = _c(seed)
    hang(c, rng, BLACK_IRON)
    bail(c, rng, 286, BLACK_IRON)
    cage = [(206, 304), (306, 304), (330, 352), (256, 484), (182, 352)]
    metal_shape(c, rng, cage, BLACK_IRON, r=14, amount=0.35)
    facet_gem(c, 256, 380, 46, 64, 'soul', rng)
    flame = blur(poly([(256, 328), (282, 378), (272, 424), (256, 440), (240, 424), (230, 378)]), 4)
    c.over(np.zeros((N, N, 3)) + np.array((0.86, 0.72, 1.0)), flame * 0.55, cast=False)
    for ang in (0.3, 1.0, 2.15, 2.85):     # iron bars of the cage over the stone
        x0, y0 = 256 + 60 * np.cos(ang + np.pi), 380
        c.over(np.zeros((N, N, 3)) + 0.22, blur(poly([(256, 312), (x0, 470)], width=5), 1) * 0.0, cast=False)
    glow(c, [190, 320, 322, 470], COL['soul'], 0.32, 24)
    return c.image()


# ---------- earrings ----------
def hook(c, rng, tint):
    pts = [(256, 30), (304, 48), (314, 100), (286, 140), (258, 160)]
    m = blur(poly(pts, width=12), 1.2)
    metal_real(c, m, tint, rng, r=5)
    o = blur(ellipse([238, 150, 276, 188]), 1); h = blur(ellipse([248, 160, 266, 178]), 1)
    metal_real(c, np.clip(o - h, 0, 1), tint, rng, r=5)


def ear_hawk(seed=7221):
    c, rng = _c(seed)
    hook(c, rng, OLD_GOLD)
    metal_shape(c, rng, [(240, 182), (272, 182), (268, 214), (244, 214)], OLD_GOLD, r=6)
    # a large barred hawk feather
    spine = [(256, 210), (250, 300), (244, 400), (240, 488)]
    vane = blur(poly([(256, 214), (178, 300), (156, 400), (196, 470), (240, 488), (300, 440), (334, 330), (300, 250)]), 2)
    u = (yy - 210) / 280.0
    bars = 0.5 + 0.5 * np.sin(u * 4.5 * np.pi * 2 + (xx - 250) / 40.0)
    barbs = 0.5 + 0.5 * np.sin((yy * 0.9 - np.abs(xx - 250) * 1.4) / 3.0)
    base = np.array((0.58, 0.40, 0.22))
    tex = base[None, None, :] * (0.80 + 0.20 * bars)[..., None] * (0.88 + 0.16 * barbs)[..., None] * (0.9 + 0.2 * noise(rng, 30, 3))[..., None]
    tex = tex * (1.0 + 0.25 * np.clip(1 - u, 0, 1))[..., None]
    c.over(light(0.35 * pillow(vane, 22), np.clip(tex, 0, 1), depth=40, spec=0.08), vane)
    notch = blur(poly([(300, 400), (334, 380), (322, 420)]), 2)
    c.px[..., 3] *= (1 - notch * 0.9)
    s = blur(poly(spine, width=6), 1)
    c.over(np.zeros((N, N, 3)) + np.array((0.92, 0.88, 0.76)), s, cast=False)
    return c.image()


def ear_calm(seed=7222):
    c, rng = _c(seed)
    hook(c, rng, SILVER)
    metal_shape(c, rng, [(234, 182), (278, 182), (270, 222), (242, 222)], SILVER, r=6)
    # a pear-cut pale crystal
    cx, cy = 256, 350
    dx = (xx - cx) / 70.0; dy = (yy - cy) / 120.0
    shape = (dx ** 2 + (np.clip(dy, -1, 0) * 1.0) ** 2 * 1 + np.clip(dy, 0, 1) ** 2)
    pear = blur(((dx / np.clip(1 - 0.65 * np.clip(-dy, 0, 1), 0.2, 1)) ** 2 + dy ** 2 <= 1).astype(np.float32), 1.3)
    a = np.arctan2(dy, dx); k = 10
    sector = np.floor((a + np.pi) / (2 * np.pi) * k)
    sh = 0.55 + 0.45 * np.cos((sector + 0.5) * 2 * np.pi / k - np.pi * 1.25)
    col = np.array(COL['sky'])
    rgb = col[None, None, :] * (0.55 + 0.6 * sh)[..., None]
    rgb = rgb + 0.4 * (np.clip(1 - np.hypot(dx + 0.25, dy + 0.35) / 0.3, 0, 1) ** 2)[..., None]
    c.over(np.clip(rgb, 0, 1), pear)
    glow(c, [226, 270, 262, 320], (1, 1, 1), 0.55, 6)
    return c.image()


# ---------- bracelets ----------
def cuff_mask(thick=72):
    outer = blur(ellipse([64, 120, 448, 404]), 2)
    inner = blur(ellipse([64 + thick, 120 + thick * 0.7, 448 - thick, 404 - thick * 0.7]), 2)
    return np.clip(outer - inner, 0, 1)


def brace_leather(seed=7231):
    c, rng = _c(seed)
    m = cuff_mask()
    tex = leather_col(rng, (0.46, 0.27, 0.13)) * (0.85 + 0.3 * noise(rng, 70, 2)[..., None])
    c.over(light(0.45 * pillow(m, 30), np.clip(tex, 0, 1), depth=50, spec=0.2, gloss=20), m)
    for f in (0.97, 0.66):
        t = np.linspace(0.08, 0.92, 26)
        for tt in t:
            ang = np.pi * tt
            x, y = 256 + 190 * f * np.cos(ang) * (1 if f > 0.9 else 0.83), 262 + 140 * f * np.sin(ang) * (1 if f > 0.9 else 0.83)
            sm = blur(ellipse([x - 5, y - 2, x + 5, y + 2]), 0.6)
            c.over(np.zeros((N, N, 3)) + np.array((0.86, 0.78, 0.58)), sm, cast=False)
    tool = np.zeros((N, N), np.float32)
    for tt in np.linspace(0.12, 0.88, 12):
        ang = np.pi * tt
        x, y = 256 + 158 * np.cos(ang), 262 + 116 * np.sin(ang)
        tool = np.maximum(tool, poly([(x - 10, y - 10), (x + 10, y + 10)], width=3))
        tool = np.maximum(tool, poly([(x - 10, y + 10), (x + 10, y - 10)], width=3))
    c.over(np.zeros((N, N, 3)) + np.array((0.22, 0.12, 0.06)), blur(tool, 0.7) * m * 0.6, cast=False)
    for tt in np.linspace(0.18, 0.82, 6):
        ang = np.pi * tt
        rivet(c, rng, 256 + 158 * np.cos(ang), 262 + 116 * np.sin(ang), 11, BRASS)
    metal_shape(c, rng, [(226, 360), (286, 360), (290, 410), (222, 410)], BRASS, r=8)
    return c.image()


def brace_scale(seed=7232):
    c, rng = _c(seed)
    m = cuff_mask(64)
    c.over(worn(chrome(0.3 * pillow(m, 20), BLACK_IRON, depth=40), rng, 0.3), m)
    for row, f in enumerate((0.95, 0.80)):
        n = 13 - row
        for tt in np.linspace(0.0, 1.0, n):
            ang = np.pi * (tt + (0.04 if row else 0))
            x, y = 256 + 190 * f * np.cos(ang), 262 + 138 * f * np.sin(ang)
            pts = [(x - 24, y - 16), (x + 24, y - 16), (x + 20, y + 10), (x, y + 32), (x - 20, y + 10)]
            metal_shape(c, rng, pts, IRON, r=8, amount=0.3)
            rivet(c, rng, x, y - 6, 4, SILVER)
    return c.image()


def brace_travel(seed=7233):
    c, rng = _c(seed)
    t = np.linspace(0, 2 * np.pi, 80)
    pts = [(256 + 176 * np.cos(a), 250 + 124 * np.sin(a)) for a in t]
    braid(c, pts, (0.62, 0.46, 0.26), 22, rng)
    for a in np.linspace(0.18, 0.82, 4):
        ang = np.pi * (0.08 + a * 0.84)
        x, y = 256 + 176 * np.cos(ang), 250 + 124 * np.sin(ang)
        m = blur(ellipse([x - 22, y - 20, x + 22, y + 20]), 1)
        c.over(light(0.6 * pillow(m, 16), wood(rng, (0.50, 0.30, 0.14), 1.0), depth=65, spec=0.3), m)
    # a little brass compass
    m = blur(ellipse([186, 320, 326, 460]), 1.5)
    metal_real(c, m, BRASS, rng, r=16, amount=0.25)
    face = blur(ellipse([204, 338, 308, 442]), 1)
    tex = np.zeros((N, N, 3)) + np.array((0.93, 0.89, 0.78))
    c.over(tex * (0.9 + 0.1 * noise(rng, 30, 2))[..., None], face, cast=False)
    for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        tm = blur(poly([(256 + 44 * np.cos(ang), 390 + 44 * np.sin(ang)), (256 + 52 * np.cos(ang), 390 + 52 * np.sin(ang))], width=2.5), 0.6)
        c.over(np.zeros((N, N, 3)) + 0.2, tm, cast=False)
    n = blur(poly([(256, 346), (268, 390), (256, 434), (244, 390)]), 1)
    c.over(np.zeros((N, N, 3)) + np.array((0.78, 0.12, 0.10)), n * (yy < 390), cast=False)
    c.over(np.zeros((N, N, 3)) + np.array((0.18, 0.18, 0.22)), n * (yy >= 390), cast=False)
    glass = blur(ellipse([212, 344, 262, 380]), 6)
    c.over(np.zeros((N, N, 3)) + 1.0, glass * 0.35, cast=False)
    return c.image()


# ---------- belts (drawn on the diagonal so they fill the slot) ----------
A, B = (40, 150), (472, 362)


def strap(c, rng, colour, half=46):
    d = np.array(B, float) - np.array(A, float); d /= np.linalg.norm(d); nrm = np.array([-d[1], d[0]])
    pts = [tuple(np.array(A) + nrm * half), tuple(np.array(B) + nrm * half), tuple(np.array(B) - nrm * half), tuple(np.array(A) - nrm * half)]
    leather_real(c, rng, pts, colour, r=16)
    for s in (-1, 1):
        stitch_line(c, tuple(np.array(A) + nrm * s * (half - 10) + d * 20), tuple(np.array(B) + nrm * s * (half - 10) - d * 20), 26)
    return d, nrm


def along(t, d, nrm, off=0.0):
    p = np.array(A, float) + (np.array(B, float) - np.array(A, float)) * t + nrm * off
    return p


def buckle(c, rng, d, nrm, t, tint):
    p = along(t, d, nrm)
    u, v = d * 64, nrm * 70
    outer = [tuple(p - u - v), tuple(p + u - v), tuple(p + u + v), tuple(p - u + v)]
    u2, v2 = d * 40, nrm * 46
    inner = [tuple(p - u2 - v2), tuple(p + u2 - v2), tuple(p + u2 + v2), tuple(p - u2 + v2)]
    m = np.clip(blur(poly(outer), 1.3) - blur(poly(inner), 1.3), 0, 1)
    metal_real(c, m, tint, rng, r=12, amount=0.25)
    tongue = [tuple(p - v * 0.95 - d * 5), tuple(p - v * 0.95 + d * 5), tuple(p + v * 0.2 + d * 4), tuple(p + v * 0.2 - d * 4)]
    tongue = [tuple(p - d * 62 - nrm * 5), tuple(p - d * 62 + nrm * 5), tuple(p + d * 48 + nrm * 4), tuple(p + d * 48 - nrm * 4)]
    metal_shape(c, rng, tongue, tint, r=5)


def tip(c, rng, d, nrm, tint):
    """The metal chape on the strap's free end."""
    p = np.array(A, float) + d * 34
    u, v = d * 30, nrm * 48
    metal_shape(c, rng, [tuple(p - u - v), tuple(p + u - v * 0.8), tuple(p + u + v * 0.8), tuple(p - u + v)], tint, r=8, amount=0.3)
    rivet(c, rng, p[0], p[1], 7, SILVER)


def keeper(c, rng, d, nrm, t, colour):
    p = along(t, d, nrm); u, v = d * 14, nrm * 56
    leather_real(c, rng, [tuple(p - u - v), tuple(p + u - v), tuple(p + u + v), tuple(p - u + v)], colour, r=6)


def holes(c, d, nrm, ts):
    for t in ts:
        p = along(t, d, nrm)
        m = blur(ellipse([p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8]), 1)
        c.over(np.zeros((N, N, 3)) + 0.08, m * 0.9, cast=False)


def belt_warrior(seed=7241):
    c, rng = _c(seed)
    d, nrm = strap(c, rng, (0.28, 0.16, 0.08), half=50)
    tip(c, rng, d, nrm, IRON)
    for t in (0.12, 0.26, 0.74, 0.88):
        p = along(t, d, nrm); u, v = d * 26, nrm * 40
        metal_shape(c, rng, [tuple(p - u - v), tuple(p + u - v), tuple(p + u + v), tuple(p - u + v)], IRON, r=10, amount=0.3)
        for s in (-1, 1):
            q = p + nrm * s * 26
            rivet(c, rng, q[0], q[1], 6, SILVER)
    buckle(c, rng, d, nrm, 0.5, IRON)
    holes(c, d, nrm, (0.62,))
    return c.image()


def belt_pouch(seed=7242):
    c, rng = _c(seed)
    d, nrm = strap(c, rng, (0.40, 0.23, 0.11))
    tip(c, rng, d, nrm, BRASS)
    keeper(c, rng, d, nrm, 0.46, (0.34, 0.19, 0.09))
    buckle(c, rng, d, nrm, 0.30, BRASS)
    holes(c, d, nrm, (0.42, 0.48))
    leather_real(c, rng, [(282, 300), (420, 300), (430, 470), (400, 496), (304, 496), (274, 470)], (0.50, 0.31, 0.15), r=26)
    leather_real(c, rng, [(276, 296), (426, 296), (420, 380), (282, 392)], (0.38, 0.22, 0.10), r=12)
    stitch_line(c, (290, 384), (414, 372), 12)
    rivet(c, rng, 352, 380, 11, BRASS)
    return c.image()


def belt_medic(seed=7243):
    c, rng = _c(seed)
    d, nrm = strap(c, rng, (0.50, 0.38, 0.24))
    tip(c, rng, d, nrm, IRON)
    keeper(c, rng, d, nrm, 0.42, (0.40, 0.29, 0.17))
    buckle(c, rng, d, nrm, 0.28, IRON)
    for t, col in ((0.56, (0.82, 0.16, 0.16)), (0.70, (0.25, 0.60, 0.92)), (0.84, (0.40, 0.75, 0.30))):
        p = along(t, d, nrm, off=58)
        x, y = p
        loop = blur(rect([x - 24, y - 50, x + 24, y - 18], 6), 1)
        leather_real(c, rng, [(x - 24, y - 52), (x + 24, y - 52), (x + 24, y - 20), (x - 24, y - 20)], (0.44, 0.33, 0.20), r=6)
        g = blur(rect([x - 18, y - 30, x + 18, y + 70], 14), 1.2)
        c.over(np.zeros((N, N, 3)) + np.array((0.86, 0.92, 0.96)), g * 0.45, cast=False)
        liq = blur(rect([x - 14, y + 6, x + 14, y + 66], 10), 1.2)
        c.over(light(0.6 * pillow(liq, 10), np.zeros((N, N, 3)) + np.array(col), depth=60, spec=0.85, gloss=55), liq)
        hl = blur(rect([x - 11, y - 20, x - 5, y + 60], 3), 1)
        c.over(np.zeros((N, N, 3)) + 1.0, hl * 0.45, cast=False)
        cork = blur(rect([x - 12, y - 44, x + 12, y - 26], 4), 1)
        c.over(light(0.5 * pillow(cork, 6), np.zeros((N, N, 3)) + np.array((0.64, 0.47, 0.27)), depth=40), cork)
    return c.image()


# ---------- charms ----------
def charm_cord(c, rng):
    braid(c, [(140, 30), (188, 104), (236, 160), (256, 176)], (0.55, 0.40, 0.22), 15, rng)
    braid(c, [(372, 30), (324, 104), (276, 160), (256, 176)], (0.55, 0.40, 0.22), 15, rng)
    knot = blur(ellipse([236, 160, 276, 200]), 1)
    c.over(light(0.6 * pillow(knot, 12), np.zeros((N, N, 3)) + np.array((0.48, 0.34, 0.18)), depth=50), knot)


def charm_medic(seed=7251):
    c, rng = _c(seed)
    charm_cord(c, rng)
    # a bundle of dried herbs hung upside down: stalks tied under the knot, leafy heads below
    greens = [(0.34, 0.46, 0.22), (0.42, 0.50, 0.26), (0.48, 0.46, 0.28), (0.38, 0.40, 0.24)]
    for k, ang in enumerate(np.linspace(-0.30, 0.30, 9)):
        x1 = 256 + 230 * np.sin(ang); y1 = 196 + 290 * np.cos(ang)
        stem = blur(poly([(256, 200), (x1, y1)], width=6), 1)
        c.over(np.zeros((N, N, 3)) + np.array((0.46, 0.40, 0.24)), stem, cast=False)
        for j in range(5):
            tt = 0.42 + j * 0.13
            lx, ly = 256 + (x1 - 256) * tt, 200 + (y1 - 200) * tt
            for side in (-1, 1):
                lp = [(lx, ly), (lx + side * 26, ly + 10), (lx + side * 22, ly + 30), (lx, ly + 16)]
                leaf = blur(poly(lp), 1.5)
                col = np.array(greens[(k + j) % len(greens)]) * (0.8 + 0.35 * noise(rng, 16, 2)[..., None])
                c.over(light(0.45 * pillow(leaf, 6), np.clip(col, 0, 1), depth=40, spec=0.06), leaf)
    for k in range(6):   # a few small lavender flowers among the leaves
        fx, fy = 256 + rng.uniform(-80, 80), rng.uniform(380, 470)
        fl = blur(ellipse([fx - 8, fy - 12, fx + 8, fy + 12]), 2)
        c.over(light(0.4 * pillow(fl, 5), np.zeros((N, N, 3)) + np.array((0.55, 0.45, 0.70)), depth=40), fl)
    tie = blur(rect([224, 196, 288, 236], 8), 1)
    c.over(light(0.5 * pillow(tie, 8), cloth(rng, (0.72, 0.18, 0.14)), depth=45), tie)
    return c.image()


def charm_wool(seed=7252):
    c, rng = _c(seed)
    charm_cord(c, rng)
    m = blur(ellipse([140, 186, 372, 432]), 8)
    fluff = 0.55 * noise(rng, 45, 3) + 0.45 * noise(rng, 18, 2)
    tufts = np.zeros((N, N), np.float32)
    for _ in range(46):
        tx, ty = rng.uniform(160, 352), rng.uniform(205, 415); tr = rng.uniform(16, 30)
        tufts = np.maximum(tufts, blur(ellipse([tx - tr, ty - tr, tx + tr, ty + tr]), 6) * rng.uniform(0.5, 1))
    fluff = 0.5 * fluff + 0.5 * tufts
    tex = np.zeros((N, N, 3)) + np.array((0.95, 0.93, 0.88))
    tex = tex * (0.78 + 0.25 * fluff)[..., None]
    c.over(light(0.45 * pillow(m, 56) + 0.25 * fluff, np.clip(tex, 0, 1), depth=50, spec=0.04), m)
    # a silver frost brooch pinned on the wool
    for ang in np.linspace(0, np.pi, 3, endpoint=False):
        dx, dy = 66 * np.cos(ang), 66 * np.sin(ang)
        arm = blur(poly([(256 - dx, 310 - dy), (256 + dx, 310 + dy)], width=11), 1)
        metal_real(c, arm, SILVER, rng, r=5)
        for s in (-1, 1):
            tip = (256 + s * dx * 0.7, 310 + s * dy * 0.7)
            for b in (-0.6, 0.6):
                br = blur(poly([tip, (tip[0] + 18 * np.cos(ang + s * np.pi + b + np.pi), tip[1] + 18 * np.sin(ang + s * np.pi + b + np.pi))], width=6), 1)
                metal_real(c, br, SILVER, rng, r=3)
    facet_gem(c, 256, 310, 16, 16, 'ice', rng)
    return c.image()


def charm_miner(seed=7253):
    c, rng = _c(seed)
    charm_cord(c, rng)
    handle = blur(poly([(190, 470), (292, 214)], width=26), 1.5)
    c.over(light(0.5 * pillow(handle, 11), wood(rng, (0.52, 0.34, 0.17), 1.2), depth=55, spec=0.2), handle)
    for t in (0.2, 0.32):     # leather grip wraps
        p = (190 + (292 - 190) * t, 470 + (214 - 470) * t)
        w = blur(poly([(p[0] - 18, p[1] - 6), (p[0] + 18, p[1] + 4)], width=12), 1)
        c.over(light(0.4 * pillow(w, 5), leather_col(rng, (0.36, 0.20, 0.10)), depth=40), w)
    head = [(130, 252), (210, 206), (300, 196), (390, 214), (420, 258), (360, 238), (290, 230), (220, 240)]
    metal_shape(c, rng, head, SILVER, r=14, amount=0.3)
    rivet(c, rng, 292, 222, 10, BRASS)
    set_gem(c, 360, 226, 16, 14, (0.55, 0.98, 0.96), SILVER, rng, prongs=4)
    return c.image()


def neck_abyss(seed=7215):
    """สร้อยดวงใจอเวจี (zone 5, 2026-11-20): a blackened iron chain, a horned obsidian frame and a deep heart-red gem."""
    c, rng = _c(seed)
    hang(c, rng, BLACK_IRON)
    bail(c, rng, 286, BLACK_IRON)
    frame = [(196, 312), (316, 312), (340, 372), (256, 486), (172, 372)]
    metal_shape(c, rng, frame, (0.22, 0.16, 0.26), r=14, amount=0.35)
    for sx in (-1, 1):
        horn = blur(poly([(256 + sx * 52, 318), (256 + sx * 96, 268), (256 + sx * 104, 214), (256 + sx * 84, 262), (256 + sx * 40, 300)]), 1.2)
        metal_real(c, horn, OLD_GOLD, rng, r=6)
    facet_gem(c, 256, 384, 44, 62, (0.80, 0.10, 0.30), rng)
    glow(c, [190, 320, 322, 470], (0.95, 0.20, 0.45), 0.35, 24)
    return c.image()
