"""รากโสม (สมุนไพร, 2026-10-25): a forked pale ginseng root, a sprig and its red berries on top."""
import numpy as np
from lib import N, yy, Canvas, light, pillow, blur, poly, ellipse, noise
from _clinic import leaves


def draw():
    rng = np.random.default_rng(2603)
    c = Canvas()
    leaves(c, rng, 250, 130, 0.8, color=(0.30, 0.55, 0.22))
    for (x, y) in ((290, 70), (306, 88), (284, 94), (300, 106)):
        b = blur(ellipse([x - 13, y - 13, x + 13, y + 13]), 1)
        c.over(light(0.7 * pillow(b, 8), np.zeros((N, N, 3)) + np.array([0.82, 0.10, 0.10]), depth=50, spec=0.5, gloss=30), b)
    body = np.maximum(ellipse([200, 170, 312, 330]), ellipse([212, 270, 300, 372]))
    leg1 = poly([(240, 350), (222, 410), (196, 466)], width=40)
    leg2 = poly([(274, 350), (300, 410), (322, 462)], width=36)
    hairs = np.maximum(poly([(206, 300), (160, 330)], width=8), poly([(306, 260), (350, 300)], width=8))
    root = blur(np.maximum.reduce([body, leg1, leg2, hairs]), 6)
    rings = 0.88 + 0.12 * np.abs(np.sin(yy / 9.0))
    col = np.array([0.88, 0.76, 0.54])[None, None, :] * (rings * (0.9 + 0.1 * noise(rng, 18, 2)))[..., None]
    c.over(light(0.55 * pillow(root, 30), np.clip(col, 0, 1), depth=50, spec=0.15), root)
    return c.image()
