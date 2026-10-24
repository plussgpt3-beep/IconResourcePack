"""ลา: a grey donkey, long ears, a pack chest on its back."""
import numpy as np
from lib import Canvas
from _animals import animal, packs


def draw():
    rng = np.random.default_rng(2422)
    c = Canvas()
    animal(c, rng, (0.52, 0.49, 0.46), 'donkey')
    packs(c, rng, x=250, w=150)
    return c.image()
