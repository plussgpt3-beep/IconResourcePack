"""ขนมปังน้ำผึ้ง (หม้อปรุงอาหาร, 2026-11-27): a crusty loaf with golden honey running down it."""
import numpy as np
from lib import Canvas
from _dishes import loaf, drizzle


def draw():
    rng = np.random.default_rng(2704)
    c = Canvas()
    loaf(c, rng)
    drizzle(c, rng, 256, 205, 280)
    return c.image()
