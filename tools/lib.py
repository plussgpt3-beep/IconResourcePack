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


# ===== Surface shading from a height map (Stage 1 onward) =====
# Draw a silhouette, turn it into a height map (pillow(), plus engraved/embossed details),
# then light() shades it with the shared LIGHT: that is what makes flat shapes read as objects.

VIEW_HALF = LIGHT + np.array([0, 0, 1.0]); VIEW_HALF /= np.linalg.norm(VIEW_HALF)


def pillow(mask, radius=12, power=0.6):
    """A soft rounded height from a 0..1 mask: flat in the middle, falling off at the edges."""
    return np.clip(blur(mask, radius) * 1.0, 0, 1) ** power * mask


def light(height, albedo, depth=60.0, ambient=0.38, spec=0.25, gloss=30):
    """Shades an albedo (N,N,3) by the normals of a height map (0..1, scaled by depth px)."""
    gy, gx = np.gradient(height * depth)
    n = np.dstack([-gx, -gy, np.ones_like(gx)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    diff = np.clip(n @ LIGHT, 0, 1)
    hl = np.clip(n @ VIEW_HALF, 0, 1) ** gloss
    return np.clip(albedo * (ambient + (1 - ambient) * diff)[..., None] + spec * hl[..., None], 0, 1)


def flat(rgb):
    return np.broadcast_to(np.array(rgb, np.float32), (N, N, 3)).copy()


def wood(rng, base=(0.55, 0.36, 0.20), angle=0.0, rings=28.0):
    """Planed wood: long grain lines along `angle` (radians), with warped streaks and knots of noise."""
    ca, sa = np.cos(angle), np.sin(angle)
    u = xx * ca + yy * sa; v = -xx * sa + yy * ca
    warp = noise(rng, 3, 3) * 40
    grain = 0.5 + 0.5 * np.sin((v + warp) / N * rings * 2 * np.pi)
    fine = noise(rng, 40, 2)
    streak = noise(rng, 2, 2)
    k = 0.72 + 0.22 * grain + 0.12 * (fine - 0.5) + 0.15 * (streak - 0.5)
    return np.array(base)[None, None, :] * k[..., None]


def parchment(rng, base=(0.90, 0.82, 0.62)):
    blot = noise(rng, 4, 4); fib = noise(rng, 50, 2)
    k = 0.88 + 0.16 * (blot - 0.5) + 0.08 * (fib - 0.5)
    return np.array(base)[None, None, :] * k[..., None]


def metal(rng, base=(0.62, 0.64, 0.68)):
    brushed = noise(rng, 60, 2)
    return np.array(base)[None, None, :] * (0.9 + 0.15 * (brushed - 0.5))[..., None]


def edge_darken(mask, radius=10, amount=0.45):
    """Ambient occlusion at a silhouette: multiply an rgb by this."""
    return (1 - amount * np.clip((1 - blur(mask, radius)) * 2.2, 0, 1) * mask)[..., None]


def poly(points, width=None):
    """Mask of a filled polygon, or of a thick polyline when width is given."""
    if width:
        return mask_from(lambda d: d.line(points, fill=255, width=width, joint='curve'))
    return mask_from(lambda d: d.polygon(points, fill=255))


def ellipse(box):
    return mask_from(lambda d: d.ellipse(box, fill=255))


def rect(box, radius=0):
    return mask_from(lambda d: d.rounded_rectangle(box, radius=radius, fill=255))


def wax_seal(c, rng, cx, cy, r, color, symbol_mask):
    """A blob of sealing wax with an embossed rim and a symbol pressed into it."""
    ang = np.arctan2(yy - cy, xx - cx)
    rr = np.hypot(xx - cx, yy - cy)
    wobble = r * (1 + 0.05 * np.sin(ang * 5 + 1.3) + 0.022 * np.sin(ang * 9 + 0.4) + 0.012 * np.sin(ang * 17))
    blob = blur((rr < wobble).astype(np.float32), 2)
    h = pillow(blob, 26, 0.7) * 0.8
    disc = blur((rr < r * 0.68).astype(np.float32), 1.5)
    ring = blur(((rr > r * 0.68) & (rr < r * 0.76)).astype(np.float32), 1.5)
    h = h - 0.18 * disc + 0.10 * ring           # the stamp's face is pressed in, its rim raised
    h = h + 0.16 * blur(symbol_mask, 2.5) * disc  # the symbol stands up out of the face
    col = np.array(color)[None, None, :] * (0.92 + 0.12 * noise(rng, 30, 2)[..., None])
    c.over(light(h, col, depth=90, ambient=0.3, spec=0.5, gloss=40), blob)
