"""A parchment leaf with a turned-down corner and an ink arrow: the page buttons."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, parchment, light, pillow, poly, blur, edge_darken, noise


def page(direction, seed):
    rng = np.random.default_rng(seed)
    c = Canvas()
    shadow(c, [70, 420, 450, 490], 0.35, 18)
    # leaf: slightly skewed, with the outer top corner folded over
    fold = 'right' if direction > 0 else 'left'
    if fold == 'right':
        leaf_pts = [(100, 70), (330, 60), (420, 150), (412, 450), (110, 458)]
        flap_pts = [(330, 60), (420, 150), (340, 140)]
    else:
        leaf_pts = [(182, 60), (412, 70), (402, 458), (100, 450), (92, 150)]
        flap_pts = [(182, 60), (92, 150), (172, 140)]
    leaf = blur(poly(leaf_pts), 1.2)
    ripple = 0.04 * np.sin(yy / 37.0) + 0.03 * noise(rng, 5, 2)
    h = pillow(leaf, 8, 0.5) * 0.25 + ripple * leaf
    col = parchment(rng)
    # age stains toward the edges
    col *= (1 - 0.25 * np.clip(1 - blur(leaf, 30) * 1.4, 0, 1))[..., None]
    c.over(light(h, col, depth=60, spec=0.05) * edge_darken(leaf, 10, 0.3), leaf)
    # the folded flap: the paper's back, a touch darker, casting a small shadow
    flap = blur(poly(flap_pts), 1)
    c.over(np.zeros((N, N, 3)), blur(flap, 8) * 0.25)
    c.over(light(pillow(flap, 6) * 0.2, parchment(rng, (0.80, 0.70, 0.50)), depth=40, spec=0.05), flap)
    # faint lines of writing
    for i, y in enumerate(range(150, 420, 34)):
        x0, x1 = 150, 370 - (i % 3) * 30
        line = poly([(x0, y), (x1, y + 2)], width=5)
        c.over(np.zeros((N, N, 3)) + np.array([0.35, 0.28, 0.20]), line * 0.18)
    # the ink arrow, brushed on
    s = direction
    shaft = poly([(256 - 95 * s, 262), (256 + 40 * s, 262)], width=30)
    head = poly([(256 + 110 * s, 262), (256 + 20 * s, 190), (256 + 20 * s, 334)])
    ink = blur(np.maximum(shaft, head), 1.5)
    inkcol = np.zeros((N, N, 3)) + np.array([0.13, 0.10, 0.08])
    c.over(inkcol * (0.9 + 0.3 * noise(rng, 20, 2))[..., None], ink * 0.92)
    return c.image()
