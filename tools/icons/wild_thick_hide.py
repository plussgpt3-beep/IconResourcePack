"""หนังหนา (แดนนอก เขต 2, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4104)
    c = canvas(2)
    hide(c, rng, (0.30, 0.22, 0.16))
    return c.image()
