"""เจ้าเมือง: the governor's chain of office - linked gold plates with a pendant medallion."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, mask_from


def draw():
    rng = np.random.default_rng(602)
    c = Canvas()
    cx, cy, rx, ry = 256, 170, 190, 200
    for k in range(23):
        a = np.pi * (0.05 + 0.9 * k / 22)
        x = cx - rx * np.cos(a); y = cy + ry * np.sin(a) * 0.9 - 40
        plate = blur(rect([x - 20, y - 14, x + 20, y + 14], 6) if k % 2 == 0 else ellipse([x - 14, y - 14, x + 14, y + 14]), 1)
        c.over(chrome(0.5 * pillow(plate, 6), gold_tint(), depth=40), plate)
    mx, my = 256, 370
    med = blur(ellipse([mx - 90, my - 90, mx + 90, my + 90]), 1.5)
    rr = np.hypot(xx - mx, yy - my) / 90
    h = 0.45 * np.clip(1 - rr, 0, 1) ** 0.3 + 0.3 * np.exp(-((rr - 0.86) / 0.06) ** 2)
    tower = blur(np.maximum(rect([mx - 30, my - 40, mx + 30, my + 45]), poly([(mx - 40, my - 40), (mx - 40, my - 60), (mx - 20, my - 60), (mx - 20, my - 48),
                                                                                 (mx - 6, my - 48), (mx - 6, my - 60), (mx + 6, my - 60), (mx + 6, my - 48), (mx + 20, my - 48),
                                                                                 (mx + 20, my - 60), (mx + 40, my - 60), (mx + 40, my - 40)])), 2)
    c.over(chrome(h * med + 0.2 * tower, gold_tint(), depth=60), med)
    gem = blur(ellipse([mx - 12, my + 50, mx + 12, my + 74]), 1)
    c.over(light(pillow(gem, 6), np.zeros((N, N, 3)) + np.array([0.75, 0.06, 0.08]), depth=30, spec=0.9), gem)
    return c.image()
