"""หนังสือราชบัลลังก์: a closed royal book - purple leather, gilt corners and clasp, a gold crown on the cover, page edges showing."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, parchment, edge_darken, chrome, gold_tint, leather_col
from king import gem


def draw():
    rng = np.random.default_rng(1810)
    c = Canvas()
    # page block (seen at the right and bottom edge, a little thicker than the cover)
    pages = blur(rect([100, 84, 456, 474], 10), 1.2)
    col = parchment(rng, (0.93, 0.88, 0.72))
    lines = (np.sin(yy / 2.2) * 0.5 + 0.5) * 0.10
    col = col * (1 - lines[..., None])
    c.over(np.clip(col, 0, 1), pages)
    # the cover
    cover = blur(rect([82, 70, 408, 436], 18), 1.5)
    leather = leather_col(rng, (0.30, 0.08, 0.36))
    c.over(light(0.32 * pillow(cover, 16), leather, depth=50, spec=0.22) * edge_darken(cover, 12, 0.45), cover)
    # spine ridges on the left
    for y in (130, 250, 370):
        ridge = blur(rect([82, y - 10, 128, y + 10], 6), 1)
        c.over(light(0.4 * pillow(ridge, 6), leather * 1.15, depth=40, spec=0.3), ridge)
    # gilt frame line on the cover
    frame = np.clip(blur(rect([140, 104, 384, 402], 8), 1) - blur(rect([152, 116, 372, 390], 6), 1), 0, 1)
    c.over(chrome(0.4 * pillow(frame, 3), gold_tint(), depth=30), frame)
    # gilt corners
    for (x0, y0, sx, sy) in [(408, 70, -1, 1), (408, 436, -1, -1)]:
        tri = blur(poly([(x0, y0), (x0 + sx * 70, y0), (x0, y0 + sy * 70)]), 1)
        c.over(chrome(0.5 * pillow(tri, 8), gold_tint(), depth=40), tri)
    # the clasp
    clasp = blur(rect([372, 228, 430, 280], 8), 1)
    c.over(chrome(0.6 * pillow(clasp, 8), gold_tint(), depth=40), clasp)
    # crown on the cover
    cx, cy, s = 262, 250, 0.55
    pts = [(-156, 90), (-156, -110), (-106, -30), (-78, -170), (-41, -50), (0, -200), (41, -50), (78, -170), (106, -30), (156, -110), (156, 90)]
    crown = blur(poly([(cx + x * s, cy + y * s) for x, y in pts]), 1.2)
    band = blur(rect([cx - 158 * s, cy + 10 * s, cx + 158 * s, cy + 92 * s], 8), 1.2)
    nx = (xx - cx) / (156 * s)
    h = np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * 0.5 * crown + 0.25 * pillow(band, 6)
    c.over(chrome(h, gold_tint(), depth=50), np.maximum(crown, band))
    for x, y in [(-156, -116), (-78, -176), (0, -206), (78, -176), (156, -116)]:
        r = 16 * s
        b = blur(ellipse([cx + x * s - r, cy + y * s - r, cx + x * s + r, cy + y * s + r]), 1)
        c.over(chrome(pillow(b, 6, 0.7), gold_tint(), depth=30), b)
    gem(c, cx, cy + 52 * s, 16, (0.15, 0.25, 0.85))
    for x in (-90, 90):
        gem(c, cx + x * s, cy + 52 * s, 11, (0.80, 0.06, 0.08))
    return c.image()
