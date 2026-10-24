"""ร้านค้า: a merchant's shopfront - timber frame over a stone sill, a lit window of wares, a green
awning, and a hanging sign with a gold coin."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, stone, chrome, edge_darken, coin_flat


def draw():
    rng = np.random.default_rng(2410)
    c = Canvas()
    wall = blur(rect([70, 120, 420, 470], 6), 1.2)
    c.over(light(0.15 * pillow(wall, 10), np.zeros((N, N, 3)) + np.array([0.86, 0.80, 0.66]), depth=30, spec=0.05) * edge_darken(wall, 8, 0.3), wall)
    for box in ([70, 120, 92, 470], [398, 120, 420, 470], [70, 120, 420, 140], [70, 300, 420, 318]):
        beam = blur(rect(box, 3), 1)
        c.over(light(0.4 * pillow(beam, 5), wood(rng, (0.36, 0.20, 0.09), angle=np.pi / 2 if box[2] - box[0] < 40 else 0, rings=5), depth=30, spec=0.15), beam)
    sill = blur(rect([60, 420, 430, 470], 6), 1)
    c.over(light(0.3 * pillow(sill, 8), stone(rng), depth=40, spec=0.1) * edge_darken(sill, 6, 0.3), sill)
    win = blur(rect([120, 330, 370, 418], 4), 1)
    c.over(light(0.1 * win, np.zeros((N, N, 3)) + np.array([0.95, 0.78, 0.40]), depth=10, ambient=0.9, spec=0.1), win)
    for k, (x, col) in enumerate(((160, (0.80, 0.55, 0.20)), (215, (0.70, 0.72, 0.78)), (270, (0.35, 0.60, 0.20)), (325, (0.75, 0.20, 0.15)))):
        g = blur(ellipse([x - 22, 365, x + 22, 410]), 1)
        c.over(light(pillow(g, 10, 0.6), np.zeros((N, N, 3)) + np.array(col), depth=40, spec=0.5), g)
    mull = blur(np.maximum(rect([241, 330, 249, 418]), rect([120, 370, 370, 376])), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.17, 0.07]), mull, cast=False)
    aw = blur(poly([(50, 250), (440, 250), (470, 312), (20, 312)]), 1.2)
    stripes = ((xx // 40) % 2 == 0)
    col = np.where(stripes[..., None], np.array([0.15, 0.45, 0.20]), np.array([0.90, 0.88, 0.78]))
    c.over(light(0.25 * pillow(aw, 10), cloth(rng, (1.0, 1.0, 1.0)) * col, depth=40, spec=0.1) * edge_darken(aw, 6, 0.3), aw)
    arm = blur(np.maximum(rect([300, 60, 500, 76], 4), poly([(470, 76), (500, 76), (500, 130)], width=10)), 1)
    c.over(chrome(0.5 * pillow(arm, 5), (0.22, 0.22, 0.24), depth=30, sky=0.6, ground=0.06), arm)
    board = blur(rect([330, 96, 470, 210], 10), 1)
    c.over(light(0.3 * pillow(board, 10), wood(rng, (0.50, 0.30, 0.14), rings=8), depth=40, spec=0.15) * edge_darken(board, 6, 0.4), board)
    coin_flat(c, 400, 153, 38)
    return c.image()
