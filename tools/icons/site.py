"""เขตก่อสร้าง: timber scaffolding lashed together around a half-built stone wall."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, wood, stone, noise, edge_darken


def draw():
    rng = np.random.default_rng(403)
    c = Canvas()
    wall = blur(poly([(120, 470), (120, 260), (200, 250), (250, 300), (330, 230), (400, 280), (400, 470)]), 1)
    row = (yy // 34).astype(int)
    joints = (((xx + (row % 2) * 34) % 68 < 3) | (yy % 34 < 3)).astype(np.float32)
    c.over(light(0.2 * wall - 0.1 * joints * wall, stone(rng, (0.62, 0.58, 0.52)) * (1 - 0.4 * joints[..., None]), depth=30, spec=0.05) * edge_darken(wall, 8, 0.3), wall)
    col = wood(rng, (0.62, 0.45, 0.24), angle=np.pi / 2, rings=4)
    poles = [(90, 60, 470), (256, 40, 470), (430, 70, 470)]
    for x, y0, y1 in poles:
        p = blur(rect([x - 12, y0, x + 12, y1], 6), 1)
        c.over(light(np.clip(1 - np.abs(xx - x) / 12, 0, 1) ** 0.5 * p, col, depth=30, spec=0.2), p)
    hcol = wood(rng, (0.58, 0.42, 0.22), rings=4)
    for y in (150, 300):
        b = blur(rect([70, y - 10, 450, y + 10], 6), 1)
        c.over(light(np.clip(1 - np.abs(yy - y) / 10, 0, 1) ** 0.5 * b, hcol, depth=30, spec=0.2), b)
        plank = blur(rect([80, y - 34, 440, y - 12], 3), 1)
        c.over(light(0.15 * pillow(plank, 4), wood(rng, (0.70, 0.52, 0.30), rings=10), depth=30, spec=0.1) * edge_darken(plank, 4, 0.3), plank)
    br = blur(np.maximum(poly([(90, 300), (256, 150)], width=12), poly([(256, 300), (430, 150)], width=12)), 1)
    c.over(light(0.3 * pillow(br, 4), hcol, depth=30, spec=0.2), br)
    for x, y in [(90, 150), (256, 150), (430, 150), (90, 300), (256, 300), (430, 300)]:
        lash = blur(rect([x - 16, y - 14, x + 16, y + 14], 6), 1)
        stripes = 0.5 + 0.5 * np.sin((xx + yy) / 3.0)
        c.over(light(0.3 * pillow(lash, 4), np.zeros((N, N, 3)) + np.array([0.75, 0.62, 0.40]) * (0.7 + 0.3 * stripes[..., None]), depth=20, spec=0.1), lash)
    return c.image()
