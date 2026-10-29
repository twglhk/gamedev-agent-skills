---
name: art-craft
description: Builds and checks the non-character art of a real-time 3D game (battle grounds, places, props, maps, card art) with a scripted Blender set kit, generated or bought props, baked flat-lit materials, AI image generation held to a written style anchor, engine check shots, numeric readability checks at the game camera, toon shading and post-process ink lines, and a performance budget (triangles, materials, texture memory, frame time). Use when building, generating, texturing, shooting or reviewing a set, prop, material, map or card picture, when setting or checking an asset or frame budget, or when a set looks noisy or flat, hides the characters, or costs too much.
license: MIT
---

# Art craft: sets, props, materials, shading, budget and the checks

Bar for done: **through the game's own camera, under the HUD, in every light state, the player characters are the clearest and brightest thing on screen, the place reads at a glance, and the set stays inside the performance budget. Show both with numbers against an approved baseline, not by eye.**

Characters live in other skills: source sheets `char-3d-source`, motion `char-anim` and `blender-anim`.

## Conventions this skill assumes

Adapt the paths to your project.

- Godot 4 (Forward+) game in `game/`; art work in `design/art/<task-name>/`, one folder per task with its build script, texture scripts, `shots/` and `report.md`.
- An **art bible** in your design docs: pillars, light and colour rules, the brightness order on screen, the battle camera, the HUD zones that must stay clear, a **written style anchor** with reference images, a post-generation checklist and drop list, and the **performance budget**.
- Values (camera, light energies, colours) live in code or data files. When the bible says "value = file CONST", read the number there at the start of each task. Values copied into a skill or report go stale.
- A small toolset you build once; what each tool must do is in [tools](references/tools.md): a Blender set kit, a PBR bake script, an engine check scene, a readability measure, a HUD compositor, a glb counter, a texture-memory estimate and an in-game frame probe.

## One set or prop, start to finish

1. **Brief in six lines.** Which screen and camera; which core verb or emotion of your design the place serves; light states that ship (e.g. evening, night, horror); the board footprint and HUD zones that must stay clear, as Blender coordinates; what the place must say at a glance ("harbour", not "a street"); its budget (triangles, materials, shadowed lamps, texture size and pixels per metre for that camera).
2. **Look up two or three best-in-class examples** of the same kind of space (auto-battler boards such as TFT arenas, HoMM battle screens, Darkest Dungeon rooms). Note how they keep the play area calm and where they spend detail.
3. **Block out first.** A build script that imports the kit, plain materials, shot through the game camera. Fix layout, silhouette and what sits under the HUD here, while change costs nothing. Bethesda's kits and Riot's maps both pass a no-texture proof or block-in stage before art production [1, 2].
4. **Value pass.** Shoot every dark state, look in grayscale and run the numbers before any material work. A layout that fails in grey won't be saved by colour [5, 6, 7].
5. **Surfaces**, in order of preference: a procedural texture script (free, exact control); a generated tile baked to PBR (paid, see below); a generated 3D prop for irregular, organic objects. Signs, doors, posters and anything that would carry letters are built by script, because generators invent fake letters.
6. **Engine check shot** with masks, the baseline set and the same cells and seed; then the HUD composite.
7. **Measure** and compare with the approved baseline through the same camera ([readability](references/readability.md)). Then count the glb and, once the set runs in a build, measure its frame cost with and without the set ([performance](references/performance.md) "Measuring").
8. **One change per pass.** Change one thing, re-shoot, re-measure, so you know what moved the number.
9. **Ask the human to choose.** One image per option at the same size and camera, numbers beside each with what they measure (readability and budget), the report attached. List what nobody checked: other OS, a PC GPU, a full board, a person looking at it at battle size.
10. **Hand off to the dev lane:** glb, textures, material names, marker names, light values and the check scene that shows them. Say that every texture is imported VRAM-compressed with mipmaps (normal maps as normal maps), and which images are shared with an earlier set so they aren't copied again. The art lane doesn't edit game code.

## Building with the kit

- **Everything rebuilds from a script.** `blender -b -P <script>`; one script per set, importing the shared kit. Blender MCP is for looking and trying; the script is the deliverable. In a live Blender, screenshot after every step and save the script before a risky one, so a crash costs one step [29]. One Blender port per agent session.
- **Materials are draws.** The kit makes one mesh per material, so a set's draws in the main pass, the depth prepass and every shadow pass follow its material count. Keep to the material cap; fold colour-only variants into one material; reuse the same material and image across a place's variants instead of exporting copies.
- **Spend triangles near the board.** Bevel the masses whose rounded edge the ink should keep; build upper floors and roofs plain, since they sit small at the top of the screen. TFT spends fidelity on points of interest and keeps the base kit cheap [25] (one source: treat as a proposal and back it with your own count).
- **What the kit's finish step must do:** merge each material into one mesh, project UVs from world space by facing axis so a texture covers the same metres on every wall, bevel masses and harden normals, and export glb with tangents. Normals matter more under cel shading than under realistic light: a small normal error becomes a hard blotch at the light threshold [3].
- **Material names are the contract.** The engine hooks toon shading, emission and per-stage light by material and marker name. A new material name needs a matching line in the check scene and later in the game's stage loader.
- **Markers, not baked lights.** Lamps, floodlights and bought props go in as named empties (`mk_lamp_*`, `mk_crates_*`); the engine places the light or prop. If lights change per stage, they can't be baked.
- **Coordinates.** Blender (x, y, z) is Godot (x, z, −y). Write the board footprint and the camera's visible floor at the top of the script, and keep everything that stands or glows out of the footprint.

## Generated 3D props (e.g. Meshy)

- 🔴 **Paid.** State count and credits before any call, and get approval. Log the actual spend. Reuse an existing prop before buying a new one.
- **When:** irregular, organic pieces where boxes look like boxes (crates, barrels, rope, a crane). Not for anything that must line up with kit geometry, carry letters, or be the main read of the place.
- **How:** text to 3D in two steps, preview (shape) then refine (texture). Ask for flat base colours without baked shadows or highlights, because the game's light and ink post make those. Per the Meshy docs, `remove_lighting` acts only on certain models and Smart Topology's `target_polycount` sets the face count directly [9]. Re-read the docs page before each batch; models and flags retire.
- **After download:** count triangles from the glb, set the real height in the check scene, recolour toward the bible's palette, and look under the ink post at battle size for texture speckle. Generators often return 2048² textures; bring them to the prop budget (a 1 m crate at a far battle camera needs a few hundred pixels per metre, not 2,000), and set `target_polycount` from the budget, not the default.

## Materials

- **A tile is lit flat.** Base colour holds no light, shadow or occlusion; the engine makes those [10, 11]. Prompts say so in capitals.
- **The bake script** turns one tile into albedo, normal and roughness: fix seams by rolling the tile half a cell, take height from luminance minus its large-scale blur, and write OpenGL-style normals (green up), which Godot expects [12]. A DirectX-style tile needs green flipped.
- **For a toon look: flat tone steps, no grain.** A procedural texture with one flat tone per stone or plank often beats a generated one. Check that joints don't draw lines across the board under the ink post.
- **Size tiles by the camera.** Texel density follows the camera [23, 24]. Formula and numbers: [performance](references/performance.md) "Pixels per metre".
- **Every 3D texture ships VRAM-compressed with mipmaps,** normal maps as normal maps (RGTC). Lossless costs about four times the memory [G14], and headless imports stay lossless until someone sets them.
- Proposal, one source: a shared trim sheet for kit mouldings (Insomniac's "Ultimate Trim") can replace per-piece UVs when the kit grows [4].

## Generated images (tiles, card art, concept, map paint)

- 🔴 **Paid.** Say count × price per image before generating and get approval.
- **Keep a written style anchor and reference images in your project.** Every prompt starts with the anchor pasted verbatim and attaches the reference images. Keep the prompt file next to the output; it is the record a Steam AI disclosure is written from [13].
- **Edit, don't regenerate.** Fix a near-miss with a pixel edit or by feeding the picture back with "change only X".
- **Post-check before anyone sees it:** drop the failures and say why, set each next to the tone reference, count figures against the prompt, and for a new set stand a reference character in it and shoot through the game camera.

## Shading, light and post

What the engine does to a set, and what that asks of a mesh: [shading](references/shading.md).

- **One toon shader for every surface.** The game swaps every set and prop material for one toon shader, so a set brings textures, material names and markers, never its own shader. A new surface trick is a request to the dev and FX lanes.
- **Ink lines from a post pass** appear at every depth jump and hard crease. Choose which corners get ink by bevel; detail under about two screen pixels flickers; thin bar rows turn into hatching; transparent surfaces get no ink and no reflection, so sets stay opaque or alpha-scissor.
- **Lights stay real-time** when the stage relights per place or with danger; LightmapGI can't change lights at run time [G12]. Each lamp's reach is a look choice and a cost: every lit pixel runs the toon maths again, fog shows the reach as a wedge, and a shadowed omni lamp redraws the set six times.
- **The post stack is the expensive part** (fog, shadows, MSAA, ink pass, SSR, SSAO): a set costs mostly by the pixels it puts under them. The art lane measures and proposes; changing settings is the dev lane's call with human approval.

## Budget and optimisation

Rule: no stutter from too many meshes. Method, numbers and traps: [performance](references/performance.md).

- **Pick a measuring machine and state its class** (e.g. an Apple M4 benchmarks near a GTX 1650 Laptop [26]); LOW at 1280×800 stands in for the Steam Deck [27]. Platforms nobody ran stay unverified.
- **In a unit-heavy game, characters, not sets, are most of the triangles;** sets cost mostly pixels, materials and shadowed lamps. Apply the budget to every asset anyway: the board fills up later.
- **Every proposal states its numbers against the budget:** triangles, materials, textures (size, VRAM), shadowed lamps and the set's own GPU ms. Going over is a question for the human, with what it buys and what it costs.
- **Auto LOD doesn't help a merged set** (one mesh spanning the scene never leaves its top level) [G4]; build far and high pieces cheap instead. MultiMesh for many identical scattered props [G3]; no occluders for a fixed camera that sees the whole set [G6].

## Reading at battle size

- **Value before hue.** Characters need the strongest light-dark step against what is right behind them; the ground stays calmer and darker; the brightest tile on screen sits next to a hero. Riot keeps a "clean zone" at character height with detail above and below; Valve's TF2 environments keep low noise and simple forms so classes read; VALORANT's shader notes say players mentally block out the environment [2, 5, 8]. For board games and auto-battlers, the board is the clean zone: detail goes to the margins.
- **Measure, then judge.** Report edge step, weak-edge share, brightest tile and ground value per shot against the approved baseline through the same camera. The numbers filter; a person decides.
- **Shoot every state you ship** and once with the HUD over it; a set that reads clean can still put its landmark under a HUD panel.
- **Also show each place lit bright at dusk,** same camera and scene, even if it ships only at night, labelled as a look reference; it shows the forms the dark hides.

## Don't

- Hand-place anything in Blender or the engine that a script doesn't rebuild.
- Put anything that glows, or a line brighter than the characters, inside the board footprint.
- Generate or buy a prop, tile or picture without stating count and cost and getting approval.
- Compare two shots with different lamp reach, seed, cells or camera, or take one run as the value of a clip with a random start.
- Copy bible values into reports, prompts or skills; point to where they live.
- Hand off a 3D texture without VRAM compression and mipmaps, or a second copy of an image a set already ships.
- Go over the performance budget without saying so, with numbers.

Sources with the claim each backs: [sources](references/sources.md) (`[n]` external, `[Gn]` Godot docs).
