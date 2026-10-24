"""เบิกยาจากคลังหลวง (2026-10-25): a soldier's red shield, a flask of remedy held before it."""
import numpy as np
from lib import Canvas, from_image
from _escort import shield
from _clinic import flask
from _tavern import place


def draw():
    rng = np.random.default_rng(2606)
    c = Canvas()
    shield(c, rng, cx=220, top=60, w=300, h=340, field=(0.62, 0.12, 0.12))
    img = c.image()
    place(img, flask(rng, (0.72, 0.10, 0.12)), 350, 340, 0.62, -10)
    return from_image(img).image()
