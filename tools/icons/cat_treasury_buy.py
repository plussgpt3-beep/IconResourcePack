"""หมวด "ซื้อ" (ซื้อจากคลัง): yellow ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'YELLOW'
TEXT = 'ซื้อ'


def draw():
    return ribbon(COLOR, 28)
