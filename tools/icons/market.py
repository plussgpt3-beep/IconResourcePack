"""ตลาด: a merchant's brass balance, one pan weighed down with gold."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_coin, wood


def draw():
    rng = np.random.default_rng(215)
    c = Canvas()
    brass = (0.95, 0.70, 0.36)
    base = blur(np.maximum(rect([176, 440, 336, 480], 12), poly([(220, 445), (292, 445), (270, 400), (242, 400)])), 1)
    c.over(light(pillow(base, 8) * 0.7, wood(rng, (0.30, 0.17, 0.08), rings=8), depth=40, spec=0.3), base)
    post = blur(rect([246, 90, 266, 410], 8), 1)
    c.over(chrome(np.clip(1 - np.abs(xx - 256) / 10, 0, 1) ** 0.5 * post, brass, depth=40), post)
    # beam, tipped: left side lower (it holds the gold)
    beam = blur(poly([(86, 156), (426, 112), (428, 126), (88, 170)]), 1)
    c.over(chrome(pillow(beam, 4) * 0.6, brass, depth=40), beam)
    knob = blur(ellipse([238, 112, 274, 148]), 1)
    c.over(chrome(pillow(knob, 8, 0.7), brass, depth=40), knob)
    for (px, py, drop) in ((96, 163, 250), (416, 119, 200)):
        for dx in (-50, 50):
            ch = blur(poly([(px, py), (px + dx, py + drop - py - 10)], width=3), 0.8)
            c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.42, 0.22]), ch)
        pan = blur(np.maximum(ellipse([px - 66, drop - 22, px + 66, drop + 14]) * (yy > drop - 4), ellipse([px - 66, drop - 16, px + 66, drop + 8])), 1)
        c.over(chrome(pillow(pan, 8) * 0.6, brass, depth=40), pan)
    for i in range(3): gold_coin(c, 96, 238 - i * 14, 40, 13, 8)
    return c.image()
