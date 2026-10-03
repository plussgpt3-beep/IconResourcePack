"""Row-category icons (the user, 2026-10-03 "ขอ icon หมวดหมู่ด้วย"): the coloured glass label at the
left of every menu row becomes a hanging pennant. The cloth keeps the label's glass colour, so the
colour still says which category a row is (the menu rule); the embossed emblem says what it holds -
the silhouette of the matching button icon, or a badge glyph."""
import numpy as np
from PIL import Image
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, cloth, load_icon, _symbol

# the glass pane colours of the current labels, as cloth
GLASS = {
    'LIGHT_BLUE': (0.20, 0.45, 0.72), 'LIME': (0.36, 0.62, 0.12), 'YELLOW': (0.86, 0.68, 0.10), 'ORANGE': (0.82, 0.40, 0.07),
    'PURPLE': (0.42, 0.16, 0.58), 'RED': (0.62, 0.09, 0.07), 'WHITE': (0.88, 0.86, 0.80), 'LIGHT_GRAY': (0.55, 0.55, 0.56),
    'CYAN': (0.08, 0.52, 0.58),
}
CLOTH_PTS = [(116, 96), (396, 96), (396, 440), (256, 380), (116, 440)]
INNER_PTS = [(134, 112), (378, 112), (378, 412), (256, 360), (134, 412)]


def _glyph(kind):
    cx, cy, r = 256, 236, 150
    if kind == 'gear':
        ang = np.arctan2(yy - cy, xx - cx); d = np.hypot(xx - cx, yy - cy)
        return ((d < 95 * (0.80 + 0.20 * (np.cos(ang * 8) > 0.1))) & (d > 34)).astype(np.float32)
    if kind == 'swap':
        top = np.maximum(rect([150, 180, 330, 206]), poly([(330, 160), (380, 193), (330, 226)]))
        bot = np.maximum(rect([182, 266, 362, 292]), poly([(182, 246), (132, 279), (182, 312)]))
        return np.maximum(top, bot)
    return _symbol(kind, cx, cy, r)


def _emblem(source):
    """(mask, relief) of the emblem, fitted into the cloth's field. An icon's own shading becomes
    the relief, so its details (lines on a page, the rose of a compass) stay readable in gold."""
    if source.startswith('glyph:'):
        m = blur(_glyph(source[6:]), 1.5)
        return m, pillow(m, 7) * 0.55
    img = load_icon(source).draw()
    a = np.asarray(img)[..., 3]
    ys, xs = np.nonzero(a > 30)
    img = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    k = 190 / max(img.size)
    small = img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)
    layer = Image.new('RGBA', (N, N)); layer.alpha_composite(small, (int(256 - small.width / 2), int(236 - small.height / 2)))
    px = np.asarray(layer, np.float32) / 255.0
    m = blur((px[..., 3] > 0.35).astype(np.float32), 1.0)
    lum = (px[..., :3] * [0.3, 0.59, 0.11]).sum(axis=2)
    return m, (0.35 * pillow(m, 6) + 0.35 * blur(lum, 1.2)) * m


def pennant(color_name, source, seed=0):
    rng = np.random.default_rng(900 + seed)
    c = Canvas()
    col = GLASS[color_name]
    # the cloth: hanging in soft folds, a swallow tail at the bottom
    cl = blur(poly(CLOTH_PTS), 1.5)
    folds = np.sin((xx - 116) / 280 * np.pi * 2.5)
    sag = np.clip((yy - 96) / 344, 0, 1)
    h = (0.28 + 0.10 * folds * sag) * cl
    c.over(light(h, cloth(rng, col, weave=2.2), depth=60, spec=0.08), cl)
    # gold trim
    inner = blur(poly(INNER_PTS), 1)
    trim = np.clip(cl - inner, 0, 1)
    c.over(chrome(0.45 * pillow(trim, 3) + 0.4 * h, gold_tint(), depth=40), trim)
    # emblem: gold on dark cloth, dark iron on light cloth
    em, relief = _emblem(source)
    em = em * inner
    lum = col[0] * 0.3 + col[1] * 0.59 + col[2] * 0.11
    tint = gold_tint() if lum < 0.5 else (0.30, 0.24, 0.16)
    c.over(chrome(relief + 0.25 * h, tint, depth=45, sky=0.95 if lum < 0.5 else 0.7, ground=0.18 if lum < 0.5 else 0.05), em)
    # the rod it hangs from, with knobs
    rod = blur(rect([90, 74, 422, 100], 12), 1)
    c.over(chrome(0.5 * pillow(rod, 8), gold_tint(), depth=40), rod)
    for x in (92, 420):
        kb = blur(ellipse([x - 22, 65, x + 22, 109]), 1)
        c.over(chrome(pillow(kb, 10, 0.7), gold_tint(), depth=40), kb)
    cord = blur(np.maximum(poly([(150, 76), (256, 20), (362, 76)], width=7), ellipse([240, 6, 272, 38]) - ellipse([248, 14, 264, 30])), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.12, 0.10]), np.clip(cord, 0, 1))
    return c.image()
