"""ทำลาย / ยุบ: a powder keg with a lit fuse."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, mask_from


def draw():
    rng = np.random.default_rng(409)
    c = Canvas()
    keg = blur(np.maximum(ellipse([100, 160, 412, 480]) * ((yy > 190) & (yy < 450)), rect([120, 190, 392, 450])), 1.2)
    nx = (xx - 256) / 156
    cyl = np.sqrt(np.clip(1 - nx ** 2, 0, 1))
    bulge = keg * np.clip(1 - ((yy - 320) / 200) ** 2, 0, 1)
    staves = 0.85 + 0.15 * (np.abs(np.sin((xx - 256) / 26.0)) > 0.1)
    c.over(light(cyl * keg * 0.8, wood(rng, (0.48, 0.28, 0.12), angle=np.pi / 2, rings=6) * staves[..., None], depth=60, spec=0.2), keg)
    for y in (215, 300, 420):
        hoop = blur(((np.abs(yy - y) < 11)).astype(np.float32) * keg, 1)
        c.over(chrome(cyl * hoop, (0.38, 0.38, 0.40), depth=40, sky=0.7, ground=0.08), hoop)
    lid = blur(ellipse([128, 168, 384, 222]), 1)
    c.over(light(0.1 * lid, wood(rng, (0.40, 0.23, 0.10), rings=8), depth=20, spec=0.1), lid)
    label = blur(rect([200, 320, 312, 400], 6), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.82, 0.74, 0.55]), label)
    xm = blur(np.maximum(poly([(225, 335), (287, 385)], width=12), poly([(287, 335), (225, 385)], width=12)), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.70, 0.08, 0.06]), xm)
    fuse = blur(poly([(256, 195), (270, 120), (310, 80), (330, 60)], width=9), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.25, 0.18]), fuse)
    spark = blur(ellipse([310, 30, 370, 90]), 8)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.75, 0.25]), np.clip(spark * 1.6, 0, 1), cast=False)
    core = blur(ellipse([328, 48, 352, 72]), 3)
    c.over(np.ones((N, N, 3)), core, cast=False)
    return c.image()
