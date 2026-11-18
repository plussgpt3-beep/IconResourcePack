"""แต้มค่าสถานะคงเหลือ (อัปเกรดตัวละคร 2026-11-18): a gold five-pointed star medallion."""
import numpy as np
from lib import xx, yy, Canvas, blur, ellipse, poly, chrome, gold_tint, pillow, light


def draw():
    c = Canvas()
    cx, cy = 256, 256
    disc = blur(ellipse([66, 66, 446, 446]), 1.5)
    c.over(chrome(pillow(disc, 30) * 0.5, (0.55, 0.40, 0.12), depth=50, ground=0.15), disc)
    pts = []
    for i in range(10):
        a = -np.pi / 2 + i * np.pi / 5
        r = 160 if i % 2 == 0 else 66
        pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
    star = blur(poly(pts), 1.2)
    c.over(chrome(pillow(star, 14) * 0.9, gold_tint(), depth=50, ground=0.2), star)
    return c.image()
