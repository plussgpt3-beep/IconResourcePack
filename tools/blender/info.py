"""รายละเอียด / วิธีใช้: an open book on its leather cover, pages bowing up from the spine."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
cover_m = leather('cover', (0.22, 0.05, 0.035))
page_m = textured('pages', os.path.join(TEX, 'book_page.png'), rough=0.9, bump=0.04)
edge_m = plain('edges', (0.80, 0.74, 0.60), rough=0.9)
red = plain('ribbon', (0.35, 0.02, 0.02), rough=0.5)
parts = []
for s in (-1, 1):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(s * 0.62, 0, -0.06)); cv = bpy.context.object
    cv.scale = (1.22, 1.62, 0.06); cv.rotation_euler.y = math.radians(-s * 6); cv.data.materials.append(cover_m)
    bevel(cv, 0.02, 2, angle=False); parts.append(cv)
    # page block: thick, its top bowing up from the spine
    blk = grid_sheet('block', 1.12, 1.5, edge_m, nx=30, ny=10, zfun=lambda x, y, s=s: 0.0, thickness=0.0)
    for v in blk.data.vertices:
        t = (v.co.x + 0.56) / 1.12 if s > 0 else (0.56 - v.co.x) / 1.12
        v.co.z = 0.16 * math.sin(math.pi * min(1.0, t * 1.1)) + 0.05
    sol = blk.modifiers.new('solid', 'SOLIDIFY'); sol.thickness = 0.14; sol.offset = -1
    blk.location.x = s * 0.58; parts.append(blk)
    top = grid_sheet('page', 1.12, 1.5, page_m, nx=30, ny=10, thickness=0.004)
    for v in top.data.vertices:
        t = (v.co.x + 0.56) / 1.12 if s > 0 else (0.56 - v.co.x) / 1.12
        v.co.z = 0.16 * math.sin(math.pi * min(1.0, t * 1.1)) + 0.052
    top.location.x = s * 0.58; parts.append(top)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.25, -0.95, 0.05)); rb = bpy.context.object
rb.scale = (0.09, 0.5, 0.008); rb.rotation_euler.x = math.radians(25); rb.data.materials.append(red); parts.append(rb)
stand(parts, tilt=-40, turn=6)
render('info')
