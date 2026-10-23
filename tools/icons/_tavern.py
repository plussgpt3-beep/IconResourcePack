"""The tavern's things (โรงเตี๊ยม, 2026-10-23): a staved wooden tankard, an oak barrel with a tap,
a wine bottle, a clay mead jug. Each painter returns an upright PIL image; icons place, tilt and
combine them."""
import numpy as np
from PIL import Image
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, noise, edge_darken


def _cyl(cx, r):
    nx = (xx - cx) / r
    return np.sqrt(np.clip(1 - nx ** 2, 0, 1))


def _iron(c, m, cx, r, k=1.0):
    c.over(chrome(_cyl(cx, r) * m * k, (0.36, 0.36, 0.38), depth=40, sky=0.7, ground=0.08), m)


def tankard(rng, foam=True, beer=(0.85, 0.55, 0.12)):
    """A staved oak tankard, two iron hoops, a handle on the right, a head of foam spilling over."""
    c = Canvas()
    cx, r = 236, 120
    body = blur(rect([cx - r, 150, cx + r, 440], 18), 1.2)
    # handle behind the body's right edge
    handle = blur(np.clip(ellipse([cx + r - 40, 200, cx + r + 110, 390]) - ellipse([cx + r - 10, 236, cx + r + 70, 354]), 0, 1)
                  * (xx > cx + r - 20), 1.2)
    c.over(light(0.6 * pillow(handle, 8), wood(rng, (0.46, 0.27, 0.12), angle=0.3, rings=5), depth=40, spec=0.2), handle)
    staves = 0.86 + 0.14 * (np.abs(np.sin((xx - cx) / 22.0)) > 0.12)
    col = wood(rng, (0.58, 0.36, 0.17), angle=np.pi / 2, rings=5) * staves[..., None]
    c.over(light(_cyl(cx, r) * body * 0.8, col, depth=60, spec=0.2) * edge_darken(body, 8, 0.3), body)
    for y in (200, 395):
        hoop = blur((np.abs(yy - y) < 13).astype(np.float32) * body, 1)
        _iron(c, hoop, cx, r)
    rim = blur(ellipse([cx - r, 128, cx + r, 172]), 1)
    c.over(light(0.1 * rim, np.zeros((N, N, 3)) + np.array(beer) * 0.8, depth=20, spec=0.2), rim)
    if foam:
        bubbles = noise(rng, 18, 2)
        froth = np.maximum(ellipse([cx - r - 6, 92, cx + r + 6, 178]), np.maximum(ellipse([cx - 70, 60, cx + 20, 140]), ellipse([cx - 10, 70, cx + 90, 150])))
        drip = poly([(cx - r + 6, 150), (cx - r + 34, 150), (cx - r + 26, 232), (cx - r + 14, 232)])
        drip = np.maximum(drip, ellipse([cx - r + 8, 214, cx - r + 32, 244]))
        froth = blur(np.maximum(froth, drip), 2)
        c.over(light(0.7 * pillow(froth, 14), np.zeros((N, N, 3)) + (0.92 + 0.08 * bubbles)[..., None] * np.array([1.0, 0.97, 0.88]),
                     depth=50, spec=0.25), froth)
    return c.image()


def barrel(rng, tap=True, liquid=None):
    """An oak barrel standing up, three iron hoops, a brass tap low on its belly."""
    c = Canvas()
    cx, r = 256, 150
    k = blur(np.maximum(ellipse([cx - r, 60, cx + r, 470]) * ((yy > 92) & (yy < 440)), rect([cx - r + 22, 92, cx + r - 22, 440])), 1.2)
    st = 0.85 + 0.15 * (np.abs(np.sin((xx - cx) / 24.0)) > 0.1)
    c.over(light(_cyl(cx, r) * k * 0.8, wood(rng, (0.52, 0.32, 0.15), angle=np.pi / 2, rings=6) * st[..., None], depth=60, spec=0.2)
           * edge_darken(k, 8, 0.3), k)
    for y in (126, 266, 404):
        hoop = blur((np.abs(yy - y) < 12).astype(np.float32) * k, 1)
        _iron(c, hoop, cx, r)
    top = blur(ellipse([cx - r + 30, 72, cx + r - 30, 116]), 1)
    c.over(light(0.1 * top, wood(rng, (0.45, 0.27, 0.12), rings=8), depth=20, spec=0.1), top)
    if tap:
        spout = blur(rect([cx - 20, 318, cx + 70, 344], 8), 1)
        c.over(chrome(0.5 * pillow(spout, 6), (0.85, 0.62, 0.25), depth=40), spout)
        knob = blur(rect([cx + 28, 292, cx + 46, 324], 5), 1)
        c.over(chrome(0.5 * pillow(knob, 4), (0.85, 0.62, 0.25), depth=40), knob)
        nose = blur(rect([cx + 52, 330, cx + 72, 366], 6), 1)
        c.over(chrome(0.5 * pillow(nose, 4), (0.80, 0.58, 0.22), depth=40), nose)
        if liquid is not None:
            drop = blur(ellipse([cx + 54, 372, cx + 70, 394]), 1.5)
            c.over(np.zeros((N, N, 3)) + np.array(liquid), drop, cast=False)
    return c.image()


def bottle(rng, glass=(0.10, 0.28, 0.14), label=(0.88, 0.80, 0.60), seal=(0.55, 0.06, 0.10)):
    """A dark green wine bottle: round shoulders, a long neck, a wax-sealed cork, a paper label."""
    c = Canvas()
    cx = 256
    body = blur(np.maximum(rect([cx - 92, 230, cx + 92, 470], 26),
                           np.maximum(ellipse([cx - 92, 170, cx + 92, 300]) * (yy > 200), rect([cx - 34, 60, cx + 34, 240], 12))), 1.2)
    nx = (xx - cx) / 92
    shade = np.sqrt(np.clip(1 - nx ** 2, 0, 1))
    col = np.zeros((N, N, 3)) + np.array(glass)
    c.over(light(shade * body * 0.7, col, depth=50, spec=0.75, gloss=60), body)
    shine = blur(rect([cx - 64, 250, cx - 46, 440], 8), 6) * body
    c.over(np.ones((N, N, 3)) * 0.9, shine * 0.55, cast=False)
    lab = blur(rect([cx - 80, 300, cx + 80, 410], 6), 1)
    c.over(light(shade * lab * 0.4, np.zeros((N, N, 3)) + np.array(label), depth=30, spec=0.1), lab)
    grape = np.zeros((N, N), np.float32)
    for (gx, gy) in ((cx - 18, 336), (cx + 2, 336), (cx + 22, 336), (cx - 8, 356), (cx + 12, 356), (cx + 2, 376)):
        grape = np.maximum(grape, ellipse([gx - 11, gy - 11, gx + 11, gy + 11]))
    c.over(np.zeros((N, N, 3)) + np.array([0.42, 0.10, 0.28]), blur(grape, 1), cast=False)
    cap = blur(rect([cx - 40, 48, cx + 40, 110], 12), 1)
    c.over(light(0.6 * pillow(cap, 8), np.zeros((N, N, 3)) + np.array(seal), depth=40, spec=0.35), cap)
    return c.image()


def jug(rng, clay=(0.62, 0.34, 0.18), glaze=(0.90, 0.66, 0.18)):
    """A round clay mead jug, honey glaze running down from the lip, a cork and a loop handle."""
    c = Canvas()
    cx = 236
    handle = blur(np.clip(ellipse([cx + 40, 110, cx + 210, 330]) - ellipse([cx + 82, 150, cx + 172, 290]), 0, 1) * (xx > cx + 60), 1.2)
    c.over(light(0.6 * pillow(handle, 8), np.zeros((N, N, 3)) + np.array(clay) * 0.9, depth=40, spec=0.2), handle)
    body = blur(np.maximum(ellipse([cx - 150, 170, cx + 150, 470]), rect([cx - 58, 90, cx + 58, 220], 18)), 1.2)
    nx = (xx - cx) / 150; ny = (yy - 330) / 150
    dome = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    grain = 0.9 + 0.1 * noise(rng, 30, 2)
    c.over(light(np.maximum(dome, 0.5 * pillow(body, 12)) * body, np.array(clay)[None, None, :] * grain[..., None], depth=60, spec=0.25)
           * edge_darken(body, 8, 0.3), body)
    edge = 236 + 12 * np.sin((xx - cx) / 21.0)
    run = (yy > 150) & (yy < edge)
    run = np.maximum(run.astype(np.float32), rect([cx - 62, 96, cx + 62, 128], 12))
    for (x0, y1) in ((cx - 70, 292), (cx + 24, 318)):
        run = np.maximum(run, np.maximum(rect([x0 - 11, 220, x0 + 11, y1], 11), ellipse([x0 - 17, y1 - 22, x0 + 17, y1 + 10])))
    run = blur(run * body, 1.5)
    c.over(light(np.maximum(dome, 0.5) * run * 0.8, np.zeros((N, N, 3)) + np.array(glaze), depth=40, spec=0.6, gloss=50), run)
    cork = blur(rect([cx - 44, 56, cx + 44, 106], 12), 1)
    c.over(light(0.5 * pillow(cork, 6), np.zeros((N, N, 3)) + np.array([0.66, 0.48, 0.28]), depth=30, spec=0.1), cork)
    return c.image()


def place(canvas_img, obj, cx, cy, scale=1.0, angle=0.0):
    """Pastes an upright painting into a canvas image: scaled, turned (degrees, anticlockwise), centred at cx, cy."""
    size = int(N * scale)
    o = obj.resize((size, size), Image.LANCZOS)
    if angle:
        o = o.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas_img.alpha_composite(o, (int(cx - o.width / 2), int(cy - o.height / 2)))
    return canvas_img
