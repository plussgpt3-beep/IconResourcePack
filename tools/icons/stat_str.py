"""ค่าสถานะ Strength (ตีแรง, อัปเกรดตัวละคร 2026-11-18): a heavy broadsword with an up badge."""
import numpy as np
from lib import Canvas, sword, badge


def draw():
    rng = np.random.default_rng(1201)
    c = Canvas()
    sword(c, rng, (96, 400), (380, 80), blade_w=44, guard_w=120, grip_len=0.24)
    badge(c, 'up')
    return c.image()
