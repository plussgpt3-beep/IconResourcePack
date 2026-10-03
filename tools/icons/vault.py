"""กล่องคลังหลวง: the royal strongbox - an oak chest bound in iron, a gold lock plate on the front."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, gold_tint, edge_darken


def draw():
    rng = np.random.default_rng(501)
    c = Canvas()
    body = blur(rect([60, 230, 452, 470], 12), 1.2)
    planks = sum(np.exp(-((yy - y) / 2.5) ** 2) for y in (310, 390))
    c.over(light(0.25 * pillow(body, 12) - 0.12 * planks * body, wood(rng, (0.40, 0.22, 0.10), rings=12), depth=40, spec=0.15) * edge_darken(body, 12, 0.45), body)
    lid = blur(np.maximum(rect([60, 150, 452, 240], 12), ellipse([60, 90, 452, 220]) * (yy > 120)), 1.2)
    ny = np.clip((yy - 90) / 150, 0, 1)
    c.over(light(0.35 * pillow(lid, 20), wood(rng, (0.46, 0.26, 0.12), rings=10), depth=50, spec=0.2) * edge_darken(lid, 10, 0.4), lid)
    iron = (0.30, 0.30, 0.33)
    for x in (100, 412):
        st = blur(rect([x - 20, 100, x + 20, 470], 6), 1)
        c.over(chrome(0.4 * pillow(st, 6), iron, depth=40, sky=0.7, ground=0.08), st)
    for y in (236, 462):
        st = blur(rect([60, y - 12, 452, y + 12], 6), 1)
        c.over(chrome(0.4 * pillow(st, 6), iron, depth=40, sky=0.7, ground=0.08), st)
    plate = blur(rect([206, 230, 306, 330], 12), 1)
    c.over(chrome(0.5 * pillow(plate, 10), gold_tint(), depth=40), plate)
    hole = blur(np.maximum(ellipse([244, 254, 268, 278]), poly([(250, 272), (262, 272), (266, 306), (246, 306)])), 1)
    c.over(np.zeros((N, N, 3)) + 0.05, hole)
    return c.image()
