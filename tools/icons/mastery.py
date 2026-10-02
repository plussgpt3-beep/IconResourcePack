"""ความชำนาญ: a sheaf of ripe wheat bound with a straw band."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, noise


def draw():
    rng = np.random.default_rng(202)
    c = Canvas()
    straw = np.array([0.80, 0.62, 0.28])
    tie_y = 330
    stalks = []
    for k in range(13):
        a = (k - 6) / 6.0
        top = (256 + a * 150 + rng.uniform(-10, 10), 120 + abs(a) * 60 + rng.uniform(-10, 10))
        bot = (256 + a * 70, 490)
        stalks.append((top, bot))
    # stalks: thin straws through the tie, fanning out above it
    for top, bot in stalks:
        m = blur(poly([top, (256 + (top[0] - 256) * 0.25, tie_y), bot], width=8), 1)
        col = straw[None, None, :] * (0.75 + 0.3 * noise(rng, 20, 2)[..., None])
        c.over(light(pillow(m, 3) * 0.5, col, depth=20, spec=0.2), m)
    # ears of grain: a chevron of plump kernels along the last stretch of each stalk
    for top, bot in stalks:
        tx, ty = top; mx, my = 256 + (tx - 256) * 0.25, tie_y
        d = np.array([tx - mx, ty - my]); d /= np.linalg.norm(d); n = np.array([-d[1], d[0]])
        for j in range(7):
            cx = tx - d[0] * j * 13; cy = ty - d[1] * j * 13
            for side in (-1, 1):
                kx, ky = cx + n[0] * side * 8, cy + n[1] * side * 8
                kern = blur(ellipse([kx - 7, ky - 10, kx + 7, ky + 10]), 1)
                col = np.array([0.86, 0.66, 0.30])[None, None, :] * (0.85 + 0.2 * rng.random())
                c.over(light(pillow(kern, 5, 0.6) * 0.6, col * np.ones((N, N, 1)), depth=30, spec=0.35), kern)
        awn = blur(poly([(tx, ty), (tx + d[0] * 45, ty + d[1] * 45)], width=2), 0.8)
        c.over(np.zeros((N, N, 3)) + straw * 0.9, awn * 0.8)
    # the band around the waist of the sheaf
    tie = blur(poly([(196, tie_y - 18), (316, tie_y - 18), (320, tie_y + 18), (192, tie_y + 18)]), 1.5)
    twist = 0.5 + 0.5 * np.sin((xx - yy) / 5.0)
    col = np.array([0.66, 0.48, 0.20])[None, None, :] * (0.6 + 0.4 * twist[..., None])
    c.over(light(pillow(tie, 8) * 0.8, col, depth=40, spec=0.2), tie)
    return c.image()
