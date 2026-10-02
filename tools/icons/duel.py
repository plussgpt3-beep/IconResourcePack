"""ดวล: two swords crossed, points up."""
import numpy as np
from lib import Canvas, sword


def draw():
    rng = np.random.default_rng(217)
    c = Canvas()
    sword(c, rng, (430, 440), (100, 70), blade_w=24, guard_w=60)
    sword(c, rng, (82, 440), (412, 70), blade_w=24, guard_w=60)
    return c.image()
