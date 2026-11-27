"""พืชใหม่แบบโมเดล 3D จริง (the user, 2026-11-27: "ไม่เอาแบบทำภาพสี่มุมแล้วมาประกบกัน เอาแบบเป็น model 3D จริงๆเลย").

Each growth stage plant_<crop>_<1-4> is a block model built from real pieces: stems and stalks are boxes, every leaf
is its own thin plane tilted and turned in 3D, fruits are rounded boxes. Nothing is a crossed picture.

Rotations use the 26.3 element format {"origin", "x", "y", "z"} (CuboidRotation.EulerXYZRotation, which the client
builds with Matrix4f.rotationZYX: X is applied first, then Y, then Z, right-handed like the single-axis form). The
same matrices drive render(), so the preview sheet shows what the game draws.

install(ns) writes the textures (textures/item/p3/), the models (models/item/plant_*.json) and the item definitions,
and returns the ids. render(model) draws one model for the preview sheet.
"""
import json
import math
import os
import random

import numpy as np
from PIL import Image

CROPS = ('chili', 'garlic', 'shallot', 'tomato', 'cabbage', 'lemongrass')
T = 32          # texture size
BASE = -1.0     # the plant's foot: the farmland top, 1px under the tripwire block (as block/crop)


# ---------------------------------------------------------------- textures

def _noise(seed, size=T, scale=4):
    rng = np.random.default_rng(seed)
    small = rng.random((size // scale + 2, size // scale + 2))
    img = Image.fromarray((small * 255).astype(np.uint8)).resize((size + scale * 2, size + scale * 2), Image.BICUBIC)
    return np.asarray(img, dtype=np.float32)[scale:scale + size, scale:scale + size] / 255.0


def _rgba(rgb, alpha, shade):
    out = np.zeros((T, T, 4), np.uint8)
    c = np.clip(np.asarray(rgb, np.float32)[None, None, :] * shade[..., None], 0, 255)
    out[..., :3] = c.astype(np.uint8)
    out[..., 3] = np.where(alpha, 255, 0).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def _grid():
    v, u = np.mgrid[0:T, 0:T].astype(np.float32)
    return (u + 0.5) / T, (v + 0.5) / T      # u across, v from the leaf's base (0) to its tip (1)


def leaf_tex(rgb, seed, shape='oval', rib=(1.25, 1.25, 1.1), serrate=0.0, veins=True, tip_rgb=None):
    """A leaf drawn base at the top (v=0), tip at the bottom: its outline, a pale midrib, side veins, mottling."""
    u, v = _grid()
    x = np.abs(u - 0.5) * 2                       # 0 at the midrib, 1 at the edge of the texture
    if shape == 'oval':
        half = np.sin(np.clip(v, 0, 1) * math.pi) ** 0.8 * 0.92
    elif shape == 'lance':
        half = np.sin(np.clip(v, 0, 1) ** 0.8 * math.pi) ** 1.2 * 0.7
    elif shape == 'round':
        half = np.sqrt(np.clip(1 - (2 * v - 1.05) ** 2, 0, 1)) * 0.98
    elif shape == 'strap':
        half = np.where(v < 0.75, 0.78, 0.78 * np.clip((1 - v) / 0.25, 0, 1) ** 0.7)
    elif shape == 'compound':                     # tomato: three pairs of leaflets and a tip leaflet on one stalk
        half = np.zeros_like(v)
        for c, w in ((0.22, 0.75), (0.47, 0.9), (0.72, 0.8)):
            half = np.maximum(half, np.sqrt(np.clip(1 - ((v - c) / 0.12) ** 2, 0, 1)) * w * np.clip((x - 0.0) * 9, 0, 1))
        half = np.maximum(half, np.sqrt(np.clip(1 - ((v - 0.9) / 0.11) ** 2, 0, 1)) * 0.45)
        half = np.maximum(half, np.where(v > 0.03, 0.09, 0))
    else:
        raise ValueError(shape)
    if serrate:
        half = half * (1 - serrate * (0.5 + 0.5 * np.sin(v * 60)))
    alpha = x <= half
    n = _noise(seed)
    shade = 0.82 + 0.3 * n - 0.18 * x
    if veins:
        side = np.abs(((v - x * 0.35) * 9) % 1 - 0.5) < 0.09
        shade = np.where(side & (x > 0.12), shade * 1.12, shade)
    shade = np.where(x < 0.07, shade * rib[0], shade)
    img = _rgba(rgb, alpha, shade)
    if tip_rgb is not None:                       # a drying tip
        a = np.asarray(img).astype(np.float32)
        t = np.clip((v - 0.6) / 0.4, 0, 1)[..., None]
        a[..., :3] = a[..., :3] * (1 - t) + np.asarray(tip_rgb, np.float32) * shade[..., None] * t
        img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    return img


def solid_tex(rgb, seed, stripes=0.0, spots=0.0, highlight=0.0, rings=0.0, grain=0.0):
    u, v = _grid()
    n = _noise(seed, scale=4)
    shade = 0.86 + 0.24 * n
    if stripes:
        shade = shade * (1 - stripes * (0.5 + 0.5 * np.sin(u * 2 * math.pi * 5 + n * 3)))
    if grain:
        shade = shade * (1 - grain * (0.5 + 0.5 * np.sin(u * 2 * math.pi * 3 + _noise(seed + 9, scale=8) * 8)))
    if rings:
        shade = shade * (1 - rings * (np.abs((v * 4) % 1 - 0.5) < 0.06))
    if spots:
        shade = shade * (1 - spots * (_noise(seed + 3, scale=2) > 0.78))
    if highlight:
        h = np.exp(-(((u - 0.32) / 0.16) ** 2 + ((v - 0.3) / 0.16) ** 2))
        shade = shade + highlight * h
    return _rgba(rgb, np.ones((T, T), bool), shade)


def star_tex(rgb, seed, petals=5, inner=0.25, centre=None):
    u, v = _grid()
    dx, dy = u - 0.5, v - 0.5
    r = np.hypot(dx, dy) * 2
    a = np.arctan2(dy, dx)
    edge = inner + (1 - inner) * (0.5 + 0.5 * np.cos(a * petals)) ** 1.5
    alpha = r <= edge * 0.95
    shade = 0.9 + 0.2 * _noise(seed) - 0.15 * r
    img = np.asarray(_rgba(rgb, alpha, shade)).copy()
    if centre is not None:
        m = r < 0.28
        img[m, :3] = np.asarray(centre, np.uint8)
    return Image.fromarray(img, 'RGBA')


BALL_TEX = ('tomato_red', 'tomato_orange', 'tomato_green', 'garlic_bulb', 'shallot_bulb', 'cabbage_head', 'cabbage_head_inner')
LEVELS = (0.74, 0.82, 0.9, 0.97, 1.04)


def textures():
    t = _base_textures()
    for name in BALL_TEX:      # the same skin at five brightnesses: a ball's faces take one by the way they face
        a = np.asarray(t[name]).astype(np.float32)
        for k, b in enumerate(LEVELS):
            c = a.copy(); c[..., :3] = np.clip(c[..., :3] * b, 0, 255)
            t['%s_%d' % (name, k)] = Image.fromarray(c.astype(np.uint8), 'RGBA')
    return t


def _base_textures():
    return {
        'leaf_tomato': leaf_tex((62, 118, 44), 11, 'compound', veins=False),
        'leaf_chili': leaf_tex((58, 128, 46), 12, 'lance'),
        'leaf_cabbage': leaf_tex((112, 160, 104), 13, 'round', rib=(1.35,), serrate=0.04),
        'leaf_cabbage_dark': leaf_tex((76, 128, 86), 14, 'round', rib=(1.4,), serrate=0.05),
        'blade_garlic': leaf_tex((98, 142, 82), 15, 'strap', rib=(1.12,), veins=False),
        'blade_garlic_dry': leaf_tex((98, 142, 82), 16, 'strap', rib=(1.12,), veins=False, tip_rgb=(196, 170, 90)),
        'blade_lemongrass': leaf_tex((128, 170, 70), 17, 'strap', rib=(1.18,), veins=False),
        'stalk_lemongrass': solid_tex((196, 206, 150), 18, stripes=0.08, rings=0.18),
        'tube_shallot': solid_tex((70, 128, 60), 19, stripes=0.1),
        'tube_shallot_dry': solid_tex((170, 160, 80), 20, stripes=0.1),
        'stem_green': solid_tex((84, 128, 52), 21, stripes=0.12),
        'stem_dark': solid_tex((66, 104, 44), 22, stripes=0.12),
        'stake': solid_tex((142, 104, 62), 23, grain=0.25),
        'tomato_red': solid_tex((204, 40, 28), 24, spots=0.03),
        'tomato_orange': solid_tex((230, 118, 40), 25, spots=0.03),
        'tomato_green': solid_tex((124, 172, 72), 26, spots=0.04),
        'calyx': star_tex((60, 110, 40), 27, petals=5, inner=0.15),
        'flower_yellow': star_tex((246, 214, 60), 28, petals=5, inner=0.3, centre=(214, 160, 30)),
        'flower_white': star_tex((244, 244, 236), 29, petals=5, inner=0.3, centre=(220, 210, 120)),
        'chili_red': solid_tex((196, 28, 22), 30, highlight=0.3),
        'chili_green': solid_tex((72, 142, 40), 31, highlight=0.25),
        'garlic_bulb': solid_tex((232, 224, 210), 32, stripes=0.1),
        'shallot_bulb': solid_tex((168, 78, 64), 33, stripes=0.1),
        'cabbage_head': solid_tex((172, 206, 138), 34, stripes=0.06),
        'cabbage_head_inner': solid_tex((198, 220, 158), 35, stripes=0.05),
    }


# ---------------------------------------------------------------- geometry

def _rot(x, y, z):
    """The game's Matrix4f.rotationZYX(z, y, x) in degrees: Rz * Ry * Rx (X applied first)."""
    cx, sx = math.cos(math.radians(x)), math.sin(math.radians(x))
    cy, sy = math.cos(math.radians(y)), math.sin(math.radians(y))
    cz, sz = math.cos(math.radians(z)), math.sin(math.radians(z))
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return rz @ ry @ rx


def heading(yaw, pitch):
    """The way a piece built along +Z points after the rotation x=pitch, y=yaw (pitch -90 = straight up)."""
    return _rot(pitch, yaw, 0) @ np.array([0.0, 0.0, 1.0])


R = lambda v: round(float(v), 3)


class Plant:
    def __init__(self, seed):
        self.el = []
        self.rng = random.Random(seed)

    def _add(self, frm, to, faces, origin=None, yaw=0.0, pitch=0.0, roll=0.0):
        e = {'from': [R(c) for c in frm], 'to': [R(c) for c in to], 'faces': faces}
        if origin is not None and (abs(yaw) > 0.01 or abs(pitch) > 0.01 or abs(roll) > 0.01):
            e['rotation'] = {'origin': [R(c) for c in origin], 'x': R(pitch), 'y': R(yaw), 'z': R(roll)}
        self.el.append(e)

    def leaf(self, base, yaw, pitch, length, width, tex, bend=0.0, parts=None):
        """A leaf from its base along +Z, tilted (pitch) and turned (yaw) about its base. With bend it is cut into
        pieces that each tilt a little more than the last, so the leaf arches instead of standing as a flat card."""
        if parts is None:
            parts = 1 if abs(bend) < 1 else (2 if length < 4 else 3)
        at = np.array(base, float)
        for i in range(parts):
            v1, v2 = 16 * i / parts, 16 * (i + 1) / parts
            L = length / parts
            p = pitch + bend * i / max(1, parts - 1) if parts > 1 else pitch
            bx, by, bz = at
            self._add((bx - width / 2, by, bz), (bx + width / 2, by, bz + L),
                      {'up': {'uv': [0, R(v1), 16, R(v2)], 'texture': '#' + tex},
                       'down': {'uv': [0, R(v2), 16, R(v1)], 'texture': '#' + tex}}, tuple(at), yaw, p)
            at = at + heading(yaw, p) * L
        return at

    def tube(self, base, yaw, pitch, length, d, tex, ends=True):
        """A stem, stalk, pod: a square rod from its base along +Z, tilted and turned about its base."""
        bx, by, bz = base
        side = {'uv': [0, 0, 4, 16], 'texture': '#' + tex}
        faces = {'north': {'uv': [6, 6, 10, 10], 'texture': '#' + tex}, 'south': {'uv': [6, 6, 10, 10], 'texture': '#' + tex}} if ends else {}
        for f in ('east', 'west', 'up', 'down'):
            faces[f] = dict(side)
        self._add((bx - d / 2, by - d / 2, bz), (bx + d / 2, by + d / 2, bz + length), faces, base, yaw, pitch)
        return np.array(base) + heading(yaw, pitch) * length

    def ball(self, c, r, tex, squash=1.0, turn=0.0):
        """A round fruit, bulb or head. Shading is the game's face shading turned off: each face takes a skin lit by
        the way it points, so the light rolls round it like a ball instead of showing the boxes.
        Small (a tomato): three crossing boxes. Large (a cabbage head, a bulb): thin round slabs stacked like the
        slices of a ball, each slab a cross of two boxes with a square in the middle, which outlines a circle."""
        x, y, z = c
        light = np.array([0.35, 0.85, 0.4]); light /= np.linalg.norm(light)
        normals = {'up': (0, 1, 0), 'down': (0, -1, 0), 'north': (0, 0, -1), 'south': (0, 0, 1), 'west': (-1, 0, 0), 'east': (1, 0, 0)}

        def skin(f, lift):
            nn = np.array(normals[f], float) + np.array((0.0, lift, 0.0))
            nn /= np.linalg.norm(nn) + 1e-9
            d = float(np.dot(nn, light))
            k = int(round((max(-0.6, d) + 0.6) / 1.6 * (len(LEVELS) - 1)))
            return {'uv': [2, 2, 14, 14], 'texture': '#%s_%d' % (tex, k)}

        def box(x0, y0, z0, x1, y1, z1, lift, keep):
            self._add((x0, y0, z0), (x1, y1, z1), {f: skin(f, lift) for f in keep})
            self.el[-1]['shade'] = False

        allf = tuple(normals)
        if r < 0.8:
            k = 0.7
            for sx, sy, sz in ((1, k, k), (k, 1, k), (k, k, 1)):
                box(x - r * sx, y - r * sy * squash, z - r * sz, x + r * sx, y + r * sy * squash, z + r * sz, 0.0, allf)
            return
        n = 3 if r < 1.6 else 6
        h = 2 * r * squash / n
        for i in range(n):
            y0 = y - r * squash + i * h
            m = (i + 0.5) / n * 2 - 1
            w = r * math.sqrt(max(0.0, 1 - m * m)) + r * 0.05
            q = w * 0.42
            sq = w * 0.72
            keep = [f for f in allf if not (f == 'up' and i < n - 1) and not (f == 'down' and i > 0)]
            box(x - w, y0, z - q, x + w, y0 + h, z + q, m * 0.9, keep)
            box(x - q, y0, z - w, x + q, y0 + h, z + w, m * 0.9, keep)
            box(x - sq, y0, z - sq, x + sq, y0 + h, z + sq, m * 0.9, keep)

    def flat(self, c, size, tex):
        """A small horizontal plane (calyx, flower) centred on c."""
        x, y, z = c
        self._add((x - size / 2, y, z - size / 2), (x + size / 2, y, z + size / 2),
                  {'up': {'uv': [0, 0, 16, 16], 'texture': '#' + tex}, 'down': {'uv': [0, 16, 16, 0], 'texture': '#' + tex}})

    def j(self, a):
        return self.rng.uniform(-a, a)


GOLD = 137.5


def tomato(s):
    p = Plant(100 + s)
    h = (4, 7.5, 11.5, 14)[s - 1]
    lean = p.j(4)
    stem_yaw = p.j(180)
    mid = p.tube((8, BASE, 8), stem_yaw, -90 + 6 + lean, h * 0.5, (0.55, 0.65, 0.75, 0.8)[s - 1], 'stem_green')
    top = p.tube(mid, stem_yaw + 160, -90 + 5, h * 0.5, (0.5, 0.6, 0.65, 0.7)[s - 1], 'stem_green')
    n = (3, 5, 7, 9)[s - 1]
    for i in range(n):
        t = 0.22 + 0.74 * i / max(1, n - 1)
        at = np.array((8, BASE, 8)) + (top - np.array((8, BASE, 8))) * t
        size = (3.6, 5.2, 6.4, 7.0)[s - 1] * (1.1 - 0.4 * t)
        p.leaf(at, i * GOLD + p.j(15), -10 - 30 * t + p.j(8), size, size * 0.72, 'leaf_tomato', bend=55)
    if s >= 3:
        p.tube((10.6, BASE - 1, 10.4), 0, -90, 16.5 if s == 4 else 14.5, 1.0, 'stake')
    if s == 2:
        p.flat((8.6, BASE + h * 0.8, 8.9), 1.6, 'flower_yellow')
    if s >= 3:
        trusses = ((0.5, 30), (0.75, 200)) if s == 3 else ((0.42, 40), (0.62, 170), (0.82, 290))
        for k, (t, yaw) in enumerate(trusses):
            at = np.array((8, BASE, 8)) + (top - np.array((8, BASE, 8))) * t
            end = p.tube(at, yaw, 35, 1.8, 0.35, 'stem_green', ends=False)
            n_f = 2
            for f in range(n_f):
                r = (1.0 if s == 3 else 1.4) * (1 - 0.12 * f)
                off = heading(yaw + (f - 1) * 55, 0) * (r * 1.3 * min(f, 1))
                c = end + off + np.array((0, -r - 0.2 * f, 0))
                if s == 3:
                    tex = 'tomato_green'
                else:
                    tex = 'tomato_red' if (k + f) % 4 else 'tomato_orange'
                p.ball(c, r, tex)
                p.flat(c + np.array((0, r * 1.01, 0)), r * 1.4, 'calyx')
        if s == 3:
            p.flat((7.2, BASE + h * 0.92, 8.4), 1.6, 'flower_yellow')
            p.flat((8.9, BASE + h * 0.66, 7.1), 1.5, 'flower_yellow')
    return p


def chili(s):
    p = Plant(200 + s)
    h = (2.5, 4.5, 6.5, 7.5)[s - 1]
    root = np.array((8, BASE, 8))
    trunk = p.tube(root, p.j(180), -86, h * 0.45, (0.6, 0.8, 0.9, 1.0)[s - 1], 'stem_dark')
    tips = []
    nb = (2, 3, 4, 5)[s - 1]
    for b in range(nb):
        yaw = b * 360 / nb + p.j(20)
        tip = p.tube(trunk, yaw, -55 + p.j(10), h * 0.75, 0.5, 'stem_green', ends=False)
        tips.append((trunk, tip, yaw))
    nl = (2, 3, 3, 3)[s - 1]
    for (a, b, yaw) in tips:
        for i in range(nl):
            t = 0.35 + 0.65 * i / max(1, nl - 1)
            at = a + (b - a) * t
            L = (2.4, 3.2, 3.8, 4.0)[s - 1]
            p.leaf(at, yaw + (60 if i % 2 else -60) + p.j(15), -10 + p.j(15), L, L * 0.45, 'leaf_chili', bend=35)
        p.leaf(b, yaw + p.j(10), -40, (2.0, 2.6, 3.0, 3.2)[s - 1], 1.2, 'leaf_chili', bend=30)
    if s == 3:
        for k, (a, b, yaw) in enumerate(tips):
            at = a + (b - a) * 0.6
            if k % 2:
                p.flat(at + np.array((0, -0.4, 0)), 1.2, 'flower_white')
            else:
                p.tube(at, yaw + 90, 70, 2.0, 0.6, 'chili_green')
    if s == 4:
        for k, (a, b, yaw) in enumerate(tips):
            for t in (0.5, 0.85):
                at = a + (b - a) * t
                end = p.tube(at, yaw + (100 if t < 0.7 else -80) * 0.3, 10, 1.2, 0.4, 'stem_green', ends=False)
                py = yaw + p.j(30)
                col = 'chili_red' if (k + int(t * 10)) % 5 else 'chili_green'
                m1 = p.tube(end, py, 55 + p.j(8), 1.3, 0.95, col)
                m2 = p.tube(m1, py, 72, 1.3, 0.78, col)
                p.tube(m2, py, 84, 1.1, 0.5, col)
    return p


def garlic(s):
    p = Plant(300 + s)
    n = (3, 5, 7, 8)[s - 1]
    L = (5, 8.5, 11.5, 12.5)[s - 1]
    root = np.array((8, BASE, 8))
    neck = root
    if s >= 2:
        neck = p.tube(root, 0, -90, (1.2, 2.2, 3.0, 3.0)[s - 1], (0.8, 1.0, 1.2, 1.2)[s - 1], 'stem_green')
    for i in range(n):
        yaw = i * GOLD + p.j(10)
        out = i / max(1, n - 1)
        tex = 'blade_garlic_dry' if s == 4 and i < 3 else 'blade_garlic'
        p.leaf(neck, yaw, -84 + 8 * out + p.j(4), L, 1.3, tex, bend=40 + 40 * out + p.j(8) + (25 if s == 4 and i < 3 else 0), parts=4)
    if s == 4:
        p.ball(root + np.array((0, 0.5, 0)), 1.9, 'garlic_bulb', squash=0.7)
    elif s == 3:
        p.ball(root + np.array((0, 0.1, 0)), 1.3, 'garlic_bulb', squash=0.6)
    return p


def shallot(s):
    p = Plant(400 + s)
    root = np.array((8, BASE, 8))
    bulbs = [(0, 0)] if s == 1 else [(-1.2, -0.6), (1.2, -0.4), (0.0, 1.2)] if s < 4 else [(-1.5, -0.8), (1.5, -0.6), (0.2, 1.6), (-0.4, -0.1)]
    per = (4, 3, 3, 3)[s - 1]
    L = (4, 7, 9.5, 10.5)[s - 1]
    k = 0
    for bx, bz in bulbs:
        base = root + np.array((bx, 0, bz))
        if s >= 3:
            r = 0.95 if s == 3 else 1.2
            p.ball(base + np.array((0, r * 0.45, 0)), r, 'shallot_bulb', squash=1.15)
            base = base + np.array((0, r * 1.5, 0))
        for i in range(per):
            yaw = k * GOLD + p.j(10)
            k += 1
            dry = s == 4 and i == 0
            tex = 'tube_shallot_dry' if dry else 'tube_shallot'
            pitch = -86 + p.j(4)
            bend = (14 + p.j(6)) if not dry else 40
            at = base
            for seg, d in enumerate((0.55, 0.5, 0.42, 0.34)):
                at = p.tube(at, yaw, pitch + bend * seg, L / 4, d, tex, ends=seg == 3)
    return p


def cabbage(s):
    p = Plant(500 + s)
    root = np.array((8, BASE + 0.3, 8))
    n = (4, 6, 8, 9)[s - 1]
    L = (3, 4.6, 6.0, 6.6)[s - 1]
    for i in range(n):
        yaw = i * 360 / n + p.j(12)
        p.leaf(root + heading(yaw, 0) * 0.4, yaw, -40 + p.j(8), L, L * 0.95, 'leaf_cabbage_dark' if i % 2 else 'leaf_cabbage', bend=45)
    if s >= 2:
        for i in range(4 if s < 4 else 6):
            yaw = i * (90 if s < 4 else 60) + 45
            p.leaf(root + np.array((0, 0.4, 0)), yaw, -62 + p.j(6), L * 0.7, L * 0.7, 'leaf_cabbage', bend=40)
    if s >= 3:
        r = 1.8 if s == 3 else 2.7
        c = root + np.array((0, r * 0.9, 0))
        p.ball(c, r, 'cabbage_head')
        for i in range(5 if s == 3 else 7):
            yaw = i * (72 if s == 3 else 360 / 7) + 20
            p.leaf(root + np.array((0, 0.2, 0)) + heading(yaw, 0) * (r * 1.0), yaw, -72, r * 2.0, r * 1.5, 'leaf_cabbage', bend=-75)
        p.ball(c + np.array((0, r * 0.3, 0)), r * 0.62, 'cabbage_head_inner')
    return p


def lemongrass(s):
    p = Plant(600 + s)
    root = np.array((8, BASE, 8))
    n = (3, 5, 7, 9)[s - 1]
    sl = (1.5, 2.6, 3.6, 4.6)[s - 1]
    L1 = (3, 4.8, 6.0, 6.8)[s - 1]
    L2 = (2, 3.6, 5.0, 6.0)[s - 1]
    for i in range(n):
        yaw = i * GOLD + p.j(10)
        spread = 0.6 + 1.8 * (i / max(1, n - 1)) if n > 1 else 0
        base = root + heading(yaw, 0) * spread
        top = p.tube(base, yaw, -80 + p.j(4), sl * 0.8, (0.5, 0.6, 0.65, 0.7)[s - 1], 'stalk_lemongrass')
        for b in range(2):
            y2 = yaw + (25 if b else -25) + p.j(10)
            p.leaf(top, y2, -80 + p.j(6), L1 + L2, 1.0, 'blade_lemongrass', bend=65 + p.j(20), parts=4)
    return p


BUILDERS = {'tomato': tomato, 'chili': chili, 'garlic': garlic, 'shallot': shallot, 'cabbage': cabbage, 'lemongrass': lemongrass}


def model(crop, stage):
    p = BUILDERS[crop](stage)
    used = sorted({f['texture'][1:] for e in p.el for f in e['faces'].values()})
    return {'textures': {**{t: 'knightsrealm:item/p3/' + t for t in used}, 'particle': 'knightsrealm:item/p3/' + used[0]},
            'elements': p.el}


def ids():
    return ['plant_%s_%d' % (c, s) for c in CROPS for s in range(1, 5)]


def install(ns, write_json):
    tex = textures()
    d = os.path.join(ns, 'textures', 'item', 'p3')
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.png') and f[:-4] not in tex:
            os.remove(os.path.join(d, f))
    for name, img in tex.items():
        img.save(os.path.join(d, name + '.png'))
    for c in CROPS:
        for s in range(1, 5):
            name = 'plant_%s_%d' % (c, s)
            write_json(os.path.join(ns, 'models', 'item', name + '.json'), model(c, s))
            write_json(os.path.join(ns, 'items', name + '.json'), {'model': {'type': 'minecraft:model', 'model': 'knightsrealm:item/' + name}})
    return ids()


# ---------------------------------------------------------------- preview renderer

_FACES = {   # corners in from/to terms, with the uv corner each takes (vanilla face layout)
    'up':    ([(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)], (0, 1, 0)),
    'down':  ([(0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 0, 0)], (0, -1, 0)),
    'north': ([(1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0)], (0, 0, -1)),
    'south': ([(0, 1, 1), (1, 1, 1), (1, 0, 1), (0, 0, 1)], (0, 0, 1)),
    'west':  ([(0, 1, 0), (0, 1, 1), (0, 0, 1), (0, 0, 0)], (-1, 0, 0)),
    'east':  ([(1, 1, 1), (1, 1, 0), (1, 0, 0), (1, 0, 1)], (1, 0, 0)),
}


def _quads(m, tex):
    out = []
    for e in m['elements']:
        f0, t0 = np.array(e['from'], float), np.array(e['to'], float)
        rot = e.get('rotation')
        M = _rot(rot['x'], rot['y'], rot['z']) if rot else np.eye(3)
        o = np.array(rot['origin'], float) if rot else np.zeros(3)
        flat = e.get('shade', True) is False
        for name, face in e['faces'].items():
            corners, normal = _FACES[name]
            pts = np.array([[f0[i] if c[i] == 0 else t0[i] for i in range(3)] for c in corners])
            pts = (M @ (pts - o).T).T + o
            u1, v1, u2, v2 = face['uv']
            uv = np.array([(u1, v1), (u2, v1), (u2, v2), (u1, v2)], float) / 16.0
            out.append((pts, uv, tex[face['texture'][1:]], None if flat else M @ np.array(normal, float)))
    return out


def render(m, tex, size=320, yaw=35.0, pitch=-30.0, ground=True):
    """Orthographic view from above-front, like a player looking down at the crop on farmland."""
    cam = _rot(pitch, 0, 0) @ _rot(0, yaw, 0)
    S = size / 21.0
    img = np.zeros((size, size, 3), np.float32)
    img[:] = (34, 37, 44)
    zb = np.full((size, size), -1e9)
    quads = _quads(m, tex)
    if ground:   # the farmland block under the crop
        soil = Image.fromarray(np.dstack([np.full((T, T), c, np.uint8) for c in (92, 60, 38)] + [np.full((T, T), 255, np.uint8)]), 'RGBA')
        g = {'elements': [{'from': [0, -17, 0], 'to': [16, -1, 16], 'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('up', 'north', 'south', 'east', 'west')}}]}
        quads = _quads(g, {'s': soil}) + quads
    light = np.array([0.3, 1.0, 0.6]); light /= np.linalg.norm(light)
    for pts, uv, timg, nrm in quads:
        P = (cam @ (pts - np.array([8, 3, 8])).T).T
        sx = size / 2 + P[:, 0] * S
        sy = size / 2 - P[:, 1] * S + size * 0.2
        z = P[:, 2] * -1
        shade = 1.0 if nrm is None else 0.55 + 0.45 * abs(float(np.dot(nrm / (np.linalg.norm(nrm) + 1e-9), light)))
        ta = np.asarray(timg, np.float32)
        th, tw = ta.shape[:2]
        for tri in ((0, 1, 2), (0, 2, 3)):
            xs, ys = sx[list(tri)], sy[list(tri)]
            x0, x1 = int(max(0, math.floor(xs.min()))), int(min(size - 1, math.ceil(xs.max())))
            y0, y1 = int(max(0, math.floor(ys.min()))), int(min(size - 1, math.ceil(ys.max())))
            if x1 < x0 or y1 < y0:
                continue
            gy, gx = np.mgrid[y0:y1 + 1, x0:x1 + 1].astype(np.float32) + 0.5
            (ax, ay), (bx, by), (cx, cy) = zip(xs, ys)
            den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            if abs(den) < 1e-9:
                continue
            w0 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / den
            w1 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / den
            w2 = 1 - w0 - w1
            inside = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
            if not inside.any():
                continue
            zz = w0 * z[tri[0]] + w1 * z[tri[1]] + w2 * z[tri[2]]
            uu = w0 * uv[tri[0], 0] + w1 * uv[tri[1], 0] + w2 * uv[tri[2], 0]
            vv = w0 * uv[tri[0], 1] + w1 * uv[tri[1], 1] + w2 * uv[tri[2], 1]
            tx = np.clip((uu * tw).astype(int), 0, tw - 1)
            ty = np.clip((vv * th).astype(int), 0, th - 1)
            col = ta[ty, tx]
            ok = inside & (col[..., 3] > 127) & (zz > zb[y0:y1 + 1, x0:x1 + 1])
            zb[y0:y1 + 1, x0:x1 + 1][ok] = zz[ok]
            img[y0:y1 + 1, x0:x1 + 1][ok] = col[..., :3][ok] * shade
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def sheet(path, yaw=35.0, pitch=-30.0, size=260):
    from PIL import ImageDraw
    tex = textures()
    W = Image.new('RGB', (size * 4, size * len(CROPS)), (24, 26, 31))
    d = ImageDraw.Draw(W)
    for r, c in enumerate(CROPS):
        for s in range(1, 5):
            W.paste(render(model(c, s), tex, size, yaw, pitch), ((s - 1) * size, r * size))
            d.text(((s - 1) * size + 6, r * size + 4), '%s %d' % (c, s), fill=(220, 220, 220))
    W.save(path)


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'plants3d.png'
    sheet(out)
    for c in CROPS:
        for s in range(1, 5):
            print(c, s, len(model(c, s)['elements']), 'elements')
