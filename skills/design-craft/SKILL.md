---
name: design-craft
description: Method for turning a game rule or level change into a written spec plus a data switch in a Godot game, measuring it with headless auto-play bots (paired seeds, standard errors, matched difficulty), laying out stage and round beats, and handing an approved change to the dev lane. Includes a full TFT trait index for synergy design. Use when changing balance data, running or reporting an auto-play probe, comparing rule options with numbers, laying out a stage's rounds or a location's choices, designing a synergy/trait, or handing a rule to a developer.
license: MIT
---

# Design craft: specify it, measure it, hand it over

A design change is decided by more than paper. The rule is written in your design doc, put behind a data switch in the game, measured by auto-play, picked by the human, and wired by dev. This skill is the method for those steps. What to ask of any idea (core verbs, emotions, the kill list) is in the `design-principles` skill. Your project's answers (rules, numbers, target bands) live in your design docs and data; read them there and never copy a value into this file or a report. Sources and strength of each claim: [references/sources.md](references/sources.md).

**Conventions this skill assumes** (adapt to your project): a Godot game in `game/`; balance data as `.tres` resources in `game/data/` with typed `@export` fields; a headless auto-play probe (`game/tools/stage_probe.gd` below) that plays a stage N times with a few bot policies (for example random, greedy, smart) and prints per-round win rates; a test suite that ends on `ALL TESTS PASSED`; a pinned golden fixture re-pinned with `PIN_FIXTURE=1`; target bands per policy (for example "smart clears 60–75% of runs") written in your design doc; reports in a `design/<area>/<topic>/` folder.

## Read first, just in time

- The design doc that owns the knob. Where the doc and the game differ, the doc wins.
- The human's exact words behind the task. Quote them at the top of the report.
- The last report on the same knob (`grep -rl <knob> design/`). Start from its seeds, policies and probe so numbers stay comparable.
- The data that holds the knob: the resource scripts (each `@export` field and its comment) and the `.tres` files.
- The header of the probe you run: the policies, what it plays and what each output line counts are defined there.
- A new or reworked synergy: [references/tft-traits.md](references/tft-traits.md), every TFT trait by family. Pick the kind there, check it against your live synergies, then tune numbers with the probe.

## 1. One question per change

A test exists to answer one question; write it before touching data (Schell, Fullerton).

- Form: "With X, does Y move, without Z moving?" For example: "With a full hand reset each round, do idle late rounds fall, without the smart bot's stage clear moving?" Name the metrics for Y and Z now, so you don't go fishing in the output later.
- Name which core verb and emotion it serves (`design-principles` §0). If none, stop and report.
- One knob per switch. If two things change, make two switches and measure each alone, then together.

## 2. Write it down, then put it behind a switch

- **Spec first.** State the rule in the design doc that owns it, one or two sentences per point, marked as a candidate until the human adopts it. The game must not do anything the doc doesn't say.
- **Data switch.** A change goes behind a field in a data resource whose default keeps today's game (a bool like `hand_reset` on the stage data). If the field exists, you only set values. If the rule needs code (a new field, a new effect kind, a new screen step), hand the rule and the switch you need to dev; a design agent doesn't edit game code.
- **Numbers.** Placeholder numbers for content already approved go straight into the `.tres`. 🔴 Changing an existing core number (enemy strength, boss, economy) is the human's call: try it in memory with a lane probe (`TRY=`, §3), show the options side by side, and write the `.tres` only after they pick.
- **Default untouched.** With the switch off, the probe prints the same lines before and after, and the tests pass with the pinned fixture unmoved.
- **Moved answers.** When an adopted data change is meant to move fights, re-pin with `PIN_FIXTURE=1` and list every `PIN moved` line in the report with the rule that moved it. Code changes are pinned by dev.
- **Determinism.** Integer ticks, the game's seeded RNG only, no wall-clock time or engine random in rules. Two runs of the same command must print the same numbers. If they don't, find out why before reading anything.
- New screen words (a label, an error line) go in the spec and the handoff; whoever wires the screen puts them in the text data the UI reads.

## 3. Measure it

Detail and arithmetic: [references/reading-probe.md](references/reading-probe.md).

- **The probe.** `godot --headless --path game -s res://tools/stage_probe.gd -- <N> random,greedy,smart`. For anything it doesn't print, write a lane probe in the task folder that `extends` it and only adds counting, in-memory trials (`TRY=`) and per-run lines (`OUT=`). It changes no data and no game file.
- **What the probe can't play, dev builds.** If the question needs a part of the run the game doesn't have yet, ask dev for it and say what you'll measure. Don't measure it on an old prototype instead.
- **Same seeds in every condition.** Seeds 1..N by default. Compare each option with today on the same seeds and report the paired difference, not two separate rates; shared seeds cancel most of the luck (common random numbers, Kelton & Barton).
- **Size.** 1000 runs per policy is the first look; quote ± one standard error on every rate and every difference. A difference smaller than two standard errors is not a finding.
- **Match difficulty before comparing.** If an option makes the team stronger, move one named knob that comes after the change (usually enemy or boss strength) until smart matches today, then compare the other metrics. Say which knob and by how much.
- **Read the spread, not one number.** Read every policy against its band. When the game can't play what a band measures (a whole run, say), write what you read instead and label it. A change that helps smart and wrecks greedy differs from one that lifts both.
- **Read the reason.** For each surprising number, open a few single runs (seed, policy) and find what happened. A counterfactual re-run (same seed, one thing swapped) shows what a mechanism caused; an average can't.
- **Suspect the bot first.** When a policy ignores a card, a choice or a placement, read its code before calling the design broken; teach your lane probe to use it, and report both.
- **What the bot can't tell you** (Holmgård; Dormans): feel, readability, whether a choice is interesting, how long a real player takes. Label every number "agent auto-play, not a playtest", and minutes "agent estimate".

## 4. Lay out the beats

For a stage's rounds, an exploration, a location's choices, or the whole run. Method and template: [references/level-beats.md](references/level-beats.md).

- **Yardstick first.** Before choosing a length or rhythm, write down what three or more games in the genre do, with sources, then turn it into pass criteria with numbers.
- **Beat chart.** One row per beat: what the player meets, what is new, intended intensity, measured intensity (smart's round win rate or HP left), and the rest after it.
- **Introduce, develop, twist, conclude.** A new enemy or option appears alone and safe first, then combines with known ones, then gets one turn the player didn't expect, then the stage closes on a test (Hayashida's kishōtenketsu; Slay the Spire's easy-then-hard pools).
- **Saw-tooth, not ramp.** Intensity climbs with a drop after each stop, like the Left 4 Dead director's build-up, peak, relax. A flat back half is padding; read it as "won easily" and "nothing worth playing" rates.
- **Content carries the beat.** Stage flavour comes from which enemy stands when, and with whom.

## 5. Report and ask

- One `report.md` per task: the human's words, how it was measured (command, seeds, N, policies, what ± means), the options with the same table columns, a reading per option, and a files list. Every number says what it counts.
- To get a decision, show the options side by side; each says what the player sees change in a fight or a stage, and quotes the report lines that back it.
- Once adopted, update the design doc to the current rule and log the change and its reason in your decision log; the report stays in the repo and the doc names its path.

## 6. Hand over to dev

Only adopted rules go to dev, with two things: the spec in words and the `.tres` numbers. Dev builds it in the game's own structure. Checklist and note template: [references/handoff.md](references/handoff.md). In short:

- The doc states the rule as it is now and the `.tres` holds the adopted numbers (or the note lists numbers for fields dev must add). The two agree.
- A measure line: probe command, seeds and today's output in the report, so dev can rerun it after wiring.
- Anything the spec says that the current build plan doesn't include is listed as out of scope.
