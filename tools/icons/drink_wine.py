"""ไวน์: a dark green wine bottle, wax-sealed cork, a paper label with a bunch of grapes."""
import numpy as np
from _tavern import bottle


def draw():
    return bottle(np.random.default_rng(2303))
