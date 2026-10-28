"""พ่อค้า: a bronze guild shield with a fat purse of coins."""
import numpy as np
from lib import load_icon
from _guild import shield, charge


def draw():
    rng = np.random.default_rng(2806)
    img = shield(rng, 'craft').image()
    charge(img, load_icon('treasury').draw(), 256, 238, 0.80)
    return img
