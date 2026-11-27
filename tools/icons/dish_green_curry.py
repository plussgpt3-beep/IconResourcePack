"""แกงเขียวหวานไก่ (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from _clinic import leaves
from lib import N, blur, ellipse, noise, chrome, gold_tint, pillow
from _dishes import bowl, broth, chunk, chili_ring, steam


def draw():
    rng = np.random.default_rng(2906)
    c = Canvas()
    inner = bowl(c, rng, clay=(0.88, 0.86, 0.80))
    broth(c, rng, inner, (0.52, 0.66, 0.30))
    cream = blur(np.clip(noise(rng, 6, 2) - 0.5, 0, 1) * 3, 3) * inner
    c.over(np.zeros((N, N, 3)) + np.array([0.90, 0.92, 0.75]), np.clip(cream, 0, 1) * 0.5, cast=False)
    chunk(c, rng, 190, 248, 28, (0.92, 0.85, 0.70), 'cube')
    chunk(c, rng, 300, 240, 30, (0.92, 0.85, 0.70), 'cube')
    leaves(c, rng, 260, 250, 0.45, color=(0.20, 0.50, 0.18))
    for (x, y) in ((345, 258), (225, 268)):
        chili_ring(c, rng, x, y, 11)
    steam(c)
    return c.image()
