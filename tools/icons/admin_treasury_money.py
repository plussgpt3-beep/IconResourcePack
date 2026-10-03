"""เพิ่ม/หักเงินคลัง (Admin): the treasury icon with a plus badge."""
from lib import variant


def draw():
    return variant('treasury', 'plus')
