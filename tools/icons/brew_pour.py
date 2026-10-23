"""เทถังทิ้ง: an oak barrel tipped on its side, ale pouring out of it into a spreading puddle."""
import numpy as np
from PIL import Image
from lib import N, light, pillow, blur, poly, ellipse, from_image
from _tavern import barrel, place


def draw():
    rng = np.random.default_rng(2306)
    img = Image.new('RGBA', (N, N))
    place(img, barrel(rng, tap=False), 300, 220, 0.78, 72)
    c = from_image(img)
    ale = np.array([0.80, 0.52, 0.12])
    puddle = blur(np.maximum(ellipse([40, 380, 360, 470]), ellipse([20, 400, 200, 480])), 2)
    c.over(light(0.25 * pillow(puddle, 20), np.zeros((N, N, 3)) + ale * 0.9, depth=30, spec=0.7, gloss=50), puddle)
    stream = blur(poly([(150, 200), (178, 210), (150, 300), (130, 420), (98, 420), (118, 290)]), 2)
    c.over(light(0.5 * pillow(stream, 10), np.zeros((N, N, 3)) + ale, depth=30, spec=0.6, gloss=40), stream)
    return c.image()
