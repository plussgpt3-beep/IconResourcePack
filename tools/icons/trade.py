"""แลกของกับผู้เล่น: two goods crossing hands - a sack and a crate with exchange arrows."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, edge_darken, noise


def draw():
    rng = np.random.default_rng(216)
    c = Canvas()
    # crate (right)
    crate = blur(rect([250, 250, 440, 440], 6), 1)
    planks = sum(np.exp(-((yy - y) / 2.0) ** 2) for y in (312, 376))
    h = 0.2 * pillow(crate, 8) - 0.2 * planks * crate
    col = wood(rng, (0.56, 0.38, 0.20), rings=14)
    c.over(light(h, col, depth=40, spec=0.1) * edge_darken(crate, 10, 0.4), crate)
    for pts in ([(262, 262), (428, 428)], [(262, 428), (428, 262)]):
        br = blur(poly(pts, width=22), 1) * crate
        c.over(light(pillow(br, 5) * 0.5 + h * 0.5, wood(rng, (0.48, 0.30, 0.15), angle=0.785, rings=6), depth=40, spec=0.15), br)
    # sack (left)
    sack = blur(np.maximum(ellipse([60, 230, 250, 450]), poly([(110, 250), (200, 250), (182, 200), (128, 200)])), 1.5)
    nx = (xx - 155) / 95; ny = (yy - 345) / 110
    h2 = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * sack + 0.1 * pillow(sack, 6)
    c.over(light(h2, cloth(rng, (0.62, 0.50, 0.32), weave=2.5), depth=70, spec=0.05), sack)
    tie = blur(rect([120, 214, 190, 230], 6), 1)
    c.over(light(pillow(tie, 4) * 0.5, np.zeros((N, N, 3)) + np.array([0.40, 0.28, 0.14]), depth=20, spec=0.1), tie)
    # exchange arrows over the top
    for (y, s) in ((90, 1), (150, -1)):
        x0, x1 = (110, 400) if s > 0 else (400, 110)
        shaft = poly([(x0, y), (x1 - s * 40, y)], width=22)
        head = poly([(x1, y), (x1 - s * 50, y - 32), (x1 - s * 50, y + 32)])
        ar = blur(np.clip(shaft + head, 0, 1), 1.2)
        col = np.zeros((N, N, 3)) + (np.array([0.28, 0.62, 0.22]) if s > 0 else np.array([0.80, 0.55, 0.12]))
        c.over(light(pillow(ar, 7) * 0.7, col, depth=40, spec=0.4), ar)
    return c.image()
