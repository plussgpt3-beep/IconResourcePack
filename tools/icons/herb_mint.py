"""สะระแหน่ป่า (สมุนไพร, 2026-10-25): a sprig of bright wild mint."""
import numpy as np
from lib import Canvas
from _clinic import leaves


def draw():
    rng = np.random.default_rng(2601)
    c = Canvas()
    leaves(c, rng, 230, 300, 1.9, color=(0.34, 0.72, 0.30))
    leaves(c, rng, 300, 330, 1.3, color=(0.28, 0.62, 0.26))
    return c.image()
