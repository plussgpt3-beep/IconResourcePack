"""เนื้อตุ๋นจักรพรรดิ (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from lib import blur, ellipse, chrome, gold_tint, pillow
from _dishes import bowl, broth, chunk, herb_root, carrot_coin, specks, crown, steam


def draw():
    rng = np.random.default_rng(2909)
    c = Canvas()
    inner = bowl(c, rng, clay=(0.14, 0.12, 0.12))
    rim = blur(np.clip(ellipse([56, 184, 456, 316]) - ellipse([74, 200, 438, 300]), 0, 1), 1)
    c.over(chrome(0.4 * pillow(rim, 4), gold_tint(), depth=30), rim * 0.9)
    broth(c, rng, inner, (0.42, 0.20, 0.08))
    for (x, y, r) in ((180, 245, 34), (260, 236, 36), (335, 250, 32)):
        chunk(c, rng, x, y, r, (0.48, 0.22, 0.10), 'cube')
    herb_root(c, rng, 300, 222, 0.5)
    carrot_coin(c, rng, 225, 268, 16)
    for (x, y) in ((360, 232),):
        carrot_coin(c, rng, x, y, 14)
    specks(c, rng, inner, 12, (0.30, 0.55, 0.20), 2, 5)
    crown(c, 256, 130, 1.0)
    steam(c)
    return c.image()
