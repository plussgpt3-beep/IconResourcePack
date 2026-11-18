"""กระเป๋าเสริม Tier 1 ย่ามหนังสัตว์ (+9 ช่อง): a small rawhide drawstring pouch, the cord tied off with a knot."""
import numpy as np
from lib import Canvas, blur, poly, ellipse, leather_col, cloth, noise
from _bag import part, strap


def draw():
    rng = np.random.default_rng(1101)
    c = Canvas()
    neck = blur(poly([(196, 150), (316, 150), (300, 200), (212, 200)]), 1.5)
    part(c, neck, leather_col(rng, (0.52, 0.35, 0.20)), 0.3, 8)
    for i, x in enumerate(range(186, 330, 24)):
        fr = blur(poly([(x, 160), (x + 14, 96 + (i % 2) * 18), (x + 26, 160)]), 1.2)
        part(c, fr, leather_col(rng, (0.55, 0.38, 0.22)), 0.25, 5, 40)
    body = blur(ellipse([110, 180, 402, 450]), 2)
    spots = (noise(rng, 40) > 0.62).astype(np.float32)
    alb = leather_col(rng, (0.58, 0.40, 0.24)) * (1 - 0.18 * spots[..., None])
    part(c, body, alb, 0.35, 30, 60, 0.15, 0.5)
    for y in range(220, 430, 22):
        st = blur(poly([(248, y), (264, y + 10)], width=5), 1)
        part(c, st, cloth(rng, (0.85, 0.78, 0.60), weave=1.0), 0.2, 2, 20, 0.1, 0.2)
    strap(c, rng, (200, 196), (312, 196), 14, (0.30, 0.18, 0.08))
    knot = blur(ellipse([288, 182, 322, 214]), 1)
    part(c, knot, leather_col(rng, (0.30, 0.18, 0.08)), 0.4, 8, 40)
    strap(c, rng, (306, 206), (346, 276), 10, (0.30, 0.18, 0.08))
    strap(c, rng, (310, 204), (368, 250), 10, (0.30, 0.18, 0.08))
    return c.image()
