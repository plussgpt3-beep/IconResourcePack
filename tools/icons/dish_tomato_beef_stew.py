"""สตูว์มะเขือเทศเนื้อ (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from _dishes import bowl, broth, chunk, tomato_slice, carrot_coin, specks, steam


def draw():
    rng = np.random.default_rng(2908)
    c = Canvas()
    inner = bowl(c, rng)
    broth(c, rng, inner, (0.70, 0.16, 0.08))
    chunk(c, rng, 180, 245, 32, (0.40, 0.18, 0.09), 'cube')
    chunk(c, rng, 300, 236, 30, (0.42, 0.19, 0.10), 'cube')
    chunk(c, rng, 350, 262, 24, (0.40, 0.18, 0.09), 'cube')
    tomato_slice(c, rng, 245, 262, 30)
    carrot_coin(c, rng, 215, 225, 16)
    specks(c, rng, inner, 16, (0.30, 0.55, 0.20), 2, 5)
    steam(c)
    return c.image()
