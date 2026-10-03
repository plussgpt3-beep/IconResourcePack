"""A fist with the thumb out, in a leather glove: shared by vote_up / vote_down."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, leather_col, cloth


def thumb(up, color, seed):
    rng = np.random.default_rng(seed)
    c = Canvas()
    glove = leather_col(rng, color)
    parts = []
    # cuff
    cuff = rect([150, 400, 340, 490], 16)
    # palm block, four curled fingers stacked down its front, the thumb standing up
    palm = rect([140, 200, 360, 420], 56)
    fingers = [rect([250, 205 + k * 52, 420, 262 + k * 52], 28) for k in range(4)]
    thumb_m = rect([150, 70, 250, 260], 48)
    full = np.clip(cuff + palm + sum(fingers) + thumb_m, 0, 1)
    if not up:
        full = full[::-1, :]
        cuff = cuff[::-1, :]; palm = palm[::-1, :]; fingers = [f[::-1, :] for f in fingers]; thumb_m = thumb_m[::-1, :]
    c.over(light(pillow(blur(cuff, 1), 16) * 0.7, cloth(rng, (0.25, 0.25, 0.30)), depth=50, spec=0.1), blur(cuff, 1))
    c.over(light(pillow(blur(palm, 1), 30) * 0.9, glove, depth=60, spec=0.25), blur(palm, 1))
    for f in fingers:
        c.over(light(pillow(blur(f, 1), 16, 0.7) * 0.9, glove, depth=50, spec=0.25), blur(f, 1))
    c.over(light(pillow(blur(thumb_m, 1), 18, 0.7) * 0.9, glove, depth=50, spec=0.25), blur(thumb_m, 1))
    return c.image()
