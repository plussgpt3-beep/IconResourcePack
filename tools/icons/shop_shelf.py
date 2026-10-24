"""ชั้นวางสินค้า: a merchant's wooden shelf, two boards stocked with bread, iron ingots, jars and cloth."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, rect, ellipse, poly, wood, cloth, chrome, edge_darken


def draw():
    rng = np.random.default_rng(2411)
    c = Canvas()
    back = blur(rect([70, 60, 442, 470], 8), 1.2)
    c.over(light(0.2 * pillow(back, 10), wood(rng, (0.36, 0.21, 0.10), angle=np.pi / 2, rings=7), depth=30, spec=0.1) * edge_darken(back, 10, 0.4), back)
    for y in (220, 380):
        # goods on this board
        if y == 220:
            loaf = blur(ellipse([100, 150, 200, 222]), 1)
            c.over(light(pillow(loaf, 14, 0.6), np.zeros((N, N, 3)) + np.array([0.78, 0.52, 0.22]), depth=40, spec=0.3), loaf)
            for k in range(3):
                bar = blur(poly([(230 + k * 6, 222 - k * 24), (330 + k * 6, 222 - k * 24), (318 + k * 6, 200 - k * 24), (242 + k * 6, 200 - k * 24)]), 1)
                c.over(chrome(0.5 * pillow(bar, 5) + 0.1, (0.74, 0.75, 0.80), depth=30, sky=1.0, ground=0.2), bar)
            jar = blur(np.maximum(rect([350, 140, 410, 222], 14), rect([360, 124, 400, 146], 4)), 1)
            c.over(light(0.5 * pillow(jar, 12), np.zeros((N, N, 3)) + np.array([0.62, 0.34, 0.18]), depth=40, spec=0.4), jar)
        else:
            for k, col in enumerate(((0.70, 0.15, 0.15), (0.20, 0.35, 0.65), (0.85, 0.75, 0.30))):
                bolt = blur(rect([100 + k * 80, 300, 170 + k * 80, 382], 10), 1)
                c.over(light(0.5 * pillow(bolt, 12), cloth(rng, col), depth=40, spec=0.15), bolt)
            pot = blur(ellipse([350, 300, 420, 382]), 1)
            c.over(light(pillow(pot, 14, 0.6), np.zeros((N, N, 3)) + np.array([0.20, 0.45, 0.30]), depth=40, spec=0.6, gloss=40), pot)
        board = blur(rect([60, y, 452, y + 22], 4), 1)
        c.over(light(0.4 * pillow(board, 6), wood(rng, (0.56, 0.36, 0.18), rings=10), depth=40, spec=0.2), board)
    for x in (60, 430):
        side = blur(rect([x, 50, x + 22, 480], 4), 1)
        c.over(light(0.4 * pillow(side, 6), wood(rng, (0.46, 0.28, 0.12), angle=np.pi / 2, rings=5), depth=40, spec=0.2), side)
    return c.image()
