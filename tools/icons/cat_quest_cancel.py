"""หมวด "ยกเลิก" (ยกเลิกเควส): red ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'RED'
TEXT = 'ยกเลิก'


def draw():
    return ribbon(COLOR, 16)
