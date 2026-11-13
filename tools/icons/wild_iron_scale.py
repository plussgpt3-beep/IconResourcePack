"""เกล็ดเหล็ก (แดนนอก เขต 3, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4108)
    c = canvas(3)
    scales(c, rng, (0.55, 0.57, 0.62))
    return c.image()
