"""ปลายลูกศรเขี้ยว (แดนนอก เขต 1, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4103)
    c = canvas(1)
    tip(c, rng)
    return c.image()
