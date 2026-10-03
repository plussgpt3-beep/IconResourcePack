"""สำนักเลขาธิการ: the secretary's writing desk - papers, an inkwell, a candle."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, rect, ellipse, wood, edge_darken, chrome, gold_tint
from petition import quill


def draw():
    rng = np.random.default_rng(604)
    c = Canvas()
    top = blur(poly([(30, 300), (180, 220), (482, 250), (350, 340)]), 1.2)
    c.over(light(0.15 * pillow(top, 10), wood(rng, (0.42, 0.24, 0.11), angle=0.3, rings=14), depth=30, spec=0.3) * edge_darken(top, 8, 0.35), top)
    front = blur(poly([(30, 300), (350, 340), (350, 380), (30, 340)]), 1)
    c.over(wood(rng, (0.30, 0.17, 0.08), rings=8), front)
    for x in (50, 320):
        leg = blur(rect([x, 340, x + 24, 490], 4), 1)
        c.over(light(0.4 * pillow(leg, 6), wood(rng, (0.30, 0.17, 0.08), angle=np.pi / 2, rings=4), depth=30, spec=0.2), leg)
    pap = blur(poly([(120, 270), (250, 240), (300, 290), (170, 320)]), 1)
    c.over(light(0.1 * pap, parchment(rng), depth=20, spec=0.05), pap)
    well = blur(np.maximum(ellipse([330, 240, 390, 290]), rect([340, 220, 380, 265], 8)), 1)
    c.over(light(0.6 * pillow(well, 10), np.zeros((N, N, 3)) + np.array([0.05, 0.06, 0.12]), depth=40, spec=0.9), well)
    quill(c, (355, 230), (440, 60), width=30)
    holder = blur(ellipse([150, 230, 210, 260]), 1)
    c.over(chrome(0.4 * pillow(holder, 6), gold_tint(), depth=30), holder)
    candle = blur(rect([166, 120, 194, 245], 6), 1)
    c.over(light(np.sqrt(np.clip(1 - ((xx - 180) / 14) ** 2, 0, 1)) * candle * 0.6, np.zeros((N, N, 3)) + np.array([0.92, 0.88, 0.78]), depth=30, spec=0.2), candle)
    flame = blur(poly([(180, 60), (194, 100), (180, 120), (166, 100)]), 3)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.75, 0.25]), flame, cast=False)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.85, 0.5]), blur(ellipse([120, 40, 240, 160]), 20) * 0.35, cast=False)
    return c.image()
