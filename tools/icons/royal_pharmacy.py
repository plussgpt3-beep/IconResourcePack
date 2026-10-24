"""คลังยาหลวง (2026-10-25): the crown's crate of remedies, three flasks in it and a gold seal on its front."""
import numpy as np
from lib import N, Canvas, light, pillow, blur, rect, wood, edge_darken, yy, from_image, coin_flat
from _clinic import flask
from _tavern import place


def draw():
    rng = np.random.default_rng(2605)
    c = Canvas()
    back = blur(rect([60, 200, 452, 340], 10), 1)
    c.over(light(0.3 * pillow(back, 10), wood(rng, (0.30, 0.17, 0.08), rings=6), depth=40, spec=0.1), back)
    img = c.image()
    place(img, flask(rng, (0.90, 0.58, 0.14)), 150, 230, 0.52, 8)
    place(img, flask(rng, (0.72, 0.10, 0.12)), 260, 214, 0.56, 0)
    place(img, flask(rng, (0.20, 0.40, 0.14)), 366, 232, 0.50, -8)
    c = from_image(img)
    front = blur(rect([40, 320, 472, 470], 14), 1.2)
    planks = 0.9 + 0.1 * (np.abs(np.sin((yy - 320) / 21.0)) > 0.12)
    c.over(light(0.3 * pillow(front, 14), wood(rng, (0.42, 0.24, 0.10), rings=6) * planks[..., None], depth=50, spec=0.15)
           * edge_darken(front, 10, 0.35), front)
    coin_flat(c, 256, 395, 62)
    return c.image()
