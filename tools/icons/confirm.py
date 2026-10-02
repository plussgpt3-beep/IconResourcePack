"""ยืนยัน: a green wax seal with a tick pressed into it."""
import numpy as np
from lib import Canvas, shadow, wax_seal, poly


def draw():
    rng = np.random.default_rng(11)
    c = Canvas()
    shadow(c, [80, 400, 440, 480], 0.4, 20)
    tick = poly([(170, 262), (230, 322), (345, 195)], width=34)
    wax_seal(c, rng, 256, 262, 190, (0.20, 0.55, 0.22), tick)
    return c.image()
