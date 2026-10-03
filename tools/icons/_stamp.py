"""A wooden-handled stamp over the mark it has just made: shared by stamp_approve / stamp_deny."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, rect, ellipse, wood, edge_darken, chrome, gold_tint, _symbol


def stamp(ink, kind, seed):
    rng = np.random.default_rng(seed)
    c = Canvas()
    sheet = blur(poly([(70, 300), (400, 270), (450, 470), (110, 500)]), 1.2)
    col = parchment(rng)
    mark = blur(_symbol(kind, 250, 400, 120) * (np.random.default_rng(seed).random((N, N)) > 0.15), 1.5)
    ring = blur(((np.abs(np.hypot(xx - 250, yy - 400) - 92) < 7)).astype(np.float32), 1.2)
    col = col * (1 - np.clip(mark + ring, 0, 1)[..., None] * (1 - np.array(ink)))
    c.over(light(0.1 * pillow(sheet, 8), col, depth=30, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    # the stamp: knob, handle, brass collar, rubber foot
    foot = blur(rect([200, 250, 350, 300], 10), 1)
    c.over(light(0.3 * pillow(foot, 6), np.zeros((N, N, 3)) + np.array(ink) * 0.6, depth=30, spec=0.2), foot)
    collar = blur(rect([215, 215, 335, 255], 8), 1)
    c.over(chrome(np.clip(1 - np.abs(xx - 275) / 60, 0, 1) ** 0.5 * collar, gold_tint(), depth=40), collar)
    handle = blur(np.maximum(rect([245, 90, 305, 220], 20), ellipse([220, 30, 330, 130])), 1)
    nx = np.clip((xx - 275) / 55, -1, 1)
    c.over(light(np.sqrt(1 - nx ** 2) * handle * 0.8, wood(rng, (0.40, 0.22, 0.10), angle=np.pi / 2, rings=5), depth=60, spec=0.4), handle)
    return c.image()
