"""พายเบอร์รี (หม้อปรุงอาหาร, 2026-11-27): a lattice-topped pie of red sweet berries."""
import numpy as np
from lib import Canvas
from _dishes import pie


def draw():
    rng = np.random.default_rng(2703)
    c = Canvas()
    pie(c, rng, filling=(0.62, 0.05, 0.16))
    return c.image()
