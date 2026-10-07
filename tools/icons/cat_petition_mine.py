"""หมวด "ฎีกา ของฉัน" (ฎีกาของฉัน): white ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'WHITE'
TEXT = 'ฎีกา\nของฉัน'


def draw():
    return ribbon(COLOR, 68)
