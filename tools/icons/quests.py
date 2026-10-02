"""เควส: an open scroll of tasks, the first ones ticked off."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, rect, ellipse, edge_darken, wood


def draw():
    rng = np.random.default_rng(214)
    c = Canvas()
    sheet = blur(rect([110, 90, 402, 420]), 1)
    col = parchment(rng)
    tick_col = np.array([0.18, 0.45, 0.12])
    for k in range(5):
        y = 150 + k * 52
        box = rect([140, y - 14, 168, y + 14])
        boxi = rect([145, y - 9, 163, y + 9])
        col = col * (1 - 0.6 * np.clip(box - boxi, 0, 1)[..., None])
        ln = poly([(190, y), (370 - (k % 3) * 30, y)], width=6)
        col = col * (1 - 0.45 * ln[..., None])
    sh = (0.12 + 0.03 * np.sin(yy / 25.0)) * sheet
    c.over(light(sh, col, depth=50, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    for k in range(3):
        y = 150 + k * 52
        tick = blur(poly([(142, y - 2), (154, y + 12), (180, y - 22)], width=7), 1)
        c.over(np.zeros((N, N, 3)) + tick_col, tick * 0.95)
    # the rolled top and bottom, on wooden rods with knobs
    for y in (80, 430):
        roll = blur(rect([96, y - 26, 416, y + 26], 26), 1)
        cyl = np.sqrt(np.clip(1 - ((yy - y) / 26) ** 2, 0, 1))
        c.over(light(cyl * roll * 0.8, parchment(rng, (0.84, 0.74, 0.54)), depth=60, spec=0.05), roll)
        for x in (82, 430):
            kn = blur(ellipse([x - 20, y - 20, x + 20, y + 20]), 1)
            c.over(light(pillow(kn, 10, 0.7), wood(rng, (0.40, 0.22, 0.10), rings=4), depth=40, spec=0.4), kn)
    return c.image()
