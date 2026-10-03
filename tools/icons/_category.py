"""Row-category icons: TEXT on a ribbon (the user's rule, 2026-10-03 - "icon หมวดหมู่ให้ใช้เป็นตัวหนังสือ").

The ribbon keeps the label's glass colour, so the colour still says which category a row is (the
menu rule), and the words say what it holds. Every category is a row of tools/categories.tsv; the
cat_<id>.py files are generated from it (tools/build.py), and the words are drawn at full texture
size after the ribbon has been finished (see build.finish_text), so they stay sharp.
"""
import os
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, chrome, gold_tint, cloth

GLASS = {
    'LIGHT_BLUE': (0.20, 0.45, 0.72), 'LIME': (0.36, 0.62, 0.12), 'YELLOW': (0.86, 0.68, 0.10), 'ORANGE': (0.82, 0.40, 0.07),
    'PURPLE': (0.42, 0.16, 0.58), 'RED': (0.62, 0.09, 0.07), 'WHITE': (0.88, 0.86, 0.80), 'LIGHT_GRAY': (0.55, 0.55, 0.56),
    'CYAN': (0.08, 0.52, 0.58),
}
TSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'categories.tsv')


def categories():
    """[(id, colour, text, [label prefixes])] in file order."""
    out = []
    for line in open(TSV, encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        cid, colour, text, labels = line.rstrip('\n').split('\t')
        out.append((cid, colour, text.replace('\\n', '\n'), labels.split('|')))
    return out


def ribbon(color_name, seed=0):
    rng = np.random.default_rng(900 + seed)
    c = Canvas()
    m = blur(poly([(10, 96), (502, 96), (476, 256), (502, 416), (10, 416), (36, 256)]), 1.5)
    wave = 0.06 * np.sin(xx / 70.0)
    c.over(light((0.25 + wave) * m, cloth(rng, GLASS[color_name], weave=2.2), depth=60, spec=0.08), m)
    inner = blur(poly([(30, 114), (482, 114), (456, 256), (482, 398), (30, 398), (56, 256)]), 1)
    trim = np.clip(m - inner, 0, 1)
    c.over(chrome(0.45 * pillow(trim, 3), gold_tint(), depth=40), trim)
    return c.image()
