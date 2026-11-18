"""ค่าสถานะ Attack Speed (ตีไว, อัปเกรดตัวละคร 2026-11-18): two crossed light swords with an up badge."""
import numpy as np
from lib import Canvas, sword, badge


def draw():
    rng = np.random.default_rng(1202)
    c = Canvas()
    sword(c, rng, (90, 380), (360, 70), blade_w=24, guard_w=80, grip_len=0.22)
    sword(c, rng, (380, 380), (100, 70), blade_w=24, guard_w=80, grip_len=0.22)
    badge(c, 'up')
    return c.image()
