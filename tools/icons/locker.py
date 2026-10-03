"""ขาตั้งเกราะของฉัน: an armour stand on its wooden cross - a steel helmet and breastplate hung on it, a small brass key tag."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, gold_tint, steel_tint, edge_darken


def draw():
    rng = np.random.default_rng(1204)
    c = Canvas()
    # the stand: base plate, post, shoulder bar
    base = blur(poly([(130, 450), (382, 450), (412, 492), (100, 492)]), 1.2)
    c.over(light(0.3 * pillow(base, 8), wood(rng, (0.38, 0.22, 0.10), rings=6), depth=40, spec=0.2), base)
    post = blur(rect([244, 120, 268, 460], 6), 1)
    c.over(light(0.5 * pillow(post, 6), wood(rng, (0.42, 0.25, 0.11), angle=np.pi / 2, rings=4), depth=40, spec=0.2), post)
    bar = blur(rect([120, 200, 392, 222], 6), 1)
    c.over(light(0.5 * pillow(bar, 6), wood(rng, (0.42, 0.25, 0.11), rings=4), depth=40, spec=0.2), bar)
    # breastplate with a ridge down the middle and shoulder guards
    chest = blur(poly([(160, 210), (352, 210), (340, 330), (300, 400), (212, 400), (172, 330)]), 1.5)
    h = np.sqrt(np.clip(1 - ((xx - 256) / 100) ** 2, 0, 1)) * 0.8 + 0.25 * np.exp(-((xx - 256) / 10) ** 2)
    c.over(chrome(h * chest, steel_tint(), depth=70) * edge_darken(chest, 10, 0.3), chest)
    for cx in (150, 362):
        sh = blur(ellipse([cx - 52, 186, cx + 52, 262]) * (yy < 240), 1.2)
        c.over(chrome(0.7 * pillow(sh, 14), steel_tint(), depth=60) * edge_darken(sh, 8, 0.3), sh)
        trim = blur(np.clip(ellipse([cx - 52, 186, cx + 52, 262]) - ellipse([cx - 44, 194, cx + 44, 256]), 0, 1) * (yy < 240), 1)
        c.over(chrome(0.4 * pillow(trim, 3), gold_tint(), depth=30), trim)
    belt = blur(rect([206, 374, 306, 398], 4), 1)
    c.over(light(0.3 * pillow(belt, 4), np.zeros((N, N, 3)) + np.array([0.30, 0.17, 0.08]), depth=30, spec=0.3), belt)
    buckle = blur(rect([244, 372, 268, 400], 3), 1)
    c.over(chrome(0.5 * pillow(buckle, 3), gold_tint(), depth=30), buckle)
    # the helmet on top of the post
    helm = blur(np.maximum(ellipse([196, 40, 316, 170]) * (yy < 130), rect([196, 100, 316, 150], 10)), 1.2)
    hh = np.sqrt(np.clip(1 - ((xx - 256) / 60) ** 2 - ((yy - 115) / 75) ** 2, 0, 1))
    c.over(chrome(0.9 * hh * helm, steel_tint(), depth=60) * edge_darken(helm, 8, 0.3), helm)
    slit = blur(rect([212, 118, 300, 128], 4), 1.5)
    c.over(np.zeros((N, N, 3)) + np.array([0.04, 0.04, 0.05]), slit)
    # a brass key tag hanging from the bar: this stand is somebody's locker
    cord = blur(poly([(370, 222), (392, 300)], width=4), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.45, 0.30, 0.15]), cord)
    tag = blur(ellipse([368, 292, 420, 344]), 1)
    c.over(chrome(0.6 * pillow(tag, 10), gold_tint(), depth=40), tag)
    hole = blur(ellipse([386, 304, 402, 320]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.10, 0.07, 0.04]), hole)
    return c.image()
