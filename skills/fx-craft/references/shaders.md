# Effect shaders and particles: recipes for Godot 4

Which technique fits which job, and the Godot behaviour that bites. Cost rules and numbers are in [perf.md](perf.md). Sources are `[S#]` at the bottom; `[n]` refers to vfx.md's list.

## A baseline worth keeping

- **Procedural shapes, no textures.** A handful of shaders (shape, ink, puff, star, guard) draw the shape from a distance field and noise in the fragment shader. Nothing to load, no texture memory, crisp edges at any size.
- **Stepped alpha, not soft fades.** `ALPHA = step(t, field)` with `ALPHA_SCISSOR_THRESHOLD = 0.5`, then erode by raising `t` over life ("eats from the inside"). This is alpha erosion: the shape is the threshold field and age moves the threshold [S15].
- **Particle age from `INSTANCE_CUSTOM`.** Read `INSTANCE_CUSTOM.y` as life phase (0 to 1) and `.x` as angle. Script-driven meshes pass an `age` uniform instead (a `particle_age` switch), so one shader serves both.
- **`unshaded` + `shadows_disabled` + `cast_shadow = OFF`** on every effect mesh and emitter. Audit for zero shadow-casting effect nodes.

## Which technique for which job

| Job | Use | Why / cost |
| --- | --- | --- |
| Hit marks, rings, shards, slashes, star bursts | Procedural shape shader on a quad or particle | Crisp at 30–60 px, one shader for many looks, no texture. ALU per pixel, so keep the quad tight |
| Ink and smoke puffs, clods, drips | Procedural lump, alpha-eroded by age | Stays toon (stepped edge). A 6–8 frame grayscale flipbook is the next step if you want hand-drawn texture |
| Hand-drawn texture | Flipbook: `StandardMaterial3D` `billboard_mode = BILLBOARD_PARTICLES` with `particles_anim_h_frames` / `_v_frames` / `_loop`, frame speed from the process material's animation settings [S9] | Draw in grayscale and colour in the shader through a ramp (`GradientTexture1D`, a gradient map) so one sheet serves both sides' palettes [S15]. Several masks in one RGBA texture (shape, erosion, noise) cost one sample |
| Moving surface (energy, ink flow) | UV scroll: `UV + TIME * speed` on a noise; distort the shape's UV by a second noise | Cheap. "Simple textures and UV-distortion make great stylized fire" [S15]. Captures repeat only with `--fixed-fps` |
| Shell or buff rim on a body | Fresnel `pow(1.0 - dot(NORMAL, VIEW), k)` | One line; on a body-sized mesh it costs that body's pixels again |
| Heat, shock, boss reveal | Screen distortion with `hint_screen_texture` | **Max strength only.** It makes the material transparent, sees only opaque things (the screen is copied before the transparent pass), and other screen-reading materials don't see it [S5]. If a post pass already reads a copy, a second reader means a second copy |
| Edge fade where an effect meets the floor | Soft particle: compare `FRAGCOORD.z` with `hint_depth_texture` (non-linear: convert with `INV_PROJECTION_MATRIX`) [S5] | Only for blended effects lying on the ground. A stepped style rarely needs it |
| Trails | `GPUParticles3D.trail_enabled` or a ribbon mesh | Forward+ and Mobile only [S21] |
| Per-unit flash or tint on a shared material | `instance uniform` + `set_instance_shader_parameter` | Up to 16 per shader, no textures; **not in particle shaders** (use `COLOR` or `INSTANCE_CUSTOM` there) [S10]. A shared material without it flashes every unit at once |

## Godot behaviour that bites

- **Alpha-scissor effects get the post-process ink line; blended ones don't.** Scissor (`ALPHA_SCISSOR_THRESHOLD`) is drawn in the opaque path and writes depth and normals, so an edge-detect post pass can draw ink at its edges [S9]. Blended surfaces (`ALPHA` without a threshold, `blend_add`, `depth_draw_never`) don't write depth or normals: no post ink line, no SSR [S6]. A blended effect needs its own rim in the shader (1–2 px dark band, vfx.md "Readable on a dark board"). Decide per effect and check one frame at battle size for doubled or missing lines.
- **Blended draws are the slowest and sorted back to front.** `TRANSPARENCY_ALPHA` is "the slowest to render"; alpha hash and scissor are cheaper; unshaded is the fastest shading mode [S9]. Transparent objects can't be batched or instanced and every layer is drawn even when covered [S7, S8].
- **`amount_ratio` saves nothing.** Buffers are allocated and processed for the full `amount`; the ratio only emits fewer [S2]. Scaling strength with `amount_ratio` is fine for the look, but the cost is `amount`. Size `amount` to the strongest use, never "plenty". Changing `amount` restarts the system [S2].
- **`visibility_aabb` culls GPU particles.** Default `AABB(-4,-4,-4, 8,8,8)`; grow it when particles pop at the screen edge, never set it huge to be safe [S2].
- **`preprocess`** "can be very expensive … can even lead to a GPU crash" [S2]. Don't use it on battle effects.
- **`fixed_fps` default 30 with `interpolate` on** [S2]. Keep it. Higher costs more process work; lower looks choppy at ×2.
- **GPU or CPU particles.** GPU particles scale to "hundreds of thousands"; CPU particles are slower per particle [S1]. At tens to hundreds either is cheap; stay on `GPUParticles3D` for one code path and take `CPUParticles3D` only if a GPU emitter shows up in a GPU profile for a handful of particles.
- **Material overrides compile when first drawn.** Mesh-step precompilation can't cover node-level material overrides [S4], and effects often build materials in code. The documented fix: instantiate the effect once, hidden or off-camera, while the level opens. See perf.md "Shader compile stutter".
- **The debug overdraw view ignores custom shaders.** `Viewport.DEBUG_DRAW_OVERDRAW` draws every mesh with one additive material (`ALBEDO 0.4, 0.8, 0.8`, `ALPHA 0.1`, `blend_add`) [S11], so a quad counts whole even where the shader discards. That is the fill the GPU pays for; `capture.py overdraw` reads it.

## Readability at battle size

- **Sizes.** Measure your unit height on screen. Example: a unit about 190 px tall at 1080p (about 127 px at 720p) puts a weak hit in a 30–60 px box, and anything finer than 2 px flickers under a post ink pass.
- **Primary vs secondary.** Riot's style guide: the gameplay-carrying element has a high value range, strong contrast, a clear silhouette, high opacity and strong motion; secondary elements are darker, smaller, softer, fainter and calmer [S16]. The contact flash and shape are primary; chips, smoke and embers are secondary and never brighter than the hero.
- **Noise adds up in a crowd.** "Visual noise adds up quickly … in teamfights"; big gameplay effects may be noisy, small ones may not [S17]. "Gameplay readability will always prevail over thematic resonance" [S18]. That's the strength ladder: weak effects stay small and quiet so strong ones read.
- **Value first.** The gray check (SKILL.md step 4) and the brightness order (heroes > enemies = background) hold for every effect.

## Other public agent skills checked

- `gamedev-skills/awesome-gamedev-agent-skills` `godot-shaders` [S19]: `source_color`, `hint_range`, `hint_screen_texture` uniforms. Correct but generic.
- `majiayu000/claude-skill-registry` `godot-convert-shaders` [S20]: its table turns `varying` into `variable`, which is **wrong for Godot 4** (the shading doc still uses `varying`). Don't follow it.

## Sources

- S1 Godot docs, Particle systems (3D): https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html
- S2 Godot class GPUParticles3D (`amount_ratio`, `visibility_aabb`, `preprocess`, `fixed_fps`, `draw_order`): https://docs.godotengine.org/en/stable/classes/class_gpuparticles3d.html
- S4 Godot docs, Reducing stutter from shader (pipeline) compilations: https://docs.godotengine.org/en/stable/tutorials/performance/pipeline_compilations.html
- S5 Godot docs, Screen-reading shaders: https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html
- S6 Godot docs, Environment and post-processing (transparent materials not in SSR, they don't write depth): https://docs.godotengine.org/en/stable/tutorials/3d/environment_and_post_processing.html
- S7 Godot docs, Optimizing 3D performance: https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html
- S8 Godot docs, GPU optimization (transparency and fill rate): https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html
- S9 Godot class BaseMaterial3D (transparency and shading modes, particle animation frames): https://docs.godotengine.org/en/stable/classes/class_basematerial3d.html
- S10 Godot docs, Shading language: per-instance uniforms (16, not in particle shaders): https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
- S11 Godot class Viewport `debug_draw`; overdraw shader in `servers/rendering/renderer_rd/forward_clustered/scene_shader_forward_clustered.cpp` (engine source)
- S12 Emil Persson, Particle trimming (2009-06-02): https://humus.name/index.php?ID=266
- S13 Emil Persson, Graphics Gems for Games: Findings from Avalanche Studios: https://humus.name/Articles/Persson_GraphicsGemsForGames.pdf
- S14 Epic, Viewport modes (Shader Complexity, Quad Overdraw): https://dev.epicgames.com/documentation/en-us/unreal-engine/viewport-modes-in-unreal-engine
- S15 Simon Trümpler, Stylized VFX in RiME (2017-06-07): https://simonschreibt.de/gat/stylized-vfx-in-rime/ · Unreal Fest Europe 2018 talk page: https://www.unrealengine.com/events/unreal-fest-europe-2018/stylized-vfx-in-rime
- S16 Riot, League's VFX Style Guide (2017-10) and its PDF (primary/secondary elements): https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/
- S17 Riot, Clarity in League (2021-03-12): https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/
- S18 Riot, Behind the Scenes of VFX Updates (2022-04-25): https://www.leagueoflegends.com/en-us/news/dev/dev-behind-the-scenes-of-vfx-updates/
- S19 gamedev-skills, godot-shaders SKILL.md: https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/main/skills/godot/godot-shaders/SKILL.md
- S20 majiayu000, godot-convert-shaders SKILL.md: https://github.com/majiayu000/claude-skill-registry/blob/main/skills/data/godot-convert-shaders/SKILL.md
- S21 Godot docs, Particle trails: https://docs.godotengine.org/en/stable/tutorials/3d/particles/trails.html
