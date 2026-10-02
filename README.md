# KnightsRealm Icon Pack

Menu icons for the KnightsRealm Minecraft server (Paper 26.1.2, resource pack format 84).
Style A (the user's choice, 2026-10-03): **painted in code** — each icon is drawn at 512×512 with
height-map lighting (one key light from the upper left) in `tools/icons/<id>.py`, then cropped,
darkened, sharpened and given a one-pixel dark outline as a 64×64 texture. (A Blender-render
style was tried the same night and dropped: too slow per icon.)

The server hands this pack to every player on join (`resource-packs.packs.knightsrealm_icons` in the
plugin's config.yml, by a commit-pinned raw URL and SHA-1). A menu button shows an icon through its
`item_model` component, `knightsrealm:<id>`; the plugin sets that only while the pack is listed.

## Icons

| id | used on | preview |
|---|---|---|
| `knightsrealm:treasury` | ท้องพระคลัง (main menu, treasurer's menu) | ![treasury](preview/treasury.png) |
| Stage 1 (draft, not handed out yet) | back, close, confirm, cancel, deny, locked, page_prev, page_next, info, empty, type_in, reset | ![stage 1](preview/stage1.png) |
| Stage 2 (draft, not handed out yet) | main menu: skills, mastery, profession, transfer, my_land, clan, capital, travel, cities, border, positions, king, board, quests, market, trade, duel, caravan, free, leave, admin | ![stage 2](preview/stage2.png) |

## Adding or changing an icon

1. Add `tools/icons/<id>.py` with `draw()` returning a 512×512 RGBA painting; the shared helpers
   (masks, height-map `light`, `chrome` metal, wood / parchment / leather / cloth / wax…) are in `tools/lib.py`.
2. `python3 tools/build.py sheet <id> <id>…` — builds the pack and zip, prints the SHA-1, and writes
   `preview/sheet.png` (big view + how it sits in a menu slot) for review.
3. Commit and push, then put the commit-pinned URL and the SHA-1 in the server's config.yml.

The zip is reproducible: the same icons always give the same SHA-1. `icons.txt` lists the ids in the pack.
