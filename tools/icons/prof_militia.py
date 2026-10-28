"""ทหาร: a green guild shield with two swords crossed."""
import numpy as np
from lib import Canvas, sword
from _guild import shield, charge


def draw():
    rng = np.random.default_rng(2803)
    img = shield(rng, 'common').image()
    s = Canvas()
    sword(s, rng, (110, 440), (420, 90), blade_w=24, guard_w=64)
    sword(s, rng, (402, 440), (92, 90), blade_w=24, guard_w=64)
    charge(img, s.image(), 256, 238, 0.80)
    return img
