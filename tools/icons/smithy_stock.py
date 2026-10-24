"""คลังวัตถุดิบของร้าน: an open wooden crate of the smith's stock - iron ingots, lumps of coal."""
import numpy as np
from lib import N, Canvas, light, pillow, blur, rect, wood, edge_darken, yy
from _smithy import ingot, coal


def draw():
    rng = np.random.default_rng(2406)
    c = Canvas()
    back = blur(rect([60, 190, 452, 340], 10), 1)
    c.over(light(0.3 * pillow(back, 10), wood(rng, (0.34, 0.20, 0.09), rings=6), depth=40, spec=0.1), back)
    coal(c, rng, 120, 250, 70)
    coal(c, rng, 390, 246, 74)
    for (x, y) in ((190, 270), (330, 266), (260, 214)):
        ingot(c, x, y, 170)
    front = blur(rect([40, 320, 472, 470], 14), 1.2)
    planks = 0.9 + 0.1 * (np.abs(np.sin((yy - 320) / 21.0)) > 0.12)
    c.over(light(0.3 * pillow(front, 14), wood(rng, (0.55, 0.34, 0.16), rings=6) * planks[..., None], depth=50, spec=0.15)
           * edge_darken(front, 10, 0.35), front)
    for x in (60, 430):
        post = blur(rect([x, 320, x + 22, 470], 4), 1)
        c.over(light(0.4 * pillow(post, 5), wood(rng, (0.40, 0.24, 0.10), angle=np.pi / 2, rings=4), depth=40, spec=0.1), post)
    return c.image()
