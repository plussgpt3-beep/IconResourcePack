"""รักษา: a red heart bound with a white linen bandage - the clinic's care."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, rect, cloth, edge_darken
from _clinic import heart


def draw():
    rng = np.random.default_rng(2507)
    c = Canvas()
    m = heart(c, 256, 280, 1.15)
    ang = -0.45
    u = (xx - 256) * np.cos(ang) + (yy - 270) * np.sin(ang)
    v = -(xx - 256) * np.sin(ang) + (yy - 270) * np.cos(ang)
    strip = blur(((np.abs(v) < 44) & (np.abs(u) < 230)).astype(np.float32), 1.5) * blur(m, 6)
    folds = 0.86 + 0.14 * np.sin(v / 7.0)
    c.over(light(0.4 * pillow(strip, 10), cloth(rng, (0.95, 0.93, 0.88), 2.2) * folds[..., None], depth=40, spec=0.1)
           * edge_darken(strip, 6, 0.2), strip)
    return c.image()
