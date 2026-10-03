"""ของรอรับ: a nailed-shut wooden crate of goods."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, wood, edge_darken


def draw():
    rng = np.random.default_rng(510)
    c = Canvas()
    front = blur(poly([(70, 200), (300, 240), (300, 470), (70, 420)]), 1)
    side = blur(poly([(300, 240), (450, 190), (450, 410), (300, 470)]), 1)
    top = blur(poly([(70, 200), (220, 150), (450, 190), (300, 240)]), 1)
    for m, base, ang, k in ((front, (0.60, 0.42, 0.22), 0.17, 1.0), (side, (0.60, 0.42, 0.22), -0.32, 0.72), (top, (0.66, 0.48, 0.26), 0.2, 1.15)):
        col = wood(rng, base, angle=ang, rings=10) * k
        c.over(light(0.1 * pillow(m, 6), col, depth=30, spec=0.1) * edge_darken(m, 6, 0.35), m)
    for pts in ([(80, 215), (290, 455)], [(80, 405), (290, 255)]):
        br = blur(poly(pts, width=22), 1) * front
        c.over(light(0.3 * pillow(br, 5), wood(rng, (0.50, 0.32, 0.16), angle=0.8, rings=5), depth=30, spec=0.1), br)
    for pts in ([(310, 250), (440, 400)], [(310, 455), (440, 205)]):
        br = blur(poly(pts, width=20), 1) * side
        c.over(light(0.3 * pillow(br, 5), wood(rng, (0.50, 0.32, 0.16), angle=-0.8, rings=5) * 0.72, depth=30, spec=0.1), br)
    return c.image()
