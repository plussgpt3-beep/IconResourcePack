"""Renders icons with Blender (pip package `bpy`, 4.2): python3 tools/render.py <id> [<id>...] | all"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, 'blender')
ids = sys.argv[1:]
if ids == ['all']:
    ids = sorted(f[:-3] for f in os.listdir(B) if f.endswith('.py') and f not in ('common.py', 'make_textures.py') and not f.startswith('_'))
for i in ids:
    r = subprocess.run([sys.executable, os.path.join(B, i + '.py')], capture_output=True, text=True)
    ok = 'Saved:' in r.stdout
    print(i, 'ok' if ok else 'FAILED')
    if not ok:
        print(r.stdout[-1500:], r.stderr[-1500:])
