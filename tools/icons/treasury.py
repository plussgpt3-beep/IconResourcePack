"""ท้องพระคลัง: a tied leather coin purse with a stack of gold coins (approved 2026-10-02)."""
import numpy as np
from lib import N, xx, yy, LIGHT as L, Canvas, mask_from, blur, noise, shadow, gold_coin


def draw():
    rng = np.random.default_rng(7)
    c = Canvas()
    shadow(c, [70, 430, 470, 500])

    # bag body: big belly with a tapered neck, lit like a sphere
    body = blur(mask_from(lambda d: (d.ellipse([60, 170, 440, 480], fill=255),
                                     d.polygon([(170, 120), (330, 120), (400, 260), (100, 260)], fill=255))), 3)
    cx, cy, r = 245, 330, 210
    nx = (xx - cx) / r; ny = (yy - cy) / r
    nz = np.sqrt(np.clip(1 - nx**2 - ny**2, 0, 1))
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    grain = noise(rng, 6, 5); pores = noise(rng, 60, 2)
    base = np.array([0.58, 0.37, 0.20])
    leather = base[None, None, :] * (0.38 + 0.85 * diff[..., None]) * (0.85 + 0.3 * grain[..., None]) * (0.93 + 0.12 * pores[..., None])
    folds = np.zeros((N, N), np.float32)
    for x0, bend in [(190, -40), (235, -8), (285, 25), (325, 55)]:
        f = mask_from(lambda d, x0=x0, bend=bend: d.line([(x0, 250), (x0 + bend * 0.5, 320), (x0 + bend, 400)], fill=255, width=7))
        folds = np.maximum(folds, blur(f, 7))
    leather *= (1 - 0.45 * folds[..., None])
    edge = 1 - blur(body, 14)
    leather *= (1 - 0.6 * np.clip(edge * 2.2, 0, 1)[..., None])
    leather += 0.18 * (diff ** 18)[..., None]
    c.over(np.clip(leather, 0, 1), body)

    # gathered top: leather flaring up out of the tie in soft pleats, wavy lip
    dx = xx - 250
    top = 52 + 9 * np.sin(dx / 13.0) + 0.0016 * dx**2
    half = 62 + (135 - yy) * 0.75
    frill = blur(((yy > top) & (yy < 140) & (np.abs(dx) < half)).astype(np.float32), 2)
    pleat = np.sin(dx / 13.0 + np.pi / 2)
    light = np.clip(0.55 - dx / 260, 0.15, 1)
    lip = np.clip(1 - (yy - top) / 14, 0, 1)
    deep = np.clip((yy - top) / 70, 0, 1)
    rgb = base[None, None, :] * ((0.55 + 0.45 * pleat) * light * (1 - 0.45 * deep) + 0.35 * lip)[..., None]
    c.over(np.clip(rgb * (0.85 + 0.3 * grain[..., None]), 0, 1), frill)

    # rope tie: a twisted cord, with its end hanging down
    rope = blur(mask_from(lambda d: d.rounded_rectangle([150, 112, 350, 150], radius=18, fill=255)), 1.5)
    twist = 0.5 + 0.5 * np.sin((xx + yy * 1.2) / 6.5)
    ry = 1 - np.abs((yy - 131) / 20)
    rope_rgb = np.array([0.80, 0.68, 0.45])[None, None, :] * (0.45 + 0.55 * twist[..., None]) * (0.55 + 0.6 * np.clip(ry, 0, 1)[..., None])
    c.over(np.clip(rope_rgb, 0, 1), rope)
    cord = mask_from(lambda d: d.line([(330, 140), (360, 190), (352, 235)], fill=255, width=14))
    c.over(np.clip(np.array([0.70, 0.58, 0.37])[None, None, :] * (0.6 + 0.5 * twist[..., None]), 0, 1), blur(cord, 1.5))

    # gold coins in front: a stack of three and one lying beside it
    for cx2, cy2 in [(370, 440), (372, 412), (366, 384)]:
        gold_coin(c, cx2, cy2, 88, 30, 18)
    gold_coin(c, 290, 455, 62, 22, 14)
    return c.image()
