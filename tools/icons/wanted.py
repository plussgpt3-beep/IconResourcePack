"""ประกาศจับตาย: a wanted notice nailed up - parchment, a dark hooded figure, a red crown seal and the coins of the bounty."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, parchment, edge_darken, wax_seal, gold_coin, ellipse, rect, chrome


def draw():
    rng = np.random.default_rng(2471)
    c = Canvas()
    sheet = blur(poly([(110, 50), (402, 62), (392, 450), (100, 440)]), 1.2)
    col = parchment(rng)
    c.over(light(0.12 * pillow(sheet, 8), col, depth=40, spec=0.05) * edge_darken(sheet, 14, 0.38), sheet)
    # The figure: a hooded head and shoulders in soot.
    head = ellipse([205, 110, 305, 215])
    body = poly([(165, 330), (190, 230), (250, 205), (312, 230), (338, 330)])
    fig = blur(np.clip(head + body, 0, 1), 1.5) * sheet
    soot = np.ones((N, N, 3), np.float32) * np.array([0.18, 0.12, 0.10], np.float32)
    c.over(light(0.2 * pillow(fig, 10), soot, depth=30, spec=0.04), fig * 0.92)
    # Lines of the notice under the figure.
    for k in range(3):
        y = 360 + k * 24
        ln = poly([(150, y), (350 - (k % 2) * 50, y + 2)], width=6)
        c.over(light(0 * ln, soot, depth=10, spec=0), ln * sheet * 0.7)
    # Nails at the top corners.
    for x, y in ((128, 72), (382, 82)):
        nail = blur(ellipse([x - 11, y - 11, x + 11, y + 11]), 1)
        c.over(chrome(0.7 * pillow(nail, 6), (0.45, 0.45, 0.48), depth=40), nail)
    wax_seal(c, rng, 352, 400, 40, (0.62, 0.06, 0.05), ellipse([342, 390, 362, 410]) * 0)
    for i in range(3): gold_coin(c, 120, 470 - i * 22, 64, 22, 14)
    return c.image()
