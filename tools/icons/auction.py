"""ขายทอดตลาด: an auctioneer's gavel striking its sounding block."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, band, chrome, gold_tint


def draw():
    rng = np.random.default_rng(308)
    c = Canvas()
    blk = blur(np.maximum(ellipse([110, 380, 400, 470]), rect([110, 350, 400, 425])) , 1.2)
    top = blur(ellipse([110, 320, 400, 400]), 1.2)
    col = wood(rng, (0.36, 0.20, 0.09), rings=10)
    c.over(light(0.2 * pillow(blk, 10), col * 0.8, depth=30, spec=0.2), blk)
    c.over(light(0.15 * pillow(top, 12), col, depth=30, spec=0.35), top)
    # handle
    s, t = band((440, 300), (220, 120), 0)
    hd = blur(((s > 0) & (s < 1) & (np.abs(t) < 13)).astype(np.float32), 1)
    c.over(light(np.clip(1 - np.abs(t) / 13, 0, 1) ** 0.5 * hd, wood(rng, (0.40, 0.23, 0.11), angle=0.7, rings=5), depth=30, spec=0.3), hd)
    # head: a barrel across the end of the handle
    s2, t2 = band((150, 210), (290, 30), 0)
    head = blur(((s2 > 0) & (s2 < 1) & (np.abs(t2) < 52)).astype(np.float32), 1.2)
    cyl = np.sqrt(np.clip(1 - (t2 / 52) ** 2, 0, 1))
    c.over(light(cyl * head * 0.9, wood(rng, (0.38, 0.21, 0.10), angle=-0.9, rings=8), depth=60, spec=0.35), head)
    for e in (0.12, 0.88):
        bandm = blur(((np.abs(s2 - e) < 0.04) & (np.abs(t2) < 54)).astype(np.float32), 1)
        c.over(chrome(cyl * bandm, gold_tint(), depth=40), bandm)
    return c.image()
