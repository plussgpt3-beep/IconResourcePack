"""Builds the NPC skin pack (the user, 2026-11-11: the capitals' NPCs become people in medieval dress, held by
Mannequin entities whose skin comes from the server's resource pack - no client mod).

    tools/npcskins/skins.py  paints a 64x64 player skin from a small spec (dress, hat, beard, kingdom accent)
    tools/npcskins/npcs.py   the 50 roles: 14 city officials and 36 skill masters
    python3 tools/npcskins/build.py -> npcskins/pack/... and KnightsRealmNpcSkins.zip (reproducible), prints its SHA-1

A skin is assets/knightsrealm/textures/entity/npc/<gf|sh>/<id>.png; the plugin gives a Mannequin the profile texture
knightsrealm:entity/npc/<gf|sh>/<id>. <id> is the plugin's own id for the role (a CityNpcs role or a job id).
"""
import hashlib, json, os, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import skins, npcs

PACK = os.path.join(ROOT, 'npcskins', 'pack')
FORMAT = 84                                   # as the icon pack: Minecraft 26.1.2 and up
PLUGIN_ID = {'commander': 'barracks_commander'}   # the plugin's role id where it differs from the drawing's


def build():
    names = []
    for kingdom, folder in (('GF', 'gf'), ('SH', 'sh')):
        out = os.path.join(PACK, 'assets', 'knightsrealm', 'textures', 'entity', 'npc', folder); os.makedirs(out, exist_ok=True)
        for n in npcs.NPCS:
            img = skins.paint(n['spec'], kingdom)
            assert img.size == (64, 64) and img.mode == 'RGBA', (n['id'], img.size, img.mode)
            name = PLUGIN_ID.get(n['id'], n['id'])
            img.save(os.path.join(out, name + '.png'), optimize=True)
            if folder == 'gf': names.append(name)
    with open(os.path.join(PACK, 'pack.mcmeta'), 'w', newline='\n') as f:
        json.dump({'pack': {'pack_format': FORMAT, 'min_format': FORMAT, 'max_format': FORMAT,
                            'description': 'KnightsRealm NPC skins © 2026 KnightsRealm - All rights reserved'}}, f, indent=2); f.write('\n')
    with open(os.path.join(ROOT, 'npcskins', 'skins.txt'), 'w', newline='\n') as f: f.write('\n'.join(sorted(names)) + '\n')
    return names


def write_zip():
    out = os.path.join(ROOT, 'KnightsRealmNpcSkins.zip')
    files = []
    for base, _, fs in os.walk(PACK):
        for fn in fs: files.append(os.path.join(base, fn))
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files):
            info = zipfile.ZipInfo(os.path.relpath(path, PACK).replace(os.sep, '/'), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o644 << 16
            z.writestr(info, open(path, 'rb').read(), compresslevel=9)
    print('KnightsRealmNpcSkins.zip', os.path.getsize(out), 'bytes, sha1', hashlib.sha1(open(out, 'rb').read()).hexdigest())


if __name__ == '__main__':
    n = build(); print(len(n), 'roles x 2 kingdoms'); write_zip()
