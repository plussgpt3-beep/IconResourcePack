"""ของขาย: a full grain sack, its neck tied with cord."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, cloth


def draw():
    rng = np.random.default_rng(507)
    c = Canvas()
    body = blur(np.maximum(ellipse([90, 180, 422, 480]), poly([(190, 190), (322, 190), (300, 120), (212, 120)])), 1.5)
    nx = (xx - 256) / 166; ny = (yy - 330) / 150
    h = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * body * 0.9 + 0.1 * pillow(body, 8)
    folds = 0.08 * np.sin((xx - 256) / 18.0) * np.clip((260 - yy) / 120, 0, 1)
    c.over(light(h + folds * body, cloth(rng, (0.70, 0.58, 0.38), weave=2.5), depth=80, spec=0.05), body)
    top = blur(poly([(200, 120), (312, 120), (340, 50), (290, 70), (256, 40), (222, 70), (172, 50)]), 1.2)
    c.over(light(0.3 * pillow(top, 8), cloth(rng, (0.64, 0.52, 0.34), weave=2.5), depth=40, spec=0.05), top)
    tie = blur(rect([196, 112, 316, 138], 10), 1)
    tw = 0.5 + 0.5 * np.sin((xx - yy) / 4.0)
    c.over(light(0.4 * pillow(tie, 5), np.zeros((N, N, 3)) + np.array([0.45, 0.30, 0.15]) * (0.7 + 0.3 * tw[..., None]), depth=30, spec=0.1), tie)
    return c.image()
