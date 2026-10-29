# Game-ready clips: rig intake, weights, export, cost, seams, feet

What a clip must survive between the approved Blender look and the Godot battle: the rig it sits on, the glTF exporter, Godot's importer, and many copies on one board. Measured with Blender 5.2 and Godot 4.7 on an Apple M4.

Labels: **[official]** engine or tool docs or source, checked · **[measured]** measured on test figures · **[talk]** conference talk · **[practitioner]** one team or person · **[proposal]** a suggested number; agree it with the project owner.

## 1. Rig intake: every new body, before any motion

Three ways a body arrives. All end on the same check (char-anim step 0, and the forearm range-of-motion test in `blender-anim`).

| Source | Skeleton as delivered | What to do |
| --- | --- | --- |
| Meshy auto-rig | 24 bones, no jaw or twist bones | Per-body rig fix, forearm twist bones, mouth rig if the mouth opens |
| Tripo `anim rig --spec mixamo` | 65 `mixamorig:*` bones with fingers | Fold fingers and toe ends into hand and toe, rename to your one naming (24 bones); add a parent root node for turn and scale; then the same checks |
| Mixamo auto-rig | Mixamo names, fingers | Same fold as Tripo |

- 🔴 Fold first, check second. Every check script should read body parts by one naming.
- 🔴 Turn and scale on a parent root node, never on the armature object: the sampled clip overwrites the armature transform on export [measured].
- Bones no vertex uses: list them with the clip audit. Keep one only when it parents something (for example the bones of an arm that a monster part replaced). Otherwise fold or delete it before motion work.
- Godot shares clips between bodies only where bone rests match, not by names alone [official: "Retargeting 3D Skeletons"]. Use one rig per family of characters, not per character.
- Godot's own retarget (BoneMap, SkeletonProfileHumanoid, Rest Fixer) isn't used here: its "Overwrite Axis" "can produce horrible results if the original Bone Rest set externally is important", and "Fix Silhouette" is for A-pose bodies [official: same page]. Retarget in Blender and ship baked clips.

## 2. Weights

- 🔴 **Four influences, normalised, before any render a human sees.** Blender's glTF exporter writes `Bone Influences = 4` by default with `Include All Bone Influences` off ("Allow more than 4 joint vertex influences. Models may appear incorrectly in many viewers") [official: Blender exporter properties]. Godot imports 4 by default ("4 Influences (Compatible)"; "All Influences" up to 8) [official: Godot import configuration]. A body painted with 5+ deforms one way in Blender and another in the game. On the body mesh: `bpy.ops.object.vertex_group_limit_total(limit=4)`, then `vertex_group_normalize_all(lock_active=False)`, then render.
- The clip audit reads the exported glb: vertices over 4 influences must be 0 and `JOINTS_1` absent; weight sum error under 0.001.
- Removing weights in a script: collect group indices first (`[g.group for g in v.groups]`), then remove. Removing while iterating skips some.
- **Automatic weights fail** ("Bone Heat Weighting: failed to find solution for one or more bones") on generated meshes. Check in this order [practitioner: blender.stackexchange 15964, 264383]:
  1. overlapping or duplicate vertices → Merge by Distance;
  2. separate intersecting pieces (straps, hair, cloth flaps) → split by linked geometry (`L`, then Separate Selection), weight each, join;
  3. inside-out or non-manifold faces → fix normals or delete;
  4. still failing → weight a remeshed or decimated proxy, then copy to the real body with a Data Transfer modifier (Vertex Data → Vertex Groups, Nearest Vertex, Generate Data Layers, apply).
- Smooth a seam by **space**, not by mesh edges, when pieces float apart.

## 3. Export (Blender glTF exporter, option names from bpy)

| Option (`export_*`) | Default | Use | Why |
| --- | --- | --- | --- |
| Always Sample Animations (`force_sampling`) | True | True | Constraints, IK and springs only reach the glb as sampled keys |
| Sampling Rate (`frame_step`) | 1 | 1 | One key per 24 fps frame |
| Optimize Animation Size | True | True | Drops repeated keys (an idle had 78 of 99 channels constant) |
| Export Deformation Bones Only (`def_bones`) | False | True when the rig has control or IK bones | Control bones never reach the game; needs sampling on |
| Bone Influences / Include All | 4 / False | 4 / False | See section 2 |
| Reset Pose Bones Between Actions | True | True | A bone unkeyed in one clip would keep the last clip's pose |
| Set All glTF Animation Starting at 0 (`anim_slide_to_zero`) | False | Keep consistent per family | Clips starting at frame 1 start at 1/24 s; read hit seconds from the glb, never convert frame numbers by hand |
| Bake All Objects Animations | False | False | Object-animated bits (flecks) are already keyed |

- Flatten every non-human chain that uses `inherit_scale = NONE` to the root bone before export (`blender-anim` section 4).

## 4. Godot import: keep the authored frames

- Godot's scene importer **bakes every track at the import `animation/fps`** and plays linearly between those keys [official: import configuration "FPS", "baking animation curves to a series of points with linear interpolation"; measured: imported tracks keyed at multiples of 1/30 s].
- 24 fps clips imported at the default 30 lose 3 of every 4 authored frames, and a one-frame snap is cut [measured: an upper arm 9.3 degrees off at the slam frame, hips 21 mm; Godot's sampled value matched the audit model to 4 decimals]. Object-animated bits suffer too: flecks that pop into place were 24 to 34 cm off on resampled frames.
- **[proposal]** Import every character glb at `animation/fps = 24`: the same keys as authored, 20% fewer than at 30. Until then, report the resample loss at the contact frame with every attack.
- `Remove Immutable Tracks` on (default) and `Trimming` off: a held start or end pose is part of the acting [official].
- **Compression:** `Animation.compress(page_size=8192, fps=120, split_tolerance=4.0)` exists. Clips of 30 to 150 KB don't need it; it trades exactness for memory. **[proposal]**
- **Mesh LOD:** Godot generates LODs for every imported glTF by default (`generate_lods=true`) and warns it "may occasionally introduce rendering issues (especially in skinned meshes)" [official: "Mesh level of detail"]. At about 127 px tall the low LODs are what shows. Check a character at the battle camera with LOD on and off before a body is final.
- **AnimationTree:** for a deterministic sim, drive one `AnimationPlayer` per figure with `callback_mode_process = MANUAL` and call `advance()` from the fight's playback clock. No AnimationTree and no root motion: the sim places the unit, the clip stays in place. An AnimationTree buys blend spaces a fixed-camera battler rarely needs [official: AnimationMixer docs].

## 5. Cost on the board

Measured on Apple M4, Godot 4.7:

- Animation CPU: `AnimationPlayer.advance` costs 9 µs (33 joints, idle) to 30 µs (37 extra object tracks, attack) per figure per frame; 16 figures take 0.14 to 0.48 ms of a 16.6 ms frame.
- GPU: one fight drew 887k primitives, 164k with units hidden; units were 81% of primitives and 83% of shadow primitives. GPU time with units on and off stayed within run-to-run noise. The cost is in triangles and passes, not bones; triangle budgets belong to `char-3d-source` and `art-craft`.
- **[proposal] bone budget per figure:** body ≤ 32 deform bones (24 + 6 twist + jaw + 1 prop), each non-human part rig ≤ 16, whole figure ≤ 48 joints; no finger bones; 4 influences.
- **[proposal] key rate:** 24 fps from Blender to the game, one key per frame, sampled.

## 6. Loops and planted feet (the clip audit)

```
clip_audit <idle.glb> <walk.glb> --loop        # seams and feet
clip_audit <attack.glb> --hit=<contact frame>  # resample loss at contact
```

Build the audit to read the glb itself (pure Python and the glTF JSON is enough), so it measures what the game receives.

- **Seam:** world-space jump of hips, head, hands and feet across the wrap, in mm and as a multiple of a normal frame step. A clip that repeats its first frame at the end shows about 0×; one that doesn't shows about 1× (both fine in Godot); well above 1× pops every cycle.
  - **[proposal] gate:** every watched point ≤ 15 mm (about 1 px on a 1.85 m figure drawn 127 px tall) **or** ≤ 1.5× its normal step.
  - Seen: a walk's foot jumping 209 mm (2.9×), a limp walk 105 mm (3.1×), a walk's head 43 mm (4.1×).
- **Planted-foot drift:** a foot counts as planted while within 2 cm of its lowest point in the clip. Per planted run, report drift (mm) and speed (m/s). This catches slow creep that a 2 cm-per-frame slide check and NVIDIA Kimodo's skate rule (toe under 5 cm moving faster than 0.2 m/s [official: Kimodo metrics]) both miss.
  - **[proposal] gate:** idles and holds ≤ 10 mm drift. In-place walks: a steady treadmill speed, which sets the unit's move speed within a 0.8 to 1.2× play range.
  - Seen: hero idles creeping 62 to 92 mm; a Tripo preset idle 243 to 261 mm; hand-built enemy idles 0 mm.
- Contact thresholds in the retargeting literature: toe contact at ≤ 3 cm height and ≤ 1 cm step on a 180 cm body [paper: Villegas et al. 2021, arXiv 2109.07431]. 2 cm by height alone is a detection setting, not a standard.

## 7. Attacks that read at about 127 px

The acting rules are in craft.md; these are what the game does to the clip.

- If the game plays an attack at `length / interval` up to 2× and starts it later rather than faster, every anticipation frame is half as long on screen at 2×. Write anticipation time **after** the rate into the clip contract: (contact − anticipation start) ÷ 24 ÷ rate.
- Anticipation gives a move "contrast, help it read and give it power even if it's short"; one frame of anticipation helped a six-frame move [talk: Skullgirls, GDC "Fluid and Powerful Animation", 2D at 60 fps].
- Overshoot "one frame" past the final key, then pull back; hold the impact pose (hitstop), since "impacts tend to look watery or weak without it" [talk: same]. Let the game own hitstop (pause playback) and the clip own the one-frame overshoot.
- Leave or enter idle with **bigger spacing around the idle pose** instead of a slow ease [talk: same], so a 0.15 s crossfade doesn't float.
- A one-frame snap survives only if the game samples that frame: section 4.

## 8. Non-human parts in the game

- A chain is bone keys in the glb, baked every frame. **[proposal]** ≤ 16 bones per part rig (5 to 10 is typical).
- Things that appear or vanish (flecks, drops): key their scale to 0 or use a step key at the jump. A linear key that teleports draws a streak once the importer resamples.
- Godot 4.7 has `SpringBoneSimulator3D` (hair, cloth, tails; no branched chains; keep the skeleton unscaled) [official: class docs]. Authored secondary motion approved in Blender and baked is safer: a runtime spring changes with frame rate and with 2× playback, so it no longer matches what was approved. **[proposal]**

## Sources

- Godot import configuration (FPS, trimming, immutable tracks, skins 4/8): https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html
- Godot mesh LOD: https://docs.godotengine.org/en/stable/tutorials/3d/mesh_lod.html
- Godot AnimationMixer (callback modes): https://docs.godotengine.org/en/stable/classes/class_animationmixer.html
- Godot retargeting 3D skeletons: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html
- Godot SpringBoneSimulator3D: https://docs.godotengine.org/en/stable/classes/class_springbonesimulator3d.html
- Blender glTF exporter source (option names, defaults): https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/addons/io_scene_gltf2/__init__.py ; manual 3.5: https://docs.blender.org/manual/en/3.5/addons/import_export/scene_gltf2.html ; defaults re-read with `bpy.ops.export_scene.gltf.get_rna_type()`
- Bone heat failures: https://blender.stackexchange.com/questions/15964 · https://blender.stackexchange.com/questions/264383
- Skullgirls, GDC Animation Bootcamp: https://www.gdcvault.com/play/1020575/Animation-Bootcamp-Fluid-and-Powerful · video https://www.youtube.com/watch?v=Mw0h9WmBlsw
- NVIDIA Kimodo benchmark metrics (foot skate): https://research.nvidia.com/labs/sil/projects/kimodo/docs/benchmark/metrics.html
- Contact-aware retargeting: https://arxiv.org/abs/2109.07431
- Other engines' defaults, for comparison: Unity "Standard (4 Bones)… recommended for performance" https://docs.unity3d.com/Manual/FBXImporter-Rig.html ; Unity "15 additional bones on a 30-bone rig = 50% more operations (Generic)" https://docs.unity.com/en-us/engine/6000.7/manual/assets-and-media/asset-types/models/creating-dccassets/modeling-optimized-characters ; ACL default error 0.01 cm https://github.com/nfrechette/acl/blob/develop/docs/compressing_raw_tracks.md
