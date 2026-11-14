"""Surface detail pass for the 512 gear paintings (weapons/armour icons): forged-steel grain along the length,
a lit bevel on every edge (outline and inner part edges), fine scratches and hammer marks on the bright metal,
and grime in the creases. Applied before the icon is shrunk, so 128 px icons keep it."""
import zlib
import numpy as np
from PIL import Image, ImageFilter
from lib import blur, N


def _stretch_noise(rng, angle_deg, along=60.0, across=1.6):
    """Noise of fine streaks running at angle (grain of forged steel / wood)."""
    small = rng.random((N // 8, N // 8)).astype(np.float32)
    img = Image.fromarray((small * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)
    a = np.radians(angle_deg)
    # blur along the direction by rotating, box-blurring horizontally, rotating back
    r = img.rotate(np.degrees(a), resample=Image.BICUBIC, expand=False)
    r = r.filter(ImageFilter.BoxBlur(0)).resize((max(1, int(N / along * 8)), N), Image.BILINEAR).resize((N, N), Image.BICUBIC)
    r = r.rotate(-np.degrees(a), resample=Image.BICUBIC, expand=False)
    return np.asarray(r).astype(np.float32) / 255.0


def enhance(img, name, strength=1.0):
    px = np.asarray(img.convert('RGBA')).astype(np.float32) / 255.0
    rgb, a = px[..., :3], px[..., 3]
    rng = np.random.default_rng(zlib.crc32(('detail' + name).encode()))
    lum = (rgb * [0.299, 0.587, 0.114]).sum(-1)
    sat = rgb.max(-1) - rgb.min(-1)
    mask = (a > 0.5).astype(np.float32)
    angle = -45.0 if '_bow_' not in name else 45.0
    # 1. grain along the item
    g = _stretch_noise(rng, angle)
    rgb = rgb * (1 + 0.55 * strength * (g - 0.5)[..., None] * mask[..., None])
    # 2. bevel: inner edges from luminance steps + outline; lit from the upper left
    lb = blur(lum, 3.0)
    gy, gx = np.gradient(lb)
    edge = np.clip(np.hypot(gx, gy) * 9, 0, 1) * mask
    am = blur(mask, 7.0); ay, ax = np.gradient(am)
    rim = np.clip(np.hypot(ax, ay) * 14, 0, 1) * mask
    facing = np.clip(-(ax + ay) * 20, -1, 1)          # >0 on edges facing the light
    rgb = rgb + (0.30 * rim * np.clip(facing, 0, 1))[..., None] * strength
    rgb = rgb * (1 - 0.30 * rim * np.clip(-facing, 0, 1))[..., None]
    rgb = rgb * (1 - 0.10 * edge * strength)[..., None]
    # 3. scratches + hammer marks on bright metal (low saturation, high luminance)
    metal = mask * np.clip((lum - 0.35) * 3, 0, 1) * np.clip(1 - sat * 2.2, 0.25, 1)
    scr = np.zeros((N, N), np.float32)
    for _ in range(int(26 * strength)):
        x, y = rng.integers(40, N - 40, 2); ln = rng.integers(18, 50); ang = np.radians(angle + rng.normal(0, 25))
        for k in range(ln):
            xx, yy = int(x + np.cos(ang) * k), int(y + np.sin(ang) * k)
            if 2 <= xx < N - 2 and 2 <= yy < N - 2: scr[yy - 1:yy + 2, xx - 1:xx + 2] = 1
    dents = blur((rng.random((N, N)) > 0.9992).astype(np.float32), 6) * 160
    rgb = rgb + (0.28 * scr * metal)[..., None] - (0.16 * np.clip(dents, 0, 1) * metal)[..., None]
    # 4. grime in creases (dark bands where parts meet)
    crease = blur(edge, 2.5) * (1 - metal * 0.5)
    rgb = rgb * (1 - 0.12 * crease)[..., None]
    out = np.dstack([np.clip(rgb, 0, 1), a])
    return Image.fromarray((out * 255).astype(np.uint8), 'RGBA')
