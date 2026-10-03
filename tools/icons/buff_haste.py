"""บัฟ มือไว: a gold pickaxe."""
import numpy as np
from _tools import *


def draw():
    f = lambda r: pickaxe(r, (1.0, 0.76, 0.30))
    return f(np.random.default_rng(631))
