"""เจ้าที่ดิน: a green guild shield with a staked and roped land plot."""
import numpy as np
from lib import load_icon
from _guild import shield, charge


def draw():
    rng = np.random.default_rng(2802)
    img = shield(rng, 'common').image()
    charge(img, load_icon('plot_bounds').draw(), 256, 240, 0.80)
    return img
