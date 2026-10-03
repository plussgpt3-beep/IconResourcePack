"""ขุนนาง: a noble house's coat of arms - a quartered shield, red and gold, a gold rim."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, cloth


def draw():
    rng = np.random.default_rng(603)
    c = Canvas()
    shape = [(80, 60), (432, 60), (432, 250), (400, 360), (256, 470), (112, 360), (80, 250)]
    shield = blur(poly(shape), 1.5)
    nx = (xx - 256) / 176
    h = np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * shield * 0.6
    q = ((xx < 256) ^ (yy < 250))
    col = np.where(q[..., None], np.array([0.62, 0.08, 0.08]), np.array([0.85, 0.65, 0.20]))
    c.over(light(h, col * (0.9 + 0.15 * np.random.default_rng(3).random((N, N)))[..., None] ** 0, depth=60, spec=0.3), shield)
    inner = blur(poly([(104, 82), (408, 82), (408, 246), (380, 346), (256, 442), (132, 346), (104, 246)]), 1)
    rim = np.clip(shield - inner, 0, 1)
    c.over(chrome(0.5 * pillow(rim, 4) + h * 0.5, gold_tint(), depth=40), rim)
    ang = np.arctan2(yy - 250, xx - 256); d = np.hypot(xx - 256, yy - 250)
    star = blur((d < 56 * (0.45 + 0.55 * np.abs(np.cos(2.5 * (ang + np.pi / 2))) ** 3)).astype(np.float32), 1.5)
    c.over(chrome(0.6 * pillow(star, 6), (0.85, 0.86, 0.90), depth=40), star)
    return c.image()
