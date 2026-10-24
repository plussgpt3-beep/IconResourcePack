"""หลักเขตไม้: a squared post of stripped oak with a red band and an iron owner's plate, in a mound of turf."""
import numpy as np
from lib import Canvas
from _claims import turf, post


def draw():
    rng = np.random.default_rng(2440)
    c = Canvas()
    turf(c, rng, rx=150)
    post(c, rng)
    return c.image()
