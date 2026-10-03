"""ราชสำนัก: the throne - carved and gilded, a red cushion on the seat."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, cloth, wood


def draw():
    rng = np.random.default_rng(601)
    c = Canvas()
    back = blur(np.maximum(rect([130, 110, 382, 330], 16), ellipse([130, 40, 382, 200])), 1.2)
    c.over(chrome(0.35 * pillow(back, 20), gold_tint(), depth=50, ground=0.25), back)
    panel = blur(np.maximum(rect([165, 140, 347, 320], 12), ellipse([165, 80, 347, 220])), 1.2)
    c.over(light(0.3 * pillow(panel, 14), cloth(rng, (0.55, 0.06, 0.08), weave=2), depth=40, spec=0.15), panel)
    crest = blur(poly([(256, 120), (296, 160), (256, 220), (216, 160)]), 1)
    c.over(chrome(0.5 * pillow(crest, 8), gold_tint(), depth=40), crest)
    seat = blur(rect([100, 310, 412, 370], 14), 1)
    c.over(light(0.4 * pillow(seat, 12), cloth(rng, (0.60, 0.07, 0.09), weave=2), depth=50, spec=0.2), seat)
    for x in (90, 380):
        arm = blur(rect([x, 270, x + 42, 400], 14), 1)
        c.over(chrome(0.45 * pillow(arm, 10), gold_tint(), depth=40, ground=0.25), arm)
    base = blur(rect([110, 370, 402, 420], 8), 1)
    c.over(chrome(0.3 * pillow(base, 8), gold_tint(), depth=40, ground=0.22), base)
    for x in (130, 360):
        leg = blur(poly([(x, 415), (x + 30, 415), (x + 26, 480), (x + 4, 480)]), 1)
        c.over(chrome(0.4 * pillow(leg, 6), gold_tint(), depth=40, ground=0.22), leg)
    return c.image()
