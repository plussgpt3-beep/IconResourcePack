"""หนังฟอก (แดนนอก เขต 1, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4102)
    c = canvas(1)
    hide(c, rng, (0.62, 0.36, 0.16), rough=False)
    return c.image()
