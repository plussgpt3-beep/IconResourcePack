"""ถอนหลักเขต: the boundary stone heaved out of its torn turf, leaning, an iron pickaxe beside it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, wood, chrome, band, noise
from _claims import turf, marker


def draw():
    rng = np.random.default_rng(2443)
    c = Canvas()
    turf(c, rng, cx=240, rx=160)
    hole = blur(ellipse([160, 410, 300, 446]), 2)
    c.over(np.array([0.20, 0.13, 0.07])[None, None, :] * (0.7 + 0.4 * noise(rng, 20, 2)[..., None]), hole)
    marker(c, rng, 150, 290, 110, 420, tilt=-0.42)
    # the pickaxe: haft and iron head
    p0, p1 = (300, 470), (440, 140)
    s, t = band(p0, p1, 0)
    haft = blur(((s > 0) & (s < 1) & (np.abs(t) < 13)).astype(np.float32), 1)
    c.over(light(np.clip(1 - np.abs(t) / 13, 0, 1) ** 0.5 * haft, wood(rng, (0.55, 0.36, 0.20), angle=-1.17, rings=5), depth=30, spec=0.2), haft)
    # the pick's iron head: a curved bar across the top of the haft, pointed both ends
    hx, hy = 440, 140
    pts = []
    for a in np.linspace(-1.0, 1.0, 21):
        pts.append((hx + 110 * a * 0.93 + 18 * a, hy - 36 * (1 - a * a) + 40 * a))
    top_edge = pts
    bot_edge = [(x + 6, y + 34 - 20 * abs(i - 10) / 10) for i, (x, y) in enumerate(pts)]
    head = blur(poly(top_edge + bot_edge[::-1]), 1)
    c.over(chrome(0.6 * pillow(head, 8), (0.62, 0.64, 0.68), depth=50), head)
    return c.image()
