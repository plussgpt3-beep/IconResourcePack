"""ของที่ให้: goods wrapped in a cloth bundle, knotted on top."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, cloth


def draw():
    rng = np.random.default_rng(512)
    c = Canvas()
    body = blur(ellipse([70, 190, 442, 470]), 1.5)
    nx = (xx - 256) / 186; ny = (yy - 330) / 140
    h = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * body
    folds = 0.1 * np.sin(np.arctan2(yy - 160, xx - 256) * 9) * np.clip((330 - yy) / 160, 0, 1)
    col = cloth(rng, (0.20, 0.30, 0.55), weave=2.5)
    check = (((xx // 40) + (yy // 40)) % 2 == 0)
    col[check] *= 0.8
    c.over(light(h + folds * body, col, depth=80, spec=0.05), body)
    for pts in ([(256, 200), (170, 90), (215, 160)], [(256, 200), (350, 80), (300, 160)]):
        ear = blur(poly(pts + [(256, 220)]), 1.2)
        c.over(light(0.4 * pillow(ear, 8), col, depth=40, spec=0.05), ear)
    knot = blur(ellipse([222, 170, 290, 230]), 1)
    c.over(light(pillow(knot, 12, 0.6), col * 0.9, depth=40, spec=0.1), knot)
    return c.image()
