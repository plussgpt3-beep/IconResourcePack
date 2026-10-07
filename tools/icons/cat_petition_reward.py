"""หมวด "รางวัล" (รางวัลฎีกา): yellow ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'YELLOW'
TEXT = 'รางวัล'


def draw():
    return ribbon(COLOR, 72)
