"""แก้ไขงาน: a carpenter's claw hammer over a few iron nails."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, band


def draw():
    rng = np.random.default_rng(410)
    c = Canvas()
    for (x, y, a) in ((110, 430, 0.3), (180, 455, -0.2), (150, 395, 1.2)):
        s, t = band((x, y), (x + 120 * np.cos(a), y - 30 * np.sin(a) - 40), 0)
        n = blur(((s > 0) & (s < 1) & (np.abs(t) < 6)).astype(np.float32), 0.8)
        c.over(chrome(np.clip(1 - np.abs(t) / 6, 0, 1) ** 0.5 * n, (0.55, 0.56, 0.60), depth=30, ground=0.1), n)
    s, t = band((140, 330), (420, 110), 0)
    h = blur(((s > 0) & (s < 0.95) & (np.abs(t) < 17)).astype(np.float32), 1)
    c.over(light(np.clip(1 - np.abs(t) / 17, 0, 1) ** 0.5 * h, wood(rng, (0.55, 0.36, 0.18), angle=-0.67, rings=4), depth=30, spec=0.3), h)
    s2, t2 = band((330, 40), (470, 230), 0)
    head = blur(np.clip((((s2 > 0.25) & (s2 < 0.75) & (np.abs(t2) < 34)) | ((s2 > 0.75) & (s2 < 1.0) & (np.abs(t2) < 24))).astype(np.float32)
                        + poly([(330, 40), (300, 30), (270, 70), (320, 100)]), 0, 1), 1)
    c.over(chrome(0.5 * pillow(head, 10), (0.45, 0.47, 0.50), depth=50, sky=0.8, ground=0.1), head)
    return c.image()
