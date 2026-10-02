"""ที่ดินของฉัน: a land deed - a rolled parchment tied with a cord and sealed in red wax."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, ellipse, wax_seal, noise, band


def draw():
    rng = np.random.default_rng(205)
    c = Canvas()
    p0, p1 = (90, 380), (420, 150)
    s, t = band(p0, p1, 0)
    R = 70
    body = ((s > 0) & (s < 1) & (np.abs(t) < R)).astype(np.float32)
    body = blur(body, 1.5)
    cyl = np.sqrt(np.clip(1 - (t / R) ** 2, 0, 1))
    col = parchment(rng) * (1 - 0.15 * (0.5 + 0.5 * np.sin(s * 60)))[..., None] ** 0
    c.over(light(cyl * body, col, depth=90, spec=0.08), body)
    # the curled end: a spiral seen end-on at the upper right
    ex, ey = p1
    end = blur(ellipse([ex - 38, ey - R, ex + 38, ey + R]), 1.2)
    rr = np.hypot((xx - ex) / 38, (yy - ey) / R)
    spiral = 0.5 + 0.5 * np.sin(rr * 22 + np.arctan2(yy - ey, xx - ex))
    endcol = parchment(rng, (0.80, 0.70, 0.50)) * (0.65 + 0.35 * spiral[..., None])
    c.over(endcol, end)
    # cord wrapped round the middle, the seal hanging below it
    cord = blur(((np.abs(s - 0.5) < 0.03) & (np.abs(t) < R + 4)).astype(np.float32), 1)
    c.over(light(pillow(cord, 3) * 0.6, np.zeros((N, N, 3)) + np.array([0.55, 0.12, 0.08]), depth=30, spec=0.3), cord)
    mx, my = 90 + (420 - 90) * 0.5, 380 + (150 - 380) * 0.5
    tail = blur(poly([(mx, my + 40), (mx - 10, my + 110), (mx + 6, my + 150)], width=8), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.50, 0.10, 0.07]), tail)
    wax_seal(c, rng, mx + 5, my + 175, 58, (0.55, 0.06, 0.05), ellipse([mx - 20, my + 155, mx + 30, my + 195]) * 0)
    return c.image()
