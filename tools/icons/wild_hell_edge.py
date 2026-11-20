"""คมมาร (แดนนอก เขต 5 แปรรูป, 2026-11-20)."""
import numpy as np
from _wild import canvas
from _abyss import *


def draw():
    c = canvas(5)
    edge(c, np.random.default_rng(5104))
    return c.image()
