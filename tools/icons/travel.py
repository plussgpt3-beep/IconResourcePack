"""เดินทาง: a brass pocket compass, lid open, needle pointing north."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, chrome, parchment, noise


def draw():
    rng = np.random.default_rng(208)
    c = Canvas()
    brass = (0.95, 0.70, 0.36)
    cx, cy, R = 256, 270, 200
    case = blur(ellipse([cx - R, cy - R, cx + R, cy + R]), 1.5)
    rr = np.hypot(xx - cx, yy - cy) / R
    h = 0.5 * np.clip(1 - rr, 0, 1) ** 0.25 + 0.2 * np.exp(-((rr - 0.9) / 0.05) ** 2)
    c.over(chrome(h * case, brass, depth=60), case)
    # bow (the ring at the top)
    bow = blur(np.clip(ellipse([cx - 36, cy - R - 54, cx + 36, cy - R + 12]) - ellipse([cx - 20, cy - R - 38, cx + 20, cy - R - 4]), 0, 1), 1)
    c.over(chrome(pillow(bow, 5) * 0.7, brass, depth=40), bow)
    # dial: aged paper with a compass rose
    r2 = R * 0.78
    dial = blur(ellipse([cx - r2, cy - r2, cx + r2, cy + r2]), 1.2)
    col = parchment(rng, (0.92, 0.86, 0.70))
    ang = np.arctan2(yy - cy, xx - cx); d = np.hypot(xx - cx, yy - cy)
    ticks = ((np.abs(np.sin(ang * 16)) < 0.08) & (d > r2 * 0.82) & (d < r2 * 0.95)).astype(np.float32)
    rose_r = r2 * (0.18 + 0.62 * np.abs(np.cos(2 * ang)) ** 8 + 0.30 * np.abs(np.cos(2 * ang + np.pi / 4)) ** 8)
    rose = (d < rose_r).astype(np.float32) * 0.35
    col = col * (1 - 0.6 * ticks[..., None]) * (1 - rose[..., None] * np.array([0.3, 0.45, 0.6]))
    c.over(light(0.1 * dial, col, depth=20, spec=0.05), dial)
    # needle: red north, dark south
    n_north = blur(poly([(cx, cy - r2 * 0.75), (cx + 16, cy), (cx - 16, cy)]), 1)
    n_south = blur(poly([(cx, cy + r2 * 0.75), (cx + 16, cy), (cx - 16, cy)]), 1)
    c.over(light(pillow(n_north, 4) * 0.5, np.zeros((N, N, 3)) + np.array([0.75, 0.10, 0.08]), depth=30, spec=0.5), n_north)
    c.over(light(pillow(n_south, 4) * 0.5, np.zeros((N, N, 3)) + np.array([0.12, 0.12, 0.14]), depth=30, spec=0.5), n_south)
    pin = blur(ellipse([cx - 12, cy - 12, cx + 12, cy + 12]), 1)
    c.over(chrome(pillow(pin, 6), brass, depth=30), pin)
    # glass over the dial: a soft glint
    c.over(np.ones((N, N, 3)), blur(ellipse([cx - 120, cy - 130, cx - 30, cy - 70]), 14) * 0.35)
    return c.image()
