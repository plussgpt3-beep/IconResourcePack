"""ผู้ร่วมอาศัย: a timber-framed cottage under a thatched roof, smoke from the chimney."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, noise, stone, edge_darken


def draw():
    rng = np.random.default_rng(306)
    c = Canvas()
    chim = blur(rect([320, 90, 362, 210]), 1)
    c.over(light(0.2 * pillow(chim, 6), stone(rng, (0.55, 0.45, 0.38)), depth=30, spec=0.05), chim)
    walls = blur(rect([100, 250, 412, 470]), 1)
    plaster = np.array([0.88, 0.82, 0.68])[None, None, :] * (0.85 + 0.2 * noise(rng, 20, 3)[..., None])
    c.over(light(0.15 * pillow(walls, 10), plaster, depth=30, spec=0.05) * edge_darken(walls, 10, 0.3), walls)
    beams = np.zeros((N, N), np.float32)
    for pts in ([(100, 250), (412, 250)], [(100, 360), (412, 360)], [(100, 470), (412, 470)], [(100, 250), (100, 470)],
                [(412, 250), (412, 470)], [(256, 250), (256, 470)], [(100, 360), (178, 250)], [(412, 360), (334, 250)]):
        beams = np.maximum(beams, poly(pts, width=16))
    beams = blur(beams * walls, 1)
    c.over(light(0.3 * pillow(beams, 4), wood(rng, (0.30, 0.17, 0.08), rings=6), depth=30, spec=0.1), beams)
    door = blur(np.maximum(rect([210, 380, 302, 470]), ellipse([210, 350, 302, 410])), 1)
    c.over(light(0.2 * door, wood(rng, (0.36, 0.20, 0.09), angle=np.pi / 2, rings=8), depth=30, spec=0.1) * edge_darken(door, 6, 0.4), door)
    for x in (140, 320):
        win = blur(rect([x, 280, x + 52, 334], 4), 1)
        glow = np.zeros((N, N, 3)) + np.array([0.95, 0.75, 0.35])
        c.over(glow * (0.8 + 0.2 * (yy > 307)[..., None]), win)
        c.over(np.zeros((N, N, 3)) + 0.12, blur(np.maximum(rect([x + 23, 280, x + 29, 334]), rect([x, 304, x + 52, 310])) * win, 0.6))
    roof = blur(poly([(60, 270), (256, 70), (452, 270), (430, 285), (82, 285)]), 1.5)
    straw = 0.5 + 0.5 * np.sin((xx * 0.4 + yy * 1.6) / 3.0)
    col = np.array([0.72, 0.58, 0.30])[None, None, :] * (0.7 + 0.35 * straw[..., None]) * (0.9 + 0.2 * noise(rng, 20, 2)[..., None])
    c.over(light(0.25 * pillow(roof, 14), col, depth=40, spec=0.05) * edge_darken(roof, 8, 0.4), roof)
    for k, (x, y, r) in enumerate([(345, 60, 22), (365, 30, 28), (390, 5, 32)]):
        sm = blur(ellipse([x - r, y - r, x + r, y + r]), 6) * (0.45 - k * 0.1)
        c.over(np.zeros((N, N, 3)) + 0.75, sm, cast=False)
    return c.image()
