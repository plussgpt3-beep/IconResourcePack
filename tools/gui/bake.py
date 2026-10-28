"""Menu frames for the game (เมนูแบบกรอบ, 2026-10-28, the user: "เริ่มทำกรอบเมนูจริงในเกม").

A frame is one glyph of the font knightsrealm:gui, set as the chest window's title by the plugin
(GuiFrames.java): the glyph is drawn from the title's place, moved left and up by the font so its
slot grid lands on the chest's slots. Each frame is painted by gui_frame2.py at 1 px = 1 GUI pixel,
cropped so it stops above the player's own inventory, then enlarged x3 so the baked labels (the
plaque and the row tabs, in Kinnari Bold) stay sharp at GUI scale 3.

Geometry (GUI px, frame coordinates): slot grid origin (68, 48) -> chest slot origin (8, 18), so the
frame's left edge is 60 px left of the chest and its top 30 px above it. The title is drawn at
(8, 6) and a glyph's top sits at (title y + 7 - ascent), so ascent = 7 + 6 + 30 = 43 and the
title starts with a 68 px step back (8 + 60).
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = '/usr/share/fonts/truetype/tlwg/Kinnari-Bold.ttf'
S = 3
CUT = 169            # frame rows kept: the chest's own inventory starts 139 px below its top (169 - 30)
ASCENT = 43
SHIFT = -68
GY = 48

# id -> (spec, glyph, plaque text, tab labels by row)
FRAMES = {
    'main': ('game_main.json', '', 'เมนูหลัก',
             {0: 'ตัวละคร', 1: 'อาณาจักร', 2: 'เควส & การค้า', 3: 'ราชการ', 4: 'ตั้งค่า'}),
}

# negative and positive steps, combined by the plugin to move the pen
SPACES = {chr(0xF800 + (1 << k)): -(1 << k) for k in range(8)}
SPACES.update({chr(0xF700 + (1 << k)): (1 << k) for k in range(8)})


def _centred(d, box, text, size, fill, shadow=None):
    x0, y0, x1, y1 = box
    while True:                                   # shrink a long label until it fits its board
        f = ImageFont.truetype(FONT, size)
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        if r - l <= (x1 - x0) - 2 * S or size <= 5 * S:
            break
        size -= 1
    x = x0 + (x1 - x0 - (r - l)) / 2 - l
    y = y0 + (y1 - y0 - (b - t)) / 2 - t
    if shadow:
        d.text((x + S, y + S), text, font=f, fill=shadow)
    d.text((x, y), text, font=f, fill=fill)


def bake(frame_id, out_png):
    spec_name, glyph, plaque, tabs = FRAMES[frame_id]
    spec = json.load(open(os.path.join(HERE, spec_name), encoding='utf-8'))
    raw = os.path.join(HERE, 'out', frame_id + '_raw.png')
    os.makedirs(os.path.dirname(raw), exist_ok=True)
    spec['out'] = raw
    tmp = os.path.join(HERE, 'out', frame_id + '_spec.json')
    json.dump(spec, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
    subprocess.run([sys.executable, os.path.join(HERE, 'gui_frame2.py'), tmp], check=True, cwd=HERE, stdout=subprocess.DEVNULL)
    img = Image.open(raw).convert('RGBA')
    img = img.crop((0, 0, img.width, CUT))
    px = img.load()
    for x in range(44, 254):                      # the cut edge gets the frame's dark outline
        if px[x, CUT - 1][3]: px[x, CUT - 1] = (34, 20, 11, 255)
    big = img.resize((img.width * S, img.height * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    _centred(d, (105 * S, 20 * S, 193 * S, 38 * S), plaque, 13 * S, (58, 33, 18, 255))
    for row, text in tabs.items():
        y0 = GY + 18 * row + 1
        _centred(d, (12 * S, y0 * S, 50 * S, (y0 + 15) * S), text, 9 * S, (244, 228, 196, 255), shadow=(42, 23, 11, 255))
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    big.save(out_png)
    return glyph, img.height


def write_font(ns_dir):
    providers = [{'type': 'space', 'advances': SPACES}]
    for frame_id in FRAMES:
        glyph, h = bake(frame_id, os.path.join(ns_dir, 'textures', 'font', 'gui_' + frame_id + '.png'))
        providers.append({'type': 'bitmap', 'file': 'knightsrealm:font/gui_' + frame_id + '.png',
                          'height': h, 'ascent': ASCENT, 'chars': [glyph]})
    p = os.path.join(ns_dir, 'font', 'gui.json')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', newline='\n', encoding='utf-8') as f:
        json.dump({'providers': providers}, f, ensure_ascii=False, indent=2)
    return ['gui_' + k for k in FRAMES]


if __name__ == '__main__':
    out = os.path.join(HERE, 'out', 'preview_ns')
    print(write_font(out))
