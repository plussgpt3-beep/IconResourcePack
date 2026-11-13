"""แก่นบริสุทธิ์ (แดนนอก เขต 4, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4114)
    c = canvas(4)
    crystal(c, rng, (0.85, 0.75, 1.00))
    return c.image()
