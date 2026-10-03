"""สกิล Active: a burning orb."""
import numpy as np
from _tools import *


def draw():
    f = flame_orb
    return f(np.random.default_rng(66))
