"""Shared painting helpers for the realistic icons.

Every icon is painted at N x N (512) with soft shading, then downsampled to 64 x 64 by build.py.
Light always comes from the upper left (LIGHT), so the whole set reads as one family.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

N = 512
yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
LIGHT = np.array([-0.55, -0.6, 0.58]); LIGHT /= np.linalg.norm(LIGHT)


def mask_from(draw_fn):
    m = Image.new('L', (N, N), 0)
    draw_fn(ImageDraw.Draw(m))
    return np.asarray(m, np.float32) / 255.0


def blur(a, r):
    return np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), np.float32) / 255.0


def noise(rng, scale, octaves=4):
    out = np.zeros((N, N), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(2, int(N / (scale * 2 ** o)))
        small = rng.random((s, s)).astype(np.float32)
        big = np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC), np.float32) / 255
        out += big * amp; tot += amp; amp *= 0.5
    return out / tot


class Canvas:
    def __init__(self):
        self.px = np.zeros((N, N, 4), np.float32)

    def over(self, rgb, alpha):
        a = np.clip(alpha, 0, 1)[..., None]
        self.px[..., :3] = self.px[..., :3] * (1 - a) + rgb * a
        self.px[..., 3:] = self.px[..., 3:] * (1 - a) + a

    def image(self):
        return Image.fromarray((np.clip(self.px, 0, 1) * 255).astype(np.uint8), 'RGBA')


def shadow(c, box, strength=0.45, radius=18):
    sh = mask_from(lambda d: d.ellipse(box, fill=255))
    c.over(np.zeros((N, N, 3)), blur(sh, radius) * strength)


def gold_coin(c, cx, cy, rx, ry, thick):
    """A gold coin lying almost flat: reeded edge below, rimmed face with a glint."""
    side = blur(mask_from(lambda d: (d.ellipse([cx - rx, cy - ry + thick, cx + rx, cy + ry + thick], fill=255),
                                     d.rectangle([cx - rx, cy, cx + rx, cy + thick], fill=255))), 1.2)
    t = np.clip((xx - (cx - rx)) / (2 * rx), 0, 1)
    side_rgb = np.array([0.62, 0.42, 0.06])[None, None, :] * (0.55 + 0.6 * np.sin(np.pi * t)[..., None])
    side_rgb *= (0.85 + 0.15 * (0.5 + 0.5 * np.sin(xx / 2.2)))[..., None]
    c.over(np.clip(side_rgb, 0, 1), side)
    face = blur(mask_from(lambda d: d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)), 1.2)
    u = (xx - cx) / rx; v = (yy - cy) / ry
    rr = np.sqrt(u**2 + v**2)
    shade = 0.75 + 0.35 * np.clip(-(u * 0.6 + v * 0.8), -1, 1)
    rgb = np.array([0.95, 0.74, 0.22])[None, None, :] * shade[..., None]
    rim = np.clip(1 - np.abs(rr - 0.88) / 0.07, 0, 1)
    ring = np.clip(1 - np.abs(rr - 0.66) / 0.035, 0, 1)
    rgb = rgb * (1 + 0.25 * rim[..., None]) * (1 - 0.3 * ring[..., None])
    g = np.exp(-(((u + 0.35) / 0.18)**2 + ((v + 0.45) / 0.10)**2))
    c.over(np.clip(rgb + 0.55 * g[..., None], 0, 1), face)
