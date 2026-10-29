---
description: Open a dev lane session (Godot code, tests, tools, builds, QA)
---

This session is the dev lane, with QA, tools and engine work attached. It builds into the Godot game what /design decided. It doesn't invent rules or numbers: behaviour follows the design docs and the data files (adapt: `game/data/`).

## Start

Load `godot-dev`. Read the current milestone and the build scope list of open screen pieces. Then do the task in $ARGUMENTS. If it is empty, give a 3-line brief of the lane's open work and wait.

## Rules

- Test logic headless. On some platforms headless Godot exits 0 even on failure, so check the test runner's final pass line, not the exit code.
- Keep combat deterministic: same seed and same team give a byte-identical log. Pure logic gets unit tests; balance values live in data.
- Prove a change in the exported build, not only in the editor.
- Tick a piece off the build scope only once it plays in the exported build.
- A build-breaking change is fixed the same day.
- When old code conflicts with the new design, ask the human what to keep before ripping it out.

## Approvals

🔴 Engine or stack changes, new external dependencies and changes to core rule parameters go to the human first. No commits, pushes or releases unless asked.

## Handoffs

Rule questions go back as a note: "→ /design: the spec doesn't say what happens on a tie".

## Done

Tests pass, the exported build runs, and there is evidence you ran it yourself (a screenshot or a log).

$ARGUMENTS
