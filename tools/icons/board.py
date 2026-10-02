"""กระดานประกาศ: a wooden notice board with papers pinned to it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, parchment, edge_darken, chrome


def draw():
    rng = np.random.default_rng(213)
    c = Canvas()
    for x in (110, 380):
        post = blur(rect([x, 60, x + 24, 490], 6), 1)
        c.over(light(pillow(post, 8, 0.6) * 0.7, wood(rng, (0.36, 0.22, 0.11), angle=np.pi / 2, rings=5), depth=40, spec=0.2), post)
    brd = blur(rect([80, 90, 432, 400], 10), 1.2)
    planks = sum(np.exp(-((yy - y) / 2.0) ** 2) for y in (167, 245, 322))
    h = 0.2 * pillow(brd, 10) - 0.15 * planks * brd
    c.over(light(h, wood(rng, (0.48, 0.30, 0.15), rings=16), depth=50, spec=0.15) * edge_darken(brd, 12, 0.45), brd)
    roof = blur(poly([(60, 100), (256, 30), (452, 100), (452, 120), (256, 52), (60, 120)]), 1.2)
    c.over(light(pillow(roof, 6) * 0.6, wood(rng, (0.30, 0.17, 0.08), rings=10), depth=40, spec=0.2), roof)
    for (x0, y0, x1, y1, tilt) in [(110, 130, 230, 270, -0.05), (250, 120, 400, 230, 0.06), (150, 270, 280, 380, 0.04), (300, 250, 410, 375, -0.07)]:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        hw, hh = (x1 - x0) / 2, (y1 - y0) / 2
        ca, sa = np.cos(tilt), np.sin(tilt)
        corners = [(cx + ca * dx - sa * dy, cy + sa * dx + ca * dy) for dx, dy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
        pap = blur(poly(corners), 1)
        c.over(np.zeros((N, N, 3)), blur(pap, 6) * 0.35)
        col = parchment(rng, (0.92, 0.88, 0.76))
        for k in range(4):
            yl = y0 + 30 + k * 22
            ln = poly([(x0 + 14, yl), (x1 - 20 - 10 * (k % 2), yl + (x1 - x0) * tilt * 0.3)], width=4)
            col = col * (1 - 0.5 * ln[..., None])
        c.over(light(pap * 0.1, col, depth=20, spec=0.05), pap)
        pin = blur(ellipse([cx - 8, y0 + 2, cx + 8, y0 + 18]), 1)
        c.over(chrome(pillow(pin, 5), (0.80, 0.15, 0.10), depth=30), pin)
    return c.image()
