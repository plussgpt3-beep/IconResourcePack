"""กระเป๋าเสริม Tier 5 กระเป๋าราชสำนัก (+45 ช่อง): a deep crimson leather bag trimmed in gold, a gold clasp and a stitched crown."""
import numpy as np
from lib import Canvas, blur, poly, rect, ellipse, leather_col, gold_tint, cloth
from _bag import part, metal_part, rivets


def draw():
    rng = np.random.default_rng(1105)
    c = Canvas()
    handle = blur(poly([(186, 150), (200, 66), (312, 66), (326, 150)], width=24), 1.5)
    part(c, handle, leather_col(rng, (0.40, 0.08, 0.10)), 0.35, 8, 40, 0.3)
    body = blur(rect([76, 140, 436, 456], 40), 1.5)
    part(c, body, leather_col(rng, (0.48, 0.09, 0.12)), 0.3, 26, 60, 0.35)
    flap = blur(poly([(76, 148), (436, 148), (436, 290), (256, 340), (76, 290)]), 1.5)
    part(c, flap, leather_col(rng, (0.56, 0.11, 0.14)), 0.25, 12, 50, 0.4)
    trim = blur(poly([(80, 290), (256, 340), (432, 290)], width=12), 1)
    metal_part(c, trim, gold_tint(), 0.6, 4)
    top = blur(rect([76, 144, 436, 160], 4), 1)
    metal_part(c, top, gold_tint(), 0.5, 3)
    crown = blur(poly([(206, 260), (206, 210), (231, 234), (256, 196), (281, 234), (306, 210), (306, 260)]), 1)
    part(c, crown, cloth(rng, (0.86, 0.70, 0.26), weave=1.0), 0.3, 5, 30, 0.4, 0.2)
    clasp = blur(ellipse([228, 318, 284, 374]), 1)
    metal_part(c, clasp, gold_tint(), 0.7, 6)
    gem = blur(ellipse([244, 334, 268, 358]), 1)
    part(c, gem, cloth(rng, (0.80, 0.08, 0.12), weave=0.5), 0.5, 6, 40, 0.9, 0.1)
    rivets(c, [(110, 420), (402, 420), (110, 180), (402, 180)], 9, gold_tint())
    return c.image()
