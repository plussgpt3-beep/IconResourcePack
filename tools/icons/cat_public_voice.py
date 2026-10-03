"""หมวด "เสียง ประชาชน" (เสียงประชาชน): yellow ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'YELLOW'
TEXT = 'เสียง\nประชาชน'


def draw():
    return ribbon(COLOR, 48)
