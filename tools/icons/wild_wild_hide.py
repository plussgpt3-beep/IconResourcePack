"""หนังสัตว์ป่าดิบ (แดนนอก เขต 1, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4100)
    c = canvas(1)
    hide(c, rng, (0.55, 0.38, 0.22))
    return c.image()
