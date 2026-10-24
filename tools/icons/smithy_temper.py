"""งานชุบแข็ง: a red-hot blade plunged into a bucket of water, steam boiling up around it."""
import numpy as np
from lib import Canvas
from _smithy import bucket, blade, steam


def draw():
    rng = np.random.default_rng(2405)
    c = Canvas()
    blade(c, (420, 30), (230, 330), w=34, hot_from=0.3)
    bucket(c, 230, 300, 0.95)
    steam(c, rng, 170, 290, h=200, k=0.9)
    return c.image()
