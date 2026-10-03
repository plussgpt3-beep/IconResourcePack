"""ไม้กำหนดเขตก่อสร้าง: a master builder's staff - oak, brass-shod, an orange marker cloth tied below its crown."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, wood, chrome, gold_tint, band, cloth


def draw():
    rng = np.random.default_rng(401)
    c = Canvas()
    s, t = band((120, 470), (400, 60), 0)
    st = blur(((s > 0) & (s < 0.92) & (np.abs(t) < 16)).astype(np.float32), 1)
    c.over(light(np.clip(1 - np.abs(t) / 16, 0, 1) ** 0.5 * st, wood(rng, (0.50, 0.32, 0.16), angle=-0.97, rings=4), depth=40, spec=0.3), st)
    for e, w in ((0.03, 0.04), (0.80, 0.03)):
        bandm = blur(((np.abs(s - e) < w) & (np.abs(t) < 19)).astype(np.float32), 1)
        c.over(chrome(np.clip(1 - np.abs(t) / 19, 0, 1) ** 0.5 * bandm, gold_tint(), depth=40), bandm)
    hx, hy = 120 + (400 - 120) * 0.95, 470 + (60 - 470) * 0.95
    head = blur(poly([(hx, hy - 60), (hx + 34, hy), (hx, hy + 40), (hx - 34, hy)]), 1)
    c.over(chrome(pillow(head, 14, 0.7), gold_tint(), depth=60), head)
    rib = blur(poly([(330, 170), (390, 200), (420, 280), (380, 240), (350, 300), (335, 215)]), 1.2)
    c.over(light(0.3 * pillow(rib, 5), cloth(rng, (0.92, 0.45, 0.08)), depth=30, spec=0.1), rib)
    return c.image()
