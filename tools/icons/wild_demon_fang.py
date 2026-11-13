"""เขี้ยวอสูร (แดนนอก เขต 4, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4113)
    c = canvas(4)
    fang(c, rng, 220, 100, 300, 440, 70, color=(0.30, 0.10, 0.18))
    fang(c, rng, 340, 140, 370, 360, 36, color=(0.40, 0.14, 0.24))
    return c.image()
