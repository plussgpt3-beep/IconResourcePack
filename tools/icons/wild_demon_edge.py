"""คมอสูร (แดนนอก เขต 4, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4115)
    c = canvas(4)
    blade(c, rng, steel_tint(), glow=(0.80, 0.30, 1.00))
    return c.image()
