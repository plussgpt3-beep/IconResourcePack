"""ม้า: a bay riding horse in profile, black mane and tail, saddled - the fastest, carries only its rider."""
import numpy as np
from lib import Canvas
from _animals import animal, saddle


def draw():
    rng = np.random.default_rng(2420)
    c = Canvas()
    animal(c, rng, (0.52, 0.30, 0.14), 'horse', mane=(0.10, 0.08, 0.07))
    saddle(c, rng)
    return c.image()
