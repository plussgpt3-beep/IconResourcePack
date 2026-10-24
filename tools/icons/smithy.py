"""ร้านตีเหล็ก: an anvil with a red-hot bar on its face, the smith's hammer raised over it, sparks flying."""
import numpy as np
from lib import Canvas, blur, rect
from _smithy import anvil, hammer, sparks, hot


def draw():
    rng = np.random.default_rng(2401)
    c = Canvas()
    anvil(c, 236, 280, 0.95)
    bar = blur(rect([150, 252, 330, 278], 10), 1.2)
    hot(c, bar)
    hammer(c, rng, (470, 250), (330, 90), head_w=36, head_len=130)
    sparks(c, rng, 290, 250, n=16, spread=150)
    return c.image()
