# Tools: what to build once

The skill needs a small toolset. These don't ship here; this page says what each must do so you can write your own or swap in one you have. Keep camera, light and colour values in the files that use them and read them there.

## Folder layout

| What | Suggested place |
| --- | --- |
| Set kit (shared library + first set) | `design/art/kit/build_set.py` → `kit/out/<set>.glb` |
| One set per task | `design/art/<task>/build_<set>.py`, texture scripts, `shots/`, `report.md` |
| Scripted props | `build_<prop>.py` → one glb each |
| Generated props | a script with a `PROPS` table → `<name>.glb`, thumbnail, spend log |
| Tiles and prompts | `surface/*.png`, `surface/prompts/*.md` |
| Baked materials | `surface/pbr/<name>_albedo|normal|rough.png` + `preview.png` |
| Engine check project | a small Godot project with check scenes |
| Game copy of a finished set | `game/assets/<place>/` (Git LFS for images) |

## The set kit (Blender, headless)

Run with `blender -b -P <script> [-- <variant>]`. A set script imports the kit, registers materials, calls build functions, then a finish step:

```python
sys.path.insert(0, str(KIT_DIR))
import build_set as kit
kit.OUT = OUT_DIR / "<name>.glb"
kit.TEX["quay"] = ("quay", 3.6)          # material: (pbr image name, metres one tile covers)
kit.COLOR["quay"] = ((1, 1, 1), 0.8, 0)  # material: (base colour sRGB, roughness, metallic)
bpy.ops.wm.read_factory_settings(use_empty=True); build(); kit.finish()
```

- Geometry goes into one bmesh per material, so every primitive takes a material name first: `box`, `cyl` (with taper and squash), `sphere`, `extrude_profile` (a 2D moulding pushed along an axis), `lathe` (posts, bollards), windows punched into walls, plus your street furniture.
- `finish()`: weld, recalc normals, UVs (world projection by facing axis using metres from `TEX`, or one face to one atlas cell for posters and lit windows), assign materials, bevel + weighted normals, export glb with tangents.
- Self-lit materials in an `EMIT` table; the engine re-sets strength per stage.
- Markers are empties named `mk_<kind>_<n>`; each check scene documents which kinds it reads.
- Put the board footprint and the camera's visible floor in Blender coordinates in the script header. Blender (x, y, z) = Godot (x, z, −y).

## Generated props

A script with `name: (prompt, target_polycount)` rows that skips names already downloaded, runs preview then refine, saves glb and thumbnail, and appends credits spent to a log. API key from an untracked `.env`. Check the provider's docs for retired models before each batch.

## Materials

- **Tile prompt file:** style anchor first, one attached reference, flat even light, no text, seamless wrap.
- **Bake script:** `name: (file, height strength, mean roughness)` rows; seam fix by half-cell roll (print seam error before and after), height = luminance minus its large blur, OpenGL normals, roughness; writes a preview sheet.
- **Procedural textures:** numpy scripts with courses, one flat tone per piece, soft joints, normal from the joint mask only.

## Engine check scenes

Run with a window (headless renders no image): `godot --path <check-project> res://<scene>.tscn -- key=value …`. Each saves one 1920×1080 still to `out=` (absolute path) and quits.

Arguments worth having: `set=` (with the approved set as baseline), `stage=` (each light state), `lamp=` (lamp reach, always explicit when comparing), `danger=`, `seed=`, `mask=` (character alpha mask, `<stem>-heroes.png`) and `units=` (all units, `<stem>-units.png`), plus light energies and toon band values for look tests. Use the game's own camera values. A new set extends the scene: load its glb, hook markers and material names, apply per-stage values.

Once the set is in the game, capture the real game view the same way (seed, round, light state) and compare with the art shot at the same lamp reach before calling a difference a bug.

## Measures

| Tool | Input | Output |
| --- | --- | --- |
| Readability measure `<stem>` | shot + hero and unit alpha masks | per unit: body L*, ring L*, edge dL, weak edge %; brightest tile (e.g. 48 px) and its distance to a hero; brightest near and away from heroes; ground L* under the board; top band L* |
| Map or UI-piece measure | shots + piece mask | piece-to-floor contrast (WCAG ratio), warm-pixel share outside pieces, brightest-place ratio |
| HUD composite `<hud.png> <shot.png> <out.png>` | a build screenshot with the HUD over an empty scene + a clean shot | the shot under the current HUD |
| Silhouette render | renders | flat-black silhouettes, for props that must read by shape |
| glb counter `<glob>` | glb files | triangles, materials, surfaces, mesh instances, bones, embedded image sizes |
| Texture memory estimate `<dir>` | imported image folders | GPU memory now (by `.import` mode) and if every texture were VRAM-compressed |
| Frame probe runner | an exported build | probe per ground and preset, with set/units hidden; table of GPU, CPU, draws, primitives, memory, load average |

Thresholds inside the readability measure (weak-edge cutoff, board area, tile size) are tool settings for one camera and resolution, not approved pass marks. Update the board area if the camera changes.
