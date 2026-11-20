"""ดวงใจเพลิง (ผลึกธาตุ fire เกรด 5, แดนนอก เขต 5, 2026-11-20)."""
import numpy as np
from _wild import canvas
from _elem import COL, GLOW
from _abyss import heart


def draw():
    c = canvas(5)
    heart(c, 'fire', np.random.default_rng(5105), COL['fire'], GLOW['fire'])
    return c.image()
