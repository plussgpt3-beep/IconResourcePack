"""แกงแกะเครื่องเทศ (หม้อปรุงอาหาร, 2026-11-27): a dark clay bowl of red spiced mutton curry."""
import numpy as np
from lib import Canvas
from _dishes import specks, bowl, broth, chunk, steam
from _clinic import leaves


def draw():
    rng = np.random.default_rng(2711)
    c = Canvas()
    inner = bowl(c, rng, clay=(0.42, 0.22, 0.14))
    broth(c, rng, inner, (0.72, 0.18, 0.06), gloss=0.6)
    chunk(c, rng, 180, 242, 30, (0.46, 0.22, 0.12), 'cube')
    chunk(c, rng, 290, 228, 30, (0.50, 0.24, 0.12), 'cube')
    chunk(c, rng, 350, 255, 26, (0.44, 0.20, 0.10), 'cube')
    leaves(c, rng, 250, 250, 0.6, color=(0.30, 0.62, 0.26))
    specks(c, rng, inner, 16, (0.15, 0.08, 0.04), 2, 5)
    steam(c)
    return c.image()
