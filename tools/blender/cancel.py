"""ยกเลิก: a red wax seal with a cross stamped in it."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _seal import seal
from common import render
seal((0.13, 0.008, 0.008), [[(-0.3, -0.3), (0.3, 0.3)], [(-0.3, 0.3), (0.3, -0.3)]], seed=1.7)
render('cancel')
