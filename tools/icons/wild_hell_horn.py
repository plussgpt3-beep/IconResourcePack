"""เขามาร (แดนนอก เขต 5 ของดิบ, 2026-11-20)."""
import numpy as np
from _wild import canvas
from _abyss import *


def draw():
    c = canvas(5)
    horn(c, np.random.default_rng(5103))
    return c.image()
