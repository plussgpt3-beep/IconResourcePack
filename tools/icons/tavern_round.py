"""เลี้ยงรอบ: two tankards of ale knocked together in a toast, foam flying from the rims."""
import numpy as np
from PIL import Image
from lib import N, Canvas, light, pillow, blur, ellipse, noise, from_image
from _tavern import tankard, place


def draw():
    rng = np.random.default_rng(2304)
    img = Image.new('RGBA', (N, N))
    left = tankard(rng)
    right = tankard(rng).transpose(Image.FLIP_LEFT_RIGHT)
    place(img, left, 170, 300, 0.78, -18)
    place(img, right, 342, 300, 0.78, 18)
    c = from_image(img)
    splash = np.zeros((N, N), np.float32)
    for (x, y, r) in ((256, 112, 34), (214, 84, 18), (300, 80, 20), (256, 56, 14), (184, 120, 12), (330, 118, 13)):
        splash = np.maximum(splash, ellipse([x - r, y - r, x + r, y + r]))
    splash = blur(splash, 2)
    c.over(light(0.7 * pillow(splash, 8), np.zeros((N, N, 3)) + np.array([0.98, 0.95, 0.85]), depth=40, spec=0.3), splash)
    return c.image()
