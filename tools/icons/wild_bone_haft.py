"""ด้ามกระดูก (แดนนอก เขต 2, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4107)
    c = canvas(2)
    haft(c, rng)
    return c.image()
