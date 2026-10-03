"""บัฟ ทนทาน: a shield."""
import numpy as np
from _tools import *


def draw():
    f = kite_shield
    return f(np.random.default_rng(764))
