"""โอนเงิน: gold passing from one stack of coins to another, along a curved arrow."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, gold_coin, mask_from


def draw():
    c = Canvas()
    for i in range(4): gold_coin(c, 140, 440 - i * 26, 95, 32, 20)
    for i in range(2): gold_coin(c, 372, 440 - i * 26, 95, 32, 20)
    # arrow arcing from the tall stack over to the short one
    cx, cy, r = 256, 330, 130
    rr = np.hypot(xx - cx, yy - cy); ang = np.arctan2(yy - cy, xx - cx)
    bandm = ((np.abs(rr - r) < 18) & (ang < -0.35) & (ang > -np.pi + 0.35)).astype(np.float32)
    hx, hy = cx + r * np.cos(-0.35), cy + r * np.sin(-0.35)
    head = poly([(hx - 40, hy - 20), (hx + 32, hy - 8), (hx + 8, hy + 62)])
    arrow = blur(np.clip(bandm + head, 0, 1), 1.5)
    col = np.zeros((N, N, 3)) + np.array([0.28, 0.62, 0.22])
    c.over(light(pillow(arrow, 8) * 0.8, col, depth=40, spec=0.4), arrow)
    return c.image()
