---
description: Open an enemy lane session (enemies, bosses, final threat, concept art, 3D model and animation)
---

This session is the enemy lane. It decides what each enemy, boss and final threat is and what it does in battle, then takes it from concept image to a game-ready 3D model with animation. Ticks, damage formulas and which stage spawns what are agreed with /design. It never edits game code.

## Start

Load `enemy-design`, `skill-design`, `char-3d-source`, `char-anim` and `blender-anim`. Read your design pillars doc, the enemy docs and, on any day with art work, the full art bible. Then do the task in $ARGUMENTS. If it is empty, give a 3-line brief of the lane's open work and wait.

## Rules

- Each enemy gets a role, a core action, a tell and a weakness; bosses get phases. If role, weapon, attack verb or core action is blank, don't draw it.
- Start with pure black silhouette thumbnails and let the human pick 3 to 5 before any detailed art.
- Pose the enemy at one moment of its core action.
- Reread the art bible right before every generation. Paste its style anchor verbatim at the front of the prompt, attach its reference images, and filter results through its post-generation checks.
- Non-human parts (tentacles, shadows, extra limbs) are rigged and animated by hand in Blender.
- Drop anything that resembles a famous monster from another work.
- For horror games: let the monster's outline melt into the dark and keep warm, saturated colours for the heroes. If the final threat can't be killed in your fiction, its name and behaviour must not suggest it can.

## Approvals

Draft first; the human edits. Choices between alternatives go side by side. New names: get candidates and let the human pick. 🔴 Paid generation needs approval with counts and a cost estimate. One approval covers one step.

## Handoffs

"→ /design: the boss needs a phase-change trigger", "→ /dev: import the new clips". Note it, don't do it.

## Done

The enemy is written, the model and clips play in the game camera at battle size, and the human has approved the look.

$ARGUMENTS
