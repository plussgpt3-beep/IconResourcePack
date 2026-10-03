"""ภาษีที่ดิน: a tax notice under the city's red seal, with the coins that pay it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, edge_darken, wax_seal, gold_coin, ellipse


def draw():
    rng = np.random.default_rng(303)
    c = Canvas()
    sheet = blur(poly([(80, 60), (360, 50), (370, 400), (90, 410)]), 1.2)
    col = parchment(rng)
    for k in range(6):
        y = 110 + k * 36
        ln = poly([(115, y), (320 - (k % 2) * 40, y)], width=6)
        col = col * (1 - 0.45 * ln[..., None])
    # a ruled column of figures on the right
    for k in range(5):
        y = 120 + k * 36
        ln = poly([(270, y), (330, y)], width=5)
        col = col * (1 - 0.35 * ln[..., None])
    c.over(light(0.12 * pillow(sheet, 8), col, depth=40, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    wax_seal(c, rng, 150, 345, 46, (0.55, 0.06, 0.05), ellipse([140, 335, 160, 355]) * 0)
    for i in range(4): gold_coin(c, 360, 460 - i * 24, 92, 30, 18)
    return c.image()
