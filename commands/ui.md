---
description: Open a UI lane session (screen layout, HUD, cards, buttons, icons, theme)
---

This session is the UI lane. It decides what each screen shows, where, and what the player presses, along with its look (card frame, hand, HUD, timers, buttons, icons, colour codes, type, theme), and builds it as Godot UI scenes. Wiring UI into other lanes' scenes belongs to /dev.

## Start

Load `ui-craft` and `design-principles`. Read your design pillars doc (controls section) and the current milestone. Then do the task in $ARGUMENTS. If it is empty, give a 3-line brief of the lane's open work and wait.

## Rules

- Everything works with one hand on the mouse.
- Put all the information one decision needs inside one glance.
- Show key stats with the same colour and icon every time instead of words.
- Drag and drop snaps to the intended slot even when the drop lands on a border.
- Screen text stays minimal and comes from one data source; UI code shows only that text.
- Work in your own folders (adapt: `game/ui/`, `game/tests/ui/`). Ask before adding a font or addon.

## Approvals

Directions are shown as comparison sheets (HTML mockups or Godot screenshots) and the human picks. Only the picked option becomes a written rule. One approval covers one step.

## Handoffs

"→ /dev: mount the new hand panel in the battle scene". Note it, don't do it.

## Done

The screen passes the `ui-craft` review with evidence, its tests pass, and no button on it does nothing.

$ARGUMENTS
