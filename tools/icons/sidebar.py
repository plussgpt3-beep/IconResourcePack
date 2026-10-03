"""UI สถานะข้างจอ: a tall status tablet - a dark slate in a carved frame, a gold heading and coloured lines of figures down its side."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, gold_tint, noise, edge_darken


def draw():
    rng = np.random.default_rng(1104)
    c = Canvas()
    frame = blur(rect([120, 30, 392, 482], 22), 1.5)
    c.over(light(pillow(frame, 18, 0.6) * 0.8, wood(rng, (0.44, 0.26, 0.12), angle=np.pi / 2, rings=9), depth=60, spec=0.25), frame)
    slate = blur(rect([146, 58, 366, 454], 10), 1.2)
    col = np.zeros((N, N, 3)) + np.array([0.13, 0.15, 0.20])
    col = col * (0.85 + 0.25 * noise(rng, 14, 3))[..., None]
    # heading bar in gold, then rows: label (pale) + value (colour), like the side board in game
    head = blur(rect([174, 82, 338, 108], 6), 1)
    col = col * (1 - head[..., None]) + np.array([0.95, 0.72, 0.20]) * head[..., None]
    values = [(0.40, 0.85, 0.95), (0.95, 0.85, 0.30), (0.45, 0.90, 0.40), (0.95, 0.40, 0.35), (0.80, 0.55, 0.95), (0.95, 0.85, 0.30)]
    for k, v in enumerate(values):
        y = 146 + k * 50
        lab = blur(rect([174, y, 174 + 70 + 14 * (k % 3), y + 14], 5), 1)
        val = blur(rect([272, y + 22, 272 + 66 - 10 * (k % 2), y + 36], 5), 1)
        col = col * (1 - lab[..., None]) + np.array([0.82, 0.82, 0.86]) * lab[..., None]
        col = col * (1 - val[..., None]) + np.array(v) * val[..., None]
    c.over(light(0.06 * pillow(slate, 8), col, depth=20, spec=0.25) * edge_darken(slate, 12, 0.5), slate)
    for (x, y) in ((136, 46), (376, 46), (136, 466), (376, 466)):
        rivet = blur(ellipse([x - 12, y - 12, x + 12, y + 12]), 1)
        c.over(chrome(0.5 * pillow(rivet, 6), gold_tint(), depth=40), rivet)
    return c.image()
