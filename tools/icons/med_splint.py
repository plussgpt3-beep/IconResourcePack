"""เฝือก: two wooden slats bound together with three strips of linen."""
import numpy as np
from lib import Canvas
from _clinic import splint


def draw():
    c = Canvas()
    splint(c, np.random.default_rng(2502))
    return c.image()
