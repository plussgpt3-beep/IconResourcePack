"""ดวงใจอสรพิษ (ผลึกธาตุ venom เกรด 5, แดนนอก เขต 5, 2026-11-20)."""
import numpy as np
from _wild import canvas
from _elem import COL, GLOW
from _abyss import heart


def draw():
    c = canvas(5)
    heart(c, 'venom', np.random.default_rng(5108), COL['venom'], GLOW['venom'])
    return c.image()
