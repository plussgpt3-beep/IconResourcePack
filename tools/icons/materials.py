"""วัสดุ: building stock - a stack of fired bricks with sawn planks leaning on it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, wood, noise, edge_darken


def brick(c, rng, x0, y0, w=110, h=48):
    m = blur(rect([x0, y0, x0 + w, y0 + h], 5), 1)
    col = np.array([0.62, 0.26, 0.15])[None, None, :] * (0.75 + 0.4 * noise(rng, 30, 3)[..., None])
    c.over(light(0.35 * pillow(m, 8), col, depth=40, spec=0.1) * edge_darken(m, 5, 0.35), m)


def draw():
    rng = np.random.default_rng(404)
    c = Canvas()
    for x0, y0, x1, y1 in ((300, 90, 340, 470), (350, 120, 390, 470), (400, 150, 438, 470)):
        p = blur(poly([(x0, y0), (x1, y0 + 10), (x1, y1), (x0, y1)]), 1)
        c.over(light(0.25 * pillow(p, 6), wood(rng, (0.78, 0.60, 0.36), angle=np.pi / 2, rings=5), depth=40, spec=0.15) * edge_darken(p, 5, 0.3), p)
    for r in range(5):
        y0 = 420 - r * 52
        off = 0 if r % 2 == 0 else 55
        for k in range(2 if r % 2 else 3):
            if r == 4 and k > 0: break
            brick(c, rng, 60 + off + k * 112, y0)
    return c.image()
