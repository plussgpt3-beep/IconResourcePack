"""ผ้าพันแผล: a rolled linen bandage with a loose tail unwound."""
import numpy as np
from lib import Canvas
from _clinic import bandage


def draw():
    c = Canvas()
    bandage(c, np.random.default_rng(2501), 210, 210, 150)
    return c.image()
