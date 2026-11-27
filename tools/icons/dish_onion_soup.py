"""ซุปหัวหอม (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from _dishes import bowl, broth, shallot_rings, specks, steam


def draw():
    rng = np.random.default_rng(2904)
    c = Canvas()
    inner = bowl(c, rng)
    broth(c, rng, inner, (0.74, 0.48, 0.18))
    shallot_rings(c, rng, inner, 9)
    specks(c, rng, inner, 14, (0.30, 0.55, 0.20), 2, 5)
    steam(c)
    return c.image()
