"""ธงอาณานิคม: a kingdom banner on a tall pole, planted in a heap of fresh earth."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, chrome, gold_tint, noise, edge_darken


def draw():
    rng = np.random.default_rng(1102)
    c = Canvas()
    # heap of earth
    heap = blur(np.clip(ellipse([96, 376, 416, 500]) - rect([0, 470, N, N]) * 0.0, 0, 1), 2)
    soil = np.zeros((N, N, 3)) + np.array([0.36, 0.24, 0.13])
    soil = soil * (0.7 + 0.5 * noise(rng, 18, 4))[..., None]
    c.over(light(pillow(heap, 30, 0.7) * 0.7, soil, depth=50, spec=0.05), heap)
    # pole
    pole = blur(rect([150, 40, 176, 448], 10), 1)
    c.over(light(pillow(pole, 10, 0.5) * 0.8, wood(rng, (0.40, 0.23, 0.10), angle=np.pi / 2, rings=4), depth=60, spec=0.25), pole)
    tip = blur(poly([(163, 8), (184, 48), (142, 48)]), 1)
    c.over(chrome(0.6 * pillow(tip, 8), gold_tint(), depth=50), tip)
    # banner hanging from a cross bar, swallow-tailed, waving
    bar = blur(rect([150, 62, 404, 80], 8), 1)
    c.over(chrome(0.5 * pillow(bar, 6), gold_tint(), depth=40), bar)
    wave = 10 * np.sin((yy - 80) / 40.0)
    flag = blur(((xx > 176 + wave * 0.3) & (xx < 396 + wave) & (yy > 80) & (yy < 330 - 70 * np.clip(1 - np.abs(xx - 286) / 60, 0, 1) * 0.0)).astype(np.float32), 1.5)
    notch = poly([(176, 330), (286, 268), (396, 330), (396, 360), (176, 360)])
    flag = np.clip(flag - blur(notch, 1.5), 0, 1)
    fold = 0.18 * np.sin((xx - 176) / 34.0) * flag
    col = cloth(rng, (0.62, 0.09, 0.08), weave=2.4)
    trim = np.clip(flag - blur((((xx > 194 + wave * 0.3) & (xx < 378 + wave) & (yy > 96) & (yy < 300))).astype(np.float32), 1), 0, 1) * flag
    col = col * (1 - trim[..., None]) + np.array([0.86, 0.66, 0.22]) * trim[..., None]
    c.over(light(0.22 * pillow(flag, 12) + fold, col, depth=50, spec=0.1) * edge_darken(flag, 8, 0.3), flag)
    # a gold tower on the cloth: the kingdom's mark
    tw = blur(np.maximum(rect([262, 150, 318, 250]), poly([(250, 150), (250, 124), (266, 124), (266, 138), (282, 138), (282, 124),
                                                            (298, 124), (298, 138), (314, 138), (314, 124), (330, 124), (330, 150)])), 1.5)
    c.over(chrome(0.4 * pillow(tw, 6), gold_tint(), depth=40), tw)
    return c.image()
