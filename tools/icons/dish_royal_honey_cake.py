"""เค้กน้ำผึ้งหลวง (หม้อปรุงอาหาร, 2026-11-27): a three-layer honey cake dripping glaze, a gold crown on top."""
import numpy as np
from lib import Canvas
from _dishes import cake, crown


def draw():
    rng = np.random.default_rng(2712)
    c = Canvas()
    top = cake(c, rng)
    crown(c, 256, top - 40, 1.2)
    return c.image()
