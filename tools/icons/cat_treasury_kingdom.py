"""หมวด "คลัง อาณาจักร" (คลัง & อาณาจักร): yellow ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'YELLOW'
TEXT = 'คลัง\nอาณาจักร'


def draw():
    return ribbon(COLOR, 61)
