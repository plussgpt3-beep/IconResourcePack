"""หมวด "จัดการ ฎีกา" (จัดการฎีกา): red ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'RED'
TEXT = 'จัดการ\nฎีกา'


def draw():
    return ribbon(COLOR, 69)
