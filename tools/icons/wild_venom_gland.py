"""ต่อมพิษ (แดนนอก เขต 3, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4109)
    c = canvas(3)
    gland(c, rng, (0.45, 0.70, 0.20))
    return c.image()
