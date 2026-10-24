"""ใบสั่งซื้อระหว่างเมือง: a purchase order - a parchment list of goods, a gold coin pinned to it, a red seal at its foot."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, parchment, edge_darken, coin_flat, wax_seal, _symbol


def draw():
    rng = np.random.default_rng(2432)
    c = Canvas()
    sheet = blur(poly([(110, 60), (380, 70), (400, 460), (120, 450)]), 1.5)
    col = parchment(rng, (0.93, 0.86, 0.66))
    for k in range(7):
        y = 130 + k * 38
        ln = poly([(150, y + k), (320 - (60 if k % 3 == 2 else 0), y + k + 2)], width=8)
        col = col * (1 - 0.55 * blur(ln, 1)[..., None])
        tick = poly([(330, y + k), (352, y + k + 1)], width=8)
        col = col * (1 - 0.45 * blur(tick, 1)[..., None])
    c.over(light(0.18 * pillow(sheet, 14), col, depth=40, spec=0.06) * edge_darken(sheet, 10, 0.35), sheet)
    coin_flat(c, 360, 110, 70)
    wax_seal(c, rng, 300, 410, 56, (0.62, 0.06, 0.08), _symbol('crown', 300, 410, 42))
    return c.image()
