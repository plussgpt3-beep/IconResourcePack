"""ตั้งคุก: a gaol's iron grate - bars riveted to two cross bands in a stone frame, and the gaoler's key hanging before it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, rect, chrome, stone, edge_darken, band


def draw():
    rng = np.random.default_rng(2472)
    c = Canvas()
    frame = blur(rect([70, 50, 442, 462], 18), 1.2)
    hole = rect([110, 90, 402, 422], 6)
    ring = np.clip(frame - hole, 0, 1)
    c.over(light(0.3 * pillow(ring, 14), stone(rng), depth=50, spec=0.06) * edge_darken(ring, 10, 0.35), ring)
    dark = blur(hole, 1)
    c.over(np.ones((N, N, 3), np.float32) * np.array([0.10, 0.09, 0.10], np.float32), dark)
    iron = (0.42, 0.43, 0.46)
    for x in range(140, 400, 52):
        bar = blur(rect([x - 12, 88, x + 12, 424], 6), 1)
        c.over(chrome(0.8 * pillow(bar, 8), iron, depth=55), bar)
    for y in (150, 350):
        b = blur(rect([108, y - 14, 404, y + 14], 4), 1)
        c.over(chrome(0.7 * pillow(b, 8), iron, depth=50), b)
        for x in range(140, 400, 52):
            r = blur(ellipse([x - 7, y - 7, x + 7, y + 7]), 1)
            c.over(chrome(0.9 * pillow(r, 4), (0.55, 0.55, 0.58), depth=40), r)
    # The key: a ring bow, a shank, a bit.
    rr = np.hypot(xx - 380, yy - 300)
    bow = blur(((rr < 44) & (rr > 26)).astype(np.float32), 1)
    s, t = band((380, 340), (380, 470), 0)
    shank = blur(((s > 0) & (s < 1) & (np.abs(t) < 9)).astype(np.float32), 1)
    bit = blur(rect([380, 432, 418, 448], 2) + rect([380, 452, 410, 466], 2), 1)
    gold = (0.86, 0.66, 0.28)
    for m in (shank, np.clip(bit, 0, 1), bow):
        c.over(chrome(0.7 * pillow(m, 5), gold, depth=45), m)
    return c.image()
