"""สกิล Passive: a glowing rune tome."""
import numpy as np
from _tools import *


def draw():
    f = rune_tome
    return f(np.random.default_rng(89))
