"""กระเทียม ระยะ 1/4 (โมเดลพืชในแปลง, 2026-11-27): a block/crop texture, not a menu icon."""
from _crops import plant_icon
CROP = True


def draw():
    return plant_icon('garlic', 1, 2839)
