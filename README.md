# KnightsRealm Icon Pack

Menu icons for the KnightsRealm Minecraft server (Paper 26.1.2, resource pack format 84).
Style B (the user's choice, 2026-10-03): every icon is **modelled in 3D and rendered with Blender
Cycles** (one camera, one light rig: key from the upper left, cool fill, warm rim), then cropped,
darkened, sharpened and given a one-pixel dark outline as a 64×64 texture.

The server hands this pack to every player on join (`resource-packs.packs.knightsrealm_icons` in the
plugin's config.yml, by a commit-pinned raw URL and SHA-1). A menu button shows an icon through its
`item_model` component, `knightsrealm:<id>`; the plugin sets that only while the pack is listed.

## Icons

| id | used on | preview |
|---|---|---|
| `knightsrealm:treasury` | ท้องพระคลัง (main menu, treasurer's menu) | ![treasury](preview/treasury.png) |
| Stage 1 (draft, not handed out yet) | back, close, confirm, cancel, deny, locked, page_prev, page_next, info, empty, type_in, reset | ![stage 1](preview/stage1.png) |

## Adding or changing an icon

1. Add `tools/blender/<id>.py`: build the object with the helpers in `tools/blender/common.py`
   (scene, materials such as metal / wood / leather / wax / glass / textured, lathe, extrude, tube,
   sheet…) and end with `render('<id>')`. Image textures are painted by `tools/blender/make_textures.py`.
2. `pip install bpy==4.2.0` once, then `python3 tools/render.py <id>` (≈45 s each, `all` for every icon).
   Renders land in `tools/renders/` and are committed.
3. `python3 tools/build.py sheet <id> <id>…` — builds the pack and zip, prints the SHA-1, and writes
   `preview/sheet.png` (big view + how it sits in a menu slot) for review.
4. Commit and push, then put the commit-pinned URL and the SHA-1 in the server's config.yml.

The zip is reproducible: the same renders always give the same SHA-1. `icons.txt` lists the ids in the pack.
