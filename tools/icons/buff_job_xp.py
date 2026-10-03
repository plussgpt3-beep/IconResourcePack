"""บัฟ Job XP: a bottle of green sparks."""
import numpy as np
from _tools import *


def draw():
    f = xp_bottle
    return f(np.random.default_rng(371))
