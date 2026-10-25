"""ผ้าพันแผลชุบว่าน (หมอขั้น 1, 2026-10-25): a bandage roll steeped green in yarrow, a sprig of it tucked in."""
import numpy as np
from lib import N, Canvas, light, pillow, blur, ellipse
from _clinic import bandage, leaves


def draw():
    rng = np.random.default_rng(2608)
    c = Canvas()
    bandage(c, rng, 210, 250, 150, tint=(0.74, 0.84, 0.56))
    leaves(c, rng, 370, 160, 0.8, color=(0.30, 0.54, 0.22))
    for (x, y) in ((360, 70), (390, 62), (412, 84), (382, 92), (350, 96)):
        f = blur(ellipse([x - 16, y - 16, x + 16, y + 16]), 1)
        c.over(light(0.6 * pillow(f, 6), np.zeros((N, N, 3)) + np.array([0.96, 0.95, 0.90]), depth=40, spec=0.2), f)
    return c.image()
