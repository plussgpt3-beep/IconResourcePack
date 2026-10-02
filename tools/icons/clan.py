"""แคลน: a clan banner - deep blue cloth with a gold star, hanging from a crossbar on a pole."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, chrome, gold_tint


def draw():
    rng = np.random.default_rng(206)
    c = Canvas()
    pole = blur(rect([236, 20, 262, 500], 10), 1)
    c.over(light(pillow(pole, 8, 0.7) * 0.8, wood(rng, (0.42, 0.25, 0.12), angle=np.pi / 2, rings=6), depth=40, spec=0.3), pole)
    bar = blur(rect([120, 70, 392, 92], 10), 1)
    c.over(light(pillow(bar, 8, 0.7) * 0.8, wood(rng, (0.42, 0.25, 0.12), rings=6), depth=40, spec=0.3), bar)
    for x in (126, 386):
        knob = blur(ellipse([x - 18, 63, x + 18, 99]), 1)
        c.over(chrome(pillow(knob, 8, 0.7), gold_tint(), depth=40), knob)
    # the cloth: swallow-tailed, hanging in soft vertical folds
    flag = blur(poly([(140, 90), (372, 90), (372, 420), (310, 380), (256, 440), (202, 380), (140, 420)]), 1.5)
    folds = np.sin((xx - 140) / 232 * np.pi * 3)
    h = (0.3 + 0.12 * folds) * flag
    col = cloth(rng, (0.10, 0.16, 0.42))
    c.over(light(h, col, depth=60, spec=0.08), flag)
    # gold trim along the top and a star in the middle
    trim = blur(rect([140, 92, 372, 106]), 1) * flag
    c.over(chrome(pillow(trim, 3) * 0.5, gold_tint(), depth=30), trim)
    cx, cy = 256, 240
    ang = np.arctan2(yy - cy, xx - cx); rr = np.hypot(xx - cx, yy - cy)
    sr = 70 * (0.45 + 0.55 * np.abs(np.cos(2.5 * (ang + np.pi / 2))) ** 3)
    star = blur((rr < sr).astype(np.float32), 1.5)
    c.over(chrome(pillow(star, 8) * 0.6 + 0.3 * folds * 0.1, gold_tint(), depth=40), star)
    return c.image()
