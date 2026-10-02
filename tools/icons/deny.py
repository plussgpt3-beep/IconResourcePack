"""ปฏิเสธ: a written document torn in two, the halves pulled apart."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, parchment, blur, poly, edge_darken, noise


def draw():
    rng = np.random.default_rng(51)
    c = Canvas()
    shadow(c, [60, 420, 452, 492], 0.35, 18)
    sheet = poly([(120, 60), (392, 60), (392, 452), (120, 452)])
    # a jagged tear running from top to bottom, wandering around x = 256
    jag = noise(rng, 18, 3) - 0.5
    tear_x = 256 + 26 * np.sin(yy / 60.0) + 22 * jag
    left = sheet * (xx < tear_x)
    right = sheet * (xx >= tear_x)
    col = parchment(rng)
    for half, dx, dy, rot in [(left, -16, 6, 1), (right, 16, -4, -1)]:
        # move each half apart (integer roll keeps it simple)
        moved = np.roll(np.roll(half, dy, axis=0), dx, axis=1)
        m = blur(moved, 1.0)
        fib = (blur(moved, 3) - blur(moved, 1)).clip(0, 1)   # fibrous torn edge, lighter
        h = pillow(m, 8, 0.5) * 0.2 + 0.012 * noise(rng, 6, 2) * m
        shaded = light(h, np.roll(np.roll(col, dy, axis=0), dx, axis=1), depth=60, spec=0.05) * edge_darken(m, 8, 0.3)
        shaded = shaded + 0.25 * fib[..., None]
        c.over(np.zeros((N, N, 3)), blur(m, 10) * 0.25)
        c.over(np.clip(shaded, 0, 1), m)
        # writing on each half, moving with it
        for i, y in enumerate(range(120, 420, 44)):
            ln = poly([(150, y), (360 - (i % 3) * 25, y + 1)], width=6) * half
            ln = np.roll(np.roll(ln, dy, axis=0), dx, axis=1)
            c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.24, 0.18]), ln * 0.35)
    # a red stroke of ink across it: the refusal
    stroke = blur(poly([(110, 330), (250, 270), (410, 200)], width=22), 2)
    c.over(np.zeros((N, N, 3)) + np.array([0.62, 0.08, 0.06]), stroke * 0.85)
    return c.image()
