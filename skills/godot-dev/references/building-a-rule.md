# Building a rule in Godot

How a rule handed over as a design doc plus `.tres` numbers becomes game code. Thresholds live in your build guide; this file is the order of work.

## What comes in

- A handoff from design naming the doc that states the rule and the numbers it plays by (already in a `.tres`, or listed for you to put there).
- Where the handoff and the design doc disagree, the doc wins; note the gap in the report and tell the designer.
- Anything the current screen plan doesn't draw stays out unless the project owner approves it. List it under "Not built".

## Order of work

1. **Say what the player sees change.** One line per rule.
2. **Measure the spread before.** Run the auto-play probe on the code as it is, so the after numbers have something to stand against.
3. **Numbers in the data.** Edit the `.tres` directly. A new number gets an `@export` field with a `##` line on its data class and its value in the `.tres`. Read the `.tres` diff before touching code.
4. **Tests first.** One test per guarantee the rule makes, in the test file of the script under test ([testing.md](testing.md)). Run them and see them fail.
5. **Change the rule code** until they pass, in the rule layer only. The view changes after.
6. **Read the pinned answers.** Run the whole suite. The pinned cases that fail are the answers the change moved. If the rule explains each, re-pin with `PIN_FIXTURE=1` ([determinism.md](determinism.md) "Checks to run") and list every `PIN moved` line in the report with its reason. A move the rule doesn't explain is a bug.
7. **Measure the spread after** with the same command; table before and after per round.
8. **Wire the view.** The view reads events the rule layer returns; it never decides a rule. A new named moment (star-up, synergy lit, boss reveal) becomes an event that effects and UI code can attach to.
9. **Drive the exported build** (SKILL §4) and tick the piece if it now plays (SKILL §6).

## Shape of the code

- **Rules know nothing of the scene.** `RefCounted`, no `Node`, no `SceneTree`, no `Time`, no global RNG, no `await`. They take a spec and inputs, step in integer ticks, and append to a log. The view is a `Node` that owns a rule object, feeds it player inputs, and draws what it reports.
- **A run is a seed plus an input list.** Inputs are the cards played and their targets, moves, and mid-fight plays with their tick. Replaying the same inputs gives the same run, across processes and across a save/restore at a round edge.
- **Streams per kind of draw.** Card draw, enemy deck, encounters and rewards each roll their own stream, seeded by hashing the run seed with the stream name, so one extra draw never moves the enemy deck. Fights keep their own seed, so any fight replays alone from its spec.
- **Two levels of pins.** Fights pin tick count, result and log hash. A stage with several streams is checked by round win rates from the probe, not bytes.
- **Order inside a tick is written down.** Simultaneous effects resolve in a fixed order, listed in the rule file's header. Change the header in the same edit as the order.
- **Numbers are data.** No literal other than 0, 1 and -1 that reads as balance in a rule `.gd`.

## Naming and style

- Godot names: `snake_case` functions and fields, `PascalCase` classes, `StringName` keys (`&"hunt"`). No JavaScript-style names or abbreviations.
- Static types on every declaration (`var n: int`, `-> void`). They catch slips at parse time, which the runner reports as a load failure.
- Comments say why, in English.
- Hand-written `.tscn` and `.tres` carry no `uid`. A duplicate uid loads the wrong scene without a warning.

## Old code

When the project holds code from an earlier design, what to keep or clear is the project owner's call. Don't delete it on your own; list what blocks you in the report.
