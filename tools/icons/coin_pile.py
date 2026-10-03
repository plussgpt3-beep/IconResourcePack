"""เงินที่ให้: a heap of gold coins."""
import numpy as np
from lib import Canvas, gold_coin, coin_flat


def draw():
    c = Canvas()
    for (x, y) in ((140, 440), (250, 455), (360, 440), (190, 410), (310, 412), (250, 380), (150, 395), (360, 395)):
        gold_coin(c, x, y, 78, 26, 14)
    coin_flat(c, 200, 280, 72)
    coin_flat(c, 320, 300, 66)
    gold_coin(c, 256, 350, 78, 26, 14)
    return c.image()
