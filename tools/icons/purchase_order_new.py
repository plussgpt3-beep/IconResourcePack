"""เปิดใบสั่งซื้อใหม่: the purchase order with a plus badge."""
from lib import variant


def draw():
    return variant('purchase_order', 'plus')
