"""ฎีกาหมวดบั๊ก: a black beetle crawling across a written report."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, parchment, edge_darken, chrome


def draw():
    rng = np.random.default_rng(1311)
    c = Canvas()
    sheet = blur(poly([(80, 70), (400, 58), (418, 430), (96, 446)]), 1.2)
    col = parchment(rng)
    for k in range(8):
        y = 120 + k * 38
        ln = poly([(120, y), (360 - (k % 3) * 40, y)], width=6)
        col = col * (1 - 0.4 * ln[..., None])
    c.over(light(0.12 * pillow(sheet, 8), col, depth=40, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    shell = (0.16, 0.20, 0.17)
    cx, cy = 262, 270
    legs = np.zeros((N, N), np.float32)
    for side in (-1, 1):
        for k, dy in enumerate((-40, 0, 40)):
            knee = (cx + side * 92, cy + dy - 18 + k * 6)
            foot = (cx + side * 128, cy + dy + 22 + k * 10)
            legs = np.maximum(legs, poly([(cx + side * 40, cy + dy), knee, foot], width=11))
    for side in (-1, 1):
        legs = np.maximum(legs, poly([(cx + side * 16, cy - 118), (cx + side * 46, cy - 168), (cx + side * 70, cy - 176)], width=8))
    legs = blur(legs, 1)
    c.over(light(0.3 * pillow(legs, 4), np.zeros((N, N, 3)) + np.array([0.10, 0.10, 0.09]), depth=30, spec=0.4), legs)
    head = blur(ellipse([cx - 34, cy - 140, cx + 34, cy - 84]), 1)
    c.over(chrome(pillow(head, 14, 0.7) * 0.8, shell, depth=60, sky=1.2), head)
    body = blur(ellipse([cx - 70, cy - 100, cx + 70, cy + 104]), 1.2)
    seam = np.clip(1 - np.abs(xx - cx) / 3, 0, 1) * (yy > cy - 96)
    h = pillow(body, 40, 0.6) - 0.12 * seam
    c.over(chrome(h, shell, depth=80, sky=1.3), body)
    return c.image()
