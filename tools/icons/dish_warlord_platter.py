"""สำรับขุนศึก (หม้อปรุงอาหาร, 2026-11-27): a board heaped with a roast on the bone, a loaf and an apple."""
import numpy as np
from lib import Canvas
from _dishes import board, roast, loaf, apple


def draw():
    rng = np.random.default_rng(2710)
    c = Canvas()
    board(c, rng)
    loaf(c, rng, 330, 300, 110, 66)
    apple(c, rng, 150, 300, 48)
    roast(c, rng, 220, 330, 120, 80, (0.50, 0.22, 0.10), bone=True)
    return c.image()
