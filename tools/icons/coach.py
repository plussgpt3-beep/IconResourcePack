"""สถานีรถม้าหลวง / นายสถานี / ไป <เมือง>: the crown's coach - a closed carriage in royal red with gold trim, a window, two wheels."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, edge_darken, chrome, gold_tint
from caravan import wheel


def draw():
    rng = np.random.default_rng(431)
    c = Canvas()
    # shaft toward the (unseen) horses
    shaft = blur(poly([(400, 330), (500, 300)], width=14), 1)
    c.over(light(pillow(shaft, 4) * 0.6, wood(rng, (0.40, 0.24, 0.11), rings=6), depth=30, spec=0.2), shaft)
    # body: a box with a curved roof
    body = blur(poly([(70, 330), (70, 170), (110, 120), (370, 120), (410, 170), (410, 330)]), 1.5)
    red = cloth(rng, (0.62, 0.10, 0.10), weave=1.4)
    c.over(light(0.25 * pillow(body, 10), red, depth=50, spec=0.25) * edge_darken(body, 10, 0.45), body)
    # roof rail and crown finial in gold
    rail = blur(rect([96, 104, 384, 124], 6), 1)
    c.over(chrome(pillow(rail, 5) * 0.6, gold_tint(), depth=40, ground=0.15), rail)
    finial = blur(poly([(210, 104), (222, 70), (240, 92), (258, 70), (270, 104)]), 1)
    c.over(chrome(pillow(finial, 5) * 0.7, gold_tint(), depth=40, ground=0.15), finial)
    # gold frame lines on the body
    frame = blur(((np.abs(yy - 300) < 5) & (xx > 80) & (xx < 400)).astype(np.float32) +
                 ((np.abs(xx - 240) < 5) & (yy > 140) & (yy < 300)).astype(np.float32), 1)
    frame = np.clip(frame, 0, 1) * body
    c.over(chrome(pillow(frame, 3) * 0.5, gold_tint(), depth=30, ground=0.15), frame)
    # windows: dark glass with a gold edge
    for x0 in (100, 262):
        win = blur(rect([x0, 160, x0 + 118, 250], 14), 1)
        edge = blur(rect([x0 - 7, 153, x0 + 125, 257], 18), 1) * (1 - win)
        c.over(chrome(pillow(edge, 3) * 0.5, gold_tint(), depth=30, ground=0.15), edge)
        glass = np.stack([0.10 + 0.10 * (1 - (yy - 160) / 90.0), 0.14 + 0.12 * (1 - (yy - 160) / 90.0), 0.20 + 0.15 * (1 - (yy - 160) / 90.0)], -1)
        c.over(light(0.1 * pillow(win, 8), np.clip(glass, 0, 1), depth=20, spec=0.6), win)
    # undercarriage and wheels
    under = blur(rect([60, 326, 420, 350], 6), 1)
    c.over(light(0.2 * pillow(under, 5), wood(rng, (0.30, 0.18, 0.08), rings=8), depth=30, spec=0.15), under)
    wheel(c, rng, 140, 400, 82)
    wheel(c, rng, 350, 400, 82)
    return c.image()
