"""ผู้ร่วมก่อตั้งกิลด์: a guild banner - white cloth with a gold gear, on a crossbar."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, chrome, gold_tint


def draw():
    rng = np.random.default_rng(307)
    c = Canvas()
    pole = blur(rect([236, 20, 262, 500], 10), 1)
    c.over(light(pillow(pole, 8, 0.7) * 0.8, wood(rng, (0.42, 0.25, 0.12), angle=np.pi / 2, rings=6), depth=40, spec=0.3), pole)
    bar = blur(rect([120, 70, 392, 92], 10), 1)
    c.over(light(pillow(bar, 8, 0.7) * 0.8, wood(rng, (0.42, 0.25, 0.12), rings=6), depth=40, spec=0.3), bar)
    flag = blur(poly([(140, 90), (372, 90), (372, 380), (256, 450), (140, 380)]), 1.5)
    folds = np.sin((xx - 140) / 232 * np.pi * 3)
    c.over(light((0.3 + 0.12 * folds) * flag, cloth(rng, (0.88, 0.86, 0.80)), depth=60, spec=0.08), flag)
    edge = blur(np.clip(flag - blur(poly([(156, 104), (356, 104), (356, 370), (256, 430), (156, 370)]), 1), 0, 1), 1)
    c.over(chrome(pillow(edge, 3) * 0.5, gold_tint(), depth=30), edge)
    cx, cy = 256, 250
    ang = np.arctan2(yy - cy, xx - cx); d = np.hypot(xx - cx, yy - cy)
    gear = blur(((d < 70 + 14 * (np.cos(ang * 8) > 0.2)) & (d > 28)).astype(np.float32), 1.5)
    c.over(chrome(pillow(gear, 6) * 0.6 + 0.04 * folds, gold_tint(), depth=40), gear)
    return c.image()
