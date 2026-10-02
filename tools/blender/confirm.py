"""ยืนยัน: a green wax seal with a tick stamped in it."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _seal import seal
from common import render
seal((0.018, 0.085, 0.02), [[(-0.36, 0.02), (-0.12, -0.24), (0.38, 0.30)]], seed=0.0)
render('confirm')
