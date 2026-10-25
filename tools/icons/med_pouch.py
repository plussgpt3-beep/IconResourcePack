"""ย่ามยา: a leather satchel with a flap and buckle, a red cross stitched on it, a green sprig and a flask peeking out."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, cloth, edge_darken, chrome, leather_col, steel_tint


def draw():
    rng = np.random.default_rng(517)
    c = Canvas()
    leather = leather_col(rng, (0.50, 0.30, 0.15))
    # strap arching over the top
    rr = np.hypot(xx - 256, yy - 230)
    strap = blur(((rr < 200) & (rr > 176) & (yy < 230)).astype(np.float32), 1)
    c.over(light(pillow(strap, 5) * 0.6, leather_col(rng, (0.40, 0.23, 0.11)), depth=40, spec=0.2), strap)
    # a flask and a sprig behind the flap
    flask = blur(ellipse([290, 120, 370, 230]), 1) + blur(rect([314, 92, 346, 130], 4), 1)
    flask = np.clip(flask, 0, 1)
    glass = np.stack([0.55 + 0 * xx, 0.80 + 0 * xx, 0.85 + 0 * xx], -1)
    c.over(light(0.3 * pillow(flask, 12), glass, depth=40, spec=0.8), flask * 0.9)
    cork = blur(rect([316, 80, 344, 100], 4), 1)
    c.over(light(0.3 * pillow(cork, 4), cloth(rng, (0.62, 0.45, 0.28), weave=1.5), depth=30, spec=0.1), cork)
    stem = blur(poly([(170, 230), (150, 110)], width=8), 1)
    c.over(light(pillow(stem, 3) * 0.5, cloth(rng, (0.25, 0.50, 0.18), weave=1.5), depth=30, spec=0.1), stem)
    for (lx, ly) in ((132, 120), (166, 140), (140, 166), (172, 182)):
        leaf = blur(ellipse([lx - 22, ly - 12, lx + 22, ly + 12]), 1)
        c.over(light(0.4 * pillow(leaf, 6), cloth(rng, (0.30, 0.62, 0.22), weave=1.2), depth=30, spec=0.15), leaf)
    # the bag body
    body = blur(rect([86, 200, 426, 440], 40), 1.5)
    c.over(light(0.3 * pillow(body, 18), leather, depth=60, spec=0.2) * edge_darken(body, 12, 0.5), body)
    # flap
    flap = blur(poly([(86, 200), (426, 200), (426, 300), (256, 350), (86, 300)]), 1.5)
    c.over(light(0.25 * pillow(flap, 12), leather_col(rng, (0.56, 0.34, 0.17)), depth=50, spec=0.25) * edge_darken(flap, 10, 0.45), flap)
    # red cross on the flap
    cross = np.clip(blur(rect([236, 222, 276, 318], 4), 1) + blur(rect([208, 250, 304, 290], 4), 1), 0, 1)
    c.over(light(0.2 * pillow(cross, 5), cloth(rng, (0.78, 0.10, 0.10), weave=1.2), depth=30, spec=0.15), cross)
    # buckle
    buckle = blur(rect([236, 346, 276, 392], 6), 1) * (1 - blur(rect([246, 356, 266, 382], 3), 1))
    c.over(chrome(pillow(buckle, 4) * 0.6, steel_tint(), depth=40, ground=0.15), buckle)
    return c.image()
