"""ระดับราคา: a merchant's price tag - a card on a string, a coin marked on it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, ellipse, edge_darken, coin_flat


def draw():
    rng = np.random.default_rng(503)
    c = Canvas()
    tag = blur(np.clip(poly([(150, 90), (300, 60), (450, 300), (300, 450), (150, 300)]) - ellipse([190, 140, 230, 180]), 0, 1), 1.2)
    c.over(light(0.2 * pillow(tag, 10), parchment(rng, (0.88, 0.78, 0.55)), depth=40, spec=0.05) * edge_darken(tag, 10, 0.4), tag)
    eyelet = blur(np.clip(ellipse([182, 132, 238, 188]) - ellipse([192, 142, 228, 178]), 0, 1), 1)
    c.over(light(0.5 * pillow(eyelet, 3), np.zeros((N, N, 3)) + np.array([0.75, 0.60, 0.30]), depth=30, spec=0.6), eyelet)
    string = blur(poly([(210, 160), (150, 120), (90, 60), (60, 30)], width=6), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.70, 0.18, 0.12]), string)
    coin_flat(c, 300, 280, 80)
    return c.image()
