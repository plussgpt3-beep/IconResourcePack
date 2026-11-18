"""Shared pieces for the กระเป๋าเสริม icons (bag_t1..bag_t5, 2026-11-18): leather, canvas, iron, wood and gold."""
from lib import Canvas, light, pillow, blur, poly, rect, ellipse, edge_darken, chrome, leather_col, steel_tint


def part(c, mask, albedo, h=0.3, r=12, depth=50, spec=0.2, dark=0.45):
    c.over(light(h * pillow(mask, r), albedo, depth=depth, spec=spec) * edge_darken(mask, 10, dark), mask)


IRON = (0.50, 0.50, 0.53)   # forged iron, darker than polished steel


def metal_part(c, mask, tint, h=0.6, r=4, sky=1.0):
    c.over(chrome(pillow(mask, r) * h, tint, depth=40, sky=sky, ground=0.12, spec=0.5 if sky < 1 else 0.9), mask)


def iron_part(c, mask, h=0.5, r=4):
    metal_part(c, mask, IRON, h, r, sky=0.6)


def rivets(c, pts, r=9, tint=None):
    for (x, y) in pts:
        m = blur(ellipse([x - r, y - r, x + r, y + r]), 1)
        if tint is None:
            iron_part(c, m, 0.8, 3)
        else:
            metal_part(c, m, tint, 0.8, 3)


def strap(c, rng, p0, p1, w, color=(0.36, 0.20, 0.10)):
    m = blur(poly([p0, p1], width=w), 1)
    part(c, m, leather_col(rng, color), 0.3, 4, 40, 0.2)
    return m


def buckle(c, cx, cy, s=22, tint=None):
    m = blur(rect([cx - s, cy - s, cx + s, cy + s], 5), 1) * (1 - blur(rect([cx - s + 9, cy - s + 9, cx + s - 9, cy + s - 9], 3), 1))
    if tint is None:
        iron_part(c, m, 0.6, 4)
    else:
        metal_part(c, m, tint, 0.6, 4)
