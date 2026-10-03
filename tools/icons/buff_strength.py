"""บัฟ พละกำลัง: a red draught."""
import numpy as np
from _tools import *


def draw():
    f = lambda r: potion(r, (0.80, 0.10, 0.08))
    return f(np.random.default_rng(728))
