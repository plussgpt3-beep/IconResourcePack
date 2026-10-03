"""ไม้รังวัด: a surveyor's measuring rod, banded every span, with a brass plumb bob on its cord."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, wood, chrome, band


def draw():
    rng = np.random.default_rng(302)
    c = Canvas()
    p0, p1 = (90, 450), (440, 70)
    s, t = band(p0, p1, 0)
    rod = blur(((s > 0) & (s < 1) & (np.abs(t) < 20)).astype(np.float32), 1)
    col = wood(rng, (0.80, 0.68, 0.48), angle=-0.83, rings=4)
    seg = ((s * 8).astype(int) % 2 == 0)
    col[seg] = col[seg] * np.array([0.95, 0.25, 0.20]) / np.array([0.80, 0.68, 0.48]) * 0.8
    ticks = (np.abs(((s * 40) % 1) - 0.5) > 0.45) & (t > 8)
    col[ticks] *= 0.3
    c.over(light(np.clip(1 - np.abs(t) / 20, 0, 1) ** 0.5 * rod, col, depth=40, spec=0.25), rod)
    for e in (0.0, 1.0):
        cap = blur(((np.abs(s - e) < 0.035) & (np.abs(t) < 23)).astype(np.float32), 1)
        c.over(chrome(np.clip(1 - np.abs(t) / 23, 0, 1) ** 0.5 * cap, (0.95, 0.70, 0.36), depth=40), cap)
    cord = blur(poly([(330, 200), (345, 300), (350, 360)], width=4), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.45, 0.30]), cord)
    bob = blur(poly([(320, 360), (380, 360), (350, 450)]) + ellipse([320, 340, 380, 380]), 1)
    nx = (xx - 350) / 30
    c.over(chrome(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * np.clip(bob, 0, 1), (0.95, 0.70, 0.36), depth=50), np.clip(bob, 0, 1))
    return c.image()
