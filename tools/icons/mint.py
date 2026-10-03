"""โรงกษาปณ์: the mint - a coining die on its anvil block, freshly struck coins around it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, gold_coin, coin_flat


def draw():
    rng = np.random.default_rng(504)
    c = Canvas()
    stump = blur(np.maximum(rect([130, 330, 382, 470]), ellipse([130, 440, 382, 490])), 1.2)
    nx = (xx - 256) / 126
    c.over(light(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * stump * 0.7, wood(rng, (0.40, 0.24, 0.12), angle=np.pi / 2, rings=8), depth=50, spec=0.15), stump)
    top = blur(ellipse([130, 300, 382, 360]), 1)
    rr = np.hypot((xx - 256) / 126, (yy - 330) / 30)
    rings_ = 0.8 + 0.2 * np.sin(rr * 30)
    c.over(np.array([0.62, 0.46, 0.28])[None, None, :] * rings_[..., None], top)
    die = blur(rect([206, 90, 306, 320], 14), 1)
    c.over(chrome(np.sqrt(np.clip(1 - ((xx - 256) / 50) ** 2, 0, 1)) * die * 0.8, (0.50, 0.52, 0.56), depth=50, sky=0.8, ground=0.1), die)
    cap = blur(ellipse([196, 70, 316, 120]), 1)
    c.over(chrome(0.5 * pillow(cap, 8), (0.60, 0.62, 0.66), depth=40, sky=0.85, ground=0.1), cap)
    for (x, y, r) in ((110, 420, 46), (400, 410, 50)):
        gold_coin(c, x, y, r, r * 0.33, 10)
    coin_flat(c, 410, 300, 48)
    return c.image()
