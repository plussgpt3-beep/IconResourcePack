"""ทำไม่ได้ / ล็อก: an iron padlock, shackle closed."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, metal, rect, blur, edge_darken, mask_from, ellipse, poly


def draw():
    rng = np.random.default_rng(31)
    c = Canvas()
    shadow(c, [90, 430, 430, 495], 0.45, 18)
    # shackle: a thick steel tube bent into an arch
    arch = mask_from(lambda d: d.arc([150, 50, 362, 300], 180, 360, fill=255, width=46))
    legs = np.maximum(poly([(173, 175), (173, 270)], width=46), poly([(339, 175), (339, 270)], width=46))
    shackle = blur(np.maximum(arch, legs), 1.5)
    hs = pillow(shackle, 16, 0.8)
    c.over(light(hs, metal(rng, (0.70, 0.72, 0.76)), depth=70, spec=0.7, gloss=25) * edge_darken(shackle, 6, 0.3), shackle)
    # body: cast iron with a bevelled face
    body = blur(rect([105, 225, 407, 470], radius=46), 1.5)
    hb = pillow(body, 24, 0.5)
    col = metal(rng, (0.38, 0.38, 0.40)) * (0.9 + 0.2 * np.clip((470 - yy) / 245, 0, 1))[..., None]
    c.over(light(hb, col, depth=80, spec=0.45, gloss=20) * edge_darken(body, 12, 0.35), body)
    # rivets
    for rx, ry in [(140, 260), (372, 260), (140, 435), (372, 435)]:
        rv = ellipse([rx - 12, ry - 12, rx + 12, ry + 12])
        c.over(light(pillow(rv, 6, 0.6) * 0.6, metal(rng, (0.55, 0.55, 0.58)), depth=40, spec=0.8), rv)
    # keyhole, sunk into a brass escutcheon
    esc = blur(ellipse([206, 290, 306, 410]), 1.5)
    c.over(light(pillow(esc, 10) * 0.5, metal(rng, (0.78, 0.60, 0.25)), depth=50, spec=0.7, gloss=30), esc)
    hole = blur(np.maximum(ellipse([238, 312, 274, 348]), poly([(246, 335), (266, 335), (272, 388), (240, 388)])), 1)
    c.over(np.zeros((N, N, 3)) + 0.05, hole)
    return c.image()
