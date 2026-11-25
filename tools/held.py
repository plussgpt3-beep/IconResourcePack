"""How evolved weapons sit in the hand (the user, 2026-11-25: "ทำให้อาวุธในการวิวัฒแต่ละขั้นมันดูดีขึ้นเมื่อถือขึ้นมือ
เช่นใหญ่ขึ้น ยาวขึ้น หรือมีออร่าแสง"; tier 5 looked tiny, like a flat item held upright).

Each tier gets its own hand pose, a little bigger every tier, and from tier 3 a glowing aura drawn only
when the weapon is held or lies on the ground (not in menus):

    models/item/held/<blade|bow>_t<N>.json     parents with the hand display (scaled about the grip)
    models/item/<gear>.json                    parent -> knightsrealm:item/held/<kind>_t<N>
    textures/item/held/aura_<gear>.png(.mcmeta) glow halo from the weapon's silhouette, pulsing from tier 4,
                                                rising sparks at tier 5
    models/item/held/aura_<gear>.json          one plane through the blade's middle, full-bright (light_emission)
    items/<gear>.json                          gui -> the plain model ; anywhere else -> weapon + aura

Called by build.py after the icons are written (so a full build keeps it); `python tools/held.py` alone
rewrites only these files from the textures already in the pack.
"""
import json, os, re, sys, zlib
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
NS = os.path.join(os.path.dirname(HERE), 'pack', 'assets', 'knightsrealm')
WEAPON = re.compile(r'^gear_(sword|axe|bow)_(fire|ice|storm|venom)(?:_[ab])?_t([2-5])$')

# size in hand against a vanilla tool: third person / first person (first person kept smaller: it fills the screen)
SCALE = {2: (1.00, 1.00), 3: (1.15, 1.08), 4: (1.30, 1.16), 5: (1.50, 1.26)}
# aura: (light_emission, halo radius px @128, strength, frames, pulse low..high, sparks)
AURA = {3: (7, 5.0, 0.60, 1, (1.0, 1.0), 0),
        4: (11, 8.0, 0.85, 8, (0.65, 1.0), 0),
        5: (15, 11.0, 1.00, 16, (0.70, 1.0), 16)}
GLOW = {'fire': ((1.00, 0.42, 0.08), (1.00, 0.86, 0.40)),     # (halo, sparks / core)
        'ice': ((0.35, 0.78, 1.00), (0.88, 0.98, 1.00)),
        'storm': ((0.62, 0.45, 1.00), (0.92, 0.88, 1.00)),
        'venom': ((0.40, 0.95, 0.25), (0.82, 1.00, 0.55))}
GRIP = np.array([-4.5, -4.5, 0.0])     # where the hand holds a blade, model px from the centre (handle lower left)
AURA_RES = 64                          # aura texture size (before the padding)
PAD = 2                                # aura plane reaches 2 model px past the item square (room for the halo)

VANILLA = {   # minecraft:item/handheld and minecraft:item/bow (26.3 client jar)
    'blade': {'thirdperson': ((0, -90, 55), (0, 4.0, 0.5), 0.85), 'firstperson': ((0, -90, 25), (1.13, 3.2, 1.13), 0.68)},
    'bow': {'thirdperson': ((-80, 260, -40), (-1, -2, 2.5), 0.9), 'firstperson': ((0, -90, 25), (1.13, 3.2, 1.13), 0.68)},
}
LEFT_ROT = {'blade': {'thirdperson': (0, 90, -55), 'firstperson': (0, 90, -25)},
            'bow': {'thirdperson': (-80, -280, 40), 'firstperson': (0, 90, -25)}}


def _rot(rx, ry, rz):
    """JOML rotationXYZ, as ItemTransform applies it."""
    a, b, c = np.radians([rx, ry, rz])
    X = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    Y = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    Z = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    return X @ Y @ Z


def _r(v):
    return [round(float(x), 2) + 0.0 for x in v]


def parent(kind, tier):
    disp = {}
    for i, view in enumerate(('thirdperson', 'firstperson')):
        rot, t, s = VANILLA[kind][view]
        k = SCALE[tier][i]
        sn = s * k
        # grow about the grip so the hand stays on the handle (a bow is held in its middle: no shift)
        tn = np.array(t, float) + (_rot(*rot) @ ((s - sn) * GRIP) if kind == 'blade' else 0)
        disp[view + '_righthand'] = {'rotation': list(rot), 'translation': _r(tn), 'scale': _r([sn] * 3)}
        disp[view + '_lefthand'] = {'rotation': list(LEFT_ROT[kind][view]), 'translation': _r(tn), 'scale': _r([sn] * 3)}
    return {'parent': 'minecraft:item/handheld' if kind == 'blade' else 'minecraft:item/generated', 'display': disp}


def _blur(a, r):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255.0


def aura_texture(tex, name, elem, tier):
    light, rad, strength, frames, (lo, hi), sparks = AURA[tier]
    w = AURA_RES                                                  # a soft glow: half the icon's detail is plenty
    rad = rad * w / 128
    tex = tex.convert('RGBA').resize((w, w), Image.LANCZOS)
    pad = w * PAD // 16
    side = w + 2 * pad
    a = np.zeros((side, side), np.float32)
    a[pad:pad + w, pad:pad + w] = np.asarray(tex.convert('RGBA'))[..., 3].astype(np.float32) / 255.0
    sil = (a > 0.35).astype(np.float32)
    halo = np.clip(_blur(sil, rad) * 2.4, 0, 1) ** 0.9          # wide soft glow
    rim = np.clip(_blur(sil, rad * 0.35) * 2.0, 0, 1)           # bright edge hugging the outline
    col, core = (np.array(c, np.float32) for c in GLOW[elem])
    rng = np.random.default_rng(zlib.crc32(name.encode()))
    ys, xs = np.nonzero(sil > 0)
    spark = [(xs[j], ys[j], rng.uniform(0, 1), rng.uniform(0.5, 1.0), rng.uniform(-0.4, 0.4))
             for j in rng.integers(0, len(xs), sparks)] if sparks and len(xs) else []
    yy, xx = np.mgrid[0:side, 0:side].astype(np.float32)
    out = []
    for f in range(frames):
        ph = f / frames
        k = lo + (hi - lo) * (0.5 - 0.5 * np.cos(2 * np.pi * ph))       # pulse
        alpha = np.clip((halo * 0.8 + rim * 0.5) * strength * k, 0, 0.95)
        rgb = col[None, None, :] * (1 - rim[..., None] * 0.45) + core[None, None, :] * rim[..., None] * 0.45
        for (sx, sy, off, spd, drift) in spark:                          # embers rising off the weapon and fading
            t = (ph + off) % 1.0
            px = sx + drift * t * w * 0.35
            py = sy - t * spd * w * 0.45
            life = np.sin(np.pi * t)
            d2 = (xx - px) ** 2 + (yy - py) ** 2
            dot = np.exp(-d2 / (2 * 1.0 ** 2)) * life
            alpha = np.maximum(alpha, np.clip(dot, 0, 1))
            rgb = rgb * (1 - dot[..., None]) + core[None, None, :] * dot[..., None]
        out.append(np.dstack([np.clip(rgb, 0, 1), alpha]))
    strip = np.concatenate(out, axis=0)
    img = Image.fromarray((strip * 255).astype(np.uint8), 'RGBA')
    meta = {'animation': {'interpolate': True, 'frametime': 3 if tier == 5 else 5}} if frames > 1 else None
    return img, meta, light


def aura_model(name, light):
    lo, hi = -PAD, 16 + PAD
    tex = '#aura'
    return {'textures': {'aura': 'knightsrealm:item/held/aura_' + name, 'particle': 'knightsrealm:item/held/aura_' + name},
            'elements': [{'from': [lo, lo, 8], 'to': [hi, hi, 8], 'shade': False, 'light_emission': light,
                          'faces': {'south': {'uv': [0, 0, 16, 16], 'texture': tex},
                                    'north': {'uv': [16, 0, 0, 16], 'texture': tex}}}]}


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def install(ns=NS):
    held_tex = os.path.join(ns, 'textures', 'item', 'held')
    held_mod = os.path.join(ns, 'models', 'item', 'held')
    for d in (held_tex, held_mod):          # rebuilt from scratch each time
        if os.path.isdir(d):
            for f in os.listdir(d):
                os.remove(os.path.join(d, f))
    for kind in ('blade', 'bow'):
        for tier in SCALE:
            _write(os.path.join(held_mod, '%s_t%d.json' % (kind, tier)), parent(kind, tier))
    names = []
    for f in sorted(os.listdir(os.path.join(ns, 'textures', 'item'))):
        m = WEAPON.match(f[:-4]) if f.endswith('.png') else None
        if not m:
            continue
        name, (wkind, elem, tier) = f[:-4], (m.group(1), m.group(2), int(m.group(3)))
        kind = 'bow' if wkind == 'bow' else 'blade'
        base = 'knightsrealm:item/' + name
        _write(os.path.join(ns, 'models', 'item', name + '.json'),
               {'parent': 'knightsrealm:item/held/%s_t%d' % (kind, tier), 'textures': {'layer0': base}})
        item = {'type': 'minecraft:model', 'model': base}
        if tier in AURA:
            img, meta, light = aura_texture(Image.open(os.path.join(ns, 'textures', 'item', f)), name, elem, tier)
            os.makedirs(held_tex, exist_ok=True)
            img.save(os.path.join(held_tex, 'aura_' + name + '.png'), optimize=True)
            if meta:
                _write(os.path.join(held_tex, 'aura_' + name + '.png.mcmeta'), meta)
            _write(os.path.join(held_mod, 'aura_' + name + '.json'), aura_model(name, light))
            item = {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                    'cases': [{'when': ['gui'], 'model': item}],
                    'fallback': {'type': 'minecraft:composite', 'models': [
                        item, {'type': 'minecraft:model', 'model': 'knightsrealm:item/held/aura_' + name}]}}
        _write(os.path.join(ns, 'items', name + '.json'), {'model': item})
        names.append(name)
    return names


if __name__ == '__main__':
    print(len(install()), 'weapons')
