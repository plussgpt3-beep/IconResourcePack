"""หมูอบแอปเปิล (หม้อปรุงอาหาร, 2026-11-27): a glazed roast pork on a plate beside a halved apple."""
import numpy as np
from lib import Canvas
from _dishes import plate, roast, apple, glaze_lines


def draw():
    rng = np.random.default_rng(2708)
    c = Canvas()
    plate(c, rng)
    roast(c, rng, 230, 305, 150, 92, (0.72, 0.36, 0.16), bone=False)
    glaze_lines(c, 230, 305, 150, 92)
    apple(c, rng, 380, 270, 50)
    apple(c, rng, 110, 330, 40)
    return c.image()
