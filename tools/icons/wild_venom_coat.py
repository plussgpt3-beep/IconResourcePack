"""น้ำยาเคลือบ (แดนนอก เขต 3, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4111)
    c = canvas(3)
    flask(c, rng, (0.40, 0.80, 0.25))
    return c.image()
