"""เมืองทั้งหมด: an unrolled map of the realm with towns, roads and a coastline."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, ellipse, noise, edge_darken


def draw():
    rng = np.random.default_rng(209)
    c = Canvas()
    # the sheet, its top and bottom edges rolled into short cylinders
    sheet = blur(poly([(80, 110), (432, 90), (440, 420), (72, 440)]), 1.2)
    col = parchment(rng)
    land = noise(rng, 110, 3)
    sea = (land < 0.45).astype(np.float32) * sheet
    col = col * (1 - sea[..., None] * np.array([0.45, 0.22, 0.0]))
    coast = np.clip(1 - np.abs(land - 0.45) / 0.012, 0, 1) * sheet
    col = col * (1 - 0.6 * coast[..., None])
    wave = 0.04 * np.sin(xx / 30.0)
    c.over(light((0.15 + wave) * sheet, col, depth=60, spec=0.05) * edge_darken(sheet, 14, 0.4), sheet)
    # roads (dashed ink) joining the towns
    towns = [(150, 190), (300, 170), (380, 300), (210, 340), (290, 390)]
    for a, b in [(0, 1), (1, 2), (0, 3), (3, 4), (2, 4)]:
        p, q = np.array(towns[a]), np.array(towns[b])
        for k in range(0, 10, 2):
            s0, s1 = k / 10, (k + 1) / 10
            seg = blur(poly([tuple(p + (q - p) * s0), tuple(p + (q - p) * s1)], width=5), 1)
            c.over(np.zeros((N, N, 3)) + np.array([0.35, 0.22, 0.12]), seg * 0.8)
    for i, (tx, ty) in enumerate(towns):
        r = 18 if i == 1 else 12
        dot = blur(ellipse([tx - r, ty - r, tx + r, ty + r]), 1)
        c.over(light(pillow(dot, 5) * 0.6, np.zeros((N, N, 3)) + (np.array([0.70, 0.10, 0.08]) if i == 1 else np.array([0.20, 0.14, 0.10])), depth=30, spec=0.4), dot)
    # rolled ends
    for y0, y1 in ((84, 128), (414, 458)):
        roll = blur(poly([(64, y0 + (6 if y0 > 200 else 14)), (446, y0 - (8 if y0 < 200 else -2)), (448, y1 - (8 if y0 < 200 else -2)), (62, y1 + (6 if y0 > 200 else 14))]), 1.2)
        cyl = np.clip(1 - np.abs((yy - (y0 + y1) / 2) / ((y1 - y0) / 2)), 0, 1) ** 0.5
        c.over(light(cyl * roll * 0.8, parchment(rng, (0.82, 0.72, 0.52)), depth=60, spec=0.05), roll)
    return c.image()
