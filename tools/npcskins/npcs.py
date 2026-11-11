"""Every NPC role of a capital: Thai name, group, what it holds, and its outfit spec (skins.paint)."""
from PIL import Image, ImageDraw

# colours
LEATHER = 0x5A3D25; LINEN = 0xCFC3A4; WOOL_G = 0x4E6B3A; WOOL_R = 0x7A2E2A; WOOL_B = 0x33466B; SOOT = 0x34302E
CREAM = 0xE4D9B8; MOSS = 0x3F5A34; SEA = 0x2E6F86; STORM = 0x3B4F7A; PURPLE = 0x4B2F6B; GOLD = 0xD8B24A; BLACK = 0x1E1C1C

def N(id, th, group, hold, **spec):
    spec['id'] = id
    return dict(id=id, th=th, group=group, hold=hold, spec=spec)

GROUPS = ['ราชสำนักและที่ทำการ', 'การค้าและการเดินทาง', 'ทักษะ Tier 1', 'ทักษะ Tier 2', 'ทักษะ Tier 3', 'ทักษะ Tier 4 และ 5']

NPCS = [
    # ---- court and offices
    N('chancellor', 'อัครมหาเสนาบดี', 0, 'scroll', style='robe', top=PURPLE, trim=GOLD, chain=True, hair='gray', beard='long', beard_color='gray', hat='circlet', skin='fair'),
    N('secretary', 'เลขาธิการ', 0, 'quill', style='robe', top='accent', trim=CREAM, hair='black', hairstyle='bun', hat='cap', hatcolor=BLACK, belt=LEATHER, skin='tan'),
    N('treasurer', 'ขุนคลัง', 0, 'key', style='robe', top=0x5B1F1F, trim=GOLD, chain=True, hair='brown', beard='mustache', hat='cap', hatcolor=0x5B1F1F, belt=GOLD, pouch=True, skin='fair'),
    N('petition_clerk', 'เจ้าพนักงานรับฎีกา', 0, 'scroll', style='tunic', top=LINEN, sleeve=LINEN, pants=0x4A4036, hair='chestnut', hairstyle='tonsure', sash='accent', belt=LEATHER, skin='pale'),
    N('registrar', 'นายทะเบียนงานหลวง', 0, 'hammer', style='apron', top=0x7A6A4A, apron=LEATHER, hair='black', beard='stubble', hat='cap', hatcolor=0x7A6A4A, bare_arms=True, belt=BLACK, skin='tan'),
    N('land_registrar', 'นายทะเบียนที่ดินราษฎร์', 0, 'map', style='jerkin', top=LINEN, sleeve=LINEN, jerkin=WOOL_G, pants=0x4A4036, hair='blond', hat='feather', hatcolor=WOOL_G, belt=LEATHER, pouch=True, skin='fair'),
    N('commander', 'ผู้บัญชาการค่าย', 0, 'sword', style='plate', sash='accent', hair='gray', beard='full', beard_color='gray', cloak='accent', eyepatch=True, pauldron=0x8E949C, skin='tan'),
    N('lists_master', 'นายสนามประลอง', 0, 'banner', style='tabard', tabard='accent2', hair='red', beard='goatee', hat='feather', hatcolor=0x8A2A2A, plume=0xE8E0C8, gloves=LEATHER, belt=BLACK, skin='fair'),
    N('quest', 'ผู้รับส่งเควส', 0, 'book', style='jerkin', top=CREAM, sleeve=CREAM, jerkin='accent', pants=0x3B3026, hair='chestnut', beard='stubble', belt=LEATHER, pouch=True, cloak=0x5A4A32, skin='olive'),
    N('memory_clearer', 'ผู้ชำระความทรงจำ', 0, 'crystal', style='robe', top=0x2B2140, trim=0x9A6BD8, hair='white', hairstyle='long', hat='hood', hatcolor=0x2B2140, eyes=0x9A6BD8, sparks=0xB48CF0, skin='pale'),
    # ---- trade and travel
    N('market', 'นายตลาด', 1, 'scale', style='apron', top=WOOL_R, apron=CREAM, hair='brown', beard='full', hat='cap', hatcolor=WOOL_R, belt=LEATHER, pouch=True, skin='tan'),
    N('banker', 'นายธนาคาร', 1, 'coin', style='jerkin', top=CREAM, sleeve=CREAM, jerkin=BLACK, pants=BLACK, chain=True, hair='black', beard='goatee', hat='cap', hatcolor=BLACK, skin='fair'),
    N('stationmaster', 'นายสถานี', 1, 'horn', style='tunic', top='accent', pants=0x3B3026, hair='brown', beard='mustache', hat='feather', hatcolor=0x3B3026, plume='accent2', cloak=0x4A3A2A, gloves=LEATHER, belt=LEATHER, boots=0x1E1612, skin='tan'),
    N('stable_master', 'นายคอก', 1, 'rope', style='jerkin', top=0x8A7A52, sleeve=0x8A7A52, jerkin=LEATHER, hair='chestnut', beard='stubble', hat='straw', bare_arms=True, belt=LEATHER, boots=0x3A2A1A, skin='brown'),
    # ---- tier 1
    N('miner', 'นักขุดแร่', 2, 'pickaxe', style='tunic', top=0x5A5148, pants=0x3A342E, hair='black', beard='full', hat='kettle', hatcolor=0x8A8F96, bare_arms=True, belt=LEATHER, sparks=SOOT, skin='tan'),
    N('lumberjack', 'คนตัดไม้', 2, 'axe', style='jerkin', top=0x8A2F2A, sleeve=0x8A2F2A, jerkin=LEATHER, pants=0x3B3026, hair='red', beard='full', hat='cap', hatcolor=0x3F5A34, gloves=LEATHER, belt=BLACK, skin='fair'),
    N('farmer', 'ชาวไร่', 2, 'hoe', style='tunic', top=0x9A8A5A, pants=0x5A4A32, hair='blond', hat='straw', bare_arms=True, belt=LEATHER, boots=0x4A3622, skin='tan'),
    N('herbalist', 'นักเก็บสมุนไพร', 2, 'herb', style='apron', top=WOOL_G, apron=0x8A7A52, hair='chestnut', hairstyle='long', hat='hood', hatcolor=MOSS, belt=LEATHER, pouch=True, skin='olive'),
    N('fisher', 'ชาวประมง', 2, 'rod', style='tunic', top=0x4E7C8C, pants=0x4A4036, hair='brown', beard='stubble', hat='straw', bare_arms=True, belt=LEATHER, boots=0x2A2A2E, skin='brown'),
    N('scout', 'นักสอดแนม', 2, 'spyglass', style='jerkin', top=0x6B6B4A, sleeve=0x6B6B4A, jerkin=0x4A3A2A, hair='black', hat='hood', hatcolor=0x4A4A36, cloak=0x4A4A36, belt=LEATHER, skin='tan'),
    N('hunter', 'นักล่า', 2, 'bow', style='jerkin', top=MOSS, sleeve=MOSS, jerkin=LEATHER, hair='brown', beard='stubble', hat='feather', hatcolor=MOSS, plume=0xE8E0C8, gloves=LEATHER, belt=LEATHER, skin='olive'),
    N('apprentice_fighter', 'นักสู้ฝึกหัด', 2, 'wsword', style='tunic', top=CREAM, pants=0x4A4036, hair='blond', hat='bandana', hatcolor='accent', gloves=LEATHER, belt=LEATHER, sash='accent', skin='fair'),
    N('cook', 'พ่อครัว', 2, 'ladle', style='apron', top=CREAM, apron=0xF2F2F2, hair='black', beard='mustache', hat='toque', bare_arms=True, belt=LEATHER, skin='tan'),
    N('merchant', 'พ่อค้า', 2, 'coin', style='jerkin', top=0xC9B26B, sleeve=0xC9B26B, jerkin=0x6B2F4B, pants=0x3B3026, chain=True, hair='brown', beard='goatee', hat='feather', hatcolor=0x6B2F4B, plume=GOLD, belt=LEATHER, pouch=True, skin='fair'),
    # ---- tier 2
    N('blacksmith', 'ช่างตีเหล็ก', 3, 'hammer', style='apron', top=SOOT, apron=LEATHER, hair='black', hairstyle='bald', beard='full', bare_arms=True, gloves=0x3A2A1A, belt=BLACK, sparks=0xF08A2E, skin='tan'),
    N('engineer', 'วิศวกร', 3, 'wrench', style='jerkin', top=CREAM, sleeve=CREAM, jerkin=0x6B4A2B, pants=0x3B3026, hair='chestnut', beard='mustache', hat='goggles', hatcolor=0x6B4A2B, gloves=LEATHER, belt=LEATHER, pouch=True, skin='fair'),
    N('guard', 'ทหารรักษาการณ์', 3, 'spear', style='tabard', hair='brown', beard='stubble', hat='kettle', gloves=LEATHER, belt=BLACK, skin='tan'),
    N('duelist', 'นักดวลดาบ', 3, 'rapier', style='jerkin', top=0xF0EAD8, sleeve=0xF0EAD8, jerkin=BLACK, pants=BLACK, hair='black', hairstyle='long', beard='goatee', hat='feather', hatcolor=BLACK, plume=0xC23B2E, gloves=BLACK, sash=0xC23B2E, skin='fair'),
    N('quartermaster', 'นายทหารส่งกำลัง', 3, 'scroll', style='tabard', tabard=0x6B5A3A, hair='gray', beard='mustache', beard_color='gray', hat='cap', hatcolor='accent', belt=LEATHER, pouch=True, skin='brown'),
    N('pathfinder', 'นักบุกเบิก', 3, 'map', style='jerkin', top=0x7A6A4A, sleeve=0x7A6A4A, jerkin=0x4A3A2A, hair='blond', beard='stubble', hat='feather', hatcolor=0x5A4A32, plume=WOOL_G, cloak=0x5A4A32, gloves=LEATHER, belt=LEATHER, pouch=True, skin='tan'),
    N('naturalist', 'นักธรรมชาติวิทยา', 3, 'book', style='jerkin', top=CREAM, sleeve=CREAM, jerkin=WOOL_G, pants=0x5A4A32, hair='gray', hairstyle='bun', hat='straw', belt=LEATHER, pouch=True, skin='fair'),
    N('alchemist', 'นักเล่นแร่แปรธาตุ', 3, 'flask', style='robe', top=0x3F6B4B, trim=0xC9B26B, hair='black', beard='goatee', hat='goggles', hatcolor=0x2E3A2E, gloves=0x2E2E2E, belt=LEATHER, sparks=0x7BE07B, skin='olive'),
    N('angler', 'นักตกปลามือฉมัง', 3, 'rod', style='jerkin', top=0x6FA0B0, sleeve=0x6FA0B0, jerkin=0x2F4F5F, pants=0x3B3026, hair='gray', beard='full', beard_color='white', hat='cap', hatcolor=0x2F4F5F, belt=LEATHER, boots=0x2A2A2E, skin='tan'),
    N('sea_trader', 'พ่อค้าทางทะเล', 3, 'coin', style='jerkin', top=0xF0EAD8, sleeve=0xF0EAD8, jerkin=0x1F3F5F, pants=0x7A2E2A, hair='black', beard='full', hat='bandana', hatcolor=0xA02A2A, eyepatch=False, chain=True, belt=GOLD, sash=0xA02A2A, boots=0x1E1612, skin='brown'),
    N('ranger', 'พรานป่า', 3, 'bow', style='jerkin', top=0x3F5A34, sleeve=0x3F5A34, jerkin=0x3A2E22, hair='chestnut', beard='stubble', hat='hood', hatcolor=0x2E4428, cloak=0x2E4428, gloves=LEATHER, belt=LEATHER, skin='olive'),
    N('storm_blade', 'นักดาบสายฟ้า', 3, 'sword', style='jerkin', top=STORM, sleeve=STORM, jerkin=0x1E2A44, pants=0x1E2433, hair='white', hat='bandana', hatcolor=0x8FD3E8, gloves=BLACK, sash=0x8FD3E8, sparks=0xBFEFFF, skin='pale'),
    # ---- tier 3
    N('artificer', 'นักประดิษฐ์', 4, 'gear', style='apron', top=0x7A5A8A, apron=0x6B4A2B, hair='white', hairstyle='long', beard='goatee', beard_color='white', hat='goggles', hatcolor=0x4B2F6B, gloves=LEATHER, belt=LEATHER, pouch=True, sparks=0xF0C040, skin='fair'),
    N('master_smith', 'ปรมาจารย์ช่างเหล็ก', 4, 'hammer', style='apron', top=0x2E2A28, apron=0x7A2E1E, hair='gray', beard='long', beard_color='gray', hat='bandana', hatcolor=0x7A2E1E, bare_arms=True, gloves=0x3A2A1A, belt=GOLD, sparks=0xF0A030, skin='brown'),
    N('knight', 'อัศวิน', 4, 'sword', style='plate', sash='accent', hair='brown', beard='stubble', cloak='accent', pauldron=0xC8CED6, skin='fair'),
    N('berserker', 'นักรบบ้าคลั่ง', 4, 'axe2', style='furs', top=0x6A5038, pants=0x4A3622, hair='red', hairstyle='long', beard='long', warpaint=0x2F5F9F, gloves=LEATHER, belt=LEATHER, boots=0x4A3622, skin='fair'),
    N('druid', 'ดรูอิด', 4, 'staff', style='robe', top=0x4E6B3A, trim=0x8A6A3A, hair='chestnut', hairstyle='long', beard='full', hat='antlers', hatcolor=0x5A4630, belt=0x8A6A3A, sparks=0x9BE07B, skin='olive'),
    N('alchemy_master', 'ปรมาจารย์เล่นแร่แปรธาตุ', 4, 'flask', style='robe', top=0x5B2F6B, trim=GOLD, chain=True, hair='white', hairstyle='bald', beard='long', beard_color='white', hat='wizard', hatcolor=0x5B2F6B, gloves=0x2E2E2E, sparks=0xE07BE0, skin='pale'),
    N('tempest_guard', 'ผู้พิทักษ์พายุ', 4, 'shield', style='plate', plate=0x7F97B8, sash=0x8FD3E8, hair='black', hat='helmet', hatcolor=0x7F97B8, plume=0x8FD3E8, cloak=STORM, pauldron=0x9FB7D8, sparks=0xBFEFFF, skin='tan'),
    N('beast_lord', 'เจ้าแห่งสัตว์ป่า', 4, 'bone', style='furs', top=0x4A3A2A, fur=0x8A7A62, pants=0x3A2E22, hair='dark', hairstyle='long', beard='full', hat='antlers', hatcolor=0x8A7A62, warpaint=0x8A2A2A, gloves=LEATHER, belt=LEATHER, skin='brown'),
    # ---- tier 4, 5
    N('war_engineer', 'วิศวกรสงคราม', 5, 'wrench', style='tabard', tabard=0x4A3A2A, hair='black', beard='full', hat='goggles', hatcolor=0x8E949C, gloves=0x3A2A1A, belt=BLACK, pouch=True, pauldron=0x6E747C, sparks=0xF08A2E, skin='tan'),
    N('grand_knight', 'อัศวินชั้นสูง', 5, 'greatsword', style='plate', plate=0xD0D6DE, sash=GOLD, hat='greathelm', hatcolor=0xD0D6DE, plume='accent', cloak='accent', pauldron=0xE2BD45, skin='fair'),
    N('storm_sentinel', 'ผู้เฝ้าระวังพายุ', 5, 'trident', style='plate', plate=0x5F7FA8, sash=0xBFEFFF, hair='white', hairstyle='long', hat='circlet', hatcolor=0xBFEFFF, cloak=0x1E2A44, pauldron=0x8FD3E8, sparks=0xBFEFFF, skin='pale'),
    N('archdruid', 'อาร์คดรูอิด', 5, 'staff', style='robe', top=0x2E4428, trim=GOLD, hair='white', hairstyle='long', beard='long', beard_color='white', hat='antlers', hatcolor=0x3F5A34, cloak=0x4E6B3A, sparks=0xBFF09B, skin='olive'),
    N('mech_warlord', 'จอมทัพจักรกล', 5, 'mace', style='plate', plate=0x4A4E56, sash=0xF08A2E, hair='black', beard='full', hat='goggles', hatcolor=0x4A4E56, cloak=0x7A2E1E, pauldron=0xB8792E, sparks=0xF08A2E, skin='tan'),
    N('storm_archmage', 'อาร์คเมจพายุ', 5, 'staff2', style='robe', top=0x1E2A5A, trim=0x8FD3E8, chain=True, hair='white', hairstyle='long', beard='long', beard_color='white', hat='wizard', hatcolor=0x1E2A5A, hatband=0x8FD3E8, cloak=0x2B3A7A, sparks=0xBFEFFF, eyes=0x52C7E8, skin='pale'),
]


# ---- tiny 16x16 item icons for the preview (the game shows the real item in the hand)
def icon(kind, scale=6):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    W = (110, 78, 46, 255); S = (176, 182, 190, 255); S2 = (120, 126, 134, 255); G = (216, 178, 74, 255)
    def handle(): d.line([(3, 13), (11, 5)], fill=W)
    k = kind
    if k == 'pickaxe':
        handle(); d.arc([5, 0, 15, 10], 180, 300, fill=S); d.line([(7, 3), (13, 3)], fill=S); d.line([(12, 3), (13, 6)], fill=S)
    elif k in ('axe', 'axe2'):
        handle(); d.polygon([(9, 2), (13, 3), (13, 8), (10, 7)], fill=S);
        if k == 'axe2': d.polygon([(6, 5), (3, 4), (2, 8), (6, 8)], fill=S)
    elif k == 'hoe':
        handle(); d.line([(8, 3), (12, 3)], fill=S); d.line([(11, 3), (11, 5)], fill=S)
    elif k in ('sword', 'wsword', 'greatsword', 'rapier'):
        c = (150, 112, 66, 255) if k == 'wsword' else S
        d.line([(4, 12), (13, 3)], fill=c, width=2 if k == 'greatsword' else 1); d.line([(3, 10), (6, 13)], fill=G if k != 'wsword' else W); d.line([(2, 14), (4, 12)], fill=W)
        if k == 'rapier': d.ellipse([3, 10, 6, 13], outline=G)
    elif k == 'hammer':
        handle(); d.rectangle([8, 2, 13, 6], fill=S2); d.line([(8, 2), (13, 2)], fill=S)
    elif k == 'mace':
        handle(); d.ellipse([9, 1, 14, 6], fill=S2); d.point([(8, 3), (11, 0), (14, 3), (11, 7)], fill=S)
    elif k in ('staff', 'staff2'):
        d.line([(4, 14), (11, 3)], fill=W); c = (120, 220, 120, 255) if k == 'staff' else (140, 220, 255, 255)
        d.ellipse([9, 0, 13, 4], fill=c); d.point((11, 2), fill=(255, 255, 255, 255))
    elif k == 'bow':
        d.arc([2, 1, 14, 15], 290, 70, fill=W); d.line([(10, 2), (10, 14)], fill=(230, 230, 230, 255)); d.line([(3, 8), (11, 8)], fill=S)
    elif k == 'rod':
        d.line([(2, 14), (13, 2)], fill=W); d.line([(13, 2), (13, 10)], fill=(230, 230, 230, 255)); d.point((13, 11), fill=(200, 60, 60, 255))
    elif k == 'book':
        d.rectangle([3, 4, 12, 13], fill=(122, 46, 42, 255)); d.rectangle([4, 5, 11, 12], outline=G); d.line([(3, 4), (3, 13)], fill=(70, 26, 24, 255))
    elif k in ('scroll', 'map', 'quill'):
        d.rectangle([3, 4, 12, 12], fill=(228, 217, 184, 255)); d.line([(3, 4), (12, 4)], fill=W); d.line([(3, 12), (12, 12)], fill=W)
        if k == 'map': d.line([(5, 9), (7, 7), (10, 9)], fill=(200, 60, 60, 255)); d.point((10, 6), fill=(60, 60, 200, 255))
        elif k == 'quill': d.line([(8, 10), (13, 1)], fill=(240, 240, 240, 255)); d.point((7, 11), fill=(20, 20, 20, 255))
        else: d.line([(5, 6), (10, 6)], fill=(90, 80, 60, 255)); d.line([(5, 8), (10, 8)], fill=(90, 80, 60, 255)); d.ellipse([9, 9, 12, 12], fill=(160, 40, 40, 255))
    elif k == 'flask':
        d.rectangle([7, 2, 8, 6], fill=(200, 220, 230, 255)); d.polygon([(7, 6), (8, 6), (12, 13), (3, 13)], fill=(120, 220, 140, 255)); d.line([(6, 2), (9, 2)], fill=W)
    elif k == 'coin':
        d.ellipse([3, 6, 12, 14], fill=(138, 106, 58, 255)); d.line([(6, 5), (9, 5)], fill=W); d.ellipse([10, 2, 13, 5], fill=G); d.ellipse([6, 1, 9, 4], fill=G)
    elif k == 'spyglass':
        d.line([(3, 12), (12, 3)], fill=(184, 121, 46, 255), width=2); d.point([(12, 3), (13, 2)], fill=(143, 211, 232, 255))
    elif k == 'ladle':
        handle(); d.ellipse([9, 2, 14, 7], fill=S2)
    elif k == 'shield':
        d.polygon([(3, 2), (12, 2), (12, 9), (7, 14), (3, 9)], fill=(127, 151, 184, 255), outline=S); d.line([(7, 3), (7, 12)], fill=(191, 239, 255, 255)); d.line([(4, 6), (11, 6)], fill=(191, 239, 255, 255))
    elif k == 'key':
        d.ellipse([2, 2, 7, 7], outline=G); d.line([(6, 6), (13, 13)], fill=G); d.line([(11, 13), (13, 11)], fill=G); d.line([(9, 11), (11, 9)], fill=G)
    elif k == 'wrench':
        d.line([(3, 13), (10, 6)], fill=S2, width=2); d.arc([8, 1, 14, 7], 300, 200, fill=S)
    elif k == 'gear':
        d.ellipse([3, 3, 12, 12], outline=(184, 121, 46, 255), width=2)
        for p in ((7, 1), (7, 14), (1, 7), (14, 7), (3, 3), (12, 12), (3, 12), (12, 3)): d.point(p, fill=(184, 121, 46, 255))
        d.point((7, 7), fill=(240, 192, 64, 255)); d.point((8, 8), fill=(240, 192, 64, 255))
    elif k == 'banner':
        d.line([(4, 1), (4, 14)], fill=W); d.polygon([(5, 2), (13, 2), (13, 9), (9, 7), (5, 9)], fill=(194, 59, 46, 255))
    elif k in ('spear', 'trident'):
        d.line([(3, 14), (12, 3)], fill=W); d.polygon([(11, 4), (14, 1), (13, 5)], fill=S)
        if k == 'trident': d.line([(9, 3), (11, 1)], fill=S); d.line([(13, 7), (15, 5)], fill=S)
    elif k == 'herb':
        d.line([(8, 14), (8, 6)], fill=(70, 120, 60, 255)); d.ellipse([4, 3, 8, 8], fill=(90, 160, 80, 255)); d.ellipse([8, 2, 12, 7], fill=(110, 180, 90, 255)); d.point((6, 4), fill=(230, 120, 200, 255))
    elif k == 'scale':
        d.line([(8, 2), (8, 13)], fill=G); d.line([(3, 4), (13, 4)], fill=G); d.arc([1, 5, 6, 10], 0, 180, fill=G); d.arc([10, 5, 15, 10], 0, 180, fill=G); d.line([(5, 13), (11, 13)], fill=G)
    elif k == 'horn':
        d.arc([2, 2, 14, 14], 20, 160, fill=(232, 220, 192, 255), width=2); d.point((13, 9), fill=G)
    elif k == 'rope':
        d.ellipse([3, 3, 12, 12], outline=(176, 142, 90, 255), width=2); d.line([(11, 11), (14, 14)], fill=(176, 142, 90, 255))
    elif k == 'bone':
        d.line([(4, 12), (11, 5)], fill=(236, 230, 214, 255), width=2); d.point([(3, 12), (4, 13), (11, 4), (12, 5)], fill=(236, 230, 214, 255))
    elif k == 'crystal':
        d.polygon([(8, 1), (12, 6), (8, 14), (4, 6)], fill=(154, 107, 216, 255)); d.line([(8, 1), (8, 14)], fill=(200, 170, 250, 255))
    return im.resize((16 * scale, 16 * scale), Image.NEAREST)

HOLD_TH = {'pickaxe': 'อีเต้อ', 'axe': 'ขวาน', 'axe2': 'ขวานสองคม', 'hoe': 'จอบ', 'sword': 'ดาบ', 'wsword': 'ดาบไม้', 'greatsword': 'ดาบใหญ่', 'rapier': 'ดาบเรเปียร์',
           'hammer': 'ค้อน', 'mace': 'กระบอง', 'staff': 'ไม้เท้า', 'staff2': 'คทาพายุ', 'bow': 'ธนู', 'rod': 'เบ็ดตกปลา', 'book': 'หนังสือ', 'scroll': 'ม้วนสาร', 'map': 'แผนที่',
           'quill': 'ปากกาขนนก', 'flask': 'ขวดยา', 'coin': 'ถุงเงิน', 'spyglass': 'กล้องส่อง', 'ladle': 'กระบวย', 'shield': 'โล่', 'key': 'กุญแจคลัง', 'wrench': 'ประแจ',
           'gear': 'เฟือง', 'banner': 'ธง', 'spear': 'หอก', 'trident': 'ตรีศูล', 'herb': 'สมุนไพร', 'scale': 'ตาชั่ง', 'horn': 'แตร', 'rope': 'เชือก', 'bone': 'กระดูก', 'crystal': 'ผลึกอเมทิสต์'}
