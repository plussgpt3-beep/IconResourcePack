"""Guild shields for the professions (อาชีพ, 2026-10-28, the user: "ทำไอคอนอาชีพเอง"): a heater shield in the
class colour of the profession (green = ชั้นสามัญ, bronze = ชั้นช่าง, purple = ชั้นขุนนาง) with a rim of iron,
bronze or gold, and the profession's charge painted on it."""
import numpy as np
from PIL import Image
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, chrome, cloth, edge_darken, gold_tint

CLASS = {
    'common': ((0.16, 0.38, 0.18), (0.40, 0.41, 0.44)),
    'craft': ((0.55, 0.28, 0.08), (0.80, 0.50, 0.26)),
    'noble': ((0.30, 0.10, 0.40), None),
}


def _outline(inset=0):
    top, left, right, bottom = 40 + inset, 56 + inset, 456 - inset, 486 - inset
    pts = [(left, top), (right, top), (right, 250)]
    for k in range(1, 20):                      # the curved lower edge down to the point
        t = k / 20
        pts.append((right - (right - 256) * t ** 1.7, 250 + (bottom - 250) * t))
    pts.append((256, bottom))
    for k in range(19, 0, -1):
        t = k / 20
        pts.append((left + (256 - left) * t ** 1.7, 250 + (bottom - 250) * t))
    pts.append((left, 250))
    return pts


def shield(rng, klass):
    """The bare shield, as a Canvas: an enamelled field inside a raised metal rim."""
    field_col, rim = CLASS[klass]
    rim = rim or gold_tint()
    c = Canvas()
    outer = blur(poly(_outline(0)), 1.5)
    inner = blur(poly(_outline(30)), 1.5)
    ring = np.clip(outer - inner, 0, 1)
    col = cloth(rng, field_col, weave=2.0)
    c.over(light(0.25 * pillow(inner, 40), col, depth=40, spec=0.15) * edge_darken(inner, 14, 0.35), inner)
    c.over(chrome(0.8 * pillow(ring, 8), rim, depth=50, sky=0.85, ground=0.12), np.maximum(ring, outer * (1 - inner)))
    for (x, y) in ((92, 76), (420, 76), (92, 236), (420, 236), (256, 450)):   # rivets in the rim
        r = blur(((xx - x) ** 2 + (yy - y) ** 2 < 11 ** 2).astype(np.float32), 1)
        c.over(chrome(pillow(r, 6), rim, depth=40), r)
    return c


def charge(base, painting, cx=256, cy=236, scale=0.62, angle=0.0):
    """Places a painted object (an image) on the shield image."""
    size = int(N * scale)
    o = painting.resize((size, size), Image.LANCZOS)
    if angle:
        o = o.rotate(angle, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(o, (int(cx - o.width / 2), int(cy - o.height / 2)))
    return base
