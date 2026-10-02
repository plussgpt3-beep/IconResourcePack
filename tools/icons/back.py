"""ย้อนกลับ: an arrow of polished oak curving back over the top, head pointing down-left."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, wood, blur, poly, ellipse, edge_darken


def draw():
    rng = np.random.default_rng(91)
    c = Canvas()
    shadow(c, [80, 410, 450, 486], 0.4, 18)
    cx, cy, r, w = 280, 300, 125, 30
    rr = np.hypot(xx - cx, yy - cy)
    band = ((np.abs(rr - r) < w) & (yy <= cy)).astype(np.float32)
    tail = ellipse([cx + r - w, cy - w, cx + r + w, cy + w]) * (yy > cy)      # rounded end on the right
    head = poly([(cx - r - 72, cy - 6), (cx - r + 72, cy - 6), (cx - r, cy + 105)])
    arrow = blur(np.clip(band + tail + head, 0, 1), 1.5)
    h = pillow(arrow, 14, 0.6)
    ang = np.arctan2(yy - cy, xx - cx)
    col = wood(rng, (0.60, 0.38, 0.20), angle=0.0, rings=14)
    c.over(light(h, col, depth=80, spec=0.35, gloss=22) * edge_darken(arrow, 8, 0.4), arrow)
    return c.image()
