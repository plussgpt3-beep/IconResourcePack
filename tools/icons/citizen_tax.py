"""ภาษีราษฎร: a head-tax roll - a citizen's name on the city's register under a red seal, and the coins due."""
import numpy as np
from lib import Canvas, light, pillow, parchment, blur, poly, edge_darken, wax_seal, gold_coin, ellipse


def draw():
    rng = np.random.default_rng(707)
    c = Canvas()
    sheet = blur(poly([(70, 55), (370, 45), (380, 420), (80, 430)]), 1.2)
    col = parchment(rng)
    # the citizen: a head and shoulders in brown ink at the top of the roll
    head = ellipse([185, 85, 255, 160])
    body = blur(poly([(160, 235), (175, 185), (220, 168), (265, 185), (280, 235)]), 1.0)
    ink = np.clip(head + body, 0, 1)
    col = col * (1 - 0.62 * ink[..., None])
    # register lines under him: name, standing, sum
    for k in range(4):
        y = 270 + k * 34
        ln = poly([(115, y), (330 - (k % 2) * 50, y)], width=6)
        col = col * (1 - 0.45 * ln[..., None])
    c.over(light(0.12 * pillow(sheet, 8), col, depth=40, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    wax_seal(c, rng, 128, 380, 44, (0.55, 0.06, 0.05), ellipse([0, 0, 1, 1]) * 0)
    for i in range(5): gold_coin(c, 370, 470 - i * 24, 96, 30, 18)
    return c.image()
