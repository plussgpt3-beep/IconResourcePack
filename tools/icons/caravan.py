"""การค้าระหว่างเมือง: a merchant's two-wheeled cart loaded with crates and a sack."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, edge_darken, chrome


def wheel(c, rng, cx, cy, r):
    rr = np.hypot(xx - cx, yy - cy); ang = np.arctan2(yy - cy, xx - cx)
    rim = blur(((rr < r) & (rr > r - 18)).astype(np.float32), 1)
    spokes = blur(((np.abs(np.sin(ang * 4)) < 0.10 * r / (rr + 1)) & (rr < r - 10)).astype(np.float32), 1)
    hub = blur((rr < 20).astype(np.float32), 1)
    col = wood(rng, (0.42, 0.25, 0.12), rings=8)
    c.over(light(pillow(spokes, 4) * 0.5, col, depth=30, spec=0.2), spokes)
    c.over(light(pillow(rim, 6) * 0.6, col, depth=40, spec=0.2), rim)
    iron = blur(((rr < r + 2) & (rr > r - 5)).astype(np.float32), 1)
    c.over(chrome(pillow(iron, 3) * 0.5, (0.45, 0.45, 0.48), depth=30, ground=0.1), iron)
    c.over(chrome(pillow(hub, 8) * 0.8, (0.45, 0.45, 0.48), depth=30, ground=0.1), hub)


def draw():
    rng = np.random.default_rng(218)
    c = Canvas()
    shafts = blur(poly([(330, 330), (490, 300)], width=14), 1)
    c.over(light(pillow(shafts, 4) * 0.6, wood(rng, (0.45, 0.27, 0.13), rings=6), depth=30, spec=0.2), shafts)
    # load: crates and a sack
    for (x0, y0, x1, y1) in ((70, 170, 200, 300), (190, 200, 310, 300), (120, 90, 230, 180)):
        cr = blur(rect([x0, y0, x1, y1], 5), 1)
        lines = sum(np.exp(-((yy - (y0 + (y1 - y0) * k / 3)) / 2.0) ** 2) for k in (1, 2))
        c.over(light(0.2 * pillow(cr, 6) - 0.15 * lines * cr, wood(rng, (0.58, 0.40, 0.22), rings=12), depth=40, spec=0.1) * edge_darken(cr, 8, 0.4), cr)
    sack = blur(ellipse([250, 130, 350, 230]), 1.5)
    nx = (xx - 300) / 50; ny = (yy - 180) / 50
    c.over(light(np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * sack, cloth(rng, (0.62, 0.50, 0.32), weave=2), depth=50, spec=0.05), sack)
    # bed of the cart
    bed = blur(rect([50, 290, 350, 340], 6), 1)
    c.over(light(0.2 * pillow(bed, 6), wood(rng, (0.38, 0.22, 0.10), rings=10), depth=40, spec=0.15) * edge_darken(bed, 8, 0.4), bed)
    wheel(c, rng, 190, 380, 100)
    return c.image()
