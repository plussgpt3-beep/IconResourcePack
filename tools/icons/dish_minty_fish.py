"""ปลาย่างสะระแหน่ (หม้อปรุงอาหาร, 2026-11-27): a grilled fish on a plate with a sprig of mint."""
import numpy as np
from lib import Canvas
from _dishes import plate, fish
from _clinic import leaves


def draw():
    rng = np.random.default_rng(2702)
    c = Canvas()
    plate(c, rng)
    fish(c, rng, 250, 310, 330, 120, (0.82, 0.58, 0.30))
    leaves(c, rng, 360, 250, 0.9, color=(0.34, 0.72, 0.30))
    return c.image()
