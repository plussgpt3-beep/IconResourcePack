"""ยกเลิก: a red wax seal with a cross pressed into it."""
import numpy as np
from lib import Canvas, shadow, wax_seal, poly


def draw():
    rng = np.random.default_rng(12)
    c = Canvas()
    shadow(c, [80, 400, 440, 480], 0.4, 20)
    cross = np.maximum(poly([(190, 196), (322, 328)], width=34), poly([(322, 196), (190, 328)], width=34))
    wax_seal(c, rng, 256, 262, 190, (0.62, 0.10, 0.10), cross)
    return c.image()
