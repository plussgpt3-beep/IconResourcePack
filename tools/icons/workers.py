"""กรรมกร: a labourer's shovel and pickaxe, crossed."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, wood, chrome, band


def handle(c, rng, p0, p1, w=13):
    s, t = band(p0, p1, 0)
    h = blur(((s > 0) & (s < 1) & (np.abs(t) < w)).astype(np.float32), 1)
    ang = np.arctan2(p1[1] - p0[1], p1[0] - p0[0])
    c.over(light(np.clip(1 - np.abs(t) / w, 0, 1) ** 0.5 * h, wood(rng, (0.60, 0.42, 0.22), angle=ang + np.pi / 2, rings=4), depth=30, spec=0.25), h)


def draw():
    rng = np.random.default_rng(406)
    c = Canvas()
    # shovel: handle from lower left up to the right, blade at the top right
    handle(c, rng, (80, 470), (330, 170))
    blade = blur(poly([(300, 190), (370, 110), (440, 60), (470, 110), (420, 180), (350, 220)]), 1.2)
    c.over(chrome(0.4 * pillow(blade, 14), (0.55, 0.57, 0.60), depth=50, sky=0.8, ground=0.12), blade)
    grip = blur(poly([(60, 470), (110, 490)], width=22), 1)
    c.over(light(0.4 * pillow(grip, 6), wood(rng, (0.50, 0.32, 0.16), rings=3), depth=30, spec=0.2), grip)
    # pickaxe: handle from lower right up to the left, curved iron head across the top
    handle(c, rng, (440, 470), (190, 150))
    cx, cy, r = 190, 330, 210
    rr = np.hypot(xx - cx, yy - cy); ang = np.arctan2(yy - cy, xx - cx)
    head = ((np.abs(rr - r) < 24 * np.clip(1 - np.abs(ang + np.pi / 2) / 1.0, 0.25, 1)) & (ang > -np.pi / 2 - 0.85) & (ang < -np.pi / 2 + 0.85)).astype(np.float32)
    head = blur(head, 1.2)
    c.over(chrome(np.clip(1 - np.abs(rr - r) / 24, 0, 1) ** 0.5 * head, (0.50, 0.52, 0.55), depth=50, sky=0.8, ground=0.1), head)
    return c.image()
