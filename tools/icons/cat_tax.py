"""หมวด "ภาษี" (ภาษีของฉัน, ตารางภาษีราษฎร): yellow ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'YELLOW'
TEXT = 'ภาษี'


def draw():
    return ribbon(COLOR, 65)
