---
description: Open an FX lane session (visual effects, sound, game feel, shaders)
---

This session is the game-feel lane. For every moment in the game (playing a card, a level-up, a hit, a skill, a death, a boss entrance), it builds the visual effect and the sound together. Wiring effects into other lanes' scenes belongs to /dev.

## Start

Load `fx-craft`, and `elevenlabs` if sound will be generated. Read your design pillars doc (core emotions) and the art bible's shared layer for colour and light. Then do the task in $ARGUMENTS. If it is empty, give a 3-line brief of the lane's open work and wait.

## Rules

- Keep one moment table as the source of truth: for each moment, the effect, the sound, the intensity, and which core emotion it feeds.
- 🔴 Never touch combat determinism. Effects and sound only watch; hitstop pauses playback, never the simulation. Intensity and volume live in data.
- Research first, build in greyscale first, then measure with numbers before calling it done.
- Work in new files in your own folders (adapt: `game/fx/`, `game/audio/`, `game/shaders/`, `game/tests/fx/`).
- Record every third-party asset's credit in an attribution file.

## Approvals

🔴 Sound tools and audio assets carry cost and licences: ask before using one, with counts and a cost estimate for paid generation. Choices between versions go to the human side by side. One approval covers one step.

## Handoffs

"→ /dev: trigger the hit effect from the damage event". Note it, don't do it.

## Done

The effect and sound play in the build, pass the measured checks in `fx-craft`, stay inside the performance budget, and leave combat logs unchanged.

$ARGUMENTS
