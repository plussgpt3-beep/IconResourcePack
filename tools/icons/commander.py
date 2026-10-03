"""ผู้บัญชาการค่าย: a commander's steel helmet with a red plume, a gold-capped marshal's baton across behind it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, steel_tint, cloth, edge_darken


def draw():
    rng = np.random.default_rng(1202)
    c = Canvas()
    # the baton: dark red velvet with gold caps and bands, lying diagonally behind
    p0, p1 = np.array([70.0, 440.0]), np.array([450.0, 120.0])
    d = (p1 - p0) / np.linalg.norm(p1 - p0); n = np.array([-d[1], d[0]])
    t = ((xx - p0[0]) * d[0] + (yy - p0[1]) * d[1]); s = ((xx - p0[0]) * n[0] + (yy - p0[1]) * n[1])
    L = np.linalg.norm(p1 - p0)
    rod = blur(((np.abs(s) < 22) & (t > 0) & (t < L)).astype(np.float32), 1.2)
    round_h = np.sqrt(np.clip(1 - (s / 22) ** 2, 0, 1))
    velvet = cloth(rng, (0.45, 0.06, 0.08), weave=1.6)
    c.over(light(round_h * rod * 0.8, velvet, depth=40, spec=0.25), rod)
    for a, b in ((0, 46), (L - 46, L), (L * 0.33, L * 0.33 + 14), (L * 0.66, L * 0.66 + 14)):
        cap = blur(((np.abs(s) < 25) & (t > a) & (t < b)).astype(np.float32), 1)
        c.over(chrome(np.sqrt(np.clip(1 - (s / 25) ** 2, 0, 1)) * cap * 0.8, gold_tint(), depth=40), cap)
    # the plume, rising and curling back from the crest
    plume = blur(np.clip(ellipse([150, 30, 330, 200]) - ellipse([110, 110, 270, 260]) + ellipse([210, 40, 300, 150]) * 0.0, 0, 1), 3)
    feathers = 0.12 * np.sin(np.arctan2(yy - 200, xx - 240) * 28)
    c.over(light(0.5 * pillow(plume, 18) + feathers * plume, cloth(rng, (0.78, 0.10, 0.10), weave=1.4), depth=40, spec=0.15), plume)
    # the helmet: a rounded bowl with a brim, a nose guard and a crest ridge
    bowl = blur(np.maximum(ellipse([130, 150, 382, 400]) * (yy < 330), rect([130, 270, 382, 330])), 1.5)
    h = np.sqrt(np.clip(1 - ((xx - 256) / 126) ** 2 - ((yy - 275) / 125) ** 2, 0, 1))
    c.over(chrome(0.9 * h * bowl, steel_tint(), depth=70) * edge_darken(bowl, 10, 0.3), bowl)
    crest = blur(rect([246, 150, 266, 330], 8), 1)
    c.over(chrome(0.6 * pillow(crest, 6), gold_tint(), depth=40), crest)
    brim = blur(np.clip(ellipse([108, 300, 404, 372]) - ellipse([142, 296, 370, 346]) * (yy < 330), 0, 1), 1.2)
    c.over(chrome(0.5 * pillow(brim, 8), steel_tint(), depth=50), brim)
    trim = blur(np.clip(ellipse([112, 302, 400, 368]) - ellipse([120, 306, 392, 360]), 0, 1), 1)
    c.over(chrome(0.4 * pillow(trim, 4), gold_tint(), depth=30), trim * 0.9)
    # eye slit shadow under the brim, the nose guard over it
    slit = blur(rect([160, 352, 352, 372], 6), 2)
    c.over(np.zeros((N, N, 3)) + np.array([0.05, 0.05, 0.06]), slit * 0.8)
    nose = blur(poly([(244, 330), (268, 330), (262, 450), (250, 450)]), 1)
    c.over(chrome(0.6 * pillow(nose, 6), steel_tint(), depth=50), nose)
    for x in (172, 340):
        rivet = blur(ellipse([x - 9, 312, x + 9, 330]), 1)
        c.over(chrome(0.6 * pillow(rivet, 4), gold_tint(), depth=40), rivet)
    return c.image()
