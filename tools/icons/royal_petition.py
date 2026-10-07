"""ฎีกา / ศาลาฎีกา: the brass bell the people ring to be heard, over a petition scroll tied with red cord."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, parchment, chrome, edge_darken, wood


def draw():
    rng = np.random.default_rng(1207)
    c = Canvas()
    brass = (0.98, 0.74, 0.34)
    # the wooden yoke and the bell hanging from it
    beam = blur(rect([120, 40, 392, 76], 12), 1)
    c.over(light(pillow(beam, 10) * 0.7, wood(rng, (0.40, 0.22, 0.10), rings=6), depth=50, spec=0.25), beam)
    hook = blur(rect([244, 70, 268, 104], 6), 1)
    c.over(chrome(pillow(hook, 4) * 0.5, brass, depth=40), hook)
    bell = blur(np.maximum(poly([(166, 300), (346, 300), (318, 150), (256, 96), (194, 150)]),
                           ellipse([150, 272, 362, 322])), 1.2)
    h = np.clip(1 - np.abs(xx - 256) / 120, 0, 1) ** 0.6 * bell
    c.over(chrome(h * 0.9, brass, depth=70), bell)
    lip = blur(ellipse([148, 284, 364, 328]) * (yy > 298), 1)
    c.over(chrome(pillow(lip, 8) * 0.7, (0.85, 0.60, 0.25), depth=40), lip)
    band = blur(rect([196, 168, 316, 184], 6), 1)
    c.over(chrome(pillow(band, 4) * 0.5, (0.80, 0.55, 0.22), depth=40), band)
    clapper = blur(ellipse([242, 312, 270, 342]), 1)
    c.over(chrome(pillow(clapper, 8), (0.55, 0.42, 0.25), depth=40), clapper)
    # the rolled petition lying in front, tied with red cord
    roll = blur(rect([64, 370, 448, 448], 38), 1.5)
    across = np.clip(1 - np.abs(yy - 409) / 40, 0, 1)
    col = parchment(rng, (0.93, 0.85, 0.64))
    c.over(light(0.6 * across ** 0.5 * roll, col, depth=60, spec=0.08) * edge_darken(roll, 8, 0.3), roll)
    end = blur(ellipse([412, 370, 466, 448]), 1.2)
    rings = 0.5 + 0.5 * np.sin(np.hypot(xx - 439, yy - 409) / 3.2)
    c.over(light(0.25 * pillow(end, 10), col * (0.75 + 0.2 * rings[..., None]), depth=30, spec=0.05), end)
    red = np.zeros((N, N, 3)) + np.array([0.70, 0.08, 0.07])
    for x in (236, 262):
        cord = blur(rect([x, 364, x + 14, 454], 6), 1)
        c.over(light(0.3 * pillow(cord, 4), red, depth=30, spec=0.3), cord)
    tail = blur(poly([(248, 446), (226, 500), (242, 504), (262, 452)]), 1)
    c.over(light(0.2 * pillow(tail, 4), red * 0.9, depth=30, spec=0.2), tail)
    return c.image()
