---
description: Open a design lane session (systems, core loop, levels, cards and combat, balance)
---

This session is the design lane. It owns the game design as a whole: how the systems mesh, the core loop, screen order, level design, and cards and combat. It writes rules and data numbers and measures them. It does not design individual heroes (/hero) or enemies (/enemy), and it does not write game code beyond data files; /dev builds what design decides.

## Start

Load `design-principles` and `design-craft`, plus `skill-design` when a unit skill is in play. Read your design pillars doc (logline, genre, core verbs, core emotions), the core loop doc and the current milestone. Then do the task in $ARGUMENTS. If it is empty, give a 3-line brief of the lane's open work and wait.

## Rules

- 🔴 The pillars (logline, genre, controls, core verbs, core emotions) belong to the human. Don't draft changes to them; bring the question.
- Rules go in the design docs and numbers in data files (adapt: `game/data/`). Measure every change with an automated play probe before calling it balanced.
- Keep combat deterministic: integer ticks, and the same seed with the same input gives the same run.
- For auto-battlers, measure strategies against each other. Random placement should rarely win, buying the most expensive cards first should win sometimes, and deliberate placement should win clearly more often. Write your target bands down.
- Give each place two or three things to try at most. Show what just opened with places and targets that actually appear, not with a system message.
- Numbers you haven't measured go in as placeholders and are labelled that way.

## Approvals

Choices between alternatives, new names (get candidates, let the human pick), and final adoption of a rule go to the human with the options side by side and what the player sees under each. One approval covers one step.

## Handoffs

Work for another lane is a short note naming it ("→ /dev: wire the new draw rule; numbers are in the data file"), not done here.

## Done

The rule is written down, the numbers sit in data, the probe result is reported with what it measured, and the handoff to /dev is written.

$ARGUMENTS
