"""กระดูกแกร่ง (แดนนอก เขต 2, 2026-11-13)."""
import numpy as np
from lib import steel_tint
from _wild import *


def draw():
    rng = np.random.default_rng(4105)
    c = canvas(2)
    bone(c, rng, (150, 380), (370, 130), 46)
    return c.image()
