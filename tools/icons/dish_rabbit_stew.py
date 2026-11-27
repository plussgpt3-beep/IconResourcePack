"""สตูว์กระต่ายป่า (หม้อปรุงอาหาร, 2026-11-27): a clay bowl of pale rabbit stew with mushroom and carrot."""
import numpy as np
from lib import Canvas
from _dishes import specks, bowl, broth, chunk, carrot_coin, mushroom, steam


def draw():
    rng = np.random.default_rng(2705)
    c = Canvas()
    inner = bowl(c, rng, clay=(0.62, 0.36, 0.24))
    broth(c, rng, inner, (0.78, 0.58, 0.32))
    chunk(c, rng, 175, 240, 28, (0.75, 0.52, 0.36), 'round')
    mushroom(c, rng, 300, 222)
    carrot_coin(c, rng, 230, 262)
    chunk(c, rng, 345, 258, 22, (0.90, 0.80, 0.50), 'cube')
    specks(c, rng, inner, 16, (0.30, 0.55, 0.20), 2, 5)
    steam(c)
    return c.image()
