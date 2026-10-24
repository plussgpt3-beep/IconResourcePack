"""คลังยาของโรงหมอ: an open wooden crate of medicine - flasks of remedy and a bandage roll."""
import numpy as np
from PIL import Image
from lib import N, Canvas, light, pillow, blur, rect, wood, edge_darken, yy, from_image
from _clinic import flask, bandage
from _tavern import place


def draw():
    rng = np.random.default_rng(2508)
    c = Canvas()
    back = blur(rect([60, 200, 452, 340], 10), 1)
    c.over(light(0.3 * pillow(back, 10), wood(rng, (0.34, 0.20, 0.09), rings=6), depth=40, spec=0.1), back)
    img = c.image()
    place(img, flask(rng, (0.90, 0.58, 0.14)), 150, 230, 0.52, 8)
    place(img, flask(rng, (0.72, 0.10, 0.12)), 260, 214, 0.56, 0)
    place(img, flask(rng, (0.20, 0.40, 0.14)), 366, 232, 0.50, -8)
    c = from_image(img)
    front = blur(rect([40, 320, 472, 470], 14), 1.2)
    planks = 0.9 + 0.1 * (np.abs(np.sin((yy - 320) / 21.0)) > 0.12)
    c.over(light(0.3 * pillow(front, 14), wood(rng, (0.55, 0.34, 0.16), rings=6) * planks[..., None], depth=50, spec=0.15)
           * edge_darken(front, 10, 0.35), front)
    return c.image()
