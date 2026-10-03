"""บริหารคลัง: the treasury ledger - an open account book of ruled columns, a quill beside it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, edge_darken, leather_col
from petition import quill


def draw():
    rng = np.random.default_rng(502)
    c = Canvas()
    cover = blur(poly([(30, 160), (256, 200), (482, 160), (482, 440), (256, 480), (30, 440)]), 1.5)
    c.over(light(0.3 * pillow(cover, 10), leather_col(rng, (0.30, 0.10, 0.06)), depth=40, spec=0.2) * edge_darken(cover, 8, 0.4), cover)
    for side in (-1, 1):
        x_out = 256 + side * 210
        pg = blur(poly([(256, 190), (256 + side * 100, 140), (x_out, 150), (x_out, 420), (256 + side * 100, 412), (256, 456)]), 1.2)
        t = np.clip((xx - 256) * side / 210, 0, 1)
        col = parchment(rng, (0.94, 0.89, 0.75))
        for k in range(8):
            y = 190 + k * 28
            ln = poly([(256 + side * 20, y + 10), (x_out - side * 14, y - 10)], width=3)
            col = col * (1 - 0.35 * ln[..., None])
        for xf in (0.55, 0.78):
            vx = 256 + side * 210 * xf
            col = col * (1 - 0.35 * poly([(vx, 160), (vx, 420)], width=3)[..., None])
        c.over(light((np.sin(t * np.pi * 0.85) * 0.5 + 0.1) * pg, col, depth=90, spec=0.05), pg)
    quill(c, (300, 330), (500, 60), width=40)
    return c.image()
