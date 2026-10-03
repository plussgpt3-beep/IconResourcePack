"""รับซื้อ: an empty wicker basket waiting to be filled."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, edge_darken, mask_from


def draw():
    c = Canvas()
    body = blur(poly([(70, 220), (442, 220), (400, 470), (112, 470)]), 1.2)
    weave = 0.55 + 0.45 * (np.sin(xx / 9.0) * np.sin(yy / 9.0) > 0)
    col = np.array([0.70, 0.52, 0.28])[None, None, :] * weave[..., None]
    nx = (xx - 256) / 186
    c.over(light(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * body * 0.7, col, depth=60, spec=0.1) * edge_darken(body, 10, 0.35), body)
    inner = blur(ellipse([90, 190, 422, 260]), 1)
    c.over(np.array([0.30, 0.20, 0.10])[None, None, :] * weave[..., None] * 0.8, inner)
    rim = blur(np.clip(ellipse([66, 180, 446, 270]) - ellipse([90, 192, 422, 258]), 0, 1), 1)
    tw = 0.5 + 0.5 * np.sin((xx + yy) / 5.0)
    c.over(light(0.5 * pillow(rim, 4), np.zeros((N, N, 3)) + np.array([0.75, 0.56, 0.30]) * (0.7 + 0.3 * tw[..., None]), depth=30, spec=0.15), rim)
    handle = blur(mask_from(lambda d: d.arc([120, 40, 392, 400], 190, 350, fill=255, width=22)), 1)
    c.over(light(0.5 * pillow(handle, 6), np.zeros((N, N, 3)) + np.array([0.72, 0.54, 0.29]) * (0.7 + 0.3 * tw[..., None]), depth=40, spec=0.15), handle)
    return c.image()
