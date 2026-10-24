"""จ้างทหารคุ้มกัน: the guard's shield with a sealed contract and the coins of his wage before it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, parchment, edge_darken, wax_seal, gold_coin, ellipse
from _escort import shield


def draw():
    rng = np.random.default_rng(2461)
    c = Canvas()
    shield(c, rng, cx=300, top=50, w=260, h=300)
    sheet = blur(poly([(60, 250), (300, 230), (310, 450), (70, 470)]), 1.2)
    col = parchment(rng)
    for k in range(5):
        y = 290 + k * 30
        ln = poly([(95, y), (260 - (k % 2) * 40, y - 3)], width=5)
        col = col * (1 - 0.45 * ln[..., None])
    c.over(light(0.12 * pillow(sheet, 8), col, depth=40, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    wax_seal(c, rng, 250, 420, 34, (0.55, 0.06, 0.05), ellipse([240, 410, 260, 430]) * 0)
    for i in range(4): gold_coin(c, 400, 470 - i * 22, 70, 24, 15)
    return c.image()
