"""พิมพ์เอง: a goose quill standing in a glass inkwell."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, blur, poly, ellipse, rect, edge_darken, noise, mask_from


def draw():
    rng = np.random.default_rng(71)
    c = Canvas()
    shadow(c, [90, 430, 400, 492], 0.45, 16)
    # inkwell: squat dark glass bottle
    bottle = blur(np.maximum(ellipse([110, 290, 360, 470]), rect([160, 250, 310, 330], 20)), 1.5)
    nx = (xx - 235) / 125; ny = (yy - 380) / 95
    h = np.sqrt(np.clip(1 - nx**2 - ny**2, 0, 1)) * 0.8 * bottle + 0.2 * pillow(bottle, 10)
    glass = np.zeros((N, N, 3)) + np.array([0.10, 0.12, 0.20])
    c.over(light(h, glass, depth=80, ambient=0.5, spec=0.9, gloss=60), bottle)
    neck = blur(ellipse([160, 236, 310, 268]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.03, 0.03, 0.05]), neck)
    # glass glints
    for box in ([150, 320, 175, 400], [190, 262, 205, 300]):
        c.over(np.ones((N, N, 3)), blur(ellipse(box), 4) * 0.55)
    # quill: shaft from the ink up to the upper right, vane along it
    a = np.array([235.0, 250.0]); b = np.array([440.0, 40.0])
    d = (b - a) / np.linalg.norm(b - a); n = np.array([-d[1], d[0]])
    s = (xx - a[0]) * d[0] + (yy - a[1]) * d[1]           # along the shaft
    t = (xx - a[0]) * n[0] + (yy - a[1]) * n[1]           # across it
    L = np.linalg.norm(b - a)
    sn = np.clip(s / L, 0, 1)
    width = 62 * np.sin(np.clip((sn - 0.18) / 0.82, 0, 1) * np.pi) ** 0.7 * (s > 0.18 * L) * (s < L)
    vane = ((t > -width * 0.45) & (t < width) & (s > 0) & (s < L)).astype(np.float32)
    vane = blur(vane, 1.5)
    barbs = 0.5 + 0.5 * np.sin((s * 0.9 - np.abs(t) * 0.6) / 3.0)
    col = np.array([0.97, 0.95, 0.90])[None, None, :] * (0.86 + 0.14 * barbs[..., None]) * (0.9 + 0.15 * noise(rng, 30, 2)[..., None])
    hv = vane * (0.5 + 0.5 * np.cos(np.clip(t / (width + 1e-3), -1, 1) * np.pi / 2)) * 0.5
    c.over(light(hv, col, depth=50, spec=0.15), vane)
    shaft = blur(poly([tuple(a + d * 5), tuple(b)], width=9), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.85, 0.80, 0.68]), shaft)
    # nib, dark with ink, just inside the neck
    nib = blur(poly([tuple(a - d * 4 + n * 6), tuple(a - d * 4 - n * 6), tuple(a - d * 40)]), 1)
    c.over(np.zeros((N, N, 3)) + 0.06, nib)
    return c.image()
