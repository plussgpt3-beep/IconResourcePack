"""เจ้าของโรงเตี๊ยม: a green guild shield with a foaming oak tankard."""
import numpy as np
from _guild import shield, charge
from _tavern import tankard


def draw():
    rng = np.random.default_rng(2804)
    img = shield(rng, 'common').image()
    charge(img, tankard(rng), 262, 232, 0.80)
    return img
