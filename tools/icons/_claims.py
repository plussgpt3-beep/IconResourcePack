"""Boundary stones outside the cities (หลักเขตนอกเมือง, 2026-10-24): a wooden post, a carved stone
marker and an inscribed stele, each set in a mound of turf."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, noise, stone, chrome, edge_darken


def turf(c, rng, cx=256, cy=430, rx=170, ry=46):
    """A low mound of grass and earth the marker stands in."""
    top = blur(ellipse([cx - rx, cy - ry, cx + rx, cy + ry]), 2)
    side = blur(ellipse([cx - rx, cy - ry + 18, cx + rx, cy + ry + 18]), 2) * (1 - top)
    soil = np.array([0.34, 0.22, 0.12])[None, None, :] * (0.6 + 0.5 * noise(rng, 26, 3)[..., None])
    c.over(soil, side)
    g = np.array([0.26, 0.48, 0.17])[None, None, :] * (0.72 + 0.5 * noise(rng, 34, 3)[..., None])
    g[noise(rng, 80, 1) > 0.62] *= 1.25
    c.over(light(0.25 * pillow(top, 22), np.clip(g, 0, 1), depth=30, spec=0.04), top)


def post(c, rng, x0=196, x1=316, top=90, bottom=440):
    """A squared post of stripped oak with a pointed cap and a red painted band."""
    body = blur(poly([(x0, top + 40), (256, top - 10), (x1, top + 40), (x1, bottom), (x0, bottom)]), 1.2)
    col = wood(rng, (0.80, 0.66, 0.44), angle=np.pi / 2, rings=6)
    face = np.clip((xx - x0) / (x1 - x0), 0, 1)
    shade = 0.75 + 0.35 * np.sin(face * np.pi)
    col = col * shade[..., None]
    band = (yy > top + 70) & (yy < top + 108)
    col[band] = col[band] * np.array([0.92, 0.22, 0.16]) / np.array([0.80, 0.66, 0.44]) * 0.85
    c.over(light(0.35 * pillow(body, 14), np.clip(col, 0, 1), depth=40, spec=0.12) * edge_darken(body, 8, 0.35), body)
    # an iron plate with the owner's mark, nailed on
    plate = blur(rect([226, 200, 286, 280], 6), 1)
    c.over(chrome(0.6 * pillow(plate, 6), (0.55, 0.56, 0.60), depth=40), plate)
    mark = blur(poly([(256, 222), (270, 240), (256, 258), (242, 240)]), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.16, 0.15, 0.15]), mark)
    for nx, ny in ((234, 208), (278, 208), (234, 272), (278, 272)):
        n = blur(ellipse([nx - 5, ny - 5, nx + 5, ny + 5]), 0.6)
        c.over(np.zeros((N, N, 3)) + np.array([0.25, 0.25, 0.27]), n)


def marker(c, rng, x0=176, x1=336, top=120, bottom=444, color=(0.62, 0.61, 0.58), tilt=0.0, carve=True):
    """A squared boundary stone with a chamfered head and a surveyor's broad arrow cut in its face."""
    cx = (x0 + x1) / 2
    pts = [(x0, bottom), (x0, top + 46), (x0 + 30, top), (x1 - 30, top), (x1, top + 46), (x1, bottom)]
    lines = [[(cx, top + 70), (cx, top + 200)], [(cx - 42, top + 118), (cx, top + 70), (cx + 42, top + 118)],
             [(cx - 52, top + 232), (cx + 52, top + 232)]]
    cap = [(x0, top + 46), (x0 + 30, top), (x1 - 30, top), (x1, top + 46)]
    if tilt:
        ca, sa = np.cos(tilt), np.sin(tilt)
        rot = lambda q: [(cx + (x - cx) * ca - (y - bottom) * sa, bottom + (x - cx) * sa + (y - bottom) * ca) for x, y in q]
        pts = rot(pts)
        lines = [rot(l) for l in lines]
        cap = rot(cap)
    body = blur(poly(pts), 1.2)
    col = stone(rng, color)
    c.over(light(0.5 * pillow(body, 24), np.clip(col, 0, 1), depth=50, spec=0.06) * edge_darken(body, 10, 0.4), body)
    ridge = blur(poly(cap, width=5), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array(color) * 1.25, np.clip(ridge * body, 0, 1) * 0.6)
    if carve:
        cut = blur(np.clip(sum(poly(l, width=12) for l in lines), 0, 1), 0.8)
        c.over(np.zeros((N, N, 3)) + np.array(color) * 0.36, cut * body)
    return body


def stele(c, rng):
    """ศิลาจารึกเขต: a tall dark stele, its inscription inlaid in gold, a compass rose at the head."""
    x0, x1, top, bottom = 170, 342, 50, 446
    body = marker(c, rng, x0, x1, top, bottom, color=(0.30, 0.31, 0.34), carve=False)
    for k in range(6):
        y = 250 + k * 28
        ln = blur(poly([(206, y), (306 - (k % 3) * 18, y)], width=6), 0.7)
        c.over(chrome(0.5 * ln, (0.95, 0.74, 0.30), depth=20), ln * body)
    cx, cy = 256, 160
    rose = []
    for i in range(8):
        a = i * np.pi / 4
        L = 52 if i % 2 == 0 else 30
        tip = (cx + L * np.sin(a), cy - L * np.cos(a))
        l = (cx + 10 * np.sin(a - np.pi / 2), cy - 10 * np.cos(a - np.pi / 2))
        rr = (cx + 10 * np.sin(a + np.pi / 2), cy - 10 * np.cos(a + np.pi / 2))
        rose.append(poly([l, tip, rr]))
    m = blur(np.clip(sum(rose), 0, 1), 0.8)
    c.over(chrome(0.7 * pillow(m, 4), (0.97, 0.76, 0.32), depth=40), m)
    ring = blur(np.clip(ellipse([cx - 62, cy - 62, cx + 62, cy + 62]) - ellipse([cx - 54, cy - 54, cx + 54, cy + 54]), 0, 1), 0.8)
    c.over(chrome(0.6 * ring, (0.95, 0.74, 0.30), depth=30), ring)
