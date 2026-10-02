"""Admin: the master key - a large gold key with a crowned bow."""
import numpy as np
from lib import N, xx, yy, Canvas, blur, ellipse, rect, poly, chrome, gold_tint, band, pillow


def draw():
    c = Canvas()
    p0, p1 = (150, 150), (430, 430)
    s, t = band(p0, p1, 0)
    shaft = blur(((s > 0.18) & (s < 1.0) & (np.abs(t) < 15)).astype(np.float32), 1)
    h = np.clip(1 - np.abs(t) / 15, 0, 1) ** 0.5 * shaft
    # bit: the toothed block at the end
    bit = blur(((s > 0.78) & (s < 0.98) & (t > 10) & (t < 70) & ~((s > 0.84) & (s < 0.88) & (t > 40))).astype(np.float32), 1)
    h = np.maximum(h, pillow(bit, 6) * 0.7)
    # bow: a ring with a crown on top
    rr = np.hypot(xx - 150, yy - 150)
    bow = blur(((rr < 92) & (rr > 52)).astype(np.float32), 1)
    h = np.maximum(h, np.clip(1 - np.abs(rr - 72) / 20, 0, 1) ** 0.5 * bow)
    m = np.clip(shaft + bit + bow, 0, 1)
    c.over(chrome(h, gold_tint(), depth=50), m)
    cr = blur(poly([(80, 70), (90, 20), (115, 50), (150, 5), (185, 50), (210, 20), (220, 70)]), 1)
    c.over(chrome(pillow(cr, 6) * 0.7, gold_tint(), depth=40), cr)
    return c.image()
