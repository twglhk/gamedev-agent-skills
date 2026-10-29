---
description: Open a hero lane session (hero identity, combat role, concept art, 3D model and animation)
---

This session is the hero lane. It decides who each hero is, how they fight and how they join the team, then takes that hero from concept image to a game-ready 3D model with animation. It fills in skills and synergies inside the frame /design sets (skill gauge, synergy rules), and it never edits game code.

## Start

Load `hero-design`, `skill-design`, `char-3d-source`, `char-anim` and `blender-anim`. Read your design pillars doc, the character docs and, on any day with art work, the full art bible. Then do the task in $ARGUMENTS. If it is empty, give a 3-line brief of the lane's open work and wait.

## Rules

- A rough concept image only needs the approximate look and role. Before the turnaround sheet, write the identity in words: real name and hero name, role, weapon, attack verb, signature skill with its motion. If any of these is blank, don't generate the turnaround.
- New ideas that come up while drawing go into the identity doc first.
- Reread the art bible right before every generation. Paste its style anchor verbatim at the front of the prompt, attach its reference images, and filter results through its post-generation checks before showing anything.
- Check every model in the real game camera, at battle size, next to the rest of the roster.
- Keep one current-state section per hero. History and credits go to your log.

## Approvals

Character, personality and look directions are drafted here and picked by the human from options shown side by side. New names: get candidates and let the human pick. 🔴 Paid generation needs the human's approval with counts and a cost estimate first. Don't stretch one approval to the next step.

## Handoffs

"→ /design: the skill needs a new target shape", "→ /dev: import the new rig". Write the note; don't do it here.

## Done

The identity is written, the model and clips play in the game camera, and the human has approved the look.

$ARGUMENTS
