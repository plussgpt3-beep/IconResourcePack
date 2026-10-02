"""อาชีพ: a guild medal - a bronze medallion with a gear, hung on a ribbon."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, chrome, cloth


def draw():
    rng = np.random.default_rng(203)
    c = Canvas()
    # ribbon: two tails meeting under the medal, folded at the top
    for pts, shade in (([(150, 40), (240, 40), (290, 260), (220, 290)], 0.85), ([(272, 40), (362, 40), (292, 290), (222, 260)], 1.0)):
        rb = blur(poly(pts), 1.2)
        col = cloth(rng, (0.12, 0.20, 0.50)) * shade
        stripe = np.exp(-((xx - (pts[0][0] + pts[1][0]) / 2 - (yy - 40) * 0.25 * (1 if shade < 1 else -1)) / 9) ** 2)
        col = col * (1 - stripe[..., None]) + np.array([0.75, 0.55, 0.15]) * stripe[..., None]
        c.over(light(pillow(rb, 6) * 0.3, col, depth=30, spec=0.1), rb)
    # medallion: raised rim, inner field, embossed star over crossed hammer
    cx, cy, r = 256, 330, 140
    disc = blur(ellipse([cx - r, cy - r, cx + r, cy + r]), 1.5)
    rr = np.hypot(xx - cx, yy - cy) / r
    h = 0.45 * np.clip(1 - rr, 0, 1) ** 0.25 + 0.30 * np.exp(-((rr - 0.88) / 0.05) ** 2)
    # embossed gear: the guilds' mark of craft and trade
    ang = np.arctan2(yy - cy, xx - cx); d = np.hypot(xx - cx, yy - cy)
    teeth = 78 + 16 * (np.cos(ang * 10) > 0.2)
    gear = ((d < teeth) & (d > 30)).astype(np.float32)
    h = h + 0.22 * blur(gear, 2.5)
    c.over(chrome(h * disc, (0.86, 0.56, 0.30), depth=60, ground=0.22), disc)
    # the ring the ribbon passes through
    ring = blur(np.clip(ellipse([cx - 24, cy - r - 40, cx + 24, cy - r + 8]) - ellipse([cx - 13, cy - r - 29, cx + 13, cy - r - 3]), 0, 1), 1)
    c.over(chrome(pillow(ring, 4) * 0.7, (0.86, 0.56, 0.30), depth=40), ring)
    return c.image()
