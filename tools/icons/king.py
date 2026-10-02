"""กษัตริย์: a gold crown set with rubies and a sapphire, on a red velvet cap."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, cloth


def gem(c, cx, cy, r, color):
    g = blur(ellipse([cx - r, cy - r, cx + r, cy + r]), 1)
    rr = np.hypot(xx - cx, yy - cy) / r
    facet = 0.6 + 0.4 * np.cos(np.arctan2(yy - cy, xx - cx) * 4) * (rr > 0.4)
    col = np.array(color)[None, None, :] * facet[..., None]
    glint = np.exp(-(((xx - cx + r * 0.35) / (r * 0.25)) ** 2 + ((yy - cy + r * 0.35) / (r * 0.25)) ** 2))
    c.over(np.clip(col * (0.6 + 0.6 * (1 - rr[..., None])) + glint[..., None], 0, 1), g)


def draw():
    rng = np.random.default_rng(212)
    c = Canvas()
    cap = blur(ellipse([150, 150, 362, 380]), 2)
    c.over(light(pillow(cap, 30) * 0.8, cloth(rng, (0.50, 0.04, 0.06), weave=2), depth=60, spec=0.15), cap)
    # the crown: a band with five points, each tipped with a ball
    pts = [(100, 420), (100, 220), (150, 300), (178, 160), (215, 280), (256, 110), (297, 280), (334, 160), (362, 300), (412, 220), (412, 420)]
    crown = blur(poly(pts), 1.5)
    nx = (xx - 256) / 156
    h = np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * 0.6 * crown
    band = blur(rect([96, 340, 416, 430], 14), 1.5)
    h = h + 0.25 * pillow(band, 10)
    c.over(chrome(h, gold_tint(), depth=60), np.maximum(crown, band))
    for x, y in [(100, 214), (178, 154), (256, 102), (334, 154), (412, 214)]:
        b = blur(ellipse([x - 18, y - 18, x + 18, y + 18]), 1)
        c.over(chrome(pillow(b, 9, 0.7), gold_tint(), depth=40), b)
    gem(c, 256, 385, 26, (0.15, 0.25, 0.85))
    for x in (160, 352): gem(c, x, 385, 18, (0.80, 0.06, 0.08))
    for x in (178, 256, 334): gem(c, x, 250 if x != 256 else 200, 13, (0.80, 0.06, 0.08))
    return c.image()
