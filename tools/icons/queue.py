"""คิวคำร้อง: a stack of petitions waiting, tied with a ribbon."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, edge_darken


def draw():
    rng = np.random.default_rng(309)
    c = Canvas()
    for k in range(6):
        off = 5 - k
        dx, dy = (k % 2) * 14 - 7, -k * 24
        pts = [(100 + dx, 300 + dy), (380 + dx, 280 + dy), (430 + dx, 360 + dy), (150 + dx, 382 + dy)]
        m = blur(poly(pts), 1.2)
        col = parchment(rng, (0.90 - 0.02 * off, 0.82 - 0.02 * off, 0.62))
        if k == 5:
            for j in range(4):
                ln = poly([(160 + dx + j * 14, 300 + dy + j * 16), (360 + dx + j * 14, 285 + dy + j * 16)], width=5)
                col = col * (1 - 0.4 * ln[..., None])
        c.over(light(0.12 * pillow(m, 8), col, depth=40, spec=0.05) * edge_darken(m, 8, 0.35), m)
        side = blur(poly([pts[3], pts[2], (pts[2][0], pts[2][1] + 12), (pts[3][0], pts[3][1] + 12)]), 1)
        c.over(parchment(rng, (0.70, 0.60, 0.42)), side)
    rib = blur(poly([(250, 160), (290, 380)], width=22), 1)
    c.over(light(0.2 * pillow(rib, 4), np.zeros((N, N, 3)) + np.array([0.60, 0.08, 0.08]), depth=30, spec=0.3), rib)
    return c.image()
