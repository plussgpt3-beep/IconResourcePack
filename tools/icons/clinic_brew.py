"""ปรุงยา: a stone mortar with its wooden pestle, a sprig of green herbs beside it."""
import numpy as np
from lib import Canvas
from _clinic import mortar, leaves


def draw():
    rng = np.random.default_rng(2506)
    c = Canvas()
    leaves(c, rng, 110, 230, 1.1)
    mortar(c, rng, 280, 240, 0.95)
    return c.image()
