"""Evolved gear tier 5 แดนอเวจี (2026-11-20, the user picked "แนวอเวจี"): the tier-4 masterwork reforged in the abyss.
The metal turns to obsidian (shading kept), gold to hell-gold, the element glow stays and grows; glowing runes are cut
into the metal and a violet-and-element aura with sparks surrounds it. abyssify() also recolours worn-armour textures."""
import zlib
import numpy as np
from PIL import Image
from lib import N, blur, poly, ellipse
from _gear import ELEMENTS

VIOLET = np.array((0.62, 0.28, 1.0))


def _hsv(rgb):
    mx = rgb.max(-1); mn = rgb.min(-1)
    sat = np.where(mx > 1e-4, (mx - mn) / np.maximum(mx, 1e-4), 0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = np.maximum(mx - mn, 1e-4)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, sat, mx


def recolour(rgb, elem):
    """Obsidian metal, hell-gold trim, the element's glow kept (rgb in 0-1, HxWx3)."""
    glow = np.array(ELEMENTS[elem][1])
    h, s, v = _hsv(rgb)
    lum = (rgb * np.array((0.3, 0.55, 0.15))).sum(-1)
    glowm = np.clip((s - 0.40) / 0.3, 0, 1) * np.clip((v - 0.72) / 0.2, 0, 1)
    goldm = np.clip((s - 0.35) / 0.2, 0, 1) * np.clip(1 - np.abs(h - 45) / 18, 0, 1) * (1 - glowm)
    l = lum[..., None]
    tint = glow * 0.55 + VIOLET * 0.25                      # the element still shows in the obsidian's light
    obs = np.array((0.04, 0.02, 0.07)) * (1 - l ** 0.9) + tint * l ** 0.9
    obs = obs + np.clip(l - 0.75, 0, 1) * 3 * np.clip(glow * 0.7 + 0.3, 0, 1)
    hell = np.array((0.30, 0.06, 0.05)) * (1 - l) + np.array((1.0, 0.58, 0.26)) * l
    lit = np.clip(rgb * 0.5 + glow * 0.6 * v[..., None], 0, 1)
    out = obs * (1 - goldm[..., None]) + hell * goldm[..., None]
    return np.clip(out * (1 - glowm[..., None]) + lit * glowm[..., None], 0, 1)


def _glow(px, mask, col, k=0.9, halo=6):
    a = np.clip(blur(mask, halo) * k, 0, 0.9)[..., None]
    px[..., :3] = px[..., :3] * (1 - a) + col * a
    px[..., 3] = np.maximum(px[..., 3], a[..., 0])
    m = np.clip(mask, 0, 1)[..., None]
    px[..., :3] = px[..., :3] * (1 - m) + np.clip(col * 0.5 + 0.5, 0, 1) * m


def abyssify(img, elem, seed, recolour_metal=True):
    rng = np.random.default_rng(zlib.crc32(repr(('abyss5', seed)).encode()))
    px = np.asarray(img.convert('RGBA')).astype(np.float32) / 255
    A = px[..., 3].copy()
    if recolour_metal: px[..., :3] = recolour(px[..., :3], elem)
    glow = np.array(ELEMENTS[elem][1])
    # runes cut into the metal
    inner = np.clip((blur((A > 0.5).astype(np.float32), 6) - 0.92) * 14, 0, 1)
    ys, xs = np.nonzero(inner > 0.5)
    runes = np.zeros((N, N), np.float32)
    if len(xs):
        for _ in range(6):
            i = rng.integers(len(xs)); x, y = float(xs[i]), float(ys[i]); r = rng.uniform(5, 8)
            strokes = [[(x - r, y - r), (x + r, y + r)], [(x, y - r * 1.2), (x, y + r * 1.2)], [(x - r, y), (x + r * 0.6, y - r)],
                       [(x - r * 0.7, y + r), (x + r * 0.7, y + r)]]
            for k in rng.choice(len(strokes), size=2 + rng.integers(2), replace=False):
                runes = np.maximum(runes, poly([(round(a), round(b)) for a, b in strokes[k]], width=4))
        runes = blur(runes, 0.8) * (A > 0.5)
        if recolour_metal: _glow(px, runes, glow * 0.6 + VIOLET * 0.4, 0.7, 5)
        # the tier-5 new shapes carry their own etched glow; no painted runes (they read as letters)
    # a glowing rim in the element's colour
    solid = (A > 0.5).astype(np.float32)
    rim = np.clip(solid - np.clip((blur(solid, 3) - 0.75) * 6, 0, 1), 0, 1)
    _glow(px, rim * 0.85, glow, 0.6, 4)
    # aura and sparks round the silhouette
    halo = np.clip(blur(A, 20) * 1.7 - A, 0, 0.85)
    aura = glow * 0.7 + VIOLET * 0.3
    a = halo[..., None]
    px[..., :3] = px[..., :3] * (1 - a * (1 - px[..., 3:4])) + aura * a * (1 - px[..., 3:4])
    px[..., 3] = np.maximum(px[..., 3], halo)
    ring = np.clip(blur(A, 26) - A, 0, 1)
    ys, xs = np.nonzero(ring > 0.12)
    if len(xs):
        for _ in range(18):
            i = rng.integers(len(xs)); x, y = float(xs[i]), float(ys[i]); r = rng.uniform(3, 6)
            _glow(px, blur(ellipse([x - r, y - r, x + r, y + r]), 1), glow if rng.random() < 0.6 else VIOLET, 0.8, 4)
    return Image.fromarray((np.clip(px, 0, 1) * 255).astype(np.uint8), 'RGBA')


def draw(kind, path):
    elem = path.split('_')[0]
    if kind == 'sword':
        from _gear import draw as d; base = d(path, 4)
    elif kind in ('axe', 'bow'):
        import _gear2; base = getattr(_gear2, kind)(path, 4)
    else:
        from _gear2 import armour; base = armour(kind, elem, 4)
    return abyssify(base, elem, (kind, path))


def texture(img, elem):
    """A worn-armour layer (small texture): recoloured, and a few pixels of rune glow on the metal."""
    px = np.asarray(img.convert('RGBA')).astype(np.float32) / 255
    px[..., :3] = recolour(px[..., :3], elem)
    rng = np.random.default_rng(zlib.crc32(repr(('abyss5tex', elem)).encode()))
    glow = np.array(ELEMENTS[elem][1]) * 0.7 + VIOLET * 0.3
    ys, xs = np.nonzero(px[..., 3] > 0.9)
    for _ in range(max(1, len(xs) // 40)):
        i = rng.integers(len(xs)); px[ys[i], xs[i], :3] = glow
    return Image.fromarray((np.clip(px, 0, 1) * 255).astype(np.uint8), 'RGBA')
