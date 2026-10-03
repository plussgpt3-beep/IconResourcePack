"""เตียงของฉัน: a soldier's plain wooden cot with a red wool blanket and a white pillow, seen from the foot corner."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, edge_darken


def draw():
    rng = np.random.default_rng(1203)
    c = Canvas()
    # legs
    for x0, y0, h in ((70, 330, 120), (400, 300, 100), (190, 400, 90), (452, 360, 80)):
        leg = blur(rect([x0, y0, x0 + 28, y0 + h], 5), 1)
        c.over(light(0.5 * pillow(leg, 6), wood(rng, (0.36, 0.21, 0.09), angle=np.pi / 2, rings=3), depth=40, spec=0.15), leg)
    # frame: the long side facing us and the foot end
    side = blur(poly([(60, 300), (196, 380), (196, 420), (60, 340)]), 1)
    c.over(light(0.3 * pillow(side, 6), wood(rng, (0.42, 0.25, 0.11), rings=6), depth=40, spec=0.2), side)
    foot = blur(poly([(196, 380), (470, 300), (470, 340), (196, 420)]), 1)
    c.over(light(0.3 * pillow(foot, 6), wood(rng, (0.34, 0.20, 0.09), rings=6), depth=40, spec=0.2), foot)
    # mattress and blanket on top
    top = blur(poly([(60, 300), (334, 220), (470, 300), (196, 380)]), 1.2)
    blanket = cloth(rng, (0.62, 0.10, 0.09), weave=2.4)
    stripe = ((np.abs(((xx - 60) * 0.80 + (yy - 300) * 0.59) - 230) < 14) | (np.abs(((xx - 60) * 0.80 + (yy - 300) * 0.59) - 262) < 6))
    blanket = blanket * (1 - stripe[..., None] * 0.9) + np.array([0.85, 0.75, 0.40]) * stripe[..., None] * 0.9
    folds = 0.06 * np.sin(((xx - 60) * 0.80 + (yy - 300) * 0.59) / 18.0)
    c.over(light(0.35 * pillow(top, 26) + folds * top, blanket, depth=50, spec=0.1) * edge_darken(top, 10, 0.3), top)
    # the pillow at the head (far end)
    pil = blur(poly([(250, 248), (334, 224), (420, 274), (338, 300)]), 6)
    c.over(light(0.8 * pillow(pil, 26), cloth(rng, (0.92, 0.90, 0.85), weave=3.0), depth=50, spec=0.1), pil)
    # the turned-down sheet edge
    sheet = blur(poly([(196, 270), (296, 241), (332, 262), (232, 292)]), 1.5)
    c.over(light(0.3 * pillow(sheet, 8), cloth(rng, (0.90, 0.88, 0.82), weave=3.0), depth=30, spec=0.05), sheet)
    # headboard
    head = blur(poly([(334, 120), (470, 200), (470, 300), (334, 222)]), 1.2)
    c.over(light(0.3 * pillow(head, 10), wood(rng, (0.40, 0.24, 0.10), angle=0.5, rings=7), depth=40, spec=0.2) * edge_darken(head, 8, 0.35), head)
    return c.image()
