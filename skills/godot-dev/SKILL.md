---
name: godot-dev
description: Method for building game rules into a Godot 4 project with AI agents. Rules live in plain RefCounted objects, numbers live in .tres data, tests run headless, battles stay deterministic behind pinned logs, every change is proven in the exported build, and frame cost is measured before and after. Use when writing or changing Godot game code, tests or .tres data, turning a design rule or number change into code, re-pinning golden fixtures, touching export presets or a daily build script, or profiling a scene.
license: MIT
---

# Godot dev: build, test, prove, ship

This skill is the method. Your project's rules and numbers live in its design docs and data; read them there and never copy a value into this file or a report.

**Conventions this skill assumes** (adapt the paths to your project):

- Godot project in `game/`. Scenes and resources are text (`.tscn`, `.tres`).
- Balance numbers in `game/data/*.tres`, the canonical copy. Rule scripts hold no balance literals.
- Tests in `game/tests/`, run by a `SceneTree` runner `res://tests/run_tests.gd` that prints `ALL TESTS PASSED` as its last line only on success. Tests extend a small base `res://tests/test_case.gd`. No external test add-on.
- Pinned answers (a golden-master fixture) in a JSON file under `game/tests/`, re-pinned by running the suite with `PIN_FIXTURE=1`.
- A headless auto-play probe (here `res://tools/stage_probe.gd`) that plays a stage N times with a few bot policies (random, greedy, smart) and prints win rates per round.
- A build script that runs the test gate and exports Windows and macOS, with `BUILD_DATE` and an output root you can point at `/tmp` for trials.
- Driver scripts that click through the exported build like a player and print one `RESULT OK|FAIL gaps=N` line.
- A frame-cost probe script that opens a screen and averages CPU/GPU ms, draws and memory.
- A written build checklist for the screen you're working on, and a quality guide with numbered criteria (determinism, spread, no literals, frame budget, code hygiene). Called "the build guide" below.

If you lack one of these, build it before relying on the step that uses it. Sources and how strong each claim is: [references/sources.md](references/sources.md).

## Read first, just in time

- The task brief and the design rule behind it. Quote the rule at the top of your report.
- The last report on the same code (`grep -rl <symbol>` in your reports folder). Reuse its seeds, drivers and measure scripts so numbers stay comparable.
- The header comment of every file you touch. Tick order, contracts and env switches belong there, not here.
- `git status -- game` before writing. If other agents edit `game/` on the same day, change only the lines your task needs and never revert theirs.

## 1. Build a rule

The design doc is the spec. Order of work, code shape and naming: [references/building-a-rule.md](references/building-a-rule.md).

- Rules sit in `RefCounted` scripts that know no node, clock or global RNG. They return what happened; the view reads it and draws. Rules stay testable headless and the view stays free to change.
- **Numbers:** edit the `.tres` directly. A new number gets an `@export` field on its data class and its value in the `.tres`. Read the `.tres` diff before touching code.
- **Tests:** each guarantee of the rule gets a unit test that fails before the change (§2).
- **Pinned answers:** the fixture holds fixed inputs (whole fights, costs, placements, checks) with the answers the game gave. Any change that moves one fails its test. When the rule explains every move, re-pin with `PIN_FIXTURE=1` (§3) and list each `PIN moved` line in the report with its reason.
- **Spread:** run the probe (`godot --headless --path game -s res://tools/stage_probe.gd -- 1000 random,greedy,smart`) before and after; table round win rates side by side.
- Where the build departs from the design doc on purpose, list it under "Differs" in the report and tell the designer.
- Screen text lives in one data table; UI code shows only text from there.

## 2. Tests

Runner internals, a template and the traps table: [references/testing.md](references/testing.md).

- Run: `godot --headless --path game -s res://tests/run_tests.gd 2>&1 | tee /tmp/t.log; grep -qx "ALL TESTS PASSED" /tmp/t.log`. Trust only that last line. macOS headless Godot can exit 0 even when a script fails to parse.
- Make the runner fail a test on any engine or script error logged while it runs, so an `ERROR:` line is a failure to fix.
- Time-limit every headless run. macOS has no `timeout`: `perl -e 'alarm 900; exec @ARGV' godot …`.
- One test file per script under test, methods named for the guarantee (`test_a_drag_cut_by_focus_loss_goes_back`), a `##` line on why it matters.
- A fix ships with the test that fails without it. Prove it: undo the fix, see red, redo it, and say so in the report.
- Keep a pyramid: many fast rule tests, fewer scene tests (the view in the tree, pointer events pushed into the viewport), one broad drive of the exported build (§4).
- A test that fails only sometimes is a bug. Find the cause (seed, clock, test order, leaked state such as a saved user config) the same day. Never rerun until green.

## 3. Determinism 🔴

For a simulation-driven game (auto-battlers, lockstep, replays): same seed and same inputs must give the same log, byte for byte. A desync stays invisible until a pinned log or a replay breaks. Detail and the divergence hunt: [references/determinism.md](references/determinism.md).

- Rules use integer ticks and your own seeded RNG streams only. No `randi()`, `randf()`, `Array.shuffle()`, `Time.*`, frame delta or float accumulation in rules. Godot's RNG algorithm is an implementation detail that may change, and float results differ across compilers and CPUs.
- Any change near a fight proves the log is unchanged: the log hash for the same seeds before and after, at every game speed, with the view on and off. Put the hashes in the report.
- A change meant to alter logs re-pins with `PIN_FIXTURE=1`, then a plain run to green. The report lists every `PIN moved` line and the rule that moves it.
- When two runs disagree, find the first line where they part (diff the logs) before forming any theory.

## 4. Prove it plays

Done means it plays in the exported build, not only in a test. Drivers, frames and footage: [references/build.md](references/build.md) "Drive the build".

- Make a trial build (§5), then run its shipped `.pck` with the editor engine and a driver: `DRIVE_OUT=<dir> godot --main-pack <pck> --resolution 1920x1080 -s <driver.gd>`. Release templates refuse `--script`, so the editor binary runs the pack.
- Read the driver's `RESULT OK gaps=0` line, then open the frames yourself. A seed variable replays a stage; a size variable sets the window, because a saved player config can override `--resolution`.
- `--headless` draws no pixels. For frames, run windowed off screen (`--position 20000,20000`) or record with `--write-movie` (fixed fps; end it from the script or `--quit-after`, not Ctrl-C).
- When layout changed, drive every window shape you ship to (16:9, 16:10, 21:9 at least).
- Write down what was not checked and why (no Windows machine, no speakers, no fullscreen). Agent driving is observation, never a player test.

## 5. Build and export

Script steps and how to read a failure: [references/build.md](references/build.md).

- Trial: `BUILD_DATE=2026-01-15 DAILY_ROOT=/tmp/<task>/daily <build script>`. Never point a trial at the real output folder; it holds the build people download and the version ledger.
- Whatever schedules the build depends on its contract (exit code, output files). Changing the script, its outputs or the presets is its own task.
- Godot can exit 0 after a failed export, so judge exports by their files: `.exe` and `.pck`, the app bundle, the version string inside each `.pck`.
- `export_presets.cfg` keeps `tests/*` and `tools/*` out of the build; dev-only scenes and scripts go under those folders. Signing secrets never go in presets; Godot keeps them in `.godot/export_credentials.cfg`.

## 6. Tick the build checklist

Tick a piece of the screen checklist only when it plays in an exported build you drove (§4), with the frame or log path in the report. Passing tests alone don't tick. Unticking and renaming pieces belong to whoever owns the plan.

## 7. Measure frame cost

Probes, reading and traps: [references/profiling.md](references/profiling.md).

- Per-step scene cost from the frame probe; whole-stage frame times from a player-paced run. Budgets come from your build guide.
- On macOS add `--rendering-driver vulkan`; Metal reports GPU time as 0.
- Same seed, steps, quality and window before and after; one change per run; profile, fix, profile again.
- Report the machine load. Other jobs on the same machine shift the numbers.

## 8. Report

- One `report.md` per task: what changed (files and why), tests (count and last line), determinism (hashes), build (trial command and result), plays (driver, seed, frames), pins moved (each with its reason), differs from the design doc, not checked.
- Code comments are English and say why. No TODOs, stubs, placeholder values or unused helpers.
- Record the built rule as one line with the report path in your decision log; record tool traps you found where the next agent will read them.
