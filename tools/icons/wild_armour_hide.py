"""หนังเสริมเกราะ (แดนนอก เขต 2, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4106)
    c = canvas(2)
    hide(c, rng, (0.45, 0.25, 0.12), rough=False)
    scales(c, rng, (0.70, 0.72, 0.76))
    return c.image()
