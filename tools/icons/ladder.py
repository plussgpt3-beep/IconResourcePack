"""ความสูงของเขต: a wooden ladder standing tall."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, wood


def draw():
    rng = np.random.default_rng(407)
    c = Canvas()
    for k in range(7):
        y = 90 + k * 56
        rung = blur(rect([180, y - 9, 332, y + 9], 6), 1)
        c.over(light(np.clip(1 - np.abs(yy - y) / 9, 0, 1) ** 0.5 * rung, wood(rng, (0.60, 0.42, 0.22), rings=3), depth=30, spec=0.25), rung)
    for x0, x1 in ((170, 196), (316, 342)):
        rail = blur(poly([(x0 - 20, 490), (x1 - 20, 490), (x1 + 10, 30), (x0 + 10, 30)]), 1)
        mid = (x0 + x1) / 2 - 5
        c.over(light(np.clip(1 - np.abs(xx - mid - (260 - yy) * 0.065) / 13, 0, 1) ** 0.5 * rail, wood(rng, (0.52, 0.34, 0.17), angle=np.pi / 2, rings=4), depth=30, spec=0.25), rail)
    return c.image()
