# KnightsRealm Icon Pack

Menu icons for the KnightsRealm Minecraft server (Paper 26.1.2, resource pack format 84).

The server hands this pack to every player on join (`resource-packs.packs.knightsrealm_icons` in the
plugin's config.yml, by URL and SHA-1). A menu button shows an icon through its `item_model`
component, `knightsrealm:<name>`; the plugin only sets that while the pack is listed in the config.

## Icons

| id | used on | preview |
|---|---|---|
| `knightsrealm:treasury` | ท้องพระคลัง (main menu, treasurer's menu) | ![treasury](preview/treasury.png) |

## Changing or adding an icon

1. Draw it in `tools/icons.py` (16x16 character grid, one character per pixel, palette at the top).
2. `python3 tools/build.py` — writes the textures, models and `KnightsRealmIcons.zip`, and prints its SHA-1.
3. Commit and push, then put the zip's URL (pinned to the commit) and SHA-1 in the server's config.yml.

The zip is reproducible: the same icons always give the same SHA-1.
