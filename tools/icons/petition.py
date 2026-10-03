"""คำร้อง: a written petition with a quill laid across it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, rect, edge_darken, band


def quill(c, p0, p1, width=46):
    s, t = band(p0, p1, 0)
    w = width * np.clip(np.sin(np.clip((s - 0.15) / 0.85, 0, 1) * np.pi), 0, 1) ** 0.7
    vane = blur(((s > 0.15) & (s < 1) & (t > -w * 0.4) & (t < w)).astype(np.float32), 1.2)
    barbs = 0.5 + 0.5 * np.sin((s * 300 - np.abs(t) * 0.8) / 3.0)
    col = np.array([0.95, 0.93, 0.88])[None, None, :] * (0.82 + 0.18 * barbs[..., None])
    c.over(light(vane * 0.3 * np.cos(np.clip(t / (w + 1e-3), -1, 1) * 1.2), col, depth=40, spec=0.15), vane)
    shaft = blur(poly([p0, p1], width=7), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.85, 0.78, 0.62]), shaft)
    nib = blur(poly([p0, (p0[0] + (p1[0] - p0[0]) * 0.08, p0[1] + (p1[1] - p0[1]) * 0.08)], width=9), 0.8)
    c.over(np.zeros((N, N, 3)) + 0.08, nib)


def draw():
    rng = np.random.default_rng(301)
    c = Canvas()
    sheet = blur(poly([(110, 60), (390, 70), (400, 460), (100, 450)]), 1.2)
    col = parchment(rng)
    for k in range(9):
        y = 120 + k * 34
        ln = poly([(140, y), (360 - (k % 3) * 35, y + 3)], width=6)
        col = col * (1 - 0.45 * ln[..., None])
    sig = poly([(250, 420), (280, 405), (300, 425), (340, 400)], width=5)
    col = col * (1 - 0.6 * sig[..., None])
    c.over(light(0.12 * pillow(sheet, 8), col, depth=40, spec=0.05) * edge_darken(sheet, 10, 0.3), sheet)
    quill(c, (180, 470), (470, 120))
    return c.image()
