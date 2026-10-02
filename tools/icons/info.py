"""รายละเอียด / วิธีใช้: an open book, pages bowing up from the spine."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, parchment, blur, poly, edge_darken, noise


def draw():
    rng = np.random.default_rng(41)
    c = Canvas()
    shadow(c, [40, 400, 472, 490], 0.45, 18)
    # leather cover peeking out under the pages
    cover = blur(poly([(40, 150), (256, 190), (472, 150), (472, 420), (256, 460), (40, 420)]), 1.5)
    leather = np.array([0.45, 0.16, 0.12])[None, None, :] * (0.85 + 0.3 * noise(rng, 30, 3)[..., None])
    c.over(light(pillow(cover, 10) * 0.3, leather, depth=40, spec=0.2) * edge_darken(cover, 8, 0.4), cover)
    # two page blocks, each bowing up from the spine (x=256) to its outer edge
    for side in (-1, 1):
        x_out = 256 + side * 200
        pts = [(256, 175), (256 + side * 100, 120), (x_out, 132), (x_out, 400), (256 + side * 100, 392), (256, 440)]
        pg = blur(poly(pts), 1.2)
        t = np.clip((xx - 256) * side / 200, 0, 1)
        h = (np.sin(t * np.pi * 0.85) * 0.6 + 0.1) * pg
        col = parchment(rng, (0.93, 0.88, 0.74))
        shaded = light(h, col, depth=110, spec=0.05) * edge_darken(pg, 6, 0.2)
        # page edges stacked along the outer border
        stack = np.clip(1 - np.abs((xx - (x_out - side * 8))) / 7, 0, 1) * pg
        shaded *= (1 - 0.15 * (0.5 + 0.5 * np.sin(yy / 2.0)) * stack)[..., None]
        c.over(shaded, pg)
        # lines of text following the bow
        for i in range(7):
            y0 = 175 + i * 30
            bow = -40 * np.sin(np.linspace(0, 1, 2) * np.pi * 0.85)
            a, b = (256 + side * 30, y0 + 8), (256 + side * 170, y0 - 30 + i * 2)
            ln = poly([a, b], width=6)
            c.over(np.zeros((N, N, 3)) + np.array([0.25, 0.20, 0.16]), ln * 0.35 * pg)
    # spine shadow
    gut = np.exp(-((xx - 256) / 10) ** 2) * (yy > 150) * (yy < 450)
    c.over(np.zeros((N, N, 3)), gut * 0.35)
    # a red ribbon bookmark
    rib = blur(poly([(300, 380), (322, 380), (330, 488), (311, 470), (292, 488)]), 1)
    c.over(light(pillow(rib, 4) * 0.2, np.zeros((N, N, 3)) + np.array([0.70, 0.12, 0.12]), depth=30, spec=0.3), rib)
    return c.image()
