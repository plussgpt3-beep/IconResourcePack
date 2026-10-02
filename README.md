# KnightsRealm Icon Pack

Menu icons for the KnightsRealm Minecraft server (Paper 26.1.2, resource pack format 84).
Style: **realistic** (the user's choice, 2026-10-02) — painted at 512×512 with one light from the
upper left, downsampled to 64×64 textures.

The server hands this pack to every player on join (`resource-packs.packs.knightsrealm_icons` in the
plugin's config.yml, by a commit-pinned raw URL and SHA-1). A menu button shows an icon through its
`item_model` component, `knightsrealm:<id>`; the plugin sets that only while the pack is listed.

## Icons

| id | used on | preview |
|---|---|---|
| `knightsrealm:treasury` | ท้องพระคลัง (main menu, treasurer's menu) | ![treasury](preview/treasury.png) |

## Adding or changing an icon

1. Add `tools/icons/<id>.py` with `draw()` returning a 512×512 RGBA image; shared painting helpers
   (lighting, noise, soft masks, gold coin…) are in `tools/lib.py`.
2. `python3 tools/build.py sheet <id> <id>…` — builds the pack and zip, prints the SHA-1, and writes
   `preview/sheet.png` (big view + how it sits in a menu slot) for review.
3. Commit and push, then put the commit-pinned URL and the SHA-1 in the server's config.yml.

The zip is reproducible: the same icons always give the same SHA-1.
