"""เขี้ยวสัตว์ป่า (แดนนอก เขต 1, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4101)
    c = canvas(1)
    fang(c, rng, 200, 120, 320, 420, 60)
    fang(c, rng, 330, 160, 380, 380, 34)
    return c.image()
