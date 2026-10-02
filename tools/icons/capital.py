"""กลับเมืองหลวง: the capital's keep - a stone tower with battlements, a gate and a pennant."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, stone, cloth, wood, edge_darken, noise


def draw():
    rng = np.random.default_rng(207)
    c = Canvas()
    # tower body with battlements along the top
    body = rect([130, 150, 382, 480])
    for k in range(5):
        x0 = 130 + k * 56
        body = np.maximum(body, rect([x0, 110, x0 + 34, 160]))
    body = blur(body, 1.2)
    # masonry: courses of blocks with offset joints
    row = (yy // 30).astype(int)
    jx = ((xx + (row % 2) * 28) % 56 < 3)
    jy = (yy % 30 < 3)
    joints = (jx | jy).astype(np.float32)
    rnd_block = noise(rng, 18, 1)
    col = stone(rng, (0.52, 0.50, 0.46)) * (0.85 + 0.25 * rnd_block[..., None]) * (1 - 0.45 * joints[..., None])
    h = 0.25 * body - 0.12 * joints * body
    # the tower is round-ish: darken towards the right edge
    roundness = np.clip(1 - ((xx - 230) / 200) ** 2, 0.4, 1)
    c.over(light(h, col * roundness[..., None], depth=40, spec=0.05) * edge_darken(body, 8, 0.3), body)
    # gate: arched opening with a wooden door
    gate = blur(np.maximum(rect([215, 370, 297, 480]), ellipse([215, 330, 297, 412])), 1.2)
    c.over(wood(rng, (0.28, 0.16, 0.08), angle=np.pi / 2, rings=10) * 0.8, gate)
    # arrow slits
    for x in (180, 330):
        slit = blur(rect([x - 6, 220, x + 6, 280], 4), 1)
        c.over(np.zeros((N, N, 3)) + 0.05, slit)
    # pennant on a short mast
    mast = blur(rect([252, 30, 260, 112]), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.25, 0.18, 0.12]), mast)
    pen = blur(poly([(260, 34), (350, 52), (260, 74)]), 1)
    c.over(light(pillow(pen, 4) * 0.3, cloth(rng, (0.60, 0.08, 0.06)), depth=20, spec=0.1), pen)
    return c.image()
