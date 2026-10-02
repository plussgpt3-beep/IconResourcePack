"""ตำแหน่ง: a steel great helm with a gold trim and a red plume - rank and office."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, steel_tint, gold_tint, cloth, noise


def draw():
    rng = np.random.default_rng(211)
    c = Canvas()
    # plume
    pl = blur(poly([(250, 120), (300, 40), (360, 30), (330, 70), (290, 130)]), 2)
    strands = 0.5 + 0.5 * np.sin((xx + yy * 0.6) / 4.0)
    c.over(light(pillow(pl, 10) * 0.6, cloth(rng, (0.62, 0.06, 0.05)) * (0.8 + 0.3 * strands[..., None]), depth=40, spec=0.1), pl)
    # helm: a rounded top over straight cheeks
    helm = blur(np.maximum(ellipse([120, 100, 392, 320]), rect([120, 210, 392, 470], 30)), 1.5)
    nx = (xx - 256) / 136
    h = np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * helm * 0.9
    # eye slit and breaths
    slit = blur(rect([150, 250, 362, 272], 8), 1)
    holes = np.zeros((N, N), np.float32)
    for k in range(5):
        for j in range(3):
            x = 300 + j * 20; y = 330 + k * 22
            holes = np.maximum(holes, ellipse([x - 5, y - 5, x + 5, y + 5]))
    ridge = np.exp(-((xx - 256) / 7) ** 2) * (yy < 250)
    h = h + 0.15 * ridge * helm - 0.3 * slit
    c.over(chrome(h, (0.66, 0.70, 0.76), depth=70, sky=0.85, ground=0.12), helm)
    c.over(np.zeros((N, N, 3)) + 0.03, slit)
    c.over(np.zeros((N, N, 3)) + 0.05, blur(holes, 1))
    # gold trim along the bottom and down the middle
    trim = blur(rect([120, 440, 392, 470], 10), 1) + blur(rect([250, 280, 262, 440]), 1)
    trim = np.clip(trim, 0, 1) * helm
    c.over(chrome(pillow(trim, 4) * 0.5 + h * 0.3, gold_tint(), depth=50), trim)
    return c.image()
