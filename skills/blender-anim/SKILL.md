---
name: blender-anim
description: Manual for an agent building rigs, animation and non-human monster parts directly in Blender, through Blender MCP or headless `blender -b` scripts. Covers keeping body and monster-part rigs separate, keyframing with per-channel lag and springs, mass-spring chains for tentacles and shadow limbs, scripted part meshes, the render-measure-fix loop, forearm twist and palm roll, glTF export and the quality gate. Use when making or fixing an animation or rig in Blender, when a monster has non-human parts (shadow, tentacle, extra arms), when exporting a rig and its clips to glb, or when motion looks stiff, floaty or the mesh tears.
license: MIT
---

# Blender animation manual: the agent builds it end to end

A living document: add a line to [references/log.md](references/log.md) after every review, and edit the section when a rule changes.

**Why this path:** non-human parts (shadow limbs, tentacles, a giant's looming shadow) can't come from preset libraries, text-to-motion or video mocap. An agent that rigs, animates, renders and fixes in Blender has no such limit. Base motion for humanoid heroes (walk, idle, hit) can come from Mixamo; see the path table in the `char-anim` skill.

**Running Blender:** use Blender MCP if it's connected. Otherwise write a script and run `blender -b -P <script.py> -- <args>`. Keep every final result as a script that rebuilds it plus the exported glb.

This skill assumes the helpers described in `char-anim` (keyframe helper, motion QA, clip audit, silhouette overlay, sheets). Below, the per-enemy build script is `<enemy>.py`, built on a shared engine module with `Chain`, `Flecks`, mesh builders and a `review` script.

## 1. Body and monster part are never joined (the most important rule)

🔴 Don't connect the monster part's rig to the character's rig. Joined rigs tear the body mesh in motion. Build **two separate meshes that move together in one clip.**

- **Body** = the auto-rigged figure as delivered (don't touch its bones or weights). If the monster part came attached, detach those faces.
- **Monster part** = a separate object with its own armature (`new_rig`, `rig_bone`, `skin_to`). Every frame, set its object transform to **how far one body bone (usually Spine) has moved from rest**, and key it (`part_rig.matrix_world = spine_delta(body_rig)`). Don't parent it.
- On export there are two objects (body, part), and both actions' keys merge into one clip (`Animation`); the game plays that one clip and both move on the same frame. One glb per clip; a loop is cut to one cycle that joins its first pose.
- The gap where the part was detached: generated meshes are split at every UV seam, so `holes_fill` fills nothing. **Build a plug blob from the gap's border points and attach it to the part object** (`new_boundary_points` → `ink_blob`).
- Choosing faces to detach: position rules + **texture colour** (faces painted the part's colour, `face_colors`) + **floating crumbs** (small islands left on the body, `crumb`). Protect arm and head flesh with `keep`.

## 2. Acting first: what and why

1. Read the character's design doc: core action, tell, three habits, three mood words.
2. One **acting paragraph** per clip: who, what, in what mood, how it ends. Put it at the top of the build script.
3. 🔴 **For monsters, the part leads and the person is dragged** (like the marionette motion of the Clickers in The Last of Us). On an attack the shadow rises and pulls him back, then slams and drags him forward with its weight. In numbers, the fastest frame comes **shadow → body → hand** in that order (for example 30 → 31 → 34).
4. Keep feedback that changed the acting in the note.
5. 🔴 **Reference first:** before blocking, find real reference as in `char-anim` "Reference first". For monster parts, measure timing, arc and weight from video of the nearest real thing (a zombie arm swing, a whip, an octopus arm).

## 3. Body: key poses plus per-channel lag

Engine = the keyframe helper's `Track`, `pose_frame`, `Spring`. Treat it as shared: subclass or wrap it rather than editing it for one enemy.

- Keys are **world-space targets**: hands (IK), feet (x, y, heel angle), hips (m), torso, chest, head (degrees). The figure faces -Y; its left is +X.
- 🔴 **Don't set a child bone's world rotation straight from the rest pose.** Ignoring the parent lets joints go past their range (a kneel folded the foot more than 100 degrees under the shin). Give limb angles relative to the parent bone.
- Leg IK on new clips: align the thigh roll to the knee's bend plane (a hinge mode). Elbows get bend amount only; auto-rigged bodies don't know which way the elbow's inside faces.
- Key types: `flow` (passes through; most keys), `stop` (a real hold: anticipation peak, brace), `hit` (stops dead at incoming speed).
- `drag` = per-channel lag (hips 0 → chest 1 → head and hands 2 to 3 frames). The centre leads, the ends follow.
- `springs` = chest, head and wrists follow late, overshoot and settle. **Turn the chest spring off for whole-body falls** (`"Spine": None`); left on, the back lagged, sagged and went through the floor.
- `alive` = breath and drift on held poses. A tired body breathes big (`breath 3.0`).
- To fall with a straight back, put the lean on the hips (`body_share = (0.78, 0.10, 0.06, 0.06)`).
- Loops like walks use a procedural track that overrides `Track.sample` (`WalkTrack`): the planted foot slides straight under the body (in place), the lifted foot drags low, the body sways right after contact.
- Floor guard (`floor_lift`): raise the hips by however far torso or leg flesh goes through the floor, then **solve again** (leg IK re-grabs the feet). 🔴 **Don't count the arms;** one arm touching the floor lifted the whole body.

## 4. Monster parts: physics with mass

- **Masses, stalks, tentacles** = `Chain` (a chain of mass particles). The root is pinned to the body; the other segments follow a target curve late on springs, sag under gravity and collide with the floor. Give each segment its own allowed `stretch`.
- **A `gain` channel creates weight.** Lower the pull during the swing over (0.45) to leave it to inertia and gravity; raise it to hold (0.9 to 1.2). The swing looks like weight falling, not a hand dragging it.
- Target curve = a quadratic Bézier from root through a control point (raised by `arc`) to the tip. A tip that touched the floor is **pinned in world space** (the fist stays put even as the body is dragged).
- At contact: `Chain.hit` (floor contact speed) kicks a squash spring (the mass squashes and spreads), ink spreads (`puddle`), and flecks scatter (`Flecks.emit`).
- Loads and masses lag the body (rotation slowed with `Spring(2.0, 0.32)`), so they sway when walking.
- New bones get **`inherit_scale = NONE`**; otherwise a stretched parent's scale spreads to the children and the chain shoots to several metres.
  - 🔴 glTF doesn't know this setting. Exported as is, stalks and fists fly thousands of metres in Godot. Right before export, reparent every segment to the root bone and re-key each frame at the same world place (`flatten_rig`).
- Tube bones stretch along their length only, thickness separately (`pose_tube(…, thick)`). For a rope that thins as it stretches, `pose_rope(thin)`.
- **Under 16 bones per part rig (proposal).** Working examples used 5, 9 and 10. Four bones per vertex (`char-anim` step 0).
- **Things that appear and vanish** (flecks, drops): key their scale to 0, or use a step key at the jump. A linear key that teleports smears into a streak when the game resamples frames (flecks were 24 to 34 cm off).
- Use Blender's Spline IK, constraints and springs as building tools, then bake to bone keys every frame. Avoid Godot's runtime `SpringBoneSimulator3D` for approved motion; it changes with frame rate and 2× playback, so it drifts from what was approved ([game-ready](../char-anim/references/game-ready.md) section 8).

## 5. Monster part meshes: build them by script

Organic bodies (people, heroes) come from a 3D generator (`char-3d-source`), hard-surface objects from a Blender script kit. **Shadows, tentacles and fists are built by script** because they must be designed together with their bones and motion.

- `club(…, profile, wobble)` = a tube rising along a thickness curve: thick where it leaves the body, narrowing like a wrist.
- `ink_blob(radius, lobes, wobble)` = a noisy sphere plus lumps (knuckles, fist). Keep the end mass (fist) a **separate mesh** on the end bone; one continuous tube stretches the fist along with the stalk.
- Style example (an ink-and-shadow horror look): no outline on the shadow part (`no_ink_lines`), a rippled edge (`wobble` 0.35 to 0.45), flecks breaking off on swings and impacts; only the human side gets a closed heavy outline. Take the rules from your own art bible.
- Reuse the body's existing unlit black material for the part. Give new meshes one UV layer (`uv_layers.new`); without it they rendered white in previews.

## 6. Build, look, fix

```
blender -b -P <enemy>.py -- <clip> <tmp>             # fast pass: workbench, 360 px, ~10 s
python3 review.py <tmp>/<clip>                       # strip, arc plate, gif, numbers
blender -b -P motion_qa.py -- <clip.glb> <tmp>/qa --render     # defect gate
python3 clip_audit.py <clip.glb> [--loop | --hit=<contact frame>]   # seams, planted feet, bones, resample loss
blender -b -P <enemy>.py -- <clip> <tmp> final       # final: toon + outlines, 560 px, ~3 min
```

1. **Pose stills first.** For a new part or rig, render a few poses without motion (for example swing angles 0, 50, 110) from the side and battle cameras. Rig flaws all show here (a load stretching like a plank, the body tearing).
2. **Fast pass, then look yourself.** Open the strip (`strip-*.jpg`) and zoomed frames around contact. Don't trust numbers alone.
3. **Filter with numbers** (`critic.txt`): dead holds (nothing moves for more than 12 frames), constant speed (speed variation under 0.25), the first accelerating frame, the order of fastest frames. Then the motion QA defect gate: zero gross defects, or one line each for the ones you keep.
4. **Fix one thing at a time,** then repeat 1 to 3. If something is suspicious, open the saved `.blend` and print bone positions or the mesh's lowest point.
5. **Final, then show the human:** battle camera, game size (0.45×) and side, side by side, per clip.

## 6½. Rig check: first use of a humanoid body, or stiff motion and odd hands

🔴 **Moving the hand doesn't set the palm.** Two-bone IK sets the wrist position and leaves the roll around the forearm free. Auto-rigged bodies are often sculpted palms forward, so without a roll every clip shows palms facing forward or out. A human's hanging arm turns inward so the palm faces the thigh.

- **Palm roll = `rollL`/`rollR` channels** (degrees, + = pronate toward the body). A ready pose needed about 80. Change it per key when the arm reaches or rises. Don't roll the whole forearm (the elbow twists); rotate the hand around the forearm axis.
- **Three twist bones:** at 1/3, 2/3 and the wrist along the forearm, sharing the hand's swing-twist around the forearm axis at 1/3, 2/3 and 1. Without them the wrist pinches like a candy wrapper. Add them when binding the body, apply them every frame from the keyframe helper, and bake them into preset clips. They're keys, not constraints, so they survive glTF and Godot.
- 🔴 **Don't trust the local axes of bones imported from glTF.** Measure forearm direction from head positions (wrist − elbow). Blender's Copy Rotation has no swing-twist mode.
- 🔴 **`for g in v.groups: remove(...)` skips some groups.** Collect indices first (`[g.group for g in v.groups]`), then remove. This bug left half the forearm weight in place and stretched the flesh 13×.
- **Range-of-motion sheet:** a script that renders and measures hanging arms (roll 0 and 80), elbow bend, full pronation (150), full supination (−60) and a raised, twisted arm from front, battle camera and close on the arm.

| Measure | Meaning | Pass |
| --- | --- | --- |
| `palm_in` | How much the palm faces the body's midline | Over 0.5 with hanging arm at roll 80 |
| `wrap` | How much wrist girth shrinks from rest | Under 0.05 (full pronation included) |
| `stretch` | Largest stretch factor of an arm mesh edge | No larger than on the unfixed body |

On a new body, run it on the body before and after the fix, compare the tables side by side, and look at the close arm renders yourself.

## 6¾. Export: the same shape in the game

- Blender glTF export: Always Sample Animations on, Sampling Rate 1, Optimize Animation Size on, Export Deformation Bones Only on if there are control bones, Bone Influences 4, Include All Bone Influences off, Reset Pose Bones Between Actions on. Reasons: [game-ready](../char-anim/references/game-ready.md) section 3.
- Run the clip audit on every exported glb: zero vertices over four bones, unused bones checked, loop seams, planted-foot drift on idles (`char-anim` "Into the game").

## 7. Quality gate: before showing

- [ ] Passed `char-anim` "Into the game": seams and foot drift within the gate, or one line each for exceptions; attacks list their resample loss at contact.
- [ ] Passed `char-anim` "Defect gate": zero gross defects (or one line each); polished clips overlaid on the approved blocking, with the changed area noted.
- [ ] A same-speed reference is attached, with a reason for every difference.
- [ ] The acting paragraph reads on screen; two of the three mood words show in the body.
- [ ] At game size, anticipation, contact and recovery are three clearly different silhouettes.
- [ ] The monster part leads and the body is dragged (fastest-frame order).
- [ ] No tearing or stretching: skull base, armpits, back (where the part was detached).
- [ ] Palms face as the action means: hanging arms toward the body, no pinched wrist (6½).
- [ ] Torso and legs don't go through the floor; legs don't crumple (planted feet on the floor, knees bending the right way).
- [ ] No fully frozen stretch over 0.5 s (idle breath and drift).
- [ ] End pose matches the start pose (joins the idle). Walks are in place.
- [ ] Art bible rules hold (for example: no outline on shadow parts, no warm colours on them, never the back to the battle camera for more than 0.5 s).
