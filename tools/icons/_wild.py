"""แดนนอก (PVE, 2026-11-13): the raw drops of the danger zones and the goods made from them.
The zone shows in the item's name colour in game."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, cloth, wood, edge_darken, chrome, steel_tint, gold_tint, noise, leather_col, stone

ZONE = {1: (0.35, 0.70, 0.30), 2: (0.85, 0.75, 0.25), 3: (0.90, 0.50, 0.15), 4: (0.55, 0.20, 0.75)}


def canvas(zone):
    return Canvas()


def hide(c, rng, color, rough=True):
    """A stretched animal hide with ragged edges."""
    pts = [(120, 110), (210, 140), (300, 100), (400, 130), (380, 230), (430, 330), (360, 420), (260, 380), (160, 430), (100, 330), (140, 230)]
    m = blur(poly(pts), 3)
    tex = leather_col(rng, color) * (0.85 + 0.3 * noise(rng, 30, 3)[..., None])
    if rough:
        tex = tex * (0.9 + 0.2 * noise(rng, 90, 2)[..., None])
    c.over(light(0.35 * pillow(m, 25), np.clip(tex, 0, 1), depth=40, spec=0.1) * edge_darken(m, 14, 0.5), m)


def fang(c, rng, x0, y0, x1, y1, w, color=(0.92, 0.88, 0.76)):
    m = blur(poly([(x0 - w, y0), (x0 + w, y0), (x1, y1)]), 1.5)
    col = np.zeros((N, N, 3)) + np.array(color)
    col = col * (0.9 + 0.15 * noise(rng, 40, 2)[..., None])
    c.over(light(0.5 * pillow(m, 10), np.clip(col, 0, 1), depth=60, spec=0.35), m)


def bone(c, rng, p0, p1, w, color=(0.90, 0.86, 0.74)):
    shaft = blur(poly([p0, p1], width=w), 1.5)
    knobs = 0
    for (x, y) in (p0, p1):
        for d in (-1, 1):
            nx, ny = (p1[1] - p0[1]), -(p1[0] - p0[0])
            L = np.hypot(nx, ny) or 1
            cx, cy = x + d * nx / L * w * 0.55, y + d * ny / L * w * 0.55
            knobs = np.maximum(knobs, blur(ellipse([cx - w * 0.6, cy - w * 0.6, cx + w * 0.6, cy + w * 0.6]), 1))
    m = np.maximum(shaft, knobs)
    col = (np.zeros((N, N, 3)) + np.array(color)) * (0.88 + 0.15 * noise(rng, 30, 3)[..., None])
    c.over(light(0.5 * pillow(m, 14), np.clip(col, 0, 1), depth=60, spec=0.3), m)


def scales(c, rng, color, metal=True):
    for row in range(4):
        for col_i in range(4 - (row % 2)):
            cx = 150 + col_i * 75 + (row % 2) * 37
            cy = 150 + row * 65
            m = blur(poly([(cx - 34, cy - 20), (cx + 34, cy - 20), (cx + 30, cy + 20), (cx, cy + 48), (cx - 30, cy + 20)]), 1.2)
            if metal:
                c.over(chrome(0.6 * pillow(m, 10), np.array(color), depth=60, ground=0.15), m)
            else:
                cc = (np.zeros((N, N, 3)) + np.array(color)) * (0.85 + 0.25 * noise(rng, 25, 2)[..., None])
                c.over(light(0.5 * pillow(m, 10), np.clip(cc, 0, 1), depth=50, spec=0.4), m)


def gland(c, rng, color):
    m = blur(ellipse([140, 150, 380, 380]), 3)
    cc = (np.zeros((N, N, 3)) + np.array(color)) * (0.8 + 0.35 * noise(rng, 18, 3)[..., None])
    c.over(light(0.6 * pillow(m, 50), np.clip(cc, 0, 1), depth=70, spec=0.6, gloss=40), m)
    vein = blur(poly([(200, 190), (260, 260), (330, 250)], width=6), 1) * m
    c.over(np.zeros((N, N, 3)) + np.array([0.35, 0.05, 0.10]), vein * 0.7)
    tube = blur(poly([(250, 150), (240, 90), (210, 60)], width=22), 1.5)
    c.over(light(0.4 * pillow(tube, 8), np.zeros((N, N, 3)) + np.array([0.60, 0.25, 0.35]), depth=40, spec=0.3), tube)


def crystal(c, rng, color, dark=False):
    shards = [[(256, 60), (330, 230), (256, 450), (182, 230)],
              [(160, 160), (215, 250), (175, 400), (110, 280)],
              [(352, 160), (402, 280), (337, 400), (297, 250)]]
    for pts in shards:
        m = blur(poly(pts), 1.5)
        base = np.array(color)
        if dark:
            base = base * 0.6
        cc = (np.zeros((N, N, 3)) + base) * (0.75 + 0.45 * (xx < pts[0][0]).astype(np.float32)[..., None])
        c.over(light(0.7 * pillow(m, 20), np.clip(cc, 0, 1), depth=80, spec=0.8, gloss=50), m)
    if dark:
        core = blur(ellipse([226, 210, 286, 290]), 8)
        c.over(np.zeros((N, N, 3)) + np.array([0.9, 0.3, 1.0]), core * 0.8, cast=False)


def ingot(c, rng, tint):
    m = blur(poly([(110, 320), (180, 200), (400, 200), (420, 320)]), 1.5)
    c.over(chrome(0.7 * pillow(m, 22), tint, depth=70, ground=0.18), m)


def blade(c, rng, tint, glow=None):
    m = blur(poly([(120, 400), (150, 370), (400, 110), (420, 100), (410, 120), (170, 390)]), 1.2)
    c.over(chrome(0.7 * pillow(m, 8), tint, depth=60, ground=0.12), m)
    if glow is not None:
        edge = blur(poly([(150, 370), (400, 110)], width=5), 3)
        c.over(np.zeros((N, N, 3)) + np.array(glow), edge * 0.8, cast=False)
    grip = blur(poly([(100, 430), (140, 390)], width=26), 1)
    c.over(light(0.5 * pillow(grip, 8), leather_col(rng, (0.30, 0.16, 0.08)), depth=40, spec=0.1), grip)


def flask(c, rng, liquid):
    body = blur(ellipse([150, 210, 362, 430]), 2)
    neck = blur(rect([226, 110, 286, 230], 8), 1.5)
    glass = np.maximum(body, neck)
    c.over(np.zeros((N, N, 3)) + np.array([0.75, 0.85, 0.90]), glass * 0.35, cast=False)
    liq = blur(ellipse([162, 270, 350, 420]), 2) * body
    c.over(light(0.5 * pillow(liq, 30), np.zeros((N, N, 3)) + np.array(liquid), depth=50, spec=0.7), liq)
    cork = blur(rect([230, 80, 282, 120], 6), 1)
    c.over(light(0.4 * pillow(cork, 6), wood(rng, (0.60, 0.42, 0.24), rings=3), depth=30, spec=0.1), cork)
    shine = blur(poly([(195, 260), (185, 330)], width=12), 3)
    c.over(np.zeros((N, N, 3)) + 1.0, shine * 0.5, cast=False)


def haft(c, rng):
    m = blur(poly([(130, 420), (380, 110)], width=40), 1.5)
    col = (np.zeros((N, N, 3)) + np.array([0.88, 0.84, 0.72])) * (0.85 + 0.2 * noise(rng, 30, 3)[..., None])
    c.over(light(0.5 * pillow(m, 14), np.clip(col, 0, 1), depth=60, spec=0.3), m)
    for t in (0.2, 0.45, 0.7):
        x = 130 + (380 - 130) * t; y = 420 + (110 - 420) * t
        wrap = blur(poly([(x - 30, y - 18), (x + 30, y + 18)], width=18), 1) * 1.0
        c.over(light(0.4 * pillow(wrap, 5), leather_col(rng, (0.40, 0.22, 0.10)), depth=30, spec=0.1), wrap)


def tip(c, rng):
    fang(c, rng, 250, 380, 330, 90, 52)
    shaft = blur(poly([(140, 470), (250, 380)], width=24), 1.2)
    c.over(light(0.5 * pillow(shaft, 6), wood(rng, (0.55, 0.38, 0.20), rings=4), depth=40, spec=0.1), shaft)
    lash = blur(poly([(225, 400), (275, 360)], width=26), 1)
    c.over(light(0.4 * pillow(lash, 5), cloth(rng, (0.65, 0.55, 0.35), weave=3), depth=30, spec=0.05), lash)


def plate(c, rng):
    m = blur(rect([120, 120, 392, 392], 30), 2)
    c.over(chrome(0.5 * pillow(m, 30), steel_tint(), depth=60, ground=0.15), m)
    scales_m = 0
    for r in range(3):
        for k in range(3):
            cx, cy = 180 + k * 76, 180 + r * 76
            s = blur(ellipse([cx - 32, cy - 26, cx + 32, cy + 30]), 1)
            c.over(chrome(0.6 * pillow(s, 8), np.array(steel_tint()) * 0.92, depth=50, ground=0.12), s)
    for (x, y) in ((140, 140), (372, 140), (140, 372), (372, 372)):
        r = blur(ellipse([x - 12, y - 12, x + 12, y + 12]), 1)
        c.over(chrome(0.6 * pillow(r, 4), gold_tint(), depth=40), r)
