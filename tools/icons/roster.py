"""ตำแหน่งในอาณาจักร: the realm's roll of offices - a bound register with a crown on its cover."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, rect, edge_darken, leather_col, chrome, gold_tint


def draw():
    rng = np.random.default_rng(605)
    c = Canvas()
    pages = blur(poly([(110, 90), (420, 70), (430, 440), (120, 465)]), 1)
    c.over(parchment(rng, (0.85, 0.78, 0.60)) * (0.8 + 0.2 * (np.sin(yy / 2.0) > 0))[..., None], pages)
    cover = blur(poly([(80, 70), (400, 50), (410, 420), (90, 445)]), 1.2)
    c.over(light(0.3 * pillow(cover, 14), leather_col(rng, (0.20, 0.10, 0.30)), depth=40, spec=0.2) * edge_darken(cover, 10, 0.45), cover)
    border = blur(np.clip(cover - blur(poly([(105, 95), (375, 78), (383, 395), (113, 418)]), 1), 0, 1), 1)
    c.over(chrome(0.3 * pillow(border, 3), gold_tint(), depth=30), border * 0.9)
    crown = blur(poly([(170, 290), (170, 190), (205, 240), (245, 160), (285, 240), (320, 190), (320, 290)]), 1.5)
    c.over(chrome(0.5 * pillow(crown, 8), gold_tint(), depth=40), crown)
    for k in range(3):
        y = 320 + k * 26
        ln = blur(rect([170, y, 320 - k * 30, y + 8]), 1)
        c.over(chrome(0.3 * ln, gold_tint(), depth=20), ln)
    return c.image()
