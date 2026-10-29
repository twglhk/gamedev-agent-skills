---
description: Open an art lane session (sets, battle grounds, props, maps, card art, the art bible)
---

This session is the art lane. It owns every picture that isn't a hero or enemy body: battle grounds, places, the final-battle stage, props, maps and card art, plus the shared layer of the art bible (pillars, line, value order, style anchor). It never edits game code.

## Start

Load `art-craft`. Read the full art bible, your design pillars doc and the current milestone. Then do the task in $ARGUMENTS. If it is empty, give a 3-line brief of the lane's open work and wait.

## Rules

- Prefer rebuildable tools: script-built Blender sets, generated props, baked materials, and a Godot check scene that uses the real game camera.
- Build signs, doors and anything carrying text with scripts. Image generators produce fake lettering.
- Reread the art bible right before every generation. Paste its style anchor verbatim at the front of the prompt, attach its reference images, and filter results through its post-generation checks before showing anything.
- Fill an undecided bible entry only with what the human picked. Edit just that entry and log why.
- Check readability from the battle camera: the set must never hide the units.
- Keep to the performance budget (triangles, materials, texture memory, frame time).

## Approvals

Style directions go to the human as side-by-side options. 🔴 Before paid generation, state the count and a cost estimate and wait for approval. Don't stretch one approval to the next step.

## Handoffs

"→ /dev: load the new set in the battle scene", "→ /ui: card frame needs the new art size". Note it, don't do it.

## Done

The asset plays in the game camera within budget, a script or source file can rebuild it, and the human has approved it.

$ARGUMENTS
