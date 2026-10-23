"""ถังหมัก: an oak barrel with a brass tap, a drop of ale at the spout, bubbles of the ferment at the lid."""
import numpy as np
from lib import N, light, pillow, blur, ellipse, from_image
from _tavern import barrel


def draw():
    rng = np.random.default_rng(2305)
    c = from_image(barrel(rng, tap=True, liquid=(0.85, 0.55, 0.12)))
    bub = np.zeros((N, N), np.float32)
    for (x, y, r) in ((200, 66, 14), (236, 46, 10), (276, 60, 16), (312, 40, 9), (252, 22, 7)):
        bub = np.maximum(bub, np.clip(ellipse([x - r, y - r, x + r, y + r]) - ellipse([x - r + 4, y - r + 4, x + r - 4, y + r - 4]) * 0.6, 0, 1))
    c.over(np.zeros((N, N, 3)) + np.array([0.95, 0.88, 0.62]), blur(bub, 1), cast=False)
    return c.image()
