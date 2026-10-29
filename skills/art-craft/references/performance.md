# Performance: budget, where the cost is, how to stay inside it

Rule: a game that stutters because of too many meshes doesn't ship. Every set, prop and character proposal states its numbers against the budget, the same way it states readability numbers against the baseline.

## Target machines

- **Name one measuring machine and its class.** Notebookcheck rates the Apple M4 10-core GPU almost at a GeForce GTX 1650 Laptop [26], the low end of what Steam players run, so a budget met there is likely held by a min-spec PC. Platforms nobody ran stay unverified.
- **Steam Deck** expects playable frame rates at default settings with 30 fps as the baseline, at 1280×800 [27]. LOW at 1280×800 gets the tightest number.
- Forward+ needs Vulkan 1.0, D3D12 or Metal 3 [G16]; that floor is Godot's.

## The budget

- Keep the approved numbers in one place (the art bible); quote that place in reports instead of copying numbers.
- Two layers: a **frame budget** (GPU and CPU ms per preset, slow frames) shared by every lane, and **asset budgets** (triangles, surfaces, texture size and memory) each lane applies to what it makes.
- Over budget isn't forbidden; it's a question for the human, with the overrun, what it buys on screen and what it costs in ms.

## Where a battle frame's cost goes

Measure your own; this is what a unit-heavy auto-battler scene showed, and what to design around:

- **Characters are most of the triangles.** With seven units on the board, unit bodies were 80 to 90% of the frame's primitives, most drawn again into the directional light's shadow splits; the set was about a quarter of a million. Bones and animation cost microseconds per figure, so the lever is triangles and surfaces, not bones. More units multiply this.
- **Pixels, not triangles, are most of the GPU time.** Fog, shadows, MSAA, the post pass and SSR run over every pixel the set covers ([shading](shading.md)). A set changes cost through wet or reflective materials, lamps and their reach, transparency, and how much of it casts shadows.
- **Shadowed lamps redraw the set.** An omni shadow renders six faces; every shadow caster in range is drawn into each. One shadowed lamp plus the sun drew a set's surfaces about 170 extra times a frame.
- **UI canvas draws dominate the "draw calls" monitor.** Godot counts 2D draws too; hiding the HUD took one frame from about 1,200 to about 430. Report 3D draws with the UI off when judging a set.
- **Texture memory is often not compressed.** Textures that skipped VRAM compression take about four times their compressed size [G14].

## Pixels per metre at the battle camera

Screen height in metres at the board = 2 × distance × tan(fov / 2). Divide the screen height in pixels by it. For a far, high battle camera this is often about 100 px per metre at 1080p, less in depth because of the tilt, and two thirds of that at 1280×800. Recompute whenever the camera changes. That sets three things:

- **Texel density.** Density follows the camera: about 1024 px/m first person, 512 third person, 256 or less top-down [24], with one target and a debug view to check it [23]. A good target is two to three times the screen's density (at 100 px/m, 200 to 300 px/m: a 1024 tile over 3.5 to 5 m). More is memory spent on mip levels the camera never shows. Nearer cameras (exploration, cut scenes) need their own number.
- **Smallest detail.** Anything under two pixels at battle size flickers and breaks ink lines ([shading](shading.md)). Make it a colour spot.
- **Triangle density.** Triangles smaller than a pixel waste GPU time [G2]. A character about 200 px tall at 1080p is why top-down games keep characters around 7,000 to 10,000 triangles [21] and per-slot budgets in the thousands [22].

## Geometry

- **Count from the glb before hand-off:** triangles, materials, surfaces, bones and embedded image sizes.
- **Sets: merge by material, cap the materials.** Main-pass draws ≈ material count, and each material is one more draw in the depth prepass and each shadow pass. Merge colour-only variants into one material where the look allows.
- **Bevel where the ink should round, not everywhere.** Spend bevels on masses near the board.
- **Things at the top of the frame** (upper floors, roofs) are small on screen: fewer triangles, no small mouldings. TFT spends fidelity on points of interest and keeps the base kit cheap [25] (one source: a proposal).
- **Generated props:** set `target_polycount` from the budget (Meshy's Smart Topology takes 100 to 15,000 [9]); a crate needs hundreds, not thousands.

## Materials and draw calls

- **One shader** for every set and prop surface; new shaders mean new pipelines and first-draw hitches [G7].
- **Reuse materials across sets.** Godot batches and instances only identical mesh and material pairs [G1]; the same brick on three variants is one material and one texture.
- **Opaque or alpha-scissor only** in sets: transparent surfaces aren't instanced [G1], aren't in the ink or SSR buffers [G9], and sort per object.

## Textures

- **Every 3D texture VRAM-compressed with mipmaps.** The `.import` says `compress/mode=2` (VRAM Compressed); normal maps go to RGTC [G14]. Lossless costs about four times the memory (2048² colour: 21 MiB against 5 MiB) [G14]. `detect_3d` only switches to VRAM after the editor sees the texture used in 3D, so headless imports stay lossless: write import settings into the hand-off instead of trusting detection.
- **Size by pixels per metre, not habit.** Battle tiles 1024² at the density above; props 512² unless big on screen. A `process/size_limit` in the import or a resize before hand-off brings 2048² generator output down.
- **One texture set per material, shared.** Don't embed the same image in every glb; put shared images in one place and point every material at it.
- **Read texture memory in the game**, per preset (shadow maps and fog volumes count too, so compare the same preset only).

## LOD, MultiMesh, occlusion

- **Mesh LOD is on for glTF imports** and picks a level by the nearest point of the mesh's bounding box [G4]. A merged set spans the scene, so it never drops a level. LOD helps separate props and characters; skinned meshes may break under it [G4].
- **Visibility ranges** suit pieces that exist only far away [G5]; under a fixed camera, just build far pieces cheap.
- **MultiMesh** draws thousands of copies in one call but culls them together [G3]: for many identical scattered props, not one or two.
- **Occlusion culling** helps many-room interiors and gains little under Forward+'s depth prepass [G6]. Skip occluders when the camera sees the whole set.

## Measuring

- **Frame cost from an exported build, not the editor.** Your frame probe loads a fixed screen and seed, settles, records a fixed number of frames at a given preset, and prints GPU ms, CPU ms, draws, primitives and texture/video memory (Godot's Performance monitors [G15]). On macOS, GPU timings need the Vulkan driver (`--rendering-driver vulkan`); Metal may read 0.
- **A set's own cost = the same run with the set hidden**, interleaved with the base run, two passes or more. Hiding units, props or UI splits the rest.
- **A shared machine skews GPU ms.** Other Godot, Blender or ffmpeg runs move it by several ms; record the load average, interleave conditions, repeat comparisons run under load. Triangle, draw and memory counts don't depend on load.
- **If the probe writes the player's settings file to set the preset,** back it up first and restore it byte-identical.

Sources: `[n]` and `[Gn]` in [sources](sources.md).
