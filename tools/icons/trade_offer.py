"""ข้อเสนอการค้า: a trade agreement between two cities - one contract under two seals."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, ellipse, edge_darken, wax_seal


def draw():
    rng = np.random.default_rng(505)
    c = Canvas()
    sheet = blur(poly([(90, 50), (420, 60), (430, 470), (80, 460)]), 1.2)
    col = parchment(rng)
    for k in range(7):
        y = 100 + k * 34
        ln = poly([(125, y), (390 - (k % 3) * 40, y + 2)], width=6)
        col = col * (1 - 0.45 * ln[..., None])
    for x in (150, 300):
        sig = poly([(x, 360), (x + 25, 345), (x + 45, 365), (x + 75, 340)], width=4)
        col = col * (1 - 0.6 * sig[..., None])
    c.over(light(0.12 * pillow(sheet, 8), col, depth=40, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    wax_seal(c, rng, 170, 420, 48, (0.55, 0.06, 0.05), ellipse([0, 0, 1, 1]) * 0)
    wax_seal(c, rng, 340, 420, 48, (0.10, 0.20, 0.50), ellipse([0, 0, 1, 1]) * 0)
    return c.image()
