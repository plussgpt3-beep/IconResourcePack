"""Pack and riding animals in profile (คอกสัตว์ขนของ, 2026-10-24): one quadruped painter shaped by a few
numbers - a horse, a mule, a donkey, a llama, a camel - with their tack: saddle, pack chests, carpet."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, chrome, leather_col, edge_darken, noise


def _limb(p0, p1, w0, w1):
    """A tapered limb from p0 to p1 as a mask."""
    p0 = np.array(p0, np.float32); p1 = np.array(p1, np.float32)
    d = p1 - p0; L = float(np.hypot(*d)); d /= L
    s = ((xx - p0[0]) * d[0] + (yy - p0[1]) * d[1]) / L
    t = np.abs((xx - p0[0]) * -d[1] + (yy - p0[1]) * d[0])
    w = w0 + (w1 - w0) * np.clip(s, 0, 1)
    return ((s >= 0) & (s <= 1) & (t <= w)).astype(np.float32)


def animal(c, rng, coat, kind='horse', mane=None, hoof=(0.18, 0.15, 0.12)):
    """Paints the animal, facing left, standing on y ~ 470. Returns the body mask."""
    col = np.array(coat)
    if kind == 'llama':
        body = ellipse([170, 250, 440, 380])
        neck = _limb((200, 300), (130, 110), 40, 34)
        head = np.maximum(ellipse([70, 70, 175, 140]), ellipse([50, 95, 120, 140]))
        ears = np.maximum(_limb((150, 80), (160, 30), 10, 4), _limb((125, 80), (125, 30), 10, 4))
        legs = [((210, 350), (205, 470)), ((250, 350), (255, 470)), ((380, 350), (375, 470)), ((415, 350), (420, 470))]
        lw = (22, 15)
        tail = _limb((435, 290), (465, 330), 16, 10)
    elif kind == 'camel':
        body = np.maximum(ellipse([170, 230, 450, 360]), ellipse([240, 150, 390, 290]))
        neck = _limb((200, 300), (110, 170), 34, 28)
        head = np.maximum(ellipse([50, 140, 150, 200]), ellipse([30, 160, 90, 200]))
        ears = _limb((125, 145), (130, 120), 8, 4)
        legs = [((210, 330), (200, 470)), ((250, 330), (255, 470)), ((390, 330), (385, 470)), ((425, 330), (435, 470))]
        lw = (20, 13)
        tail = _limb((445, 270), (470, 330), 8, 5)
    else:
        big = {'horse': 1.0, 'mule': 0.95, 'donkey': 0.88}[kind]
        body = ellipse([160, 220, 450, 360])
        neck = _limb((215, 270), (140, 140), 52 * big, 36 * big)
        head = np.maximum(_limb((150, 120), (70, 230), 38 * big, 24 * big), ellipse([110, 100, 185, 165]))
        ear = 26 if kind == 'horse' else 46
        ears = np.maximum(_limb((160, 112), (168, 112 - ear), 11, 4), _limb((140, 112), (138, 112 - ear), 11, 4))
        legs = [((205, 330), (195, 470)), ((245, 330), (250, 470)), ((395, 330), (385, 470)), ((430, 320), (440, 470))]
        lw = (24 * big, 13 * big)
        tail = _limb((445, 250), (480, 380), 18, 8) if kind == 'horse' else _limb((445, 250), (468, 360), 7, 5)
    legmask = np.zeros((N, N), np.float32)
    for p0, p1 in legs:
        legmask = np.maximum(legmask, _limb(p0, p1, *lw))
    far = blur(np.maximum(_limb(*legs[1], *lw), _limb(*legs[3], *lw)), 1)
    c.over(light(0.4 * pillow(far, 6), np.zeros((N, N, 3)) + col * 0.7, depth=40, spec=0.15), far)
    m = blur(np.clip(body + neck + head + ears + _limb(*legs[0], *lw) + _limb(*legs[2], *lw), 0, 1), 1.2)
    fur = 0.92 + 0.08 * noise(rng, 30, 2)
    c.over(light(0.45 * pillow(m, 18), col[None, None, :] * fur[..., None], depth=60, spec=0.2) * edge_darken(m, 8, 0.3), m)
    if kind == 'llama':
        wool = blur(np.maximum(ellipse([180, 240, 440, 330]), _limb((200, 280), (140, 140), 44, 38)), 3) * m
        c.over(light(0.4 * pillow(wool, 10) * (0.85 + 0.15 * noise(rng, 14, 2)), np.zeros((N, N, 3)) + col * 1.05, depth=40, spec=0.05), wool * 0.8)
    t = blur(tail, 1.5)
    c.over(light(0.4 * pillow(t, 6), np.zeros((N, N, 3)) + np.array(mane or col * 0.6), depth=30, spec=0.15), t)
    if mane is not None and kind in ('horse', 'mule'):
        mm = blur(_limb((220, 235), (155, 110), 14, 10), 1.5)
        c.over(light(0.4 * pillow(mm, 6), np.zeros((N, N, 3)) + np.array(mane), depth=30, spec=0.15), mm)
    hooves = np.zeros((N, N), np.float32)
    for p0, p1 in legs:
        hooves = np.maximum(hooves, ellipse([p1[0] - lw[1] - 3, p1[1] - 18, p1[0] + lw[1] + 3, p1[1] + 4]))
    c.over(light(0.3 * pillow(hooves, 4), np.zeros((N, N, 3)) + np.array(hoof), depth=30, spec=0.3), blur(hooves, 1))
    eye_at = {'llama': (115, 95), 'camel': (95, 160)}.get(kind, (140, 145))
    eye = blur(ellipse([eye_at[0] - 7, eye_at[1] - 7, eye_at[0] + 7, eye_at[1] + 7]), 0.8)
    c.over(np.zeros((N, N, 3)) + 0.05, eye, cast=False)
    return m


def saddle(c, rng, x0=250, x1=350, y=225):
    s = blur(np.maximum(ellipse([x0, y - 25, x1, y + 30]) * (yy < y + 22), rect([x0 + 30, y + 10, x0 + 52, y + 80], 6)), 1)
    c.over(light(0.5 * pillow(s, 10), leather_col(rng, (0.42, 0.20, 0.08)), depth=40, spec=0.35), s)


def packs(c, rng, x=240, y=230, w=170):
    """Two wooden pack chests slung over the back."""
    for dx in (0, w // 2 + 6):
        box = blur(rect([x + dx, y, x + dx + w // 2, y + 90], 6), 1)
        c.over(light(0.3 * pillow(box, 8), wood(rng, (0.55, 0.36, 0.17), rings=6), depth=40, spec=0.15) * edge_darken(box, 6, 0.4), box)
        band = blur(rect([x + dx, y + 36, x + dx + w // 2, y + 48]), 0.8) * box
        c.over(chrome(0.4 * band, (0.35, 0.35, 0.38), depth=20), band)
    strap = blur(rect([x - 10, y - 12, x + w + 16, y + 2], 4), 1)
    c.over(light(0.4 * pillow(strap, 4), leather_col(rng, (0.35, 0.18, 0.07)), depth=30, spec=0.2), strap)


def carpet(c, rng, color, x0=190, x1=430, y=240):
    k = blur(rect([x0, y, x1, y + 80], 8), 1)
    weave = cloth(rng, color)
    stripe = (np.abs(((yy - y) % 26) - 13) < 4)[..., None]
    c.over(light(0.3 * pillow(k, 8), np.where(stripe, weave * 0.6 + 0.35, weave), depth=30, spec=0.1), k)
