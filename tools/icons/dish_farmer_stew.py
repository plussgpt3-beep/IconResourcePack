"""สตูว์เนื้อชาวนา (หม้อปรุงอาหาร, 2026-11-27): a wooden bowl of brown beef stew with potato and carrot."""
import numpy as np
from lib import Canvas
from _dishes import specks, bowl, broth, chunk, carrot_coin, steam


def draw():
    rng = np.random.default_rng(2701)
    c = Canvas()
    inner = bowl(c, rng)
    broth(c, rng, inner, (0.45, 0.24, 0.10))
    chunk(c, rng, 170, 245, 30, (0.42, 0.20, 0.10), 'cube')
    chunk(c, rng, 300, 236, 28, (0.90, 0.80, 0.50), 'cube')
    chunk(c, rng, 350, 258, 26, (0.40, 0.19, 0.09), 'cube')
    carrot_coin(c, rng, 240, 262)
    carrot_coin(c, rng, 210, 225, 17)
    specks(c, rng, inner, 16, (0.30, 0.55, 0.20), 2, 5)
    steam(c)
    return c.image()
