"""ลามะ: a cream llama in a woven carpet with a pack chest - the caravan animal."""
import numpy as np
from lib import Canvas
from _animals import animal, carpet, packs


def draw():
    rng = np.random.default_rng(2423)
    c = Canvas()
    animal(c, rng, (0.86, 0.80, 0.66), 'llama')
    carpet(c, rng, (0.70, 0.15, 0.12))
    packs(c, rng, x=230, y=215, w=170)
    return c.image()
