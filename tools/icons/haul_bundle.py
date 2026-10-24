"""ห่อสินค้าตราหลวง: a goods bale wrapped in sacking, roped crosswise, closed with a red wax seal bearing the crown."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, cloth, edge_darken, wax_seal, _symbol


def draw():
    rng = np.random.default_rng(2430)
    c = Canvas()
    bale = blur(rect([80, 130, 432, 450], 46), 1.5)
    c.over(light(0.5 * pillow(bale, 40), cloth(rng, (0.70, 0.58, 0.38), weave=4.0), depth=60, spec=0.1) * edge_darken(bale, 12, 0.35), bale)
    rope = np.maximum(rect([80, 270, 432, 292]), rect([244, 130, 266, 450])) * bale
    rope = blur(rope, 1)
    twist = 0.8 + 0.2 * (np.sin((xx + yy) / 6.0) > 0)
    c.over(light(0.5 * pillow(rope, 5), np.array([0.62, 0.46, 0.24])[None, None, :] * twist[..., None], depth=30, spec=0.2), rope)
    wax_seal(c, rng, 256, 282, 62, (0.62, 0.06, 0.08), _symbol('crown', 256, 282, 46))
    return c.image()
