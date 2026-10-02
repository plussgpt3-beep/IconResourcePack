"""ปิดเมนู: an arched plank door, shut, in a stone surround, with iron straps and a ring pull."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
stone = plain('stone', (0.085, 0.08, 0.075), rough=0.9, spec=0.2, bump=1.2, scale=7)
oak = wood('oak', (0.30, 0.16, 0.07), (0.11, 0.05, 0.02), axis='X', scale=9)
iron = metal('iron', (0.07, 0.07, 0.075), rough=0.5, var=0.15, bump=0.3)
parts = []
for s in (-1, 1):   # the surround in two mirrored halves (outlines without holes)
    o_arc = [(s * x, y) for x, y in arc(0, 0.2, 1.0, math.pi, math.pi / 2, 24)]
    i_arc = [(s * x, y) for x, y in arc(0, 0.2, 0.78, math.pi / 2, math.pi, 20)]
    pts = [(s * -1.0, -1.35)] + o_arc + i_arc + [(s * -0.78, -1.35)]
    if s > 0: pts = pts[::-1]
    parts.append(extrude('frame', pts, 0.34, stone, bevel_w=0.04, segs=3))
for i in range(4):   # four planks under the arch
    x0, x1 = -0.78 + i * 0.39 + 0.008, -0.78 + (i + 1) * 0.39 - 0.008
    top = lambda x: 0.2 + math.sqrt(max(0.0, 0.78 ** 2 - x * x))
    xs = [x0 + (x1 - x0) * k / 10 for k in range(11)]
    pts = [(x0, -1.35), (x1, -1.35)] + [(x, top(x) - 0.01) for x in reversed(xs)]
    p = extrude('plank', pts, 0.14, oak, bevel_w=0.012, segs=2); p.location.z = -0.04; parts.append(p)
for y in (-0.85, 0.05):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, 0.06)); st = bpy.context.object
    st.scale = (1.56, 0.13, 0.04); st.data.materials.append(iron); bevel(st, 0.01, 2, angle=False); parts.append(st)
    for x in (-0.6, -0.2, 0.2, 0.6):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(x, y, 0.085)); r = bpy.context.object
        r.data.materials.append(iron); bpy.ops.object.shade_smooth(); parts.append(r)
bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.028, location=(0.45, -0.42, 0.06))
ring = bpy.context.object; ring.data.materials.append(iron); bpy.ops.object.shade_smooth(); parts.append(ring)
stand(parts, tilt=-8, turn=16)
render('close')
