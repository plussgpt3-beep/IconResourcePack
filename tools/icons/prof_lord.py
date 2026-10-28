"""ขุนนาง: a purple guild shield with a gold coronet."""
import numpy as np
from lib import load_icon
from _guild import shield, charge


def draw():
    rng = np.random.default_rng(2808)
    img = shield(rng, 'noble').image()
    charge(img, load_icon('king').draw(), 256, 230, 0.80)
    return img
