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


# ---------------------------------------------------------------------------------------------
# Every other menu (2026-10-28, the user: "ทำกรอบอื่นทั้งหมดให้เสร็จและใส่ UI เข้าไปให้หมดเลย"): one frame
# per theme and row count, painted at 1 px = 1 GUI px with a socket under every slot and the plaque
# left blank; the plugin writes the menu's own title on the plaque in the title fonts below.
THEMES = ['oak', 'treasury', 'registry', 'coach', 'store', 'guild', 'bank', 'clinic', 'market', 'royal',
          'forge', 'arena', 'board', 'admin', 'stable', 'gaol', 'heraldry', 'throne', 'harbor']
ROW_COUNTS = range(2, 7)


def frame_char(theme, rows):
    return chr(0xE210 + THEMES.index(theme) * 8 + rows)


def ink_width(img):
    """Minecraft's advance source: the rightmost column holding any pixel with alpha, plus one."""
    px = img.load()
    for x in range(img.width - 1, -1, -1):
        if any(px[x, y][3] for y in range(img.height)):
            return x + 1
    return 0


def bake_theme(theme, rows, out_png):
    spec = {'rows': rows, 'theme': theme, 'layout': ['x'] * (9 * rows), 'tabs': []}
    raw = os.path.join(HERE, 'out', 'gen', '%s_%d_raw.png' % (theme, rows))
    os.makedirs(os.path.dirname(raw), exist_ok=True)
    spec['out'] = raw
    tmp = raw[:-4] + '.json'
    json.dump(spec, open(tmp, 'w', encoding='utf-8'))
    subprocess.run([sys.executable, os.path.join(HERE, 'gui_frame2.py'), tmp], check=True, cwd=HERE, stdout=subprocess.DEVNULL)
    img = Image.open(raw).convert('RGBA')
    cut = 61 + 18 * rows                          # the chest's own inventory starts 31 + 18 * rows below its top
    img = img.crop((0, 0, img.width, cut))
    px = img.load()
    for x in range(44, 254):
        if px[x, cut - 1][3]: px[x, cut - 1] = (34, 20, 11, 255)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    img.save(out_png)
    return img


# ---------------------------------------------------------------------------------------------
# Title fonts: the menu's title written on the plaque. Three sizes (the plugin takes the largest that
# fits the plaque), each glyph cut from Kinnari Bold at x3 with its ink at the cell's left edge; the
# plugin places every glyph itself (GuiFrames.titleText) from the metrics in guifont.txt, so Thai
# vowels and tone marks sit where the font puts them (the font's own positional forms, chosen by the
# rules in thai_forms below, stand in for the shaping Minecraft does not do).
TITLE_SIZES = {'t1': 26, 't2': 22, 't3': 18}     # font px at x3
CELL_W, CELL_H, BASE = 48, 96, 36                  # cell px at x3; baseline row in the cell
PLAQUE_CX, PLAQUE_CY, PLAQUE_W = 81, -1.5, 86      # title coordinates (0 = the title's x, chest y)
PUA = 0xE300                                       # Kinnari's positional forms U+F700.. moved here
TALL = {0x0E1B, 0x0E1D, 0x0E1F, 0x0E2C}
UPPER = {0x0E31: 0xF710, 0x0E34: 0xF701, 0x0E35: 0xF702, 0x0E36: 0xF703, 0x0E37: 0xF704, 0x0E47: 0xF712, 0x0E4D: 0xF711}
TONE_LOW = {0x0E48: 0xF70A, 0x0E49: 0xF70B, 0x0E4A: 0xF70C, 0x0E4B: 0xF70D, 0x0E4C: 0xF70E}
TONE_LOW_LEFT = {0x0E48: 0xF705, 0x0E49: 0xF706, 0x0E4A: 0xF707, 0x0E4B: 0xF708, 0x0E4C: 0xF709}
TONE_HIGH_LEFT = {0x0E48: 0xF713, 0x0E49: 0xF714, 0x0E4A: 0xF715, 0x0E4B: 0xF716, 0x0E4C: 0xF717}
LOWER = {0x0E38: 0xF718, 0x0E39: 0xF719, 0x0E3A: 0xF71A}
DESCLESS = {0x0E0D: 0xF70F, 0x0E10: 0xF700}


def title_chars():
    from fontTools.ttLib import TTFont
    cmap = TTFont(FONT).getBestCmap()
    cps = [c for c in range(0x21, 0x7F)] + [c for c in range(0x0E01, 0x0E5C) if c in cmap]
    cps += [c for c in range(0xF700, 0xF71B) if c in cmap]
    return cps


def font_cp(cp):
    return PUA + (cp - 0xF700) if 0xF700 <= cp <= 0xF71F else cp


def thai_forms(text):
    """The text's characters with Thai marks swapped for the font's positional forms (old Windows rules)."""
    cps = [ord(c) for c in text]
    out = list(cps)
    base = base_at = None
    for i, c in enumerate(cps):
        prev = cps[i - 1] if i else None
        nxt = cps[i + 1] if i + 1 < len(cps) else None
        if c in UPPER:
            if base in TALL: out[i] = UPPER[c]
        elif c in TONE_LOW:
            high = prev in UPPER or nxt == 0x0E33
            if high:
                if base in TALL: out[i] = TONE_HIGH_LEFT[c]
            else:
                out[i] = TONE_LOW_LEFT[c] if base in TALL else TONE_LOW[c]
        elif c in LOWER:
            if base in DESCLESS and base_at is not None: out[base_at] = DESCLESS[base]
            elif base in (0x0E0E, 0x0E0F): out[i] = LOWER[c]
        else:
            base, base_at = c, i
    return out


def title_metrics():
    """size -> {codepoint as written in the font: (lsb3, adv3, mc_advance, cell image)}."""
    from PIL import ImageFont as IF
    out = {}
    for key, size in TITLE_SIZES.items():
        f = IF.truetype(FONT, size, layout_engine=IF.Layout.BASIC)
        table = {0x20: (0, round(f.getlength(' ')), 0, None)}
        for cp in title_chars():
            ch = chr(cp)
            canvas = Image.new('L', (200, 160), 0)
            ImageDraw.Draw(canvas).text((80, 100), ch, font=f, fill=255, anchor='ls')
            box = canvas.getbbox()
            if not box:
                continue
            l, t, r, b = box
            cell = Image.new('RGBA', (CELL_W, CELL_H), (255, 255, 255, 0))
            ink = canvas.crop((l, 0, r, 160))
            assert r - l <= CELL_W and t >= 100 - BASE and b <= 100 - BASE + CELL_H, (key, hex(cp))
            alpha = Image.new('L', (CELL_W, CELL_H), 0)
            alpha.paste(ink.crop((0, 100 - BASE, r - l, 100 - BASE + CELL_H)), (0, 0))
            cell.putalpha(alpha)
            w = ink_width(cell)
            table[font_cp(cp)] = (l - 80, round(f.getlength(ch)), int(0.5 + w / 3) + 1, cell)
        out[key] = table
    return out


def floor_div(a, b):
    return a // b


def title_layout(text, metrics):
    """(font key, [(x in GUI px from the title's start, font codepoint)]) for a title, centred on the plaque."""
    for key in TITLE_SIZES:
        table = metrics[key]
        glyphs, pen = [], 0
        for c in thai_forms(text):
            fc = font_cp(c)
            if c == 0x20:
                pen += table[0x20][1]
                continue
            if fc not in table:
                fc = ord('?')
            lsb, adv, mc, _ = table[fc]
            glyphs.append((pen + lsb, fc))
            pen += adv
        if floor_div(pen + 1, 3) <= PLAQUE_W or key == list(TITLE_SIZES)[-1]:
            start = PLAQUE_CX - floor_div(pen + 3, 6)
            return key, [(start + floor_div(x + 1, 3), fc) for x, fc in glyphs]


def write_title_fonts(ns_dir, metrics):
    for key, table in metrics.items():
        cps = sorted(c for c in table if c != 0x20)
        cols = 16
        rows = (len(cps) + cols - 1) // cols
        atlas = Image.new('RGBA', (cols * CELL_W, rows * CELL_H), (255, 255, 255, 0))
        chars = []
        for r in range(rows):
            line = ''
            for c in range(cols):
                i = r * cols + c
                if i < len(cps):
                    atlas.paste(table[cps[i]][3], (c * CELL_W, r * CELL_H))
                    line += chr(cps[i])
                else:
                    line += '\u0000'
            chars.append(line)
        tex = os.path.join(ns_dir, 'textures', 'font', 'gui_' + key + '.png')
        os.makedirs(os.path.dirname(tex), exist_ok=True)
        atlas.save(tex)
        xh = 16 * TITLE_SIZES[key] / 26 / 3        # height of the body of a consonant, GUI px
        base = round(PLAQUE_CY + xh / 2)            # baseline, chest y
        ascent = 13 - (base - BASE // 3)            # glyph top = title y (6) + 7 - ascent
        p = os.path.join(ns_dir, 'font', 'gui_' + key + '.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', newline='\n', encoding='utf-8') as f:
            json.dump({'providers': [{'type': 'space', 'advances': SPACES},
                                     {'type': 'bitmap', 'file': 'knightsrealm:font/gui_' + key + '.png',
                                      'height': CELL_H // 3, 'ascent': ascent, 'chars': chars}]},
                      f, ensure_ascii=False, indent=2)


# Minecraft cannot load a font glyph larger than 256 x 256 texture px (it draws a box instead, seen in the
# game 2026-10-30), so every frame is cut into tiles no larger than that, one character each, laid side by
# side by the plugin from the tile list in guifont.txt (each tile's x and the advance the game gives it).
TILE_MAX = 255


def _cuts(total, scale):
    """Edges cutting {total} texture px into near-equal parts of at most TILE_MAX, on whole GUI px."""
    n = -(-total // TILE_MAX)
    gui = total // scale
    edges = [round(gui * k / n) * scale for k in range(n + 1)]
    edges[-1] = total
    return edges


def tile_frame(img, scale, name, chars, ns_dir):
    """Cut {img} (drawn at {scale} texture px per GUI px) into tiles; returns (providers, [(char, x, advance)])."""
    providers, tiles = [], []
    xs, ys = _cuts(img.width, scale), _cuts(img.height, scale)
    k = 0
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            part = img.crop((xs[i], ys[j], xs[i + 1], ys[j + 1]))
            if not part.getbbox():
                continue
            ch = chars[k]; k += 1
            tex = '%s_%d.png' % (name, k)
            part.save(os.path.join(ns_dir, 'textures', 'font', tex))
            h_gui = part.height // scale
            providers.append({'type': 'bitmap', 'file': 'knightsrealm:font/' + tex,
                              'height': h_gui, 'ascent': ASCENT - ys[j] // scale, 'chars': [ch]})
            w = ink_width(part)
            adv = int(0.5 + w * h_gui / part.height) + 1
            tiles.append((ch, xs[i] // scale, adv))
    return providers, tiles


def frame_chars(index):
    """Eight private-use characters for frame number {index} (0 = the main menu)."""
    return [chr(0xE400 + index * 8 + k) for k in range(8)]


def write_font(ns_dir, metrics_out=None):
    providers = [{'type': 'space', 'advances': SPACES}]
    lines = []
    os.makedirs(os.path.join(ns_dir, 'textures', 'font'), exist_ok=True)
    for frame_id in FRAMES:
        full = os.path.join(HERE, 'out', 'gen', 'gui_' + frame_id + '_full.png')
        os.makedirs(os.path.dirname(full), exist_ok=True)
        bake(frame_id, full)
        prov, tiles = tile_frame(Image.open(full).convert('RGBA'), S, 'gui_' + frame_id, frame_chars(0), ns_dir)
        providers += prov
        lines.append('frame %s 0 %s' % (frame_id, ' '.join('%04X:%d:%d' % (ord(c), x, a) for c, x, a in tiles)))
    ids = ['gui_' + k for k in FRAMES]
    n = 1
    for theme in THEMES:
        for rows in ROW_COUNTS:
            name = 'gui_%s_%d' % (theme, rows)
            full = os.path.join(HERE, 'out', 'gen', name + '_full.png')
            img = bake_theme(theme, rows, full)
            prov, tiles = tile_frame(img, 1, name, frame_chars(n), ns_dir)
            n += 1
            providers += prov
            lines.append('frame %s %d %s' % (theme, rows, ' '.join('%04X:%d:%d' % (ord(c), x, a) for c, x, a in tiles)))
            ids.append(name)
    p = os.path.join(ns_dir, 'font', 'gui.json')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', newline='\n', encoding='utf-8') as f:
        json.dump({'providers': providers}, f, ensure_ascii=False, indent=2)
    metrics = title_metrics()
    write_title_fonts(ns_dir, metrics)
    for key, table in metrics.items():
        lines.append('space %s %d' % (key, table[0x20][1]))
        for cp in sorted(c for c in table if c != 0x20):
            lsb, adv, mc, _ = table[cp]
            lines.append('glyph %s %04X %d %d %d' % (key, cp, lsb, adv, mc))
    if metrics_out:
        with open(metrics_out, 'w', newline='\n', encoding='utf-8') as f:
            f.write('# GUI frame and title-font metrics from tools/gui/bake.py (do not edit)\n')
            f.write('\n'.join(lines) + '\n')
            for sample in SAMPLES:
                key, glyphs = title_layout(sample, metrics)
                f.write('sample %s %s|%s\n' % (key, ' '.join('%d:%04X' % g for g in glyphs), sample))
    return ids + ['gui_title']


# titles whose layout the plugin's test checks against this file
SAMPLES = ['ท้องพระคลัง GearFord', 'นายทะเบียนที่ดินราษฎร์ GearFord', 'ปุ่ม ป่า ฟ้า ฝั่ง ปิ่น', 'ญาติ ฐูป ฎุ ฏู',
           'น้ำ ที่ ก่อ กี่ ก็ ผู้ ปื้น', 'ฎีกา #12 2/3', 'การค้าระหว่างเมือง', 'อาชีพ', 'แลกของกับ Bpor2_x']


if __name__ == '__main__':
    out = os.path.join(HERE, 'out', 'preview_ns')
    print(len(write_font(out, os.path.join(HERE, 'out', 'guifont.txt'))))


def title_top(key):
    """Chest y of the top of a title-font cell (same sums as write_title_fonts)."""
    xh = 16 * TITLE_SIZES[key] / 26 / 3
    return round(PLAQUE_CY + xh / 2) - BASE // 3


def preview(frame_png, title, metrics, out_png, ink=(58, 33, 18)):
    """The window as the game should draw it (x3): the frame, and the title placed by title_layout."""
    frame = Image.open(frame_png).convert('RGBA')
    if frame.width < 400:
        frame = frame.resize((frame.width * S, frame.height * S), Image.NEAREST)
    canvas = Image.new('RGBA', frame.size, (20, 17, 14, 255))
    canvas.alpha_composite(frame)
    key, glyphs = title_layout(title, metrics)
    for x, fc in glyphs:
        cell = metrics[key][fc][3]
        tinted = Image.new('RGBA', cell.size, ink + (255,))
        tinted.putalpha(cell.getchannel('A'))
        canvas.alpha_composite(tinted, ((x + 68) * S, (title_top(key) + 30) * S))
    canvas.save(out_png)
