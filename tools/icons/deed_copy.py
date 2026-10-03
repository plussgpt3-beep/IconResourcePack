"""รับสำเนาโฉนด: two copies of a deed, one over the other, both sealed."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, edge_darken, wax_seal, ellipse


def sheet(c, rng, pts, sx, sy):
    m = blur(poly(pts), 1.2)
    col = parchment(rng)
    for k in range(7):
        y = sy + 50 + k * 32
        ln = poly([(sx + 30, y), (sx + 210 - (k % 3) * 30, y + 2)], width=6)
        col = col * (1 - 0.45 * ln[..., None])
    c.over(light(0.12 * pillow(m, 8), col, depth=40, spec=0.05) * edge_darken(m, 10, 0.3), m)
    wax_seal(c, rng, sx + 200, sy + 300, 38, (0.55, 0.06, 0.05), ellipse([0, 0, 1, 1]) * 0)


def draw():
    rng = np.random.default_rng(305)
    c = Canvas()
    sheet(c, rng, [(60, 80), (300, 60), (320, 400), (80, 420)], 60, 70)
    sheet(c, rng, [(190, 110), (440, 120), (430, 470), (180, 460)], 185, 120)
    return c.image()
