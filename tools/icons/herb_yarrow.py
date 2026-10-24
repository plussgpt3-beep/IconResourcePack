"""ว่านห้ามเลือด (สมุนไพร, 2026-10-25): a stem of yarrow, its flat head of tiny white flowers, feathery leaves."""
import numpy as np
from lib import N, Canvas, light, pillow, blur, poly, ellipse
from _clinic import leaves


def draw():
    rng = np.random.default_rng(2602)
    c = Canvas()
    stem = blur(poly([(256, 480), (250, 330), (256, 170)], width=14), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.46, 0.18]), stem)
    leaves(c, rng, 230, 380, 0.9, color=(0.30, 0.52, 0.22))
    leaves(c, rng, 280, 300, 0.75, color=(0.32, 0.56, 0.24))
    # the flat head: many small florets
    for _ in range(46):
        a = rng.uniform(0, 2 * np.pi)
        r = rng.uniform(0, 1) ** 0.6 * 130
        x, y = 256 + r * np.cos(a), 150 + r * np.sin(a) * 0.45
        s = rng.uniform(15, 22)
        f = blur(ellipse([x - s, y - s, x + s, y + s]), 1)
        c.over(light(0.6 * pillow(f, 6), np.zeros((N, N, 3)) + np.array([0.96, 0.95, 0.90]), depth=40, spec=0.2), f)
        d = blur(ellipse([x - 5, y - 5, x + 5, y + 5]), 1)
        c.over(np.zeros((N, N, 3)) + np.array([0.90, 0.80, 0.45]), d, cast=False)
    return c.image()
