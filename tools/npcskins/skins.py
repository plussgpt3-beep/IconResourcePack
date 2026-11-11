"""Medieval NPC skins (64x64 player skins) painted from a small spec, and a front-view preview of each.

One spec per NPC role; the kingdom gives the accent colour (GearFord steel blue, Stormhold sea teal).
Skin layout = the standard 1.8+ player skin (base layer + hat/jacket/sleeve/pants overlay).
"""
import random
from PIL import Image, ImageDraw

# ---- palette helpers
def rgb(h): return ((h >> 16) & 255, (h >> 8) & 255, h & 255, 255)
def shade(c, f): return (max(0, min(255, int(c[0] * f))), max(0, min(255, int(c[1] * f))), max(0, min(255, int(c[2] * f))), 255)

SKIN = {'fair': 0xE8B894, 'tan': 0xC68E63, 'olive': 0xB48A5A, 'brown': 0x8D5A3B, 'dark': 0x5E3A25, 'pale': 0xF1CDB0}
HAIR = {'black': 0x1E1A18, 'brown': 0x4A2F1B, 'chestnut': 0x6B3E1E, 'blond': 0xC9A24B, 'red': 0x8E3B1A, 'gray': 0x8A8A8A, 'white': 0xD9D9D9, 'dark': 0x2B2320}
ACCENT = {'GF': 0x2F4F8F, 'SH': 0x1F7A72}
ACCENT2 = {'GF': 0xB8BEC8, 'SH': 0xD9B44A}

# part boxes on the skin: (x, y) of the FRONT face, size (w, h); faces laid out right/front/left/back with top above front
PARTS = {'head': (8, 8, 8, 8, 8), 'body': (20, 20, 8, 12, 4), 'rarm': (44, 20, 4, 12, 4), 'larm': (36, 52, 4, 12, 4),
         'rleg': (4, 20, 4, 12, 4), 'lleg': (20, 52, 4, 12, 4)}
OVER = {'head': (32, 0), 'body': (0, 16), 'rarm': (0, 16), 'larm': (16, 0), 'rleg': (0, 16), 'lleg': (-16, 0)}


class Skin:
    def __init__(self, seed=0):
        self.im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        self.px = self.im.load()
        self.rnd = random.Random(seed)

    def _faces(self, part, over=False):
        fx, fy, w, h, d = PARTS[part]
        ox, oy = OVER[part] if over else (0, 0)
        fx += ox; fy += oy
        return {'front': (fx, fy, w, h), 'right': (fx - d, fy, d, h), 'left': (fx + w, fy, d, h), 'back': (fx + w + d, fy, w, h),
                'top': (fx, fy - d, w, d), 'bottom': (fx + w, fy - d, w, d)}

    def fill(self, part, color, faces=None, over=False, noise=0.06, rows=None):
        """Fill faces of a part; rows=(y0,y1) limits to rows of the side faces (0 = top of the part)."""
        F = self._faces(part, over)
        for name in (faces or F.keys()):
            x, y, w, h = F[name]
            for j in range(h):
                if rows and name not in ('top', 'bottom') and not (rows[0] <= j < rows[1]):
                    continue
                if rows and name == 'top' and rows[0] > 0: continue
                if rows and name == 'bottom' and rows[1] < h: continue
                for i in range(w):
                    f = 1 + (self.rnd.random() - 0.5) * 2 * noise
                    if name in ('right', 'left'): f *= 0.92
                    if name == 'back': f *= 0.88
                    if name == 'bottom': f *= 0.75
                    self.px[x + i, y + j] = shade(color, f)

    def dot(self, part, face, i, j, color, over=False):
        x, y, w, h = self._faces(part, over)[face]
        if 0 <= i < w and 0 <= j < h:
            self.px[x + i, y + j] = color

    def rect(self, part, face, i0, j0, i1, j1, color, over=False, noise=0.05):
        for j in range(j0, j1 + 1):
            for i in range(i0, i1 + 1):
                self.dot(part, face, i, j, shade(color, 1 + (self.rnd.random() - 0.5) * 2 * noise), over)


def paint(spec, kingdom='GF'):
    import zlib
    s = Skin(seed=zlib.crc32(spec.get('id', '').encode()) & 0xffff)   # not hash(): that changes from run to run
    A = rgb(ACCENT[kingdom]); A2 = rgb(ACCENT2[kingdom])
    col = lambda v: A if v == 'accent' else A2 if v == 'accent2' else rgb(v)
    skin = rgb(SKIN[spec.get('skin', 'fair')]); hair = rgb(HAIR[spec.get('hair', 'brown')])
    top = col(spec.get('top', 0x6B4A2B)); pants = col(spec.get('pants', 0x3B3026)); boots = col(spec.get('boots', 0x2A1E16))
    sleeve = col(spec.get('sleeve', spec.get('top', 0x6B4A2B)))
    # ---- base body
    s.fill('head', skin)
    for p in ('rarm', 'larm'):
        s.fill(p, sleeve)
        if spec.get('bare_arms'):
            s.fill(p, skin, rows=(4, 12))
        hand = col(spec['gloves']) if spec.get('gloves') else skin
        s.fill(p, hand, rows=(10, 12))
    s.fill('body', top)
    for p in ('rleg', 'lleg'):
        s.fill(p, pants)
        s.fill(p, boots, rows=(9, 12))
    # ---- hair
    style = spec.get('hairstyle', 'short')
    if style != 'bald':
        s.fill('head', hair, faces=['top'])
        s.fill('head', hair, faces=['back'], rows=(0, 8 if style in ('long', 'bun') else 5))
        s.fill('head', hair, faces=['right', 'left'], rows=(0, 6 if style in ('long', 'bun') else 3))
        s.rect('head', 'front', 0, 0, 7, 1 if style != 'tonsure' else 0, hair)
        if style in ('long', 'bun'):
            s.rect('head', 'front', 0, 2, 0, 6, hair); s.rect('head', 'front', 7, 2, 7, 6, hair)
        if style == 'short':
            s.dot('head', 'front', 0, 2, hair); s.dot('head', 'front', 7, 2, hair)
    else:
        s.fill('head', shade(skin, 1.04), faces=['top'])
    # ---- face
    eye = rgb(spec.get('eyes', 0x3A2A1A))
    for i in (1, 5):
        s.dot('head', 'front', i, 4, (245, 245, 245, 255)); s.dot('head', 'front', i + 1, 4, eye)
    s.dot('head', 'front', 2, 4, eye); s.dot('head', 'front', 5, 4, eye)
    s.dot('head', 'front', 1, 4, (245, 245, 245, 255)); s.dot('head', 'front', 6, 4, (245, 245, 245, 255))
    s.rect('head', 'front', 1, 3, 2, 3, shade(hair, 0.9), noise=0); s.rect('head', 'front', 5, 3, 6, 3, shade(hair, 0.9), noise=0)
    s.rect('head', 'front', 3, 5, 4, 5, shade(skin, 0.86), noise=0)       # nose shadow
    s.rect('head', 'front', 3, 6, 4, 6, shade(skin, 0.72), noise=0)       # mouth
    beard = spec.get('beard')
    bc = rgb(HAIR[spec.get('beard_color', spec.get('hair', 'brown'))])
    if beard == 'full':
        s.rect('head', 'front', 0, 5, 7, 7, bc); s.rect('head', 'front', 2, 5, 5, 5, skin); s.rect('head', 'front', 3, 6, 4, 6, shade(skin, 0.7), noise=0)
        s.fill('head', bc, faces=['right', 'left'], rows=(5, 8)); s.fill('head', bc, faces=['bottom'])
    elif beard == 'long':
        s.rect('head', 'front', 0, 5, 7, 7, bc); s.rect('head', 'front', 2, 5, 5, 5, skin); s.rect('head', 'front', 3, 6, 4, 6, shade(skin, 0.7), noise=0)
        s.fill('head', bc, faces=['right', 'left'], rows=(5, 8)); s.fill('head', bc, faces=['bottom'])
        s.rect('body', 'front', 2, 0, 5, 3, bc, over=True)
    elif beard == 'stubble':
        s.rect('head', 'front', 1, 6, 6, 7, shade(skin, 0.8)); s.rect('head', 'front', 3, 6, 4, 6, shade(skin, 0.66), noise=0)
    elif beard == 'mustache':
        s.rect('head', 'front', 2, 6, 5, 6, bc, noise=0); s.dot('head', 'front', 1, 7, bc); s.dot('head', 'front', 6, 7, bc)
    elif beard == 'goatee':
        s.rect('head', 'front', 2, 6, 5, 6, bc, noise=0); s.rect('head', 'front', 3, 7, 4, 7, bc, noise=0)
    # ---- torso styles
    belt = spec.get('belt')
    T = spec.get('style', 'tunic')
    trim = col(spec.get('trim', 0x2A1E16))
    if T == 'tunic':
        s.rect('body', 'front', 3, 0, 4, 1, shade(skin, 0.95)); s.rect('body', 'front', 3, 2, 4, 3, shade(top, 0.75), noise=0)   # collar opening + lacing
        s.rect('body', 'front', 0, 11, 7, 11, shade(top, 0.8))
    elif T == 'apron':
        ap = col(spec.get('apron', 0x5A3D25))
        s.rect('body', 'front', 1, 3, 6, 11, ap); s.rect('body', 'front', 2, 1, 2, 3, shade(ap, 0.8), noise=0); s.rect('body', 'front', 5, 1, 5, 3, shade(ap, 0.8), noise=0)
        for p in ('rleg', 'lleg'):
            s.rect(p, 'front', 0, 0, 3, 3, ap, over=True)
        s.rect('body', 'front', 3, 0, 4, 0, shade(skin, 0.95))
    elif T == 'tabard':
        tb = col(spec.get('tabard', 'accent'))
        under = col(spec.get('mail', 0x8E949C))
        s.fill('body', under); _mail(s, 'body')
        for p in ('rarm', 'larm'):
            s.fill(p, under, rows=(0, 10)); _mail(s, p)
        s.rect('body', 'front', 1, 0, 6, 11, tb); s.rect('body', 'back', 1, 0, 6, 11, shade(tb, 0.88))
        s.rect('body', 'front', 3, 3, 4, 6, A2 if tb == A else A, noise=0); s.rect('body', 'front', 2, 4, 5, 5, A2 if tb == A else A, noise=0)   # emblem cross
        for p in ('rleg', 'lleg'):
            s.rect(p, 'front', 0, 0, 3, 2, tb, over=True)
    elif T == 'plate':
        pl = col(spec.get('plate', 0xAEB4BC))
        for p in ('body', 'rarm', 'larm'):
            s.fill(p, pl, rows=(0, 10) if p != 'body' else None)
        s.rect('body', 'front', 0, 0, 7, 0, shade(pl, 1.12), noise=0); s.rect('body', 'front', 3, 1, 4, 9, shade(pl, 1.1), noise=0)
        s.rect('body', 'front', 0, 5, 7, 5, shade(pl, 0.78), noise=0); s.rect('body', 'front', 1, 8, 6, 8, shade(pl, 0.82), noise=0)
        for p in ('rarm', 'larm'):
            s.rect(p, 'front', 0, 0, 3, 2, shade(pl, 1.12)); s.rect(p, 'front', 0, 6, 3, 6, shade(pl, 0.78), noise=0)
        for p in ('rleg', 'lleg'):
            s.fill(p, shade(pl, 0.92), rows=(0, 9)); s.rect(p, 'front', 0, 4, 3, 5, shade(pl, 1.1)); s.fill(p, shade(pl, 0.7), rows=(9, 12))
        if spec.get('sash'):
            for k in range(8):
                s.dot('body', 'front', k, min(11, 1 + k), col(spec['sash'])); s.dot('body', 'front', k, min(11, 2 + k), col(spec['sash']))
    elif T == 'robe':
        s.fill('body', top)
        for p in ('rleg', 'lleg'):
            s.fill(p, top, rows=(0, 10)); s.fill(p, shade(top, 0.8), rows=(10, 11))
        s.rect('body', 'front', 3, 0, 4, 11, trim, noise=0.03)
        for p in ('rleg', 'lleg'):
            pass
        s.rect('rleg', 'front', 3, 0, 3, 9, trim, noise=0.03); s.rect('lleg', 'front', 0, 0, 0, 9, trim, noise=0.03)
        for p in ('rarm', 'larm'):
            s.rect(p, 'front', 0, 8, 3, 9, trim, noise=0.03)
        s.rect('body', 'front', 2, 0, 5, 0, trim, noise=0.03)
    elif T == 'jerkin':
        jk = col(spec.get('jerkin', 0x5B3A22))
        s.rect('body', 'front', 0, 0, 2, 11, jk); s.rect('body', 'front', 5, 0, 7, 11, jk); s.fill('body', jk, faces=['back', 'right', 'left'])
        for j in (2, 4, 6, 8):
            s.dot('body', 'front', 3, j, shade(jk, 0.6)); s.dot('body', 'front', 4, j, shade(jk, 0.6))
    elif T == 'furs':
        fur = col(spec.get('fur', 0x6A5038))
        s.fill('body', skin); s.rect('body', 'front', 2, 3, 5, 4, shade(skin, 0.9), noise=0)
        s.rect('body', 'front', 0, 0, 7, 2, fur, noise=0.18); s.fill('body', fur, faces=['back'], rows=(0, 6), noise=0.18)
        for k in range(8):
            s.dot('body', 'front', k, min(11, 2 + k // 2), shade(fur, 0.7))
        for p in ('rarm', 'larm'):
            s.fill(p, fur, rows=(0, 3), noise=0.18)
        for p in ('rleg', 'lleg'):
            s.rect(p, 'front', 0, 0, 3, 3, fur, over=True, noise=0.18)
    if spec.get('cloak'):
        ck = col(spec['cloak'])
        s.fill('body', ck, faces=['back'], over=True); s.rect('body', 'front', 0, 0, 0, 11, ck, over=True); s.rect('body', 'front', 7, 0, 7, 11, ck, over=True)
        s.rect('body', 'front', 0, 0, 7, 0, ck, over=True); s.dot('body', 'front', 3, 1, A2, over=True); s.dot('body', 'front', 4, 1, A2, over=True)
        for p in ('rarm', 'larm'):
            s.fill(p, ck, faces=['back', 'right' if p == 'rarm' else 'left', 'top'], over=True, rows=(0, 9))
            s.rect(p, 'front', 0, 0, 3, 1, ck, over=True)
        s.fill('rleg', ck, faces=['back'], over=True, rows=(0, 6)); s.fill('lleg', ck, faces=['back'], over=True, rows=(0, 6))
    if belt:
        b = col(belt)
        s.rect('body', 'front', 0, 9, 7, 9, b, noise=0.02); s.rect('body', 'back', 0, 9, 7, 9, b, noise=0.02)
        s.rect('body', 'right', 0, 9, 3, 9, b, noise=0.02); s.rect('body', 'left', 0, 9, 3, 9, b, noise=0.02)
        s.dot('body', 'front', 3, 9, rgb(0xD8B24A)); s.dot('body', 'front', 4, 9, rgb(0xD8B24A))
        if spec.get('pouch'):
            s.rect('body', 'front', 6, 10, 7, 11, shade(b, 1.3)); s.rect('lleg', 'front', 2, 0, 3, 1, shade(b, 1.3), over=True)
    if spec.get('sash') and T != 'plate':
        sc = col(spec['sash'])
        for k in range(8):
            s.dot('body', 'front', k, min(8, 1 + k), sc); s.dot('body', 'front', k, min(8, 2 + k), sc)
    if spec.get('chain'):
        g = rgb(0xD8B24A)
        for (i, j) in ((1, 1), (2, 2), (3, 3), (4, 3), (5, 2), (6, 1)):
            s.dot('body', 'front', i, j, g)
        s.rect('body', 'front', 3, 4, 4, 4, shade(g, 1.15), noise=0)
    # ---- headgear
    H = spec.get('hat')
    hc = col(spec.get('hatcolor', 0x4A3A2A))
    if H == 'cap':
        s.fill('head', hc, faces=['top'], over=True); s.fill('head', hc, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 2))
    elif H == 'hood':
        s.fill('head', hc, faces=['top', 'back', 'right', 'left'], over=True)
        s.rect('head', 'front', 0, 0, 7, 1, hc, over=True); s.rect('head', 'front', 0, 2, 0, 7, hc, over=True); s.rect('head', 'front', 7, 2, 7, 7, hc, over=True)
        s.rect('body', 'front', 0, 0, 7, 1, hc, over=True); s.rect('body', 'back', 0, 0, 7, 2, hc, over=True)
    elif H == 'straw':
        st = rgb(0xD2B55B)
        s.fill('head', st, faces=['top'], over=True, noise=0.12); s.fill('head', st, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 3), noise=0.12)
        s.rect('head', 'front', 0, 2, 7, 2, shade(st, 0.7), over=True, noise=0)
    elif H == 'coif':
        s.fill('head', hc, faces=['top', 'back'], over=True); s.fill('head', hc, faces=['right', 'left'], over=True, rows=(0, 8))
        s.rect('head', 'front', 0, 0, 7, 0, hc, over=True); s.rect('head', 'front', 0, 1, 0, 7, hc, over=True); s.rect('head', 'front', 7, 1, 7, 7, hc, over=True)
        s.rect('head', 'front', 1, 7, 6, 7, hc, over=True)
    elif H in ('helmet', 'kettle', 'greathelm'):
        st = col(spec.get('hatcolor', 0xAEB4BC))
        s.fill('head', st, faces=['top', 'back'], over=True); s.fill('head', st, faces=['right', 'left'], over=True, rows=(0, 8 if H != 'kettle' else 3))
        if H == 'helmet':
            s.rect('head', 'front', 0, 0, 7, 2, st, over=True); s.rect('head', 'front', 3, 3, 4, 5, shade(st, 0.9), over=True, noise=0)
            s.rect('head', 'front', 0, 3, 0, 7, st, over=True); s.rect('head', 'front', 7, 3, 7, 7, st, over=True)
        elif H == 'kettle':
            s.rect('head', 'front', 0, 0, 7, 1, st, over=True); s.rect('head', 'front', 0, 2, 7, 2, shade(st, 0.75), over=True, noise=0)
        else:
            s.rect('head', 'front', 0, 0, 7, 7, st, over=True); s.rect('head', 'front', 1, 3, 6, 3, (20, 20, 22, 255), over=True, noise=0)
            s.rect('head', 'front', 3, 0, 4, 7, shade(st, 1.12), over=True, noise=0); s.rect('head', 'front', 1, 3, 6, 3, (20, 20, 22, 255), over=True, noise=0)
            for i in (2, 5):
                s.dot('head', 'front', i, 5, (40, 40, 44, 255), True); s.dot('head', 'front', i, 6, (40, 40, 44, 255), True)
        if spec.get('plume'):
            s.rect('head', 'top', 3, 1, 4, 6, col(spec['plume']), over=True)
    elif H == 'crown':
        g = rgb(0xE2BD45)
        s.fill('head', g, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 2), noise=0.03)
        for i in (0, 2, 5, 7):
            s.dot('head', 'front', i, 0, (0, 0, 0, 0), True)
        s.dot('head', 'front', 3, 1, rgb(0xB02A2A), True); s.dot('head', 'front', 4, 1, rgb(0x2A6FB0), True)
    elif H == 'circlet':
        g = col(spec.get('hatcolor', 0xE2BD45))
        s.fill('head', g, faces=['right', 'left', 'back', 'front'], over=True, rows=(1, 2), noise=0.03); s.dot('head', 'front', 3, 1, rgb(0x52C7E8), True); s.dot('head', 'front', 4, 1, rgb(0x52C7E8), True)
    elif H == 'wizard':
        s.fill('head', hc, faces=['top'], over=True); s.fill('head', hc, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 3))
        s.rect('head', 'front', 0, 2, 7, 2, col(spec.get('hatband', 'accent2')), over=True, noise=0)
        s.dot('head', 'front', 3, 0, rgb(0xF2E27A), True); s.dot('head', 'front', 5, 1, rgb(0xF2E27A), True)
    elif H == 'toque':
        w = rgb(0xF2F2F2)
        s.fill('head', w, faces=['top'], over=True); s.fill('head', w, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 3)); s.rect('head', 'front', 0, 2, 7, 2, shade(w, 0.85), over=True, noise=0)
    elif H == 'bandana':
        s.fill('head', hc, faces=['top'], over=True); s.fill('head', hc, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 2)); s.rect('head', 'back', 5, 2, 6, 4, hc, over=True)
    elif H == 'feather':
        s.fill('head', hc, faces=['top'], over=True); s.fill('head', hc, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 2))
        s.rect('head', 'front', 6, 0, 7, 1, col(spec.get('plume', 0xC23B2E)), over=True, noise=0); s.rect('head', 'left', 0, 0, 3, 1, col(spec.get('plume', 0xC23B2E)), over=True, noise=0)
    elif H == 'antlers':
        s.fill('head', hc, faces=['top'], over=True, noise=0.15); s.fill('head', hc, faces=['right', 'left', 'back'], over=True, rows=(0, 4), noise=0.15)
        s.rect('head', 'front', 0, 0, 7, 0, hc, over=True)
        for i in (1, 6):
            s.dot('head', 'front', i, 1, rgb(0xE8DCC0), True)
        s.dot('head', 'front', 0, 0, rgb(0xE8DCC0), True); s.dot('head', 'front', 7, 0, rgb(0xE8DCC0), True)
    elif H == 'goggles':
        s.fill('head', hc, faces=['top'], over=True); s.fill('head', hc, faces=['right', 'left', 'back', 'front'], over=True, rows=(0, 2))
        br = rgb(0xB8792E)
        s.rect('head', 'front', 0, 2, 7, 2, shade(br, 0.6), over=True, noise=0)
        s.rect('head', 'front', 1, 2, 2, 2, rgb(0x8FD3E8), over=True, noise=0); s.rect('head', 'front', 5, 2, 6, 2, rgb(0x8FD3E8), over=True, noise=0)
        s.dot('head', 'front', 0, 2, br, True); s.dot('head', 'front', 3, 2, br, True); s.dot('head', 'front', 4, 2, br, True); s.dot('head', 'front', 7, 2, br, True)
    if spec.get('eyepatch'):
        s.rect('head', 'front', 5, 4, 6, 4, (15, 15, 15, 255), noise=0); s.rect('head', 'front', 0, 3, 7, 3, (25, 25, 25, 255), over=True, noise=0)
    if spec.get('warpaint'):
        s.rect('head', 'front', 0, 5, 2, 5, col(spec['warpaint']), noise=0); s.rect('head', 'front', 5, 5, 7, 5, col(spec['warpaint']), noise=0)
    if spec.get('pauldron'):
        pc = col(spec['pauldron'])
        for p in ('rarm', 'larm'):
            s.fill(p, pc, faces=['top'], over=True); s.fill(p, pc, over=True, rows=(0, 3), faces=['front', 'back', 'right', 'left'])
    if spec.get('sparks'):
        for (p, i, j) in (('body', 1, 2), ('body', 6, 6), ('rarm', 1, 4), ('larm', 2, 7), ('rleg', 1, 6)):
            s.dot(p, 'front', i, j, col(spec['sparks']), True)
    return s.im


def _mail(s, part):
    x, y, w, h = s._faces(part)['front']
    for j in range(h):
        for i in range(w):
            if (i + j) % 2 == 0:
                c = s.px[x + i, y + j]; s.px[x + i, y + j] = shade(c, 0.8)


# ---- preview: the front of the model, base then overlay, drawn like the game shows it from the front
def front(skin, scale=10):
    W, Hh = 16 * scale, 32 * scale
    out = Image.new('RGBA', (W, Hh), (0, 0, 0, 0))
    def blit(part, dx, dy, over):
        fx, fy, w, h, d = PARTS[part]
        ox, oy = OVER[part] if over else (0, 0)
        tile = skin.crop((fx + ox, fy + oy, fx + ox + w, fy + oy + h)).resize((w * scale, h * scale), Image.NEAREST)
        if over:
            g = Image.new('RGBA', (w * scale + 2, h * scale + 2), (0, 0, 0, 0))
            g.paste(tile.resize((w * scale + 2, h * scale + 2), Image.NEAREST), (0, 0))
            out.alpha_composite(g, (dx * scale - 1, dy * scale - 1)) if dx * scale - 1 >= 0 and dy * scale - 1 >= 0 else out.alpha_composite(tile, (dx * scale, dy * scale))
        else:
            out.alpha_composite(tile, (dx * scale, dy * scale))
    for over in (False, True):
        blit('rleg', 4, 20, over); blit('lleg', 8, 20, over)
        blit('body', 4, 8, over)
        blit('rarm', 0, 8, over); blit('larm', 12, 8, over)
        blit('head', 4, 0, over)
    # soft shading lines between parts
    d = ImageDraw.Draw(out)
    for x in (4 * scale, 12 * scale):
        d.line([(x, 8 * scale), (x, 20 * scale - 1)], fill=(0, 0, 0, 60), width=1)
    d.line([(8 * scale, 20 * scale), (8 * scale, 32 * scale - 1)], fill=(0, 0, 0, 70), width=1)
    d.line([(4 * scale, 8 * scale), (12 * scale - 1, 8 * scale)], fill=(0, 0, 0, 60), width=1)
    return out
