"""ว่าง / ไม่มีรายการ: an empty turned wooden bowl."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
oak = wood('bowl', (0.24, 0.11, 0.04), (0.07, 0.03, 0.01), axis='Z', scale=9, rough=0.35)
prof = [(0, 0), (0.45, 0), (0.50, 0.03), (0.80, 0.14), (0.98, 0.38), (1.06, 0.62), (1.07, 0.70), (1.03, 0.73),
        (0.97, 0.70), (0.95, 0.62), (0.86, 0.40), (0.68, 0.22), (0.40, 0.14), (0, 0.13)]
b = lathe('bowl', prof, 96, oak)
b.location.z = -0.35
render('empty')
