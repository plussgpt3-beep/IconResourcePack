"""ช่างฝีมือ: a bronze guild shield with an anvil and a smith's hammer."""
import numpy as np
from lib import Canvas
from _guild import shield, charge
from _smithy import anvil, hammer


def draw():
    rng = np.random.default_rng(2805)
    img = shield(rng, 'craft').image()
    a = Canvas()
    anvil(a, 256, 270, 0.9)
    hammer(a, rng, (420, 250), (250, 90), head_w=36, head_len=110)
    charge(img, a.image(), 256, 226, 0.80)
    return img
