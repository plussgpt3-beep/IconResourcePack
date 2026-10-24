"""งานขนส่งหลวง: a laden caravan llama under the crown's sealed bales - the royal haul."""
import numpy as np
from PIL import Image
from lib import N, Canvas, from_image
from _animals import animal, carpet
from _tavern import place


def draw():
    rng = np.random.default_rng(2431)
    c = Canvas()
    animal(c, rng, (0.86, 0.80, 0.66), 'llama')
    carpet(c, rng, (0.55, 0.10, 0.12))
    img = c.image()
    bale = __import__('lib').load_icon('haul_bundle').draw()
    place(img, bale, 330, 215, 0.48, 0)
    return img
