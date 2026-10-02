"""ว่าง / ไม่มีรายการ: an empty turned wooden bowl."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, wood, blur, ellipse, mask_from, edge_darken


def draw():
    rng = np.random.default_rng(61)
    c = Canvas()
    shadow(c, [70, 380, 442, 470], 0.5, 18)
    # outer body: the lower half of an ellipse below the rim, plus the rim ellipse
    body = mask_from(lambda d: (d.chord([60, 60, 452, 440], 0, 180, fill=255), d.ellipse([60, 170, 452, 330], fill=255)))
    body = blur(body, 1.5)
    nx = (xx - 256) / 196; ny = (yy - 250) / 190
    h = np.sqrt(np.clip(1 - nx**2 - (ny * 0.9)**2, 0, 1)) * body
    col = wood(rng, (0.62, 0.40, 0.22), angle=0.0, rings=20)
    c.over(light(h, col, depth=90, spec=0.35, gloss=25) * edge_darken(body, 10, 0.35), body)
    # inside: a darker hollow, lit on the far (lower right) wall
    inner = blur(ellipse([88, 186, 424, 316]), 1.5)
    u = (xx - 256) / 168; v = (yy - 251) / 65
    wall = np.clip(0.35 + 0.65 * np.clip(u * 0.55 + v * 0.75, -1, 1), 0, 1)
    hollow = wood(rng, (0.48, 0.30, 0.16), angle=0.3, rings=14) * (0.45 + 0.6 * wall)[..., None]
    c.over(np.clip(hollow, 0, 1), inner)
    # rim highlight
    rim = blur(np.clip(ellipse([60, 170, 452, 330]) - ellipse([88, 186, 424, 316]), 0, 1), 1)
    c.over(np.clip(col * 1.25, 0, 1), rim * 0.8)
    return c.image()
