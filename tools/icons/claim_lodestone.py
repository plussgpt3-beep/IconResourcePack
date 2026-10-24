"""ศิลาจารึกเขต: a tall dark stele with a gold compass rose and gold-inlaid inscription, in a mound of turf."""
import numpy as np
from lib import Canvas
from _claims import turf, stele


def draw():
    rng = np.random.default_rng(2442)
    c = Canvas()
    turf(c, rng, rx=180)
    stele(c, rng)
    return c.image()
