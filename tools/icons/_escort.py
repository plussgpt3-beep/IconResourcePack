"""Caravan guards (ทหารคุ้มกันคาราวาน, 2026-10-24): a soldier's heater shield bearing a cart wheel, a spear behind."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, wood, chrome, cloth, edge_darken, band


def spear(c, rng, p0, p1):
    s, t = band(p0, p1, 0)
    shaft = blur(((s > 0) & (s < 0.82) & (np.abs(t) < 9)).astype(np.float32), 1)
    c.over(light(np.clip(1 - np.abs(t) / 9, 0, 1) ** 0.5 * shaft, wood(rng, (0.55, 0.36, 0.20), angle=-0.8, rings=5), depth=30, spec=0.2), shaft)
    head = blur(((s > 0.8) & (s < 1.0) & (np.abs(t) < 26 * (1 - (s - 0.8) / 0.2))).astype(np.float32), 1)
    c.over(chrome(0.7 * pillow(head, 6), (0.70, 0.72, 0.76), depth=50), head)


def shield(c, rng, cx=256, top=90, w=300, h=340, field=(0.16, 0.30, 0.62)):
    """A heater shield: steel rim, painted field, a gold cart wheel."""
    x0, x1 = cx - w / 2, cx + w / 2
    pts = [(x0, top), (x1, top), (x1, top + h * 0.45)]
    for a in np.linspace(0, 1, 16):
        pts.append((x1 - (x1 - cx) * a, top + h * 0.45 + (h * 0.55) * np.sin(a * np.pi / 2)))
    for a in np.linspace(1, 0, 16):
        pts.append((x0 + (cx - x0) * a, top + h * 0.45 + (h * 0.55) * np.sin(a * np.pi / 2)))
    pts.append((x0, top + h * 0.45))
    outer = blur(poly(pts), 1.2)
    c.over(chrome(0.7 * pillow(outer, 18), (0.62, 0.64, 0.68), depth=60), outer)
    inner_pts = [(cx + (x - cx) * 0.86, top + 18 + (y - top) * 0.88) for x, y in pts]
    inner = blur(poly(inner_pts), 1.2)
    c.over(light(0.35 * pillow(inner, 24), cloth(rng, field, weave=1.5), depth=40, spec=0.12) * edge_darken(inner, 12, 0.35), inner)
    wy = top + h * 0.42
    rr = np.hypot(xx - cx, yy - wy); ang = np.arctan2(yy - wy, xx - cx)
    rim = blur(((rr < 70) & (rr > 56)).astype(np.float32), 1)
    spokes = blur(((np.abs(np.sin(ang * 4)) < 7.0 / (rr + 1)) & (rr < 60)).astype(np.float32), 1)
    hub = blur((rr < 15).astype(np.float32), 1)
    gold = (0.96, 0.76, 0.30)
    for m in (spokes, rim, hub):
        c.over(chrome(0.6 * pillow(m, 4), gold, depth=40), m * inner)
