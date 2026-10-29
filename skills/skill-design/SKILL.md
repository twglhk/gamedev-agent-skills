---
name: skill-design
description: Design the one active skill a hero, enemy or boss casts when its gauge fills in an auto-battler or similar auto-resolved combat game. Covers role and the placement question it asks, target shape, damage type and look, the tell, damage measured with a headless auto-play probe, and extras added one at a time, inside the skill kinds your battle sim already supports, readable at battle size, compared against the roster and presented as clear options. Use when designing, reviewing, tuning or presenting a unit skill, or when a skill feels overloaded, unreadable, random or like every other unit's.
license: MIT
---

# Skill design: damage first, one extra at a time

A skill is the moment a unit stops basic-attacking and does its one thing. In an auto-battler the player can't steer it; they decide *who stands where* before the fight. So a skill earns its place by changing placement and by being read in the fight that follows. Your project's answers (rules, roster, numbers) live in your design docs and data; read them fresh, and never copy a value into a draft or into this file. Sources and how strong each claim is: [references/sources.md](references/sources.md). Lines marked **(own view)** have no outside source yet.

**This skill assumes:** a deterministic battle sim on integer ticks; skills defined as data (a skill definition with a `kind`, numbers, and a `cast` delay in ticks); balance numbers in data files (e.g. Godot `.tres` under `game/data/`); and a headless auto-play probe that plays N runs with fixed seeds and a few player policies and prints per-round results. Adapt the names to your project.

## Read first

- `design-principles`: which core verb and which emotion the skill grows. No verb, no skill.
- Your skill rules doc: rules every skill must keep (damage by role, tanks, enemy skills), the gauge, the shapes already in play.
- The unit's own sheet (hero or enemy).
- Battle size and colour rules from your art bible (battle unit height, reserved hero colours).
- The engine: the skill definition (fields and kinds), the cast function (what each kind targets and does), and the data file holding today's skills.

## 0. Who owns what

| Part | Owner |
| --- | --- |
| A hero's skill (concept, shape, numbers) | hero design |
| An enemy's or boss's skill | enemy design |
| The frame: gauge, damage formula, damage types, the list of kinds, balance bands | systems design |
| A new kind or field in the sim | dev, after approval |
| The look and sound of the cast | VFX and audio, from the tell and look lines you write |

Hand work outside your row to its owner.

## 1. Role and question

- Name the unit's one role and write one sentence: *with this skill in the fight, how does the player change their placement?* Example: "Who stands next to the bell-ringer so the ring reaches them?" Two questions mean two skills; cut one.
- One verb per skill: hit, pull, guard, heal, mark. A skill that does three things is three rules to learn at once (TFT cut overloaded champions; Riot: "less will be more").
- The skill completes the unit's concept: name, look, body and skill tell one story (Rosewater's top-down design; `enemy-design` step 3 core action; `hero-design` one big power). If the skill could belong to any unit, rewrite it.

## 2. Shape: who it hits

Pick the target pattern before any number. Common patterns, and the placement each asks for:

| Pattern | Placement it asks for |
| --- | --- |
| Current target | whoever the caster is already fighting |
| Current target and the foes next to it | spread out so one burst can't catch two |
| Every foe within N cells of the caster | where the caster stands matters |
| Every foe adjacent to the caster | who stands in front of it |
| Farthest foe (leap there, or pull it close) | protect the back row |
| Lowest-health foe | keep the weak unit covered |
| Self, nearest allies, adjacent allies, most-hurt ally, all allies | how the team is grouped |

Map these to the kinds your sim already has before inventing any.

- Fixed targeting, never random: random single-target skills made fights "feel like dice rolls" in TFT, which moved to fixed rules. The player must be able to predict the target from the board.
- The shape follows the question in §1. A back-row diver asks "who guards the back?"; a burst around the caster asks "who stands next to it?".
- On one stage, two units with the same shape and damage type ask the same question. Change one.

## 3. Look and type

- **Damage type.** If your game has types (e.g. physical and magic, each met by its own resist), choose one so a unit with the matching defence is a soft counter. Soft counters are good, hard counters are not (TFT).
- **Look.** One cue that tells cast, caster and shape apart from every other skill on the stage: a shape on the ground, a colour, a sound. Enemy skills stay out of colours reserved for heroes. Write the look as one line for the VFX owner; the effect itself is their work.
- **Name and text.** One or two words for the name. Card text carries the effect only, in one fixed template (*target → effect*). Templates let players read new cards fast (Ben Brode); keep ability text short and simple (Super Auto Pets).

## 4. Tell

- The tell is the `cast` delay: ticks between the gauge filling and the effect landing, shown by the caster's pose and the look in §3. Zero means instant.
- Length goes with impact: a big hit gets a long, obvious wind-up; a small one may land at once (Riot: impact and counterplay proportional; Cuphead's big attacks have big build-ups; Mike Stout). TFT made spells slower, gave them travel time and made them clearer.
- Show the threat so the decision stays the player's (Into the Breach; Slay the Spire's intents). **(own view)** In an auto-battler nobody dodges, so the tell is for reading *why* a fight went the way it did, and placing differently next round.
- Each unit's tell is its own (`enemy-design` step 4). Two units on a stage with the same wind-up at the same length blur together.

## 5. Damage

- Decide whether every skill deals damage and how much each role deals; write that rule in your skill doc. Start from the existing skill nearest in role and cost and write the new number next to it.
- Read how damage, heal and shield scale (skill power, armour, resist) in the sim's damage code before guessing how much actually lands.
- Measure, never by feel:
  1. Baseline: run the probe (e.g. `godot --headless --path game -s res://tools/<probe>.gd -- 1000 random,greedy,smart`) and save the output.
  2. Change the number in the data file, run the same command (same seeds; the battle is deterministic) and compare per round.
  3. Read the result against your balance bands.
  4. A per-skill damage share needs a counter on the sim's damage events. Count them in a separate probe script, or ask dev to expose them, rather than editing the battle code from a design task.
- Label every number with what it measured (policy, seeds, rounds) and as agent auto-play, not a playtest. Keep a run a reviewer can repeat.

## 6. Extras: later, one at a time

- **Enemy skills start with shape, look, type and damage only.** Stun, slow, shield, pull, heal, damage over time and the rest come later.
- Add an extra only when the damage version fails to ask the question in §1, and say which fight showed it. Each extra is its own decision with its own measurement; never two in one change. Stacking rules on a moment that worked turned it into "a problem to solve" (TFT Reckoning); complexity creeps upward as components pile on (Rosewater).
- Heroes may carry one extra from the start when the role needs it (a tank's shield). The one-at-a-time rule holds after that.
- An extra costs power elsewhere: with an extra, the skill's damage comes down. **(own view)** Built on Riot's proportional rule; confirm it in the probe.
- Simple skills still make deep fights: complexity moves from the card to how cards combine (Rosewater, "Keeping It Simple"). Let synergies, placement and the deck carry the depth.

## 7. Stay inside the engine

- First try an existing kind with new numbers in data. Most new skills are a known shape with a new look, type and damage.
- A shape or effect your sim doesn't hold is a new kind: engine work for dev, and a rule change the human approves first. Write the kind's targeting and effect in one line each so dev can build it.
- Any new kind must give the same log for the same seed and team.

## 8. Readable at battle size

- At battle unit height and the battle camera, beside the stage's other units: in about one second can you tell *who* cast, *on whom*, and *what shape*? (Riot clarity: what matters most draws the most attention; noise stays low.)
- One cue per skill. A second competing cue, or an effect that hides units, fails (TFT's lasting problem was "overly subtle effects or targeting").
- Until the cast exists in the build, judge from the tell and look lines and existing captures, label it agent observation, and rerun on footage.

## 9. Compare against the roster

Before showing anyone, build a short table fresh from data and unit sheets: unit, role, kind, shape, type, tell ticks, damage, extra. Then check:

- On the same stage, no two skills share shape, type and tell.
- Damage sits where your role rules put it (a tank below a damage dealer).
- The new skill asks a question no unit on that stage already asks.

## 10. Presenting options

Each option, in this order, in plain words:

1. **What it does.** One line: shape, type, damage, tell ("Leaps to the farthest hero, physical damage, 0.5 s wind-up").
2. **The scene.** What the player sees when it fires, and what they'll place differently.
3. **Numbers.** The probe result and what it measured.
4. **Extras.** None, or the one extra and the fight that asks for it.

- Give two or three options that differ in shape or tell, not in damage alone. Numbers inside approved bands are yours to tune, not a question.
- Each extra is its own decision. Don't bundle "shape + stun + shield" into one approval.
- Names stay provisional until the human picks.

## Checks before showing anyone

A fail goes back to the step named.

- **One question, one verb.** Placement question in one sentence. (→ 1)
- **Fixed shape.** The target is predictable from the board. (→ 2)
- **Tell fits impact.** Bigger hit, longer and clearer wind-up. (→ 4)
- **Measured.** Probe before and after, same seeds, labelled. (→ 5)
- **Extras.** An enemy skill has none unless a decision added one; never two new at once. (→ 6)
- **No new kind by accident.** Or the new kind is named and sent for approval. (→ 7)
- **Battle size.** Who, on whom, what shape in one look. (→ 8)
- **Roster.** No twin on the same stage. (→ 9)
- **Pillars.** Verb and emotion named. An unkillable final threat's skills never read as something that can be knocked down (`enemy-design`).

## Tuning this skill

Log what the human kept or rejected and why. When two answers point the same way, change the step here. Replace **(own view)** lines when evidence arrives.
