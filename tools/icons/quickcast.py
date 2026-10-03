"""Quickcast (ปุ่มลัด Z/X/C/V): four ivory key caps marked Z X C V, a spark over the first."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, noise

FONT = '/usr/share/fonts/truetype/tlwg/Garuda-Bold.ttf'


def letter_mask(ch, cx, cy, size):
    m = Image.new('L', (N, N), 0); d = ImageDraw.Draw(m)
    f = ImageFont.truetype(FONT, size)
    w = d.textlength(ch, font=f)
    d.text((cx - w / 2, cy - size * 0.62), ch, font=f, fill=255)
    return np.asarray(m, np.float32) / 255.0


def draw():
    rng = np.random.default_rng(1103)
    c = Canvas()
    keys = [('Z', 130, 170), ('X', 382, 170), ('C', 130, 390), ('V', 382, 390)]
    for ch, cx, cy in keys:
        base = blur(rect([cx - 104, cy - 92, cx + 104, cy + 104], 30), 1.5)
        col = np.zeros((N, N, 3)) + np.array([0.52, 0.48, 0.42])
        c.over(light(pillow(base, 20, 0.6) * 0.7, col, depth=50, spec=0.15), base)
        top = blur(rect([cx - 84, cy - 84, cx + 84, cy + 74], 26), 1.5)
        ivory = np.zeros((N, N, 3)) + np.array([0.93, 0.89, 0.80])
        ivory = ivory * (0.94 + 0.08 * noise(rng, 20, 2))[..., None]
        dish = 0.12 * np.clip(1 - np.hypot(xx - cx, yy - cy + 5) / 90, 0, 1)
        lm = blur(letter_mask(ch, cx, cy - 4, 120), 1)
        ivory = ivory * (1 - 0.82 * lm[..., None]) + np.array([0.10, 0.07, 0.05]) * 0.82 * lm[..., None]
        c.over(light(pillow(top, 18, 0.6) * 0.6 - dish - 0.05 * lm, ivory, depth=60, spec=0.35), top)
    # a spark: the skill fires the moment the key is pressed
    ang = np.arctan2(yy - 256, xx - 256); d = np.hypot(xx - 256, yy - 256)
    star = blur((d < 70 * (0.25 + 0.75 * np.abs(np.cos(2 * ang)) ** 6)).astype(np.float32), 2)
    glow = blur(star, 14) * 0.8
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.86, 0.35]), glow, cast=False)
    c.over(chrome(0.5 * pillow(star, 6), (1.0, 0.92, 0.55), depth=40), star)
    return c.image()
