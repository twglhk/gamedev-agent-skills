# Shading, light and post: what the engine does to your set

Assumes a stylised Godot 4 Forward+ pipeline: one toon shader on every set surface and ink lines from a full-screen post pass. Game shaders belong to the dev lane; read them for current values and never copy the values into a report. If the art check project carries its own copy of the shaders, an art shot can drift from the game: compare in a game capture before calling a look final.

## The shading model

- **One toon shader for every set and prop surface.** The stage loader swaps every material in a set or prop glb for the game's toon shader and carries over albedo, normal map, emission and recolour values. A set brings no shaders of its own. One shader means few render pipelines and no new compile hitch per set [G7]; a new surface trick goes to the dev and FX lanes as a request.
- **Light cut into a few steps** (e.g. three: ink shadow below a low band, fully lit above a high band, one flat middle tone). Bind the shadow map to the same steps so shadow edges are hard. Albedo carries colour only; the steps carry light [10, 11].
- **Normal maps only wobble the step edges.** Under stepped light a normal map shows only where light crosses a band; on a flat lit wall it shows nothing. So derive normals from the joint mask only: joints catch the edge, faces stay flat. Strong per-pixel noise in a normal map becomes speckle at the band edge [3].
- **Normals decide the look more than triangles do.** A small normal error becomes a large blotch at a band edge [3]; Guilty Gear Xrd edited vertex normals by hand for that reason. Bevel masses and use weighted normals; a generated prop's normals are whatever the generator made, so check every prop at a band edge under each key light before handing it over.
- **Each light runs `light()` once per lit pixel.** In Forward+ every omni or spot light reaching a pixel adds another pass of the toon maths [G8]. A lamp covering the whole board costs on every board pixel; keep reach to what the shot needs.

## Ink lines and what they ask of a mesh

- **Lines come from the post pass, not the meshes.** The pass draws a one-pixel line wherever depth jumps or the surface normal turns sharply, reading Godot's depth and normal-roughness buffers [G10]. The other common method, an inverted hull per mesh (Guilty Gear Xrd, many anime games), costs a second draw of every outlined mesh and gives per-object control; the post method costs one full-screen pass whatever the scene holds [3, 19].
- **So every depth step and hard crease draws a line:**
  - Big flat masses stay clean; a bevel under the normal threshold keeps a rounded edge line-free, a sharp corner draws a line. Choose which corners you want inked.
  - Detail under about two pixels at battle size draws flickering line fragments. Make it a colour spot or leave it out.
  - A row of thin bars (railings, fire escapes, wires) becomes black hatching at battle size. Thicken or space it.
- **Transparent surfaces get no ink and no reflection.** Alpha-blended materials don't write the buffers the post pass reads, and SSR skips them [G9]. Use opaque or alpha-scissor materials (glass can be a dark opaque material with emission).
- **Anti-aliasing must keep a one-pixel line.** MSAA suits a cartoon look with few reflective surfaces [G11]; TAA ghosts and smears thin post lines (a published Godot toon-outline project says it doesn't work well with TAA [20]). Check a new set at the lowest preset too: FXAA blurs the ink a little.

## Lights: real-time, and what they cost

- **No baked lightmaps when light changes per stage.** LightmapGI is near free at run time but can't change lights [G12]. Place lamps as markers; a reflection probe rendered once is a fine bake to keep.
- **Ambient occlusion is SSAO, not painted.** Base colour holds no occlusion [10, 11].
- **Shadows are the dearest light feature.** A directional light with four shadow splits draws every shadow-casting mesh again into each split it touches [G13], and a merged set mesh goes through them whole. One omni lamp shadow is cheap; they add up. Shadowed lamp count is part of a set's budget.
- **Lamp light in fog shows as a lit wedge.** Volumetric fog makes every light's reach visible; under stepped light a big reach draws a hard pale wedge over the board. Reach is a look choice and a cost.

## The post stack and its costs

Example measurement, one boss fight on an Apple M4 at HIGH 1920×1080. Re-measure on your own scene before quoting; this only tells you which effects are heavy.

| Effect | GPU ms | What it gives the look |
| --- | ---: | --- |
| Volumetric fog | 3.4 | night air, the lamp wedge |
| Directional shadow, 4 splits, 8192 map | 2.5 | big graphic shadow shapes |
| MSAA 4× | 2.5 | clean edges and clean ink |
| Post pass (ink, grading) + character mask | 2.2 + 0.7 | ink lines and the brightness order |
| SSR | 1.4 | wet stone, water |
| SSAO | 0.75 | contact darkness |
| Glow | 0.5 | lamp and window bloom |

- In that scene the set's own share was 4.2 ms, mostly these effects running on its pixels, not its triangles. A set changes cost by what it puts on screen (lamps, wet materials, transparency) and by how much it draws into shadow maps.
- AgX is Godot's slowest tonemapper [G9]. Pick grading once for the game, not per set.

## Who changes what

- Art lane: meshes, textures, material names, markers, lamp reach and energy proposals, measurements.
- Dev lane: game shaders, environment, graphics presets, import settings, the stage loader.
- FX lane: effect shaders and particles.
- The human: anything that changes the approved look or the performance budget.

Sources: `[n]` and `[Gn]` in [sources](sources.md).
