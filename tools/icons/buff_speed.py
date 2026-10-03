"""บัฟ ว่องไว: a white wing."""
import numpy as np
from _tools import *


def draw():
    f = wing
    return f(np.random.default_rng(672))
