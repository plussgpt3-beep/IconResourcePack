"""ตั้งค่าแรง: the smith's hammer with a gold coin - what the shop charges for its work."""
import numpy as np
from lib import Canvas, coin_flat
from _smithy import hammer


def draw():
    rng = np.random.default_rng(2407)
    c = Canvas()
    hammer(c, rng, (110, 460), (330, 150), head_w=44, head_len=170)
    coin_flat(c, 380, 390, 96)
    return c.image()
