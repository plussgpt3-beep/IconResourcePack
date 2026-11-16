"""ผลึกธาตุ (แดนนอก, 2026-11-16): one stone per element and zone, dropped by the zone's monster of that element.
Grade = zone: 1 เศษ (broken shard), 2 ผลึก (a whole prism), 3 แก่น (a glowing orb in a stone claw), 4 มณี (a cut gem)."""
import numpy as np
from lib import N, xx, yy, light, pillow, blur, poly, ellipse, chrome, stone, gold_tint, steel_tint
from _wild import canvas

COL = {'fire': (1.00, 0.42, 0.10), 'ice': (0.55, 0.88, 1.00), 'storm': (1.00, 0.86, 0.22), 'venom': (0.42, 0.92, 0.28)}
GLOW = {'fire': (1.0, 0.85, 0.4), 'ice': (0.92, 1.0, 1.0), 'storm': (1.0, 1.0, 0.75), 'venom': (0.85, 1.0, 0.6)}


def facet(c, pts, base, lit, spec=0.8):
    m = blur(poly(pts), 1.3)
    cc = np.zeros((N, N, 3)) + np.array(base) * lit
    c.over(light(0.55 * pillow(m, 14), np.clip(cc, 0, 1), depth=70, spec=spec, gloss=50), m)


def glow(c, box, colour, a=0.75, r=10):
    c.over(np.zeros((N, N, 3)) + np.array(colour), blur(ellipse(box), r) * a, cast=False)


def shard(c, el):
    b = COL[el]
    facet(c, [(205, 120), (290, 175), (300, 330), (215, 405), (165, 300)], b, 1.0)
    facet(c, [(205, 120), (165, 300), (215, 405), (190, 300)], b, 0.65)
    facet(c, [(320, 250), (385, 300), (360, 410), (300, 400)], b, 0.9)
    facet(c, [(320, 250), (300, 400), (318, 330)], b, 0.6)
    glow(c, [205, 220, 275, 320], GLOW[el], 0.45, 14)


def prism(c, el):
    b = COL[el]
    facet(c, [(256, 55), (320, 130), (320, 380), (256, 455), (256, 130)], b, 0.7)
    facet(c, [(256, 55), (256, 130), (256, 455), (192, 380), (192, 130)], b, 1.05)
    facet(c, [(256, 55), (192, 130), (256, 130), (320, 130)], b, 1.25)
    glow(c, [216, 170, 296, 360], GLOW[el], 0.55, 18)
    facet(c, [(150, 330), (195, 300), (205, 440), (160, 440)], b, 0.8)
    facet(c, [(362, 320), (318, 300), (308, 440), (352, 440)], b, 0.85)


def orb(c, el, rng):
    b = COL[el]
    claw_col = stone(rng, (0.30, 0.28, 0.27))
    for pts in ([(150, 430), (170, 300), (200, 250), (215, 300), (195, 430)], [(362, 430), (342, 300), (312, 250), (297, 300), (317, 430)],
                [(225, 440), (240, 330), (256, 300), (272, 330), (287, 440)]):
        m = blur(poly(pts), 1.3)
        c.over(light(0.5 * pillow(m, 10), claw_col, depth=50, spec=0.15), m)
    m = blur(ellipse([150, 110, 362, 322]), 2)
    d = np.hypot(xx - 236, yy - 196) / 120.0
    cc = np.zeros((N, N, 3)) + np.array(b)
    cc = cc * (1.2 - 0.6 * np.clip(d, 0, 1))[..., None]
    c.over(light(0.8 * pillow(m, 60), np.clip(cc, 0, 1), depth=80, spec=0.9, gloss=60), m)
    glow(c, [200, 150, 290, 240], GLOW[el], 0.7, 16)
    for pts in ([(170, 300), (200, 250), (220, 280)], [(342, 300), (312, 250), (292, 280)]):
        m = blur(poly(pts), 1.2)
        c.over(light(0.5 * pillow(m, 8), claw_col, depth=50, spec=0.15), m)


def gem(c, el):
    b = COL[el]
    # crown and pavilion of a brilliant cut, seen from the side, set in a gold mount
    facet(c, [(130, 210), (180, 140), (332, 140), (382, 210)], b, 1.2)
    facet(c, [(180, 140), (220, 210), (130, 210)], b, 0.95)
    facet(c, [(332, 140), (382, 210), (292, 210)], b, 0.8)
    facet(c, [(220, 210), (256, 140), (292, 210)], b, 1.35)
    facet(c, [(130, 210), (256, 440), (220, 210)], b, 0.85)
    facet(c, [(220, 210), (256, 440), (292, 210)], b, 1.05)
    facet(c, [(292, 210), (256, 440), (382, 210)], b, 0.65)
    band = blur(poly([(126, 206), (386, 206), (386, 222), (126, 222)]), 1)
    c.over(chrome(0.5 * pillow(band, 4), gold_tint(), depth=40), band)
    glow(c, [206, 180, 306, 300], GLOW[el], 0.6, 20)
    for (x, y) in ((176, 128), (340, 132), (256, 96)):
        glow(c, [x - 10, y - 10, x + 10, y + 10], (1, 1, 1), 0.9, 4)


def draw_grade(el, grade, seed):
    rng = np.random.default_rng(seed)
    c = canvas(grade)
    if grade == 1: shard(c, el)
    elif grade == 2: prism(c, el)
    elif grade == 3: orb(c, el, rng)
    else: gem(c, el)
    return c.image()
