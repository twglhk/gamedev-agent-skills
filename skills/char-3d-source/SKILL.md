---
name: char-3d-source
description: Turns an approved character design (hero, enemy, boss) into a game-ready 3D figure. Covers the grey-mannequin 4-view model sheet (front, left, back, right), cutting it to one floor line, generating the mesh with the Tripo CLI (multi-view, face_limit, Mixamo-spec rig, retarget), the triangle and texture budget, and checking the result against the concept at battle size. Use when making a 3D source image, a turnaround / model sheet / A-pose sheet, running the tripo CLI for a character, or deciding a character's triangle and texture budget.
license: MIT
---

# Character 3D source: the 4-view sheet and the path to a mesh

One approved concept image becomes a blueprint a 3D generator can read, and that blueprint becomes the main characters (heroes, enemies, bosses) through Tripo. Props and background NPCs can come from a cheaper single-image generator such as Meshy. The sheet is a production input, never a picture shown in the game.

This skill assumes:
- character art lives in a folder per character (`<art>/<character>/turnaround/`, `<art>/<character>/3d/`);
- an image generator you can call from a script with attachments, aspect ratio and size (any model that follows reference images well);
- Blender on the command line (`blender -b -P script.py -- args`), or Blender MCP if connected;
- a Godot scene that shows a unit at the real battle camera, which you can render headless.

## Why four views

- Modelers work from a model sheet (turnaround): the same character at the same size, pose and floor line, seen from several sides, so nobody has to invent the hidden side.
- Generators ask for the same thing. Meshy: up to four images (front, left, back, right), the first one the front, same size, light and background in each, the sheet cut into separate images, side views at least 45 to 90 degrees off the front (docs.meshy.ai multi-image-to-3d, help.meshy.ai Multi-View Best Practices). Tripo multi-view slots are the same four, `front` required, at least two images, same pose, light, background and scale (developers.tripo3d.ai multiview-to-model).
- 🔴 A body whose left and right differ (one arm a monster limb, a cape on one shoulder) needs both side views. Give one side and the generator mirrors it.
- Asking for the pose in words alone fails. A single front-view prompt for an "A-pose" came back with arms pressed to the body and a different arm angle in each panel.

## The sheet spec

| Item | Value |
| --- | --- |
| Panels | Four in one image, left to right: front, left (the character's left side, facing image left), back, right (facing image right) |
| Pose | A-pose: arms straight, 45 degrees down and out, clear of the body; feet shoulder width, soles flat; face forward |
| Camera | Orthographic, chest height |
| Light | Flat, shadowless studio light; surfaces show base colour only. A part that is black by design (a shadow body part) is painted flat matte black as a material, not as shading |
| Background | Plain light grey #E6E6E6, no floor line, no floor shadow |
| Text | None. No FRONT/SIDE labels or rulers; the generator reads them as part of the body |
| Format | 21:9, 2K. Height and build belong to the character, not the mannequin |

The picture sets the pose, panels and floor line, not the prompt. Render a grey mannequin in the four views once in Blender (A-pose, orthographic, same floor line) and attach it as the first image every time. This is the same trick as laying an OpenPose skeleton or a mannequin render under a drawing.

## Triangle budget

- Pick a target from the use, the battle camera size and how many figures share the screen, and report it with the cost. Starting points: low-poly props in the hundreds and characters 1,000 to 3,000; detailed-style props in the thousands and characters 10,000 to 20,000.
- A working baseline for stylised 3D figures seen small: about 30k triangles and 2K textures. Tripo `face_limit=30000` lands near 28k. `face_limit` is a ceiling, so count the received file in Blender.
- A 15k retopology of a 28k figure looked the same at battle size, but it re-cut the UVs into thousands of islands and ended with more vertices. Lowering the budget is a project decision; don't change the default or regenerate paid models on your own.

## Steps

0. **Battle-size lineup first.** Shrink the approved concept to battle camera size and stand it next to the other enemies of the same stage and one hero. Don't make a sheet until it passes. A monster that was modelled and animated before this check failed on the game screen.
1. **Prompt.** One prompt file per character (`<character>/turnaround/sheet.md`). Keep a fixed template and change only the CHARACTER, clothing and four PANEL descriptions.
   - First line: your art bible's style anchor, copied as is.
   - 🔴 State for every panel what is on IMAGE LEFT and IMAGE RIGHT. "His left" alone gets mixed up from panel to panel.
   - Count limbs ("EXACTLY TWO ARMS"). A held object goes "ONLY in that hand".
   - If the concept shows an action pose (bent waist, crawling, kneeling), say the sheet stands it upright; the pose belongs to animation.
2. **Attach** (1) the mannequin sheet, (2) the one approved design. 🔴 Never attach earlier drafts; the generator copies their flaws too.
3. **Generate.** 🔴 Before spending, tell the human how many images and the rough cost. Two candidates per run is enough.
4. **Check before choosing:**
   - clothes, colours, black parts and held objects stay on the same side in all four (front image-left = back image-right);
   - the two side panels face opposite ways; arms in front and back are 45 degrees off the body;
   - drop any sheet where trouser colour changes between panels or something covers the head in the back view.
   Then show the human the candidates side by side and let them pick.
5. **Cut.** Write a small script that splits the sheet into `1-front.png`, `2-left.png`, `3-back.png`, `4-right.png` on one square canvas with one floor line, plus a `check.png` with the floor line in red and the highest point in blue. Have it warn when heights differ by more than 3%. Look at `check.png`: a size difference means drop the sheet; one panel with a taller part means ask before going on.
6. **3D with the Tripo CLI.** Read [references/tripo.md](references/tripo.md) before the first command.
   - 🔴 State credits first (`tripo balance`). One character costs about model 40 + rig 25 + 10 per clip. Buying more credits is the human's decision.
   ```
   tripo make 1-front.png 2-left.png 3-back.png 4-right.png --model tripo-v3.1 -p face_limit=30000 \
       -p texture_quality=detailed -p texture_version=v3.5-20260815 -p delight=true --dry-run --json   # plan and price only
   # same command without --dry-run, plus: --name <id> -o <character>/3d/tripo --json --yes --no-open
   tripo anim check <model task>                                   # free; stop if not riggable
   tripo anim rig <model task> --rig-type biped --spec mixamo --out-format fbx -o <character>/3d/tripo
   tripo anim retarget <rig task> --animation preset:idle preset:walk --out-format fbx --animate-in-place -o <...>
   ```
   - File names carry the slot (`front`/`left`/`back`/`right`); the CLI reads them. Keep every task id. Resume a timeout with `tripo task watch <id> --download`, never by running `make` again.
   - Then turn, scale and shrink textures for the game in Blender (Tripo exports 1 m tall, +X forward, 4K maps). See the pitfalls in the reference.
   - Non-human bodies (four legs, tentacles): `tripo anim check` reports the rig type, the biped presets don't apply, and motion is built in Blender (`blender-anim` skill).
   - 🔴 A character whose body colour is black may come back with skin-coloured black parts. Don't regenerate; paint them in step 7.
7. **Paint black parts (no credits).** After rigging, select the faces by their strongest bone weight and position, give them a flat matte black material, and break the border with 3D noise. Save `.blend`, `.glb`, an unlit four-view render and a toon render at the battle camera. If auto-rigging bound a big attached mass (a sack, a hump) to the arm or shoulder bones, rebind those vertices to one spine bone, or the mass warps whenever the arm moves.
8. **Concept against game, twice:** after the mesh (step 6) and after painting (step 7), before any motion polish. Enemies that skipped this ended up looking nothing like their concept.
   - One pair: the approved concept and the unit rendered in the game at the battle camera (evening and night lighting if you have them). Same pixel height, two separate files.
   - Black silhouettes of both at the same height, plus an overlay (grey where only the concept has shape, red where only the unit does). Cut the concept to a transparent PNG if its background isn't flat.
   - Check that black parts read as black, there's no texture blotching under the outline pass, and the key shape is there at rest too.
9. **Log** what you made, how many, what it cost, what you dropped and why, in your decision log.

## Don't

- Generate 3D from a single front image; it invents the back and sides.
- Upload the whole sheet as one image; cut it per view.
- Drive the Tripo web app through a browser to spend subscription credits, or use unofficial cookie-based tools. The agent's path is the official CLI.
- Paint flying debris, smoke or floating ink into the source. It becomes floating junk geometry; add it as a game effect.
