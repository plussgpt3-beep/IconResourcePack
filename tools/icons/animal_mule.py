"""ล่อ: a brown mule, long ears, two pack chests slung over its back."""
import numpy as np
from lib import Canvas
from _animals import animal, packs


def draw():
    rng = np.random.default_rng(2421)
    c = Canvas()
    animal(c, rng, (0.40, 0.27, 0.17), 'mule', mane=(0.18, 0.12, 0.08))
    packs(c, rng)
    return c.image()
