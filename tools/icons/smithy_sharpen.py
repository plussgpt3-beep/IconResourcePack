"""งานลับคม: a sword's edge held to a turning grindstone, a fan of sparks thrown off the wheel."""
import numpy as np
from lib import Canvas, sword
from _smithy import grindstone, sparks


def draw():
    rng = np.random.default_rng(2404)
    c = Canvas()
    grindstone(c, rng, 230, 250, 150)
    sword(c, rng, (490, 470), (250, 110), blade_w=24, guard_w=56)
    sparks(c, rng, 330, 260, n=18, spread=170)
    return c.image()
