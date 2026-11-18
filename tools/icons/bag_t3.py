"""กระเป๋าเสริม Tier 3 กระเป๋าหนังหุ้มเหล็ก (+27 ช่อง): a dark leather satchel with iron corner plates, bands and rivets."""
import numpy as np
from lib import Canvas, blur, poly, rect, leather_col, steel_tint
from _bag import part, iron_part, rivets, buckle


def draw():
    rng = np.random.default_rng(1103)
    c = Canvas()
    handle = blur(poly([(196, 150), (206, 70), (306, 70), (316, 150)], width=22), 1.5)
    part(c, handle, leather_col(rng, (0.28, 0.16, 0.08)), 0.35, 8, 40)
    body = blur(rect([80, 140, 432, 450], 26), 1.5)
    part(c, body, leather_col(rng, (0.32, 0.19, 0.10)), 0.3, 22, 60, 0.25)
    flap = blur(poly([(80, 150), (432, 150), (432, 280), (80, 280)]), 1.5)
    part(c, flap, leather_col(rng, (0.38, 0.23, 0.12)), 0.25, 12, 50, 0.3)
    for (x0, y0, sx, sy) in ((80, 140, 1, 1), (432, 140, -1, 1), (80, 450, 1, -1), (432, 450, -1, -1)):
        tri = blur(poly([(x0, y0), (x0 + sx * 90, y0), (x0, y0 + sy * 90)]), 1.2)
        iron_part(c, tri, 0.5, 5)
    for x in (176, 336):
        band = blur(rect([x - 14, 150, x + 14, 450], 4), 1)
        iron_part(c, band, 0.5, 4)
        rivets(c, [(x, y) for y in range(180, 450, 52)], 7)
    buckle(c, 256, 280, 24)
    return c.image()
