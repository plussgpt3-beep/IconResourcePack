"""หลักเขตหิน: a round-topped boundary stone with a chiselled cross, in a mound of turf."""
import numpy as np
from lib import Canvas
from _claims import turf, marker


def draw():
    rng = np.random.default_rng(2441)
    c = Canvas()
    turf(c, rng)
    marker(c, rng)
    return c.image()
