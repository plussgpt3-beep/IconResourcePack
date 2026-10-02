"""Paints the image textures the Blender scenes use (parchment, written pages, the feather)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tex')
os.makedirs(TEX, exist_ok=True)
N = 1024
rng = np.random.default_rng(3)


def noise(scale, octaves=4):
    out = np.zeros((N, N), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(2, int(N / (scale * 2 ** o)))
        small = rng.random((s, s)).astype(np.float32)
        out += np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC), np.float32) / 255 * amp
        tot += amp; amp *= 0.5
    return out / tot


def parchment():
    base = np.array([0.86, 0.76, 0.56])
    k = 0.86 + 0.20 * (noise(4) - 0.5) + 0.10 * (noise(60, 2) - 0.5)
    yy, xx = np.mgrid[0:N, 0:N] / N
    edge = np.minimum.reduce([xx, 1 - xx, yy, 1 - yy])
    k *= 1 - 0.35 * np.clip(1 - edge / 0.12, 0, 1) ** 2
    return Image.fromarray((np.clip(base * k[..., None], 0, 1) * 255).astype(np.uint8), 'RGB')


def ink_lines(img, x0, x1, y0, y1, step, color=(70, 52, 36), width=7, alpha=150, seed=0):
    r = np.random.default_rng(seed)
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    y = y0
    while y < y1:
        x = x0
        end = x1 - r.integers(0, 140)
        while x < end:                                    # words of random length
            w = int(r.integers(30, 110)); d.line([(x, y), (min(x + w, end), y + r.integers(-2, 3))], fill=color + (alpha,), width=width)
            x += w + int(r.integers(14, 26))
        y += step
    layer = layer.filter(ImageFilter.GaussianBlur(1.2))
    img.paste(layer, (0, 0), layer)
    return img


def brushed(img, points, width, color=(30, 22, 16), poly=False):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    if poly: d.polygon(points, fill=color + (235,))
    else: d.line(points, fill=color + (235,), width=width, joint='curve')
    layer = layer.filter(ImageFilter.GaussianBlur(2))
    img.paste(layer, (0, 0), layer)
    return img


parchment().save(os.path.join(TEX, 'parchment.png'))
for name, s in (('page_prev', -1), ('page_next', 1)):
    im = ink_lines(parchment(), 150, 880, 140, 900, 64, alpha=60, seed=5)
    cx, cy = 512, 520
    im = brushed(im, [(cx - 210 * s, cy), (cx + 90 * s, cy)], 80)
    im = brushed(im, [(cx + 250 * s, cy), (cx + 40 * s, cy - 175), (cx + 40 * s, cy + 175)], 0, poly=True)
    im.save(os.path.join(TEX, name + '.png'))
doc = ink_lines(parchment(), 120, 900, 120, 920, 70, alpha=170, seed=9)
doc = brushed(doc, [(80, 760), (520, 560), (960, 300)], 46, (150, 22, 16))
doc.save(os.path.join(TEX, 'document.png'))
ink_lines(Image.fromarray((np.clip(np.array([0.93, 0.88, 0.74]) * (0.92 + 0.1 * noise(30, 2))[..., None], 0, 1) * 255).astype(np.uint8)),
          90, 940, 110, 930, 62, alpha=140, seed=13).save(os.path.join(TEX, 'book_page.png'))

# feather: RGBA, vane along the vertical axis, barbs angled, transparent outside
yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
t = yy / N                                       # 0 top (tip) .. 1 bottom (quill end)
half = 300 * np.clip(np.sin(np.clip((1 - t - 0.08) / 0.92, 0, 1) * np.pi), 0, 1) ** 0.75 * (t < 0.9)
dx = xx - N / 2 - 25 * np.sin(t * 3)
inside = (np.abs(dx) < half * np.where(dx < 0, 0.75, 1.0))
barbs = 0.5 + 0.5 * np.sin((yy * 0.9 + np.abs(dx) * 0.9) / 5.0)
gaps = (noise(6, 2) > 0.72) & (np.abs(dx) > half * 0.55)           # a few split barbs near the edge
col = np.array([0.96, 0.95, 0.91]) * (0.80 + 0.2 * barbs[..., None]) * (0.92 + 0.12 * noise(40, 2)[..., None])
rach = np.abs(dx) < 6 + 6 * t
col[rach] = [0.88, 0.82, 0.68]
alpha = (inside & ~gaps) | (rach & (t < 0.995))
rgba = np.dstack([np.clip(col, 0, 1), alpha.astype(np.float32)])
Image.fromarray((rgba * 255).astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(0.8)).save(os.path.join(TEX, 'feather.png'))
print('textures ok')
