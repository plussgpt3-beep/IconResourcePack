"""ส่งยาตามใบสั่ง (2026-10-25): a flask of remedy handed in, gold coins paid for it."""
import numpy as np
from lib import Canvas, from_image, gold_coin, coin_flat
from _clinic import flask
from _tavern import place


def draw():
    rng = np.random.default_rng(2607)
    c = Canvas()
    for (x, y) in ((300, 450), (400, 440), (350, 420), (350, 390)):
        gold_coin(c, x, y, 64, 22, 12)
    coin_flat(c, 410, 330, 56)
    img = c.image()
    place(img, flask(rng, (0.90, 0.58, 0.14)), 180, 270, 0.78, 6)
    return from_image(img).image()
