"""ต้มยำปลา (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from _dishes import bowl, broth, chunk, mushroom, lemongrass_bits, chili_ring, specks, steam


def draw():
    rng = np.random.default_rng(2905)
    c = Canvas()
    inner = bowl(c, rng, clay=(0.30, 0.28, 0.26))
    broth(c, rng, inner, (0.86, 0.34, 0.10))
    chunk(c, rng, 190, 245, 30, (0.95, 0.92, 0.84), 'round')
    chunk(c, rng, 310, 240, 28, (0.95, 0.92, 0.84), 'round')
    mushroom(c, rng, 255, 262, 22)
    lemongrass_bits(c, rng, inner, 5)
    for (x, y) in ((230, 230), (350, 262), (160, 262)):
        chili_ring(c, rng, x, y, 11)
    specks(c, rng, inner, 12, (0.30, 0.60, 0.22), 3, 6)
    steam(c)
    return c.image()
