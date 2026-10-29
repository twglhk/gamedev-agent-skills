---
name: char-anim
description: Makes character and monster animation that feels alive and in character, from rig check to key-pose blocking, keyframe in-betweening, Mixamo base clips for humanoid heroes, render-and-fix loops, defect and quality gates, and game-ready glb export. Use when bringing in a Mixamo clip; when making or fixing any character or monster animation (attack, idle, hit, death, skill, roar, victory, tentacles); when a clip goes into the game (rig intake from Meshy/Tripo/Mixamo, weights, glTF export, Godot import, loop seams, foot drift, bone budget); or when motion looks stiff, robotic, floaty or lifeless.
license: MIT
---

# Character animation: motion that is alive and belongs to the character

Motion is acting. "The arm comes down" is not enough; the clip has to show who strikes, why, and in what mood. The bar: personality plus dynamism, nothing stiff or idle from head to toe.

Craft knowledge (acting, posing, timing, game animation, with sources) is in [references/craft.md](references/craft.md). Read it before writing an acting note and before showing poses.

This skill assumes these project helpers. Build or swap in your own; each is described by what it must do.
- **Keyframe helper** (Python on `bpy`): per-channel interpolation; key types `flow` (passes through), `stop` (a real hold) and `hit` (stops dead at incoming speed); per-channel `drag` in frames; damped `springs` on chest, head and wrists; two-bone IK for hands and feet with pole targets; planted feet; `squash`/`stretch` with volume kept. Keys are world-space targets.
- **Retarget script**: moves a mocap clip onto your body with hip-joint-based root motion, rest-pose matching per limb, a face turn offset, and IK-locked planted feet. Has a `preflight` (proportion and rest-pose differences) and a `qa` (did slide or floor penetration get worse than the source).
- **Mixamo intake script**: renames `mixamorig:*` bones to your body's naming and folds fingers and toe ends into hand and foot.
- **Motion QA script**: per clip, counts gross defects (limbs through body or floor, foot slide over 2 cm per frame, hands buried in thighs) and renders check views (left side blue, right side red, 25 cm checker floor; front, left, top, battle camera).
- **Clip audit script**: reads the exported glb and reports loop seams, planted-foot drift, bones per vertex, unused bones, and the pose loss at a given frame when the engine resamples.
- **Silhouette overlay script**: black silhouettes of two clips (or a concept and a unit) at battle camera and game size, and the changed area per key frame.
- **Sheets script**: from rendered frames makes the battle-camera gif, a game-size gif, a side gif, a frame strip and an arc plate (dots per frame for hands, head and hips; wider gaps mean faster).

Coordinates below: the figure faces -Y and its left is +X.

## Which path

| What | Path | Cost |
| --- | --- | --- |
| 🔴 Motion that belongs to this character: signature skill, attacks, roars, habits, victory, and everything non-human (monster parts, shadows, tentacles) | **Build it in Blender** (below). The human picks key poses first, the agent connects them, renders and fixes | Free, takes time |
| Base motion for humanoid heroes (walk, idle, hit) | **Mixamo**, then polish in Blender. A clip that fails the gate is built by hand | Free |
| Fallback | Library presets and text-to-motion from Meshy or similar ([references/text-to-motion.md](references/text-to-motion.md)). Most text-to-motion output gets rejected | Credits |

- Building by hand works. Earlier hand-keyed attacks were rejected because of the order of work, not the method: nobody looked until everything was built, poses weren't agreed first, and it was baked in one go without renders.
- 🔴 **Retargeting bought mocap onto another body:** use only the retarget script. Read `preflight` first, take only the stretch of the source that matches the acting note, and key the rest. Never play the source to the end and layer a different pose (lying down, a hand on the floor) on top; that wrecked a fall clip. Run `qa` before handing it on.
- 🔴 Before any generation that costs credits, say how many and roughly how much.

## Mixamo base clips (humanoid heroes only)

Mixamo is free with an Adobe account and allowed in commercial games.

- **Fine to take:** walk, idle, hit for human-shaped heroes.
- **Can't do, so build by hand:** signature skills, attacks, roars, habits, victory poses; every enemy and monster; non-human parts (shadow arms, tentacles, four legs). Mixamo auto-rig and clips are two-legged human skeletons without jaw or twist bones. There's no standing overhead slam either; the nearest (Mutant Jump Attack) leaves its tile and reads as a jump.
- 🔴 **Gate: a clip that fails any check is dropped and built by hand.**
  - View at the battle camera and game size. Drop it if a small head sinks behind the shoulders (a breathing idle buried the head for the whole loop).
  - Drop it if the base motion erases the hero's personality. Mixamo moves are generic; walks fit best, idles are seen longest and get judged hardest. If another hero already uses the clip, put the two side by side and check they don't look alike.
  - Run the defect and quality gates below exactly as for hand-built clips. An in-place walk's slide count may be the treadmill step itself; confirm before you call it a defect.
- **Upload:** export the unrigged body as FBX, feet at z=0. Auto-rig markers on chin, wrists, elbows, knees, groin; symmetry on; Standard Skeleton. Download FBX, **With Skin**, 24 fps, Keyframe Reduction none; walks In Place. Keep FBX files under `<character>/motion/mixamo/`.
- **Move onto the body**, headless, in two steps: (1) intake script renames and folds bones (a retarget source only, never shipped); (2) retarget onto the fixed hero body (after the step-0 rig fix, with its face turn), key every frame, one action out. Read the preflight first.
- **Polish** as in "Touch-ups": a long arm's fist through the floor, body intersections, a few keys that bring back personality. Budget about half a day per clip.

## 0. The puppet first: rig check (once per new body, free)

- **Three ways a rig arrives:** Meshy auto-rig (24 bones), Tripo `--spec mixamo` (65 bones with fingers), Mixamo auto-rig. Fold and rename Tripo and Mixamo rigs to one naming **before** the checks below, so every check reads the same part names. Turn and scale on a parent root node, never the armature. Details: [references/game-ready.md](references/game-ready.md) section 1.
- **Four bones per vertex, sum 1.** glTF export and Godot import carry four influences per vertex by default. A body painted with five or more bends differently in Blender and in the game. Before any render a human sees: `vertex_group_limit_total(limit=4)` then `vertex_group_normalize_all`. If automatic weights fail (Bone Heat): merge by distance, separate loose pieces, then transfer from a proxy mesh (game-ready section 2).

🔴 **When motion looks wrong, suspect the rig before the prompt or the keys.** Auto-rigs are reliable on average bodies only; a small head, huge shoulders or long arms put bones and weights in the wrong place. On one figure the head bone's pivot sat 23 cm behind the head inside the trapezius, the neck bone owned no flesh, and the whole trapezius was bound to the shoulder bones, so the head tore like a wedge whenever it lifted.

- **Check:** a weight map coloured by each vertex's strongest bone (front, side, back) and a list of bone positions. Look at head and neck (does the neck own anything, is the head pivot at the skull base), trapezius and upper chest (do the shoulder bones eat it all), armpits.
- **Fix** with a per-character `fix_rig.py`: the head on the head bone alone, its base blended between head and neck, the middle of the trapezius moved to the chest bone. Move the head and neck pivots to the skull base without changing their direction. Smooth borders by **spatial distance**; Blender's default smoothing follows edges and tears apart floating straps, flaps and duplicate vertices.
- **Confirm** with the torn frame before and after, side by side. 🔴 Apply the same fix to every motion glb before rendering or handing it to the game.
- **Face direction:** put every bone at rest, render the face close from the front (-Y). Generated bodies are sometimes sculpted with the face turned (one came 40 degrees to his right). Measure the head turn that brings both eyes to the front (render turns from -40 to 40) and add it to the head turn of every clip.
- **Mouth:** auto-rigs have no jaw. If the mouth must open (roar, shout), add a thin face across the lip line with a dark MouthInside material, folded shut, and a shape key MouthOpen that drops the lower jaw on a hinge in front of the ears so that face stretches into the dark of the mouth. Measure lip height and face direction on that body. Dropping the jaw without the shape key gives a longer chin, not an open mouth.

## Building by hand in Blender

Build headless (`blender -b -P`, or Blender MCP if connected) and open every render yourself.

1. **Acting note.** One sentence per clip plus **goal, obstacle, action** (craft.md section 1), and which pose carries the anticipation, the hesitation, the strike, the overshoot, the hold and the end.
2. 🔴 **Reference first.** Before blocking, find at least one real reference and write it into `<character>/motion/reference.md`: source (film or game scene, mocap library entry, animation reference site), timestamp or frame, what you take from it (timing, arc, weight). For monster parts, find the nearest real thing (whip, octopus arm, wet cloth). No reference found means report it; don't block.
   - Data you may retarget: CMU, Mixamo, 100STYLE, your own library previews. **Watch only, never copy data or frames:** film and game scenes, and non-commercial datasets (AMASS, HumanML3D, LAFAN1, Bandai Namco, HY-Motion). Note which kind in `reference.md`.
   - When showing a blocking, attach the reference as a separate video at the **same speed** (24 fps) and write one line on where and why the result differs.
3. **Blocking at real speed first (free).** Never show a set of still poses; that reads as an art collection, with too few frames to judge. Thumbnails (acting note plus frames measured from the reference) → keys and breakdowns every 2 to 4 frames, two options (three at most) → score yourself with craft.md's scoring table and keep only what passes → show the human a battle-camera gif, a front gif and a game-size gif, separate key-frame stills, and the arc plate. Stand grey placeholder figures where neighbours really stand on the board so you can see the move works in place. The human picks.
   - The human may change the staging after seeing poses. Write the changed staging into the character's design doc first.
4. **Connect** the chosen poses with the keyframe helper. Timing template:
   - eyes lead (head about 5 frames ahead) → deep, slow anticipation (bend the knees, drop the hips more than 0.2 m, crouch) → a `stop` key that gathers force in a moving hold (breath and springs alive) → within **3 frames** a big `hit` key (unfold and burst, `squash`/`stretch` around 1.06) → a `flow` key that overshoots and returns → a `stop` hold → back to the ready pose.
   - `drag` handles joint order (hands 1, head 2, wrists 2 frames late); springs handle overshoot. Never land the whole body on the same frame.
   - **Charging tremble** (slow, then sudden): during the charge, lay small keys every 2 frames alternating left-right and up-down (about 6 Hz) with growing amplitude while the body sinks slowly; then `hit` in 2 frames. Speed the springs up to 7 to 9 Hz or the tremble smears. A tremble under 1 px at game size is invisible, so check the game-size gif.
   - Hands are world targets for the wrist (m), the pole sets the elbow direction. Keep a list at the top of `<character>/motion/notes.md` of poses this body can't do (for example: fist no higher than the head, no big back arch).
5. **Effects for viewing (if the effect is half the staging):** build only path and timing as Blender objects. An effect that flies along the arm looks like a bead on a string; give it an arc that rises forward and drops. Effects don't go into the glb. Write down the release frame and hand the real effect to the effects and dev lanes.
6. **Render and fix yourself.** Run the defect gate first and fix gross defects. Then render front, battle and side for every frame and make gifs and the arc plate with the sheets script. Before handing on, open **one key-frame sheet** (front and battle, 10 frames) and go through the quality gate; fix one failure at a time and re-render. Crop and enlarge small areas (face, hands).
7. **glb.** Add a shape-key slot to the same action so body keys and shape keys export as one clip. After export, read the glb JSON and confirm the clip has a `weights` channel, then run the clip audit.
8. **Show** each clip to the human with battle, game-size, side and arc views and the same-speed reference. Write the gross-defect count and the silhouette area change in the note. Record their verdict in the decision log.

**Monsters and shadows:** code does these better than human acting. Tentacles: a bone chain with phase-shifted sine waves, later and larger toward the tip (springs). A mass that swells and collapses: shape keys. A spreading outline: a shader. glTF carries no constraints, drivers or geometry nodes, so bake everything into per-frame bone and shape keys. See the `blender-anim` skill.

**Pitfalls:** after loading a rig, reset it to rest or the render comes out empty; a camera with 0 degrees of tilt can render front and side views empty (use 3 degrees or more); an effect blob the same colour as the body disappears.

## Speed: author at a reference length, the game adjusts

- Author an attack at **one reference attack interval** and write the contact frame in `<character>/motion/notes.md`. The game scales playback by attack speed up to 2×; faster than that needs a separate short version (Dota 2 and Warcraft III tie attack speed to animation the same way).
- For deterministic games, the simulation decides the contact moment and the clip follows it. The animation never decides when damage lands.
- Scale walks only within 0.8 to 1.2× of authored speed or the feet slide. The clip audit measures the treadmill speed of a planted foot.
- A sped-up attack has a shorter anticipation on screen. Write the anticipation time **after** the rate into the clip contract: (contact − anticipation start) ÷ 24 ÷ rate. A one-frame overshoot or snap survives only if the engine samples that frame (see "Into the game").
- If the game's attack interval is far shorter than your clips (a greybox hitting every 0.25 s versus a 3 s attack), settle the reference interval with design before building more attacks.

## Defect gate (before the quality gate)

The maker only measures what they aimed for. A fall clip passed its own palm and distance checks with a hand buried in the thigh.

- Run the motion QA script with renders on every clip you show, blocking included. Zero gross defects, or one line per remaining defect (what, frame, why).
- Judge with the check renders (colour-coded sides, checker floor), not the dark textured render. Check renders are for you, not the human.
- An image-only look says where to look; it was wrong both ways in calibration. Confirm with numbers or a zoomed crop.
- **New body, calibrate first:** run the gate on one clip the human liked and one they disliked. If the disliked one passes, the check is wrong.
- **Silhouette overlay:** lay a polished clip over its approved blocking (or chosen pose glb) at the key frames (pair frames like `26:28` if timing moved). A frame with a big change has left the approved pose; if intended, say why in one line, otherwise fix. Calibration: a polish over its own blocking changed up to about 5%; a different take changed 60 to 100%.

## Into the game: seams, planted feet, cost

The defect gate checks whether the body breaks. This gate checks the glb plays **the same** in the game, and what it weighs. Evidence, numbers and sources: [references/game-ready.md](references/game-ready.md). The numbers are proposals; agree them with the project owner.

- **Seam:** how far hips, head, hands and feet jump when a loop wraps. Under 15 mm (about 1 px on a figure 127 px tall) or under 1.5× a normal frame step. Over that, re-bake the last frame to meet the first.
- **Planted-foot drift:** how far a foot moves while within 2 cm of the floor. Idles and holds under 10 mm. This catches the slow creep a 2 cm-per-frame slide check misses.
- **Frame rate:** Blender 24 fps, a key every frame. If Godot imports at `animation/fps = 30`, three of every four authored frames are never sampled (a one-frame slam pose lost 9.3 degrees on one arm). Import at 24; until then, report the resample loss at the contact frame for every attack.
- **Weight:** body ≤ 32 bones, each monster-part rig ≤ 16, whole figure ≤ 48, four bones per vertex, no finger bones. Fold bones no vertex uses unless they parent something. Animation CPU per figure is microseconds; cost comes from triangles.
- Export settings table: game-ready section 3. Read contact seconds from the glb, not by converting frame numbers by hand (some clips start at frame 1).

## Quality gate (any failure, redo)

Based on Animation Mentor "Overlap and Follow-Through", Richard Williams "The Animator's Survival Kit", AWN "Taking the Computer out of Computer Animation", GDKeys "Anatomy of an Attack", Skullgirls GDC "Animation Bootcamp".

- [ ] **Acting:** the one-sentence acting note reads on screen; at least two of the character's three personality words read in the body.
- [ ] **Three silhouettes:** anticipation, contact and recovery read clearly different in the game-size gif.
- [ ] **Arcs and spacing** (arc plate): hands and head travel in arcs; spacing is widest in the strike and tight in anticipation and recovery; no evenly spaced dots (constant speed).
- [ ] **Sequence:** hips and torso lead, arms and hands follow; hands and feet don't move as twins.
- [ ] **Weight:** planted feet don't slide; weight shifts to the front foot on the strike; knees don't pop.
- [ ] **Hold and settle:** 0.1 to 0.25 s hold after contact, rebound settles within 2 to 3 swings; **no fully frozen stretch longer than 0.5 s.**
- [ ] **End:** ends in place, close to the ready pose (joins the idle).
- [ ] **Body:** no tearing or stretching (skull base, armpits, chest; if seen, go back to step 0); no arm or hand through body or head; a small head doesn't vanish in a bow; the right hand is used.
- [ ] **Facing:** never shows its back to the battle camera for more than 0.5 s.
- [ ] **Style:** screen height and facing match your art bible; no copy of a famous move from an existing licensed character.

## Touch-ups (Blender, free)

- In place: remove horizontal hip travel; do the same to the glb that goes to the game.
- Shorten holds, retime, attach weapons and props to hand bones, fix intersecting frames: save each as a per-character `fix_*.py`. To find a stretch to retime, print head and hand speed per frame.
- After touch-ups, redo steps 6 and the quality gate.

## Don't

- Block without a reference; build motion without a pose board; look for the first time after everything is built; put two actions in one clip; fill a prompt with looks, clothes or backstory; change several things at once between takes; start text-to-motion on the expensive mode before testing on the cheap one; edit prompts without checking the rig.
- Use a preset clip as a hero's attack as is (it's the same for everyone, no personality).
- Judge toon shading from motion check renders; judge toon and outlines in the engine.
