"""ขมิ้น (สมุนไพร, 2026-10-25): knobbly turmeric roots, one cut to show its deep orange flesh."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, ellipse, poly, noise


def draw():
    rng = np.random.default_rng(2604)
    c = Canvas()
    skin = (0.66, 0.46, 0.24)
    for (p0, p1, w) in (((110, 320), (290, 270), 86), ((200, 290), (225, 165), 68), ((270, 270), (370, 215), 64), ((140, 330), (125, 420), 58)):
        f = blur(poly([p0, p1], width=w), 7)
        rings = 0.86 + 0.14 * np.abs(np.sin((xx + yy) / 11.0))
        col = np.array(skin)[None, None, :] * (rings * (0.9 + 0.12 * noise(rng, 16, 2)))[..., None]
        c.over(light(0.5 * pillow(f, 18), np.clip(col, 0, 1), depth=45, spec=0.12), f)
    # a cut slice, bright orange inside a brown rim
    rim = blur(ellipse([290, 320, 450, 470]), 1.2)
    c.over(light(0.4 * pillow(rim, 14), np.zeros((N, N, 3)) + np.array(skin) * 0.85, depth=40, spec=0.1), rim)
    face = blur(ellipse([302, 332, 438, 458]), 1.2)
    rr = np.hypot((xx - 370) / 68, (yy - 395) / 63)
    col = np.array([0.98, 0.58, 0.06])[None, None, :] * (0.85 + 0.15 * np.cos(rr * 9))[..., None] * (0.92 + 0.1 * noise(rng, 12, 2))[..., None]
    c.over(light(0.2 * pillow(face, 10), np.clip(col, 0, 1), depth=30, spec=0.3), face)
    return c.image()
