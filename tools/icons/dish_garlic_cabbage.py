"""ผัดกะหล่ำกระเทียม (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from lib import N, blur, ellipse, noise, chrome, gold_tint, pillow
from _dishes import plate, greens, specks


def draw():
    rng = np.random.default_rng(2902)
    c = Canvas()
    plate(c, rng)
    greens(c, rng, 256, 300, 140, (0.62, 0.80, 0.42), 11)
    sauce = blur(ellipse([150, 260, 360, 350]), 6)
    c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.36, 0.14]), sauce * 0.25, cast=False)
    specks(c, rng, ellipse([150, 250, 360, 350]), 22, (0.95, 0.85, 0.55), 5, 9)
    specks(c, rng, ellipse([170, 260, 350, 340]), 6, (0.82, 0.10, 0.05), 4, 7)
    return c.image()
