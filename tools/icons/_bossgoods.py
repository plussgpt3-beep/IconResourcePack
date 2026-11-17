"""ของเฉพาะบอสประจำธาตุ (แดนนอก, 2026-11-17): one good per element boss, drawn like the other wild goods.
Each wild_<id>.py calls draw('<id>')."""
import numpy as np
from lib import N, xx, yy, light, pillow, blur, poly, ellipse, chrome, stone, steel_tint, gold_tint, noise, leather_col, mask_from
from _wild import canvas
from _elem import glow as _glow


def glow(c, box, colour, a=0.75, r=10):
    """A glow that stays on what is already painted (a halo outside would get cropped in and outlined)."""
    m = blur(ellipse(box), r) * a * c.px[..., 3]
    c.over(np.zeros((N, N, 3)) + np.array(colour), m, cast=False)


def taper(pts, r0, r1, steps=160):
    """Mask of a stroke along a polyline, radius r0 at the start to r1 at the end."""
    p = np.array(pts, np.float32)
    seg = np.hypot(*(p[1:] - p[:-1]).T); tot = seg.sum(); cum = np.concatenate([[0], np.cumsum(seg)])

    def at(t):
        d = t * tot; i = min(int(np.searchsorted(cum, d, 'right')) - 1, len(seg) - 1)
        f = (d - cum[i]) / (seg[i] or 1)
        return p[i] + (p[i + 1] - p[i]) * f

    def drw(d):
        for k in range(steps + 1):
            t = k / steps; x, y = at(t); r = r0 + (r1 - r0) * t
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return mask_from(drw)


def paint(c, m, col, h=None, depth=60, spec=0.3, gloss=30, soft=1.5):
    m = blur(m, soft)
    if h is None:
        h = pillow(m, 18)
    c.over(light(h, np.clip(col, 0, 1), depth=depth, spec=spec, gloss=gloss), m)
    return m


def solid(rgb):
    return np.zeros((N, N, 3)) + np.array(rgb)


def tone(rng, a, b, scale=8):
    t = noise(rng, scale, 3)[..., None]
    return np.array(a) * (1 - t) + np.array(b) * t


def lightning(c, pts, core=(1, 1, 1), halo=(0.55, 0.9, 1.0), w=7):
    m = poly(pts, width=w)
    c.over(solid(halo), blur(m, 9) * 0.85 * c.px[..., 3], cast=False)
    c.over(solid(core), blur(m, 1.2), cast=False)


def boar_tusk(c, rng):
    # a curved tusk: old ivory at the root, glowing ember at the tip, a leather binding
    m = taper([(110, 420), (180, 300), (290, 200), (400, 150)], 66, 8)
    t = np.clip((xx - 170) / 230, 0, 1)[..., None] ** 1.5
    ivory = tone(rng, (0.94, 0.88, 0.74), (0.72, 0.62, 0.45), 10)
    fire = tone(rng, (1.0, 0.36, 0.06), (1.0, 0.82, 0.30), 14)
    paint(c, m, ivory * (1 - t) + fire * t, pillow(m, 40), depth=70, spec=0.4)
    for pts in ([(230, 290), (270, 255), (300, 262)], [(300, 230), (340, 212)], [(195, 345), (230, 312)]):
        c.over(solid((1.0, 0.70, 0.20)), blur(poly(pts, width=6), 1.5), cast=False)
    glow(c, [300, 110, 440, 210], (1.0, 0.6, 0.2), 0.55, 22)
    band = taper([(96, 400), (140, 440)], 44, 44)
    paint(c, band, leather_col(rng, (0.38, 0.20, 0.10)), depth=40, spec=0.15)


def stag_antler(c, rng):
    pale = tone(rng, (0.88, 0.84, 0.72), (0.55, 0.50, 0.40), 12)
    m = np.maximum.reduce([
        taper([(130, 450), (180, 340), (240, 240), (295, 140), (312, 70)], 44, 14),
        taper([(205, 300), (300, 285), (370, 225)], 28, 9),
        taper([(260, 210), (350, 170), (410, 100)], 24, 7),
        taper([(165, 375), (120, 300), (110, 230)], 24, 7)])
    paint(c, m, pale, pillow(m, 22), depth=60, spec=0.3)
    lightning(c, [(150, 420), (192, 345), (176, 322), (236, 248), (220, 225), (292, 145)])
    lightning(c, [(300, 285), (342, 245), (334, 232), (368, 226)], core=(1, 1, 0.8), halo=(1.0, 0.85, 0.3), w=5)


def widow_sac(c, rng):
    sac = np.maximum(ellipse([110, 160, 400, 440]), ellipse([195, 110, 315, 215]))
    shade = np.clip((yy - 140) / 320, 0, 1)[..., None]
    col = tone(rng, (0.36, 0.14, 0.46), (0.22, 0.08, 0.30), 10) * (1 - 0.55 * shade)
    paint(c, sac, col, pillow(sac, 70), depth=80, spec=0.6, gloss=40)
    for (x, y, r) in ((200, 280, 22), (300, 255, 16), (270, 350, 26), (340, 330, 14), (190, 365, 12)):
        glow(c, [x - r - 10, y - r - 10, x + r + 10, y + r + 10], (0.55, 1.0, 0.3), 0.6, 12)
        paint(c, ellipse([x - r, y - r, x + r, y + r]), solid((0.62, 1.0, 0.36)), depth=30, spec=0.5)
    stalk = taper([(256, 125), (248, 90), (276, 58)], 14, 8)
    paint(c, stalk, tone(rng, (0.35, 0.24, 0.26), (0.18, 0.12, 0.13)), depth=40)
    drip = np.maximum(taper([(240, 430), (238, 465)], 9, 6), ellipse([226, 458, 250, 482]))
    c.over(solid((0.55, 1.0, 0.30)), blur(drip, 1.5), cast=False)


def ember_spore(c, rng):
    balls = [(236, 264, 104), (344, 224, 60), (328, 348, 68), (164, 372, 48), (192, 168, 40)]
    for (x, y, r) in balls:
        glow(c, [x - r - 26, y - r - 26, x + r + 26, y + r + 26], (1.0, 0.45, 0.10), 0.35, 20)
    for (x, y, r) in balls:
        m = ellipse([x - r, y - r, x + r, y + r])
        d = np.clip(np.hypot(xx - x + r * 0.3, yy - y + r * 0.3) / r, 0, 1)[..., None]
        col = tone(rng, (0.55, 0.10, 0.03), (1.0, 0.42, 0.06), 10) * d + np.array([1.0, 0.86, 0.45]) * (1 - d)
        paint(c, m, col, pillow(m, r * 0.7), depth=70, spec=0.35)
        for k in range(5):
            a = rng.random() * 6.28; rr = r * (0.3 + 0.55 * rng.random())
            px, py = x + np.cos(a) * rr, y + np.sin(a) * rr
            c.over(solid((0.25, 0.06, 0.02)), blur(ellipse([px - 4, py - 4, px + 4, py + 4]), 1), cast=False)


def bear_pelt(c, rng):
    pts = [(108, 192), (192, 140), (320, 152), (412, 120), (428, 236), (392, 336), (428, 412), (300, 392), (204, 428), (100, 380), (132, 284)]
    m = poly(pts)
    rag = noise(rng, 20, 3)
    m = blur(m, 6); m = np.clip((m - 0.5 + (rag - 0.5) * 0.45) * 6, 0, 1)
    streak = 0.5 + 0.5 * np.sin((xx * 0.35 + yy * 0.9 + noise(rng, 6, 3) * 60) / 3.2)
    fur = (0.84 + 0.10 * noise(rng, 90, 2) + 0.10 * streak)[..., None]
    edge = np.clip(1 - blur(m, 18) * 1.6, 0, 1)[..., None] * m[..., None]
    col = np.array([0.95, 0.97, 0.99]) * fur * (1 - edge) + np.array([0.55, 0.80, 1.0]) * edge
    paint(c, m, col, pillow(m, 36) + 0.04 * streak * m, depth=55, spec=0.1, soft=0.5)
    c.over(solid((0.70, 0.80, 0.88)), blur(poly([(140, 272), (392, 240)], width=5), 2) * 0.8, cast=False)
    for (x, y) in ((180, 200), (352, 184), (388, 364), (144, 352)):
        paint(c, poly([(x, y - 24), (x + 8, y), (x, y + 24), (x - 8, y)]), solid((0.85, 0.96, 1.0)), depth=20, spec=0.9, gloss=60)


def hag_orb(c, rng):
    root = tone(rng, (0.36, 0.27, 0.18), (0.18, 0.12, 0.08))
    for pts in ([(190, 335), (180, 410), (220, 470)], [(322, 335), (332, 410), (292, 470)]):
        paint(c, taper(pts, 18, 10), root, depth=40)
    orb = ellipse([124, 92, 388, 356])
    sw = noise(rng, 4, 4)
    swirl = np.clip(np.sin((xx + 60 * np.sin(yy / 50)) / 40 + sw * 6) * 0.5 + 0.5, 0, 1)[..., None]
    col = np.array([0.10, 0.08, 0.26]) * (1 - swirl) + np.array([0.48, 0.36, 0.86]) * swirl
    col = col + np.array([0.3, 0.6, 0.7]) * np.clip(sw - 0.6, 0, 1)[..., None] * 2
    glow(c, [104, 72, 408, 376], (0.6, 0.45, 1.0), 0.35, 24)
    paint(c, orb, col, pillow(orb, 90), depth=90, spec=0.9, gloss=70)
    lightning(c, [(212, 140), (262, 208), (236, 220), (300, 300)])
    c.over(solid((1, 1, 1)), blur(ellipse([180, 130, 222, 160]), 6) * 0.8, cast=False)
    for pts in ([(172, 320), (212, 352)], [(340, 320), (300, 352)]):
        paint(c, taper(pts, 16, 9), root, depth=40)


def queen_stinger(c, rng):
    ice = tone(rng, (0.20, 0.50, 0.80), (0.70, 0.94, 1.0), 9)
    segs = [(128, 420, 52), (188, 352, 46), (248, 284, 40), (304, 220, 34)]
    for (x, y, r) in segs:
        m = ellipse([x - r, y - r, x + r, y + r])
        paint(c, m, ice, pillow(m, r * 0.8), depth=80, spec=0.8, gloss=50)
    barb = taper([(320, 200), (392, 140), (428, 88)], 36, 4)
    glow(c, [330, 50, 470, 210], (0.65, 0.92, 1.0), 0.45, 18)
    paint(c, barb, tone(rng, (0.55, 0.85, 1.0), (0.95, 1.0, 1.0), 8), depth=80, spec=1.0, gloss=60)


def titan_core(c, rng):
    a = np.pi / 6 + np.arange(6) * np.pi / 3
    hexa = poly([(256 + 172 * np.cos(t), 256 + 172 * np.sin(t)) for t in a])
    paint(c, hexa, stone(rng, (0.46, 0.48, 0.53)), pillow(hexa, 40), depth=60, spec=0.25)
    for pts in ([(256, 196), (236, 140), (264, 112)], [(312, 280), (376, 300), (400, 272)], [(208, 292), (160, 340), (172, 376)], [(300, 220), (352, 184)]):
        lightning(c, pts, w=6)
    core = ellipse([196, 196, 316, 316])
    d = np.clip(np.hypot(xx - 256, yy - 256) / 60, 0, 1)[..., None]
    glow(c, [170, 170, 342, 342], (0.45, 0.85, 1.0), 0.7, 24)
    paint(c, core, np.array([1.0, 0.97, 0.75]) * (1 - d) + np.array([0.3, 0.78, 1.0]) * d, pillow(core, 40), depth=50, spec=0.6)


def lizard_scale(c, rng):
    pts = [(256, 80), (392, 184), (412, 312), (256, 452), (100, 312), (120, 184)]
    m = poly(pts)
    rim = np.clip(1 - blur(m, 14) * 1.5, 0, 1)[..., None] * m[..., None]
    col = tone(rng, (0.40, 0.46, 0.39), (0.17, 0.20, 0.17), 10) * (1 - rim) + np.array([0.42, 1.0, 0.22]) * rim
    paint(c, m, col, pillow(m, 50), depth=70, spec=0.55, gloss=30)
    paint(c, taper([(256, 112), (256, 400)], 12, 6), solid((0.24, 0.29, 0.23)), depth=30, spec=0.5)
    for (x, y) in ((192, 240), (320, 240), (208, 340), (304, 340)):
        paint(c, ellipse([x - 26, y - 18, x + 26, y + 18]), solid((0.23, 0.29, 0.21)), depth=25, spec=0.4)
    c.over(solid((0.55, 1.0, 0.3)), blur(taper([(256, 446), (252, 482)], 9, 3), 1.5), cast=False)


def lich_crown(c, rng):
    ice = tone(rng, (0.25, 0.55, 0.82), (0.88, 0.98, 1.0), 8)
    grad = np.clip((420 - yy) / 360, 0, 1)[..., None]
    spikes = np.maximum.reduce([poly([(120, 304), (144, 188), (180, 304)]), poly([(184, 304), (216, 128), (248, 304)]),
                                poly([(240, 304), (256, 72), (276, 304)]), poly([(264, 304), (296, 128), (328, 304)]),
                                poly([(332, 304), (368, 188), (392, 304)])])
    glow(c, [100, 60, 412, 320], (0.70, 0.92, 1.0), 0.3, 18)
    paint(c, spikes, ice * (0.75 + 0.35 * grad), pillow(spikes, 14), depth=70, spec=1.0, gloss=60)
    band = poly([(104, 300), (408, 300), (392, 392), (120, 392)])
    paint(c, band, tone(rng, (0.62, 0.78, 0.90), (0.30, 0.48, 0.64), 9), pillow(band, 22), depth=50, spec=0.7)
    for x in (164, 256, 348):
        g = ellipse([x - 22, 320, x + 22, 372])
        d = np.clip(np.hypot(xx - x + 8, yy - 336) / 26, 0, 1)[..., None]
        paint(c, g, np.array([0.25, 0.42, 0.85]) * (1 - d) + np.array([0.04, 0.08, 0.28]) * d, pillow(g, 14), depth=40, spec=1.0, gloss=70)


def demon_chain(c, rng):
    iron = tone(rng, (0.24, 0.25, 0.30), (0.10, 0.10, 0.13), 10)

    def link(cx, cy, ang):
        ca, sa = np.cos(ang), np.sin(ang)
        u = (xx - cx) * ca + (yy - cy) * sa; v = -(xx - cx) * sa + (yy - cy) * ca
        r = np.hypot(u / 78, v / 52)
        return np.clip((0.26 - np.abs(r - 1) * 1.0) * 30, 0, 1)
    for (x, y, a) in ((172, 184, -0.6), (344, 344, -0.6), (258, 264, 0.95)):
        m = link(x, y, a)
        paint(c, m, iron, pillow(m, 10), depth=50, spec=0.7, gloss=28, soft=0.8)
    for pts in ([(112, 120), (148, 140), (132, 160), (180, 192)], [(300, 240), (340, 252), (324, 280), (372, 296)], [(392, 392), (420, 412), (408, 428), (444, 444)]):
        lightning(c, pts, core=(1, 1, 0.85), halo=(1.0, 0.85, 0.25), w=6)


def wyrm_fang(c, rng):
    roots = np.maximum(taper([(192, 92), (168, 48)], 24, 12), taper([(216, 92), (236, 44)], 22, 10))
    paint(c, roots, tone(rng, (0.75, 0.68, 0.58), (0.45, 0.38, 0.30)), depth=40, spec=0.2)
    fang = taper([(180, 80), (232, 200), (260, 328), (268, 428)], 68, 6)
    tip = np.clip((yy - 300) / 160, 0, 1)[..., None]
    col = tone(rng, (0.24, 0.10, 0.30), (0.07, 0.03, 0.10), 10) * (1 - tip * 0.6) + np.array([0.30, 0.85, 0.20]) * tip * 0.6
    paint(c, fang, col, pillow(fang, 40), depth=70, spec=0.65, gloss=32)
    c.over(solid((0.75, 0.55, 1.0)), blur(poly([(206, 128), (234, 240)], width=7), 3) * 0.6, cast=False)
    drip = np.maximum(taper([(268, 424), (268, 456)], 10, 7), ellipse([254, 452, 282, 482]))
    glow(c, [236, 420, 300, 496], (0.5, 1.0, 0.3), 0.5, 12)
    c.over(solid((0.62, 1.0, 0.36)), blur(drip, 1.5), cast=False)


def alpha_fang(c, rng):
    # เขี้ยวเงินจ่าฝูง: a long silver wolf fang with frost at the tip, bound with a leather cord
    m = taper([(170, 70), (220, 190), (262, 320), (280, 450)], 62, 6)
    tip = np.clip((yy - 280) / 180, 0, 1)[..., None]
    silver = tone(rng, (0.86, 0.88, 0.92), (0.52, 0.55, 0.62), 10)
    paint(c, m, silver * (1 - tip * 0.5) + np.array([0.60, 0.88, 1.0]) * tip * 0.5, pillow(m, 40), depth=70, spec=0.9, gloss=50)
    c.over(solid((1, 1, 1)), blur(poly([(192, 110), (226, 230)], width=8), 3) * 0.7, cast=False)
    cord = taper([(130, 116), (240, 92)], 16, 16)
    paint(c, cord, leather_col(rng, (0.40, 0.22, 0.10)), depth=35, spec=0.15)
    for (x, y) in ((262, 380), (282, 440)):
        paint(c, poly([(x, y - 16), (x + 6, y), (x, y + 16), (x - 6, y)]), solid((0.88, 0.97, 1.0)), depth=20, spec=1.0, gloss=60)


def ancient_heart(c, rng):
    # หัวใจไม้โบราณ: a wooden heart knot wrapped in roots, a venom-green glow at its core
    heart = np.maximum.reduce([ellipse([120, 120, 270, 290]), ellipse([242, 120, 392, 290]), poly([(130, 230), (382, 230), (256, 430)])])
    bark = tone(rng, (0.42, 0.28, 0.16), (0.20, 0.12, 0.06), 9)
    paint(c, heart, bark, pillow(heart, 50), depth=70, spec=0.2)
    for pts in ([(140, 190), (220, 250), (250, 380)], [(372, 190), (300, 240), (268, 380)], [(200, 140), (256, 220), (310, 140)]):
        paint(c, poly(pts, width=16), tone(rng, (0.30, 0.20, 0.10), (0.14, 0.09, 0.05), 6), depth=30, spec=0.2, soft=1)
    glow(c, [196, 200, 316, 320], (0.45, 1.0, 0.30), 0.8, 22)
    paint(c, ellipse([226, 232, 286, 292]), solid((0.70, 1.0, 0.45)), depth=30, spec=0.5)
    for (x, y) in ((170, 160), (350, 170), (300, 330)):
        paint(c, ellipse([x - 14, y - 9, x + 14, y + 9]), solid((0.32, 0.55, 0.18)), depth=15, spec=0.2)


def bandit_crown(c, rng):
    # มงกุฎราชาโจร: a battered gold crown with bone spikes and a fire ruby
    band = poly([(96, 268), (416, 268), (400, 380), (112, 380)])
    spikes = np.maximum.reduce([poly([(112, 272), (136, 168), (168, 272)]), poly([(200, 272), (228, 128), (256, 272)]),
                                poly([(256, 272), (284, 128), (312, 272)]), poly([(344, 272), (376, 168), (400, 272)])])
    paint(c, spikes, tone(rng, (0.92, 0.88, 0.76), (0.62, 0.55, 0.42), 9), pillow(spikes, 14), depth=50, spec=0.3)
    paint(c, band, chrome(0.6 * pillow(blur(band, 1.5), 24), gold_tint(), depth=60) * (0.85 + 0.25 * noise(rng, 20, 3)[..., None]), depth=1, spec=0.0)
    for (x, y) in ((150, 300), (330, 350), (390, 300)):
        c.over(solid((0.30, 0.20, 0.05)), blur(poly([(x, y), (x + 18, y + 8)], width=4), 1) * 0.8, cast=False)
    g = ellipse([226, 296, 286, 356])
    glow(c, [206, 276, 306, 376], (1.0, 0.45, 0.15), 0.55, 16)
    d = np.clip(np.hypot(xx - 248, yy - 316) / 34, 0, 1)[..., None]
    paint(c, g, np.array([1.0, 0.45, 0.30]) * (1 - d) + np.array([0.45, 0.04, 0.04]) * d, pillow(g, 18), depth=40, spec=1.0, gloss=70)


def knight_soul(c, rng):
    # แก่นวิญญาณอัศวิน: a soul flame caught in a dark iron cage, a sword hilt through it
    cage = np.maximum.reduce([poly([(176, 120), (176, 400)], width=16), poly([(336, 120), (336, 400)], width=16),
                              poly([(256, 96), (256, 424)], width=12), ellipse([160, 92, 352, 148]) - ellipse([176, 104, 336, 136]),
                              ellipse([160, 372, 352, 428]) - ellipse([176, 384, 336, 416])])
    cage = np.clip(cage, 0, 1)
    fl = poly([(256, 150), (318, 260), (300, 350), (256, 372), (212, 350), (194, 260)])
    fl = np.clip(blur(fl, 14) * 1.6, 0, 1)
    d = np.clip(np.hypot(xx - 256, yy - 300) / 110, 0, 1)[..., None]
    col = np.array([1.0, 0.95, 0.75]) * (1 - d) + np.array([1.0, 0.45, 0.10]) * d
    c.over(np.clip(col, 0, 1), fl, cast=False)
    glow(c, [176, 160, 336, 380], (1.0, 0.65, 0.25), 0.4, 20)
    paint(c, cage, tone(rng, (0.30, 0.30, 0.34), (0.12, 0.12, 0.14), 8), pillow(cage, 8), depth=40, spec=0.6, gloss=26, soft=0.8)


SEED = {'boar_tusk': 7101, 'stag_antler': 7102, 'widow_sac': 7103, 'ember_spore': 7104, 'bear_pelt': 7105, 'hag_orb': 7106,
        'queen_stinger': 7107, 'titan_core': 7108, 'lizard_scale': 7109, 'lich_crown': 7110, 'demon_chain': 7111, 'wyrm_fang': 7112,
        'alpha_fang': 7113, 'ancient_heart': 7114, 'bandit_crown': 7115, 'knight_soul': 7116}
ZONE = {'boar_tusk': 1, 'stag_antler': 1, 'widow_sac': 1, 'ember_spore': 2, 'bear_pelt': 2, 'hag_orb': 2,
        'queen_stinger': 3, 'titan_core': 3, 'lizard_scale': 3, 'lich_crown': 4, 'demon_chain': 4, 'wyrm_fang': 4,
        'alpha_fang': 1, 'ancient_heart': 2, 'bandit_crown': 3, 'knight_soul': 4}


def draw(name):
    rng = np.random.default_rng(SEED[name])
    c = canvas(ZONE[name])
    globals()[name](c, rng)
    return c.image()
