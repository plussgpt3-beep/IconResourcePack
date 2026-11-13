"""แผ่นเกล็ด (แดนนอก เขต 3, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4110)
    c = canvas(3)
    plate(c, rng)
    return c.image()
