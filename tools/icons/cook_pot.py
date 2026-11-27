"""หม้อปรุงอาหาร (2026-11-27): an iron cauldron of bubbling stew over a lit campfire - the cooking pot itself."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, rect, wood, chrome, noise
from _tools import glow
from _dishes import grain, specks, oil


def draw():
    rng = np.random.default_rng(2720)
    c = Canvas()
    for p0, p1 in (((70, 470), (440, 400)), ((70, 400), (440, 470))):
        m = blur(poly([p0, p1], width=44), 1.2)
        c.over(light(0.6 * pillow(m, 14), wood(rng, (0.45, 0.28, 0.14), angle=0.2, rings=5), depth=40, spec=0.2), m)
    for (x, h, w, col) in ((256, 150, 80, (1.0, 0.55, 0.08)), (180, 100, 50, (1.0, 0.45, 0.05)), (332, 110, 54, (1.0, 0.45, 0.05)),
                           (256, 90, 40, (1.0, 0.85, 0.30))):
        f = blur(poly([(x - w, 440), (x - w * 0.5, 440 - h * 0.6), (x, 440 - h), (x + w * 0.5, 440 - h * 0.6), (x + w, 440)]), 5)
        c.over(np.zeros((N, N, 3)) + np.array(col), f, cast=False)
    pot = blur(ellipse([96, 110, 416, 390]) * (yy > 140), 1.2)
    nx = (xx - 256) / 160; ny = (yy - 250) / 140
    hammer = 0.012 * noise(rng, 8, 2) * pot
    c.over(chrome(np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * pot * 0.8 + hammer, (0.24, 0.24, 0.27), depth=70, sky=0.55, ground=0.05), pot)
    rust = np.clip(noise(rng, 14, 3) - 0.62, 0, 1) * 3 * pot
    c.over(np.zeros((N, N, 3)) + np.array([0.35, 0.16, 0.07]), np.clip(rust, 0, 1) * 0.25, cast=False)
    for hx in (96, 416):
        ring = blur(np.clip(ellipse([hx - 28, 170, hx + 28, 226]) - ellipse([hx - 16, 182, hx + 16, 214]), 0, 1), 1)
        c.over(chrome(0.4 * pillow(ring, 4), (0.30, 0.30, 0.33), depth=40, sky=0.7, ground=0.08), ring, cast=True)
    for a in np.linspace(0.15, np.pi - 0.15, 7):
        rx, ry = 256 - 150 * np.cos(a), 200 + 26 * np.sin(a)
        rv = blur(ellipse([rx - 7, ry - 7, rx + 7, ry + 7]), 1)
        c.over(chrome(0.6 * pillow(rv, 3), (0.42, 0.42, 0.45), depth=30), rv)
    rim = blur(ellipse([86, 118, 426, 172]), 1)
    c.over(chrome(0.3 * pillow(rim, 6), (0.36, 0.36, 0.40), depth=40, sky=0.7, ground=0.08), rim)
    stew = blur(ellipse([108, 128, 404, 162]), 1)
    c.over(light(0.1 * stew, grain(rng, (0.62, 0.34, 0.12), 8, 0.3), depth=20, spec=0.6, gloss=40), stew)
    specks(c, rng, stew, 10, (0.85, 0.45, 0.10), 4, 8)
    specks(c, rng, stew, 8, (0.30, 0.55, 0.20), 2, 4)
    oil(c, rng, stew, 6)
    glow(c, 256, 380, 150, (1.0, 0.55, 0.15), 0.35)
    return c.image()
