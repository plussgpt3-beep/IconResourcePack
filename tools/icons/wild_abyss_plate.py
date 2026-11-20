"""แผ่นเกราะอเวจี (แดนนอก เขต 5 แปรรูป, 2026-11-20)."""
import numpy as np
from _wild import canvas
from _abyss import *


def draw():
    c = canvas(5)
    plate(c, np.random.default_rng(5102))
    return c.image()
