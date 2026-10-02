"""ดูเขตเมือง: a surveyor's boundary stake driven into a mound, flying a red pennant."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, noise


def draw():
    rng = np.random.default_rng(210)
    c = Canvas()
    mound = blur(ellipse([110, 400, 400, 500]) * (yy > 400), 2)
    soil = np.array([0.30, 0.20, 0.12])[None, None, :] * (0.7 + 0.5 * noise(rng, 30, 3)[..., None])
    grass = (noise(rng, 40, 2) > 0.55) & (yy < 440)
    soil[grass] = soil[grass] * 0 + np.array([0.25, 0.42, 0.15])
    c.over(light(pillow(mound, 20) * 0.6, soil, depth=50, spec=0.05), mound)
    stake = blur(poly([(236, 40), (276, 40), (276, 420), (256, 455), (236, 420)]), 1)
    col = wood(rng, (0.62, 0.45, 0.26), angle=np.pi / 2, rings=5)
    # red-and-white survey bands near the top
    bands = ((yy > 80) & (yy < 200) & (((yy - 80) // 30) % 2 == 0))
    col[bands] = np.array([0.72, 0.10, 0.08])
    c.over(light(np.clip(1 - np.abs(xx - 256) / 22, 0, 1) ** 0.5 * stake * 0.8, col, depth=40, spec=0.2), stake)
    pen = blur(poly([(276, 46), (440, 80), (420, 104), (446, 128), (276, 140)]), 1.2)
    folds = 0.5 + 0.5 * np.sin((xx - 276) / 22.0)
    c.over(light((0.2 + 0.1 * folds) * pen, cloth(rng, (0.70, 0.08, 0.06)), depth=40, spec=0.1), pen)
    return c.image()
