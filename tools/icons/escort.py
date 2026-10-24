"""คุ้มกันคาราวาน: a soldier's blue heater shield bearing a gold cart wheel, a spear behind it."""
import numpy as np
from lib import Canvas
from _escort import spear, shield


def draw():
    rng = np.random.default_rng(2460)
    c = Canvas()
    spear(c, rng, (90, 470), (440, 40))
    shield(c, rng)
    return c.image()
