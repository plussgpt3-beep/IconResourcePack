"""งานซ่อม: a notched, cracked sword laid on the anvil, the hammer coming down on the crack."""
import numpy as np
from lib import Canvas, blur, poly, sword, N
from _smithy import anvil, hammer, sparks


def draw():
    rng = np.random.default_rng(2402)
    c = Canvas()
    anvil(c, 256, 320, 0.85)
    sword(c, rng, (40, 300), (470, 250), blade_w=24, guard_w=56)
    crack = blur(poly([(300, 256), (312, 270), (304, 280), (318, 296)], width=5), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.08, 0.08, 0.09]), crack, cast=False)
    hammer(c, rng, (440, 100), (330, 170), head_w=34, head_len=120)
    sparks(c, rng, 310, 262, n=12, spread=120)
    return c.image()
