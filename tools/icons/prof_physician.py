"""หมอ: a bronze guild shield with a stone mortar, its pestle, and a sprig of herbs."""
import numpy as np
from lib import Canvas
from _guild import shield, charge
from _clinic import mortar, leaves


def draw():
    rng = np.random.default_rng(2807)
    img = shield(rng, 'craft').image()
    m = Canvas()
    leaves(m, rng, 130, 220, 1.0)
    mortar(m, rng, 270, 230, 0.85)
    charge(img, m.image(), 256, 232, 0.80)
    return img
