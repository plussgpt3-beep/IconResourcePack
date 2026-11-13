"""แก่นต้องสาป (แดนนอก เขต 4, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4112)
    c = canvas(4)
    crystal(c, rng, (0.35, 0.12, 0.50), dark=True)
    return c.image()
