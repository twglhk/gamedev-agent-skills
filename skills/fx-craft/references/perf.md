# Effect performance: what costs, measuring it in a real fight, the budget

Rule: no stutter from too much on screen. Effects are one share of the scene's frame budget (the `art-craft` skill owns the whole); this page is the effects' share. Sources `[S#]` are listed in [shaders.md](shaders.md).

## Where an effect's cost goes

- **Pixels, not triangles.** An effect is a few quads; its cost is fragment work over every pixel each quad covers, layer on layer (overdraw). Transparent layers are all drawn even when covered, can't be batched, and are sorted back to front [S7, S8]. The quad pays for its whole area even where the shader discards.
- **Trim the quad to the shape.** A rectangle fitted to the visible shape saved over 30% of pixels on a smoke sprite; an 8-vertex outline drew 52% of the quad's pixels, 4 vertices 60%; past about 8 vertices isn't worth it [S12, S13]. Fit the quad to the shape's outline (including any grow-out), and use an octagon mesh for round ground decals instead of a square.
- **Transparent is the expensive path.** Blend is slowest; alpha scissor and hash are cheaper; unshaded is the cheapest shading [S9]. Default to scissor + unshaded.
- **Shadows.** A shadow-casting effect is drawn again into every shadow cascade. Keep `cast_shadow = OFF`.
- **Screen copies.** A `hint_screen_texture` material forces a copy of the opaque frame and itself counts as transparent [S5]. Distortion is for max strength only.
- **Particles cost by `amount`.** GPU buffers are allocated and processed for the full `amount`; `amount_ratio` only emits fewer [S2]. Finished one-shot emitters don't simulate.
- **First draw compiles pipelines.** Since Godot 4.4, ubershaders and load-time precompilation cover meshes and materials the renderer sees while loading, but node-level material overrides can't be precompiled at the mesh step, and an effect first added during play compiles on the frame it appears. Documented fix: instantiate it once, even hidden or out of view, while loading [S4]. Specialization compiles run in the background and don't stutter; **Draw** compiles "should never happen" and are an engine bug report [S4].

## Shader compile stutter

1. Instantiate every effect scene the level can play once while the level opens (or between beats), hidden, so its materials are built then, not on first play.
2. Check with a census script that logs pipeline compiles per frame (`RenderingServer` monitors for canvas, mesh, surface, draw, specialization): after the settle, no Surface or Draw compiles caused by effects. Log what geometry is new on each compiling frame. A compile with no new geometry that also appears with effects off isn't an effect's.
3. The driver's pipeline cache hides compile *time* after the first run but not the *count*: read counts, not ms. A first-run player on Windows pays the full cost.

## Measure in a real fight

Use an exported build, not only preview scenes. Run the engine on the exported `.pck` (`godot --main-pack X.pck`) with `--rendering-driver vulkan` (Metal reports GPU time 0). If your probe changes the player's quality settings file, back it up and restore it.

You need two small scripts of your own (any names):

| Tool | What it must do |
| --- | --- |
| Frame probe | Load a given fight with a fixed seed, step at a fixed 1/60 s, skip a settle period, record per-frame wall, process, render-CPU and GPU ms; take a switch that hides all effects. Run effects on and off interleaved, at least two passes per quality preset |
| Effects census | Same fight; per frame count emitting particle systems, live and allocated particles, effect meshes drawn, shadow-casting effects, effect shaders and materials, pipeline compiles; optionally dump overdraw-view PNGs every N frames (on and off) for `capture.py overdraw ON_DIR OFF_DIR`, and list effect nodes drawn at a given frame |

Caveat: an "effects off" switch is rarely clean. Hiding effects can change what else gets drawn (one fight drew about 0.14 M *more* primitives with effects hidden, mostly in shadow passes). Read GPU differences with that in mind and prefer census and overdraw numbers for the effects' own share.

## What a healthy baseline looks like

One reference measurement (Apple M4 10-core GPU, Godot 4.7, Forward+ on Vulkan via MoltenVK, vsync off, a 3-vs-4 boss fight, stepped 1/60 s): effects' GPU share was within noise (−0.3 to +1.1 ms across passes at 8–19 ms frames), peak 2 emitting systems, 7 live particles, 212 allocated, 6 effect meshes, 0 shadow casters, 5 effect shaders, overdraw screen-mean peak 0.043 extra layers, p99 layers where drawn ≤ 4.2. The largest single area (2.3–2.5%) was one square ground-decal quad: a trimming candidate. Opening frames compiled ~55 Surface and 2–4 Draw pipelines; mid-fight compiles also appeared with effects off, so they weren't the effects'.

The lesson: well-built effects are cheap and the frame's cost is the set and the units. The budget below keeps it that way as the board fills and strong moments land.

## Proposed effect budget

Starting caps, measured on the worst fight. Adjust to your target hardware; agree frame ceilings per quality tier with the project owner before treating them as verdicts.

| Item | Cap |
| --- | --- |
| Effects' GPU share, medium preset 1080p | **≤ 1.0 ms** (about 8% of a 12 ms frame) |
| Effects' GPU share, low preset | **≤ 0.7 ms** |
| Effects' extra layers, screen mean | **≤ 0.15 in any shot, ≤ 0.05 over the fight** |
| Effects' layers in one pixel (p99) | **≤ 4; max strength ≤ 8 for its peak frames** |
| One quad's drawn area | the strength's area cap (vfx.md §5), counted on the **drawn quad**, not the visible shape |
| Allocated particles (`amount`) on screen | **≤ 1,000** |
| Effect meshes drawn | **≤ 48** (three weak marks per body for a full board, plus strong moments) |
| Effect nodes casting shadows | **0** |
| Effect shaders in a fight | **≤ 8** (new looks as uniforms on existing shaders first) |
| Surface or Draw compiles caused by an effect after the level opens | **0** |
| Screen-reading effects | **max strength only, one at a time** |
| Effect textures (flipbooks) | **≤ 512² a sheet, VRAM-compressed, mipmaps; ≤ 16 MB in all** |

Why: no engine or studio publishes a layer budget (Godot's overdraw view and Unreal's shader complexity view give colours, "bright red or white over most of the screen is poor" [S14]), so layer caps come from a measured baseline with headroom for a full board and one max-strength moment (10% area). The GPU share keeps effects under a tenth of the frame. The texture cap follows the battle camera: a strong effect at about 10% of 1080p is roughly 300 px across, so a 512² sheet of 4×4 frames gives 128 px a frame, already below screen size for weak and medium effects.
