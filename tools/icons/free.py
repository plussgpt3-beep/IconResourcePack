"""ยกเลิกการเป็น Slave: an iron shackle and chain, the chain broken apart."""
import numpy as np
from lib import N, xx, yy, Canvas, blur, ellipse, chrome, mask_from


def link_ring(c, cx, cy, rx, ry, angle, w=16, open_gap=False):
    ca, sa = np.cos(angle), np.sin(angle)
    u = ((xx - cx) * ca + (yy - cy) * sa) / rx
    v = (-(xx - cx) * sa + (yy - cy) * ca) / ry
    rr = np.hypot(u, v)
    ring = (np.abs(rr - 1) < w / min(rx, ry))
    if open_gap:
        ring &= ~((u > 0.6) & (np.abs(v) < 0.45))
    ring = blur(ring.astype(np.float32), 1.2)
    h = np.clip(1 - np.abs(rr - 1) / (w / min(rx, ry)), 0, 1) ** 0.5 * ring
    c.over(chrome(h, (0.42, 0.42, 0.45), depth=40, sky=0.8, ground=0.08), ring)


def draw():
    c = Canvas()
    # the cuff, hinged open
    link_ring(c, 150, 330, 110, 110, 0.0, w=26, open_gap=True)
    # chain running up and to the right, snapped in the middle
    pts = [(250, 270, 0.6), (300, 235, -0.9), (350, 200, 0.6)]
    for (x, y, a) in pts:
        link_ring(c, x, y, 34, 20, a, w=8)
    link_ring(c, 400, 150, 34, 20, -0.9, w=8, open_gap=True)
    link_ring(c, 455, 105, 34, 20, 0.6, w=8)
    return c.image()
