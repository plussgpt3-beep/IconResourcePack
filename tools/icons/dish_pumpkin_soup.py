"""ซุปฟักทองนม (หม้อปรุงอาหาร, 2026-11-27): a bowl of orange pumpkin soup with a swirl of cream."""
import numpy as np
from lib import Canvas, poly, blur
from _dishes import bowl, broth, steam, specks


def draw():
    rng = np.random.default_rng(2709)
    c = Canvas()
    inner = bowl(c, rng)
    broth(c, rng, inner, (0.96, 0.52, 0.08), gloss=0.6)
    t = np.linspace(0, 3.2 * np.pi, 60)
    pts = [(256 + (12 + 9 * a) * np.cos(a) * 1.6, 250 + (12 + 9 * a) * np.sin(a) * 0.6) for a in t]
    swirl = blur(poly(pts, width=9), 2) * inner
    c.over(np.zeros((512, 512, 3)) + np.array([0.99, 0.95, 0.86]), swirl * 0.9, cast=False)
    specks(c, rng, inner, 18, (0.25, 0.50, 0.18), 2, 4)
    specks(c, rng, inner, 10, (0.20, 0.12, 0.06), 1.5, 3, shade=False)
    steam(c)
    return c.image()
