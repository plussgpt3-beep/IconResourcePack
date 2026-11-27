"""ไก่ตุ๋นโสม (หม้อปรุงอาหาร, 2026-11-27): a bowl of clear chicken broth with a whole ginseng root."""
import numpy as np
from lib import Canvas
from _dishes import specks, bowl, broth, roast, herb_root, steam


def draw():
    rng = np.random.default_rng(2706)
    c = Canvas()
    inner = bowl(c, rng, clay=(0.52, 0.66, 0.58))
    broth(c, rng, inner, (0.90, 0.80, 0.52), gloss=0.7)
    roast(c, rng, 220, 240, 90, 40, (0.95, 0.82, 0.60), bone=False)
    herb_root(c, rng, 330, 200, 0.8)
    specks(c, rng, inner, 16, (0.75, 0.15, 0.10), 2, 5)
    steam(c)
    return c.image()
