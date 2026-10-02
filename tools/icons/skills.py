"""ทักษะ: a knight's sword, point up to the right."""
import numpy as np
from lib import Canvas, sword


def draw():
    rng = np.random.default_rng(201)
    c = Canvas()
    sword(c, rng, (110, 430), (430, 70), blade_w=30, guard_w=74)
    return c.image()
