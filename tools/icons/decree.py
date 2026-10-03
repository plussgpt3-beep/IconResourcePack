"""ออกประกาศ: a royal proclamation - an unrolled parchment between two wooden rollers, lines of writing, a red crown seal."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, parchment, wood, edge_darken, chrome, gold_tint, wax_seal, _symbol


def draw():
    rng = np.random.default_rng(1101)
    c = Canvas()
    # the sheet, a little wavy at the edges
    sheet = blur(poly([(118, 92), (394, 92), (402, 250), (394, 420), (118, 420), (110, 250)]), 1.5)
    curl = 0.08 * np.sin((yy - 92) / 38.0) * sheet
    col = parchment(rng, (0.93, 0.86, 0.66))
    for k in range(7):
        y = 150 + k * 30
        right = 360 - (40 if k in (2, 6) else 0)
        ln = poly([(150, y), (right, y)], width=7)
        col = col * (1 - 0.55 * blur(ln, 1)[..., None])
    head = poly([(190, 122), (322, 122)], width=12)                          # the heading, darker and wider
    col = col * (1 - 0.7 * blur(head, 1)[..., None])
    c.over(light(0.18 * pillow(sheet, 14) + curl, col, depth=40, spec=0.06) * edge_darken(sheet, 10, 0.35), sheet)
    # wooden rollers top and bottom, gold knobs at the ends
    for y in (92, 420):
        rod = blur(rect([92, y - 20, 420, y + 20], 18), 1.2)
        h = pillow(rod, 14, 0.5) * 0.8
        c.over(light(h, wood(rng, (0.42, 0.24, 0.11), rings=6), depth=60, spec=0.3), rod)
        for x in (84, 428):
            knob = blur(ellipse([x - 26, y - 26, x + 26, y + 26]), 1.2)
            c.over(chrome(0.6 * pillow(knob, 12), gold_tint(), depth=50), knob)
    # the king's seal hanging over the foot of the sheet
    ribbon = blur(poly([(330, 330), (352, 330), (372, 470), (350, 455), (336, 478)]), 1.2)
    c.over(light(0.2 * pillow(ribbon, 5), np.zeros((N, N, 3)) + np.array([0.62, 0.08, 0.07]), depth=30, spec=0.2), ribbon)
    wax_seal(c, rng, 330, 345, 62, (0.70, 0.08, 0.07), _symbol('crown', 330, 345, 62))
    return c.image()
