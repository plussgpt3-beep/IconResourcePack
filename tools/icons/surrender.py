"""มอบตัว: a plain white flag of truce on a short pole, and a sword laid down across its foot."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, wood, cloth, edge_darken, sword


def draw():
    rng = np.random.default_rng(2481)
    c = Canvas()
    pole = blur(rect([120, 50, 144, 430], 10), 1)
    c.over(light(pillow(pole, 10, 0.5) * 0.8, wood(rng, (0.42, 0.26, 0.12), angle=np.pi / 2, rings=4), depth=60, spec=0.25), pole)
    wave = 14 * np.sin((xx - 144) / 46.0)
    flag = blur(((xx > 144) & (xx < 410) & (yy > 70 + wave) & (yy < 260 + wave)).astype(np.float32), 1.5)
    fold = 0.22 * np.sin((xx - 144) / 30.0) * flag
    col = cloth(rng, (0.93, 0.92, 0.88), weave=2.2)
    c.over(light(0.2 * pillow(flag, 12) + fold, col, depth=50, spec=0.08) * edge_darken(flag, 8, 0.25), flag)
    sword(c, rng, (440, 470), (90, 380), blade_w=24, guard_w=64)
    return c.image()
