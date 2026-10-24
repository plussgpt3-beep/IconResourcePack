"""โรงหมอ: an apothecary's hanging signboard on an iron bracket, a mortar and pestle painted on it."""
import numpy as np
from lib import N, Canvas, light, pillow, blur, poly, rect, wood, chrome, edge_darken, from_image
from _clinic import mortar, leaves


def draw():
    rng = np.random.default_rng(2509)
    c = Canvas()
    arm = blur(np.maximum(rect([40, 60, 470, 84], 8), poly([(420, 84), (470, 84), (470, 200)], width=14)), 1)
    curl = blur(poly([(60, 84), (110, 140), (170, 120), (190, 84)], width=12), 1)
    c.over(chrome(0.5 * pillow(np.maximum(arm, curl), 6), (0.22, 0.22, 0.24), depth=40, sky=0.6, ground=0.06), np.maximum(arm, curl))
    for x in (110, 400):
        chain = blur(rect([x - 6, 84, x + 6, 150], 4), 1)
        c.over(chrome(0.5 * pillow(chain, 4), (0.30, 0.30, 0.32), depth=30), chain)
    board = blur(rect([70, 146, 440, 470], 22), 1.2)
    c.over(light(0.35 * pillow(board, 18), wood(rng, (0.50, 0.30, 0.14), angle=0.0, rings=9), depth=50, spec=0.15)
           * edge_darken(board, 10, 0.4), board)
    frame = blur(np.clip(rect([70, 146, 440, 470], 22) - rect([96, 172, 414, 444], 14), 0, 1), 1)
    c.over(light(0.5 * pillow(frame, 6), wood(rng, (0.36, 0.20, 0.09), angle=np.pi / 2, rings=6), depth=40, spec=0.15), frame)
    leaves(c, rng, 160, 320, 0.7)
    mortar(c, rng, 280, 300, 0.55)
    return c.image()
