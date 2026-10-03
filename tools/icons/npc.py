"""NPC ประจำเมือง: a townsperson in a hooded cloak."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, cloth, leather_col


def draw():
    rng = np.random.default_rng(607)
    c = Canvas()
    body = blur(poly([(80, 480), (130, 330), (200, 290), (312, 290), (382, 330), (432, 480)]), 1.5)
    nx = (xx - 256) / 176
    c.over(light(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * body * 0.7, cloth(rng, (0.30, 0.22, 0.14), weave=2.5), depth=60, spec=0.05), body)
    hood = blur(ellipse([150, 60, 362, 330]), 1.5)
    hx = (xx - 256) / 106; hy = (yy - 195) / 135
    c.over(light(np.sqrt(np.clip(1 - hx ** 2 - hy ** 2, 0, 1)) * hood * 0.8, cloth(rng, (0.34, 0.25, 0.16), weave=2.5), depth=70, spec=0.05), hood)
    opening = blur(ellipse([188, 120, 324, 300]), 2)
    c.over(np.zeros((N, N, 3)) + 0.08, opening)
    face = blur(ellipse([205, 150, 307, 285]), 2)
    fx = (xx - 256) / 51; fy = (yy - 218) / 67
    skin = np.zeros((N, N, 3)) + np.array([0.78, 0.58, 0.42])
    shade = np.clip(0.35 + 0.65 * np.clip(-fx * 0.5 + 0.6, 0, 1) * np.clip(1 - (fy + 0.3) ** 2, 0, 1), 0, 1)
    c.over(light(np.sqrt(np.clip(1 - fx ** 2 - fy ** 2, 0, 1)) * face * 0.6, skin * shade[..., None], depth=50, spec=0.1), face)
    for ex in (232, 280):
        eye = blur(ellipse([ex - 7, 205, ex + 7, 217]), 1)
        c.over(np.zeros((N, N, 3)) + 0.1, eye)
    belt = blur(rect([150, 420, 362, 440]) * body, 1)
    c.over(light(0.3 * pillow(belt, 3), leather_col(rng, (0.25, 0.14, 0.07)), depth=20, spec=0.2), belt)
    return c.image()
