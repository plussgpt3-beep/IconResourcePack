"""จำนวน: a counting frame - wooden beads on brass rods in an oak frame."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, gold_tint


def draw():
    rng = np.random.default_rng(509)
    c = Canvas()
    frame = blur(np.clip(rect([60, 80, 452, 440], 14) - rect([92, 112, 420, 408], 6), 0, 1), 1.2)
    c.over(light(0.4 * pillow(frame, 10), wood(rng, (0.42, 0.24, 0.11), rings=8), depth=40, spec=0.25), frame)
    colors = [(0.70, 0.12, 0.08), (0.80, 0.60, 0.15), (0.20, 0.40, 0.15), (0.15, 0.25, 0.55), (0.70, 0.12, 0.08)]
    for r in range(5):
        y = 150 + r * 60
        rod = blur(rect([92, y - 4, 420, y + 4]), 0.8)
        c.over(chrome(0.4 * rod, gold_tint(), depth=20), rod)
        n = 3 + (r * 2) % 4
        for k in range(n):
            bx = 120 + k * 42 if k < n - 1 else 380
            bead = blur(ellipse([bx - 20, y - 22, bx + 20, y + 22]), 1)
            c.over(light(pillow(bead, 10, 0.6), np.zeros((N, N, 3)) + np.array(colors[r]), depth=40, spec=0.5), bead)
    return c.image()
