"""ตรวจ Quickcast (Admin): the skill_active icon with a check badge."""
from lib import variant


def draw():
    return variant('skill_active', 'check')
