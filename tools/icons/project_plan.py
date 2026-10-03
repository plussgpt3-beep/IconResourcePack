"""ขั้นตอนโครงการ: a builder's plan - a blue drawing of a house front, a ruler laid on it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, edge_darken, noise, wood, band


def draw():
    rng = np.random.default_rng(402)
    c = Canvas()
    sheet = blur(poly([(70, 90), (440, 70), (450, 420), (60, 440)]), 1.2)
    col = np.array([0.16, 0.30, 0.55])[None, None, :] * (0.85 + 0.2 * noise(rng, 6, 3)[..., None])
    grid = ((xx % 26 < 2) | (yy % 26 < 2)).astype(np.float32) * 0.25
    lines = np.zeros((N, N), np.float32)
    for pts in ([(150, 380), (360, 380)], [(150, 380), (150, 230)], [(360, 380), (360, 230)], [(130, 240), (255, 140), (380, 240)],
                [(230, 380), (230, 300), (280, 300), (280, 380)], [(170, 260), (210, 260), (210, 300), (170, 300), (170, 260)],
                [(300, 260), (340, 260), (340, 300), (300, 300), (300, 260)]):
        lines = np.maximum(lines, poly(pts, width=5))
    col = col * (1 + grid[..., None] * 0.6) + lines[..., None] * np.array([0.75, 0.70, 0.55])
    c.over(light(0.1 * pillow(sheet, 8), np.clip(col, 0, 1), depth=30, spec=0.05) * edge_darken(sheet, 10, 0.35), sheet)
    s, t = band((90, 470), (430, 360), 0)
    ruler = blur(((s > 0) & (s < 1) & (t > -22) & (t < 22)).astype(np.float32), 1)
    rc = wood(rng, (0.80, 0.66, 0.42), angle=-0.31, rings=3)
    ticks = ((np.abs(((s * 30) % 1) - 0.5) > 0.42) & (t < -6))
    rc[ticks] *= 0.35
    c.over(light(0.2 * pillow(ruler, 4), rc, depth=30, spec=0.2), ruler)
    return c.image()
