"""ค้นหา: a magnifying glass - a brass ring holding a pale glass lens with a glint, on a turned oak handle
(2026-11-01, the user: search boxes in every list of goods)."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, wood, blur, poly, ellipse, edge_darken, metal


def draw():
    rng = np.random.default_rng(311)
    c = Canvas()
    shadow(c, [90, 400, 470, 480], 0.4, 18)
    cx, cy, r = 212, 206, 138
    # handle: from the ring's lower right towards the corner, a turned oak grip with a brass ferrule
    hx0, hy0, hx1, hy1 = cx + r * 0.66, cy + r * 0.66, 452, 452
    handle = blur(poly([(hx0 + 18, hy0 + 2), (hx1, hy1), (hx0 + 2, hy0 + 18)], width=None), 1.0)
    grip = blur(poly([(hx0 + 30, hy0 + 30), (hx1, hy1)], width=62), 1.5)
    hgrip = pillow(grip, 18, 0.55)
    c.over(light(hgrip, wood(rng, (0.50, 0.30, 0.15), angle=np.pi / 4, rings=10), depth=70, spec=0.3, gloss=20)
           * edge_darken(grip, 8, 0.45), grip)
    ferrule = blur(poly([(hx0 - 6, hy0 - 6), (hx0 + 40, hy0 + 40)], width=74), 1.5)
    brass = metal(rng, (0.80, 0.60, 0.24))
    c.over(light(pillow(ferrule, 16, 0.5), brass, depth=70, spec=0.6, gloss=30) * edge_darken(ferrule, 6, 0.4), ferrule)
    # lens: pale blue-green glass, darker towards the rim, a soft reflected window
    rr = np.hypot(xx - cx, yy - cy)
    lens = blur((rr < r - 22).astype(np.float32), 1.2)
    t = np.clip(rr / (r - 22), 0, 1)
    glass = np.dstack([0.62 - 0.18 * t, 0.80 - 0.20 * t, 0.86 - 0.16 * t])
    c.over(glass, lens * 0.92)
    glint = blur(((((xx - (cx - 52)) / 46) ** 2 + ((yy - (cy - 58)) / 26) ** 2) < 1).astype(np.float32), 6)
    c.over(np.ones((N, N, 3)) * 0.98, glint * 0.75 * lens)
    dot = blur(((((xx - (cx + 50)) / 12) ** 2 + ((yy - (cy + 46)) / 12) ** 2) < 1).astype(np.float32), 3)
    c.over(np.ones((N, N, 3)) * 0.95, dot * 0.5 * lens)
    # brass ring around the lens
    ring = blur(((rr < r) & (rr > r - 30)).astype(np.float32), 1.2)
    hr = np.clip(1 - np.abs(rr - (r - 15)) / 15, 0, 1) ** 0.6 * ring
    c.over(light(hr, brass, depth=60, spec=0.7, gloss=34) * edge_darken(ring, 5, 0.35), ring)
    return c.image()
