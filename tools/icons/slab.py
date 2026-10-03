"""A cut stone slab, seen from above at an angle: the base of the floor / ceiling buttons."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, stone, edge_darken


def draw():
    rng = np.random.default_rng(408)
    c = Canvas()
    top = blur(poly([(60, 230), (256, 130), (452, 230), (256, 330)]), 1.2)
    c.over(light(0.2 * pillow(top, 10), stone(rng, (0.68, 0.64, 0.58)), depth=30, spec=0.1) * edge_darken(top, 6, 0.2), top)
    left = blur(poly([(60, 230), (256, 330), (256, 420), (60, 320)]), 1)
    c.over(stone(rng, (0.48, 0.45, 0.40)), left)
    right = blur(poly([(256, 330), (452, 230), (452, 320), (256, 420)]), 1)
    c.over(stone(rng, (0.34, 0.32, 0.29)), right)
    return c.image()
