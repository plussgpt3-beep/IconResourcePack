"""สลัดมะเขือเทศ (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from _dishes import bowl, greens, tomato_slice, specks


def draw():
    rng = np.random.default_rng(2903)
    c = Canvas()
    inner = bowl(c, rng, clay=(0.86, 0.84, 0.78))
    greens(c, rng, 256, 250, 140, (0.45, 0.72, 0.30), 9)
    for (x, y, r) in ((190, 240, 44), (300, 230, 46), (250, 270, 42), (340, 262, 36)):
        tomato_slice(c, rng, x, y, r)
    specks(c, rng, inner, 10, (0.95, 0.92, 0.80), 3, 6)
    return c.image()
