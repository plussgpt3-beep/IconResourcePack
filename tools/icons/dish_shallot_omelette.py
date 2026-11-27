"""ไข่เจียวหอมแดง (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from lib import ellipse
from _dishes import plate, omelette, shallot_rings, chili_ring, specks


def draw():
    rng = np.random.default_rng(2901)
    c = Canvas()
    plate(c, rng)
    omelette(c, rng, 256, 300, 170, 82)
    shallot_rings(c, rng, ellipse([150, 260, 360, 340]), 7)
    for (x, y) in ((220, 290), (310, 310)):
        chili_ring(c, rng, x, y, 9)
    specks(c, rng, ellipse([170, 250, 350, 340]), 10, (0.30, 0.55, 0.20), 3, 6)
    return c.image()
