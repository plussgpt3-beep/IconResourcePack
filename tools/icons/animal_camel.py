"""อูฐ: a tan camel with its hump, a saddle blanket over it."""
import numpy as np
from lib import Canvas
from _animals import animal, carpet


def draw():
    rng = np.random.default_rng(2424)
    c = Canvas()
    animal(c, rng, (0.76, 0.60, 0.38), 'camel')
    carpet(c, rng, (0.20, 0.35, 0.65), x0=250, x1=380, y=200)
    return c.image()
