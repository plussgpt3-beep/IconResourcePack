"""enchant (ตีบวก): a glowing enchanted book."""
import numpy as np
from _tools import *


def draw():
    f = enchanted_book
    return f(np.random.default_rng(28))
