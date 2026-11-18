"""กระเป๋าเสริม Tier 2 เป้ผ้าใบเดินทาง (+18 ช่อง): a canvas backpack with a leather flap and straps, a bedroll on top."""
import numpy as np
from lib import Canvas, blur, poly, rect, leather_col, cloth
from _bag import part, strap, buckle


def draw():
    rng = np.random.default_rng(1102)
    c = Canvas()
    roll = blur(rect([96, 70, 416, 150], 40), 1.5)
    part(c, roll, cloth(rng, (0.42, 0.30, 0.22), weave=3.0), 0.35, 30, 50, 0.1)
    for x in (150, 362):
        strap(c, rng, (x, 62), (x, 158), 18)
    body = blur(rect([110, 140, 402, 460], 36), 1.5)
    part(c, body, cloth(rng, (0.74, 0.66, 0.48), weave=3.5), 0.3, 22, 60, 0.1)
    pocket = blur(rect([126, 330, 216, 440], 16), 1)
    part(c, pocket, cloth(rng, (0.66, 0.58, 0.42), weave=3.0), 0.3, 10, 40, 0.1)
    flap = blur(poly([(110, 150), (402, 150), (402, 290), (256, 320), (110, 290)]), 1.5)
    part(c, flap, leather_col(rng, (0.50, 0.30, 0.15)), 0.25, 12, 50, 0.25)
    for x in (196, 316):
        strap(c, rng, (x, 280), (x, 452), 22)
        buckle(c, x, 300, 18)
    return c.image()
