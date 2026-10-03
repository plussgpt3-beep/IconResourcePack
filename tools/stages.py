"""Which icons belong to which stage of the plan (CLAUDE.md "แผนวาดไอคอนเมนูทั้งเกม").
build.py writes ICONS.md from this list and the first line of each icon's docstring, and
`python3 tools/build.py sheet stage3` draws one stage's review sheet."""

JOBS = ['miner', 'lumberjack', 'farmer', 'herbalist', 'fisher', 'scout', 'hunter', 'apprentice_fighter', 'cook', 'merchant',
        'blacksmith', 'engineer', 'guard', 'duelist', 'quartermaster', 'pathfinder', 'naturalist', 'alchemist', 'angler',
        'sea_trader', 'ranger', 'storm_blade', 'artificer', 'master_smith', 'knight', 'berserker', 'druid', 'alchemy_master',
        'tempest_guard', 'beast_lord', 'war_engineer', 'grand_knight', 'storm_sentinel', 'archdruid', 'mech_warlord', 'storm_archmage']

STAGES = {
    'stage1': ('ปุ่มกลาง (ทุกเมนู)', 'back close confirm cancel deny locked page_prev page_next info empty type_in reset treasury'.split()),
    'stage2': ('เมนูหลัก', 'skills mastery profession transfer my_land clan capital travel cities border positions king board quests market trade duel caravan free leave admin quickcast sidebar'.split()),
    'stage3': ('ที่ดิน', 'petition survey_rod land_tax pay_ahead plot_bounds land_expand deed_copy land_sell co_resident add_resident guild land_return land_seize auction queue queue_return stamp_approve stamp_deny vote_up vote_down land_move land_turn'.split()),
    'stage4': ('ก่อสร้าง + งานหลวง', 'zone_staff project_plan project_new site handover materials materials_add foreman apply_foreman workers apply_worker wage ladder floor ceiling demolish renovate job_fix buildings'.split()),
    'stage5': ('เศรษฐกิจ', 'vault treasury_buy treasury_sell vault_expand ledger market_tax price_tag unit_price mint trade_offer stall stall_close sack sell basket buy_order abacus crate claim coin_pile bundle city_materials city_work'.split()),
    'stage6': ('ราชการ + อาณาจักร', 'court governor governor_appoint governor_dismiss noble noble_appoint noble_dismiss city_upgrade abdicate secretariat roster npc npc_skill ballot decree colony_flag colony_found'.split()),
    'stage7': ('ทักษะ / อาชีพ', ['job_' + j for j in JOBS] + 'job_switch job_rest job_return bag_empty skill_active skill_passive enchant life_mining life_woodcutting life_cooking buff_speed buff_strength buff_resistance buff_regeneration buff_haste buff_job_xp buff_extra_drop buff_cooldown'.split()),
    'stage8': ('Admin', 'admin_cooldown_off admin_cooldown_on admin_quickcast admin_fx admin_npc_treasurer admin_npc_memory admin_npc_quest admin_npc_secretary admin_village_spawn admin_quest_board admin_king_appoint admin_king_remove admin_skill_give admin_skill_remove admin_skill_level admin_mastery_level admin_player_level admin_player_money admin_village_xp admin_slave_test admin_items admin_treasury_open admin_treasury_items admin_treasury_money admin_player_menu admin_city_tier'.split()),
    'stage9': ('หมวดหมู่ (ป้ายซ้ายแถว, ตัวหนังสือ)', [l.split('\t')[0] for l in open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'categories.tsv'), encoding='utf-8') if l.strip() and not l.startswith('#')]),
}
