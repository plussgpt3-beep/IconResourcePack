"""ฎีกาหมวดข้อเสนอแนะ: a brass oil lamp burning - a bright idea in a medieval hand."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, ellipse, chrome


def draw():
    c = Canvas()
    brass = (0.98, 0.72, 0.30)
    body = blur(np.maximum(ellipse([110, 300, 380, 430]), poly([(330, 330), (440, 280), (452, 300), (360, 380)])), 1.2)
    c.over(chrome(pillow(body, 40, 0.6), brass, depth=70), body)
    handle = blur(poly([(120, 340), (64, 320), (60, 390), (118, 404)], width=18), 1)
    c.over(chrome(pillow(handle, 6) * 0.6, brass, depth=40), handle)
    lid = blur(ellipse([190, 280, 300, 320]), 1)
    c.over(chrome(pillow(lid, 10) * 0.6, (0.85, 0.60, 0.25), depth=40), lid)
    foot = blur(ellipse([170, 418, 320, 452]), 1)
    c.over(chrome(pillow(foot, 8) * 0.6, (0.80, 0.56, 0.22), depth=40), foot)
    flame = blur(poly([(430, 290), (486, 214), (452, 70), (408, 180), (398, 250)]), 3)
    t = np.clip((yy - 70) / 220, 0, 1)
    rgb = np.dstack([np.ones_like(t), 0.95 - 0.45 * t, 0.55 - 0.5 * t])
    c.over(np.clip(rgb, 0, 1), flame)
    core = blur(poly([(432, 284), (458, 226), (446, 150), (420, 230)]), 3)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 1.0, 0.85]), 0.9 * core)
    return c.image()
