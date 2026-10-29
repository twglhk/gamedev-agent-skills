---
name: design-principles
description: Checklist for reviewing game design, game UI, controls, feedback and card readability against the project's core experience, plus a method for finding a genre-breaking core constraint. Separates what the player expects from what the game actually does, input forgiveness from hidden result fudging, and observation from playtest. Use before deciding or reviewing game rules, systems, screens, locations, characters, enemies, controls, feedback or card layouts, before handing a prototype to dev, or when play feels generic, wordy or like a clone.
license: MIT
---

# Design principles checklist

Part A asks about the core experience and consistency; part B asks about a genre-breaking core constraint. Don't run every item every time; pick the ones the task touches.

- Turn examples into questions for the current task. Don't copy them as rules.
- 🔴 **Answers don't go in this file.** The project's core verbs, core emotions, core constraint, kill list and check results live in your design doc. This file holds only how to ask.
- 🔴 **The human picks the core emotions and the core constraint.** The agent proposes candidates with reasons and shows them side by side. Once the design doc holds a value, use it as the yardstick for every check.
- Per-discipline questions, the limits of the evidence and the probability note: [references/player-expectations.md](references/player-expectations.md). They don't replace the craft skills.
- Part B in full: [references/core-constraint.md](references/core-constraint.md).

## Checking one task

1. From the design doc, name the verb and emotion this task should grow and what the player is trying to do. Don't copy the doc's rules here.
2. Look at the current screen, sound and response, and write first what the player will expect to do and expect to happen. Keep apart the intent, the way to carry it out (execution), and reading the current state and result (evaluation).
3. Check what the player can actually do and how the game answers, then pick only the A and B questions that apply. Anything not built is unchecked. A picture review or a proposal is not a playtest; never call it one.
4. Note it in the existing report as `observation → effect on the player → evidence / approval still needed`. Keep what you verified (screen, reproduced input, log) apart from what you inferred. No separate full document needed.
5. A proposal that changes a rule, a parameter, the scope or a name goes through the normal approval path. Don't add features to meet an expectation, and don't decide game content on the human's behalf.

## 0. Compass: ask this before shipping anything

- [ ] **Pillars and core loop.** Open the design doc's pillars (logline, core verbs, core emotions) and the core loop, and write which verb, emotion and loop step this task grows. If it reaches none, it's a kill-list candidate. Check that it builds on the real game build and doesn't blur the game's differentiators.

## A. Core experience and consistency

### A1. Core experience

- [ ] Do the primary and supporting emotions combine the way the doc intends? Don't collapse two emotions into one or force a single emotion on every game. Ask which leads in this scene and, if they clash, which action causes the clash.
- [ ] Do this task's costs, failures and rewards serve that experience? Compare the trade-offs of flipping time, damage, resources, growth or recruitment, but leave removal to the human. The kill list holds candidates, not delete orders.

### A2. Feel and the gulf of execution

- [ ] Where do the player's intent and their input part? Reproduce clicks on map and card edges, drags, and input during transitions. Input buffering, snapping and larger hit areas are candidates to test in context. Celeste's coyote time and forgiveness windows are examples, not universal timings or an order to build them.
- [ ] Is the correction predictable, and does it avoid picking another target, double input or an unintended spend? Check separately that the player can see the input was received and can read the resulting state. Don't promise the same curve or perfect trust for every move.
- [ ] Have you kept input forgiveness apart from changing odds or outcomes? Quietly forcing a success after three misses is not input correction. Determinism doesn't license a hidden odds change either. Rule and parameter changes get approval first.
- [ ] For simulation games: with the same seed, team and inputs, is the battle log byte-identical? The sim runs on integer ticks and no wall-clock or float time. Input display and VFX never change combat rules.

### A3. Visual and interaction feedback (affordance and detail)

- [ ] Have you listed the visible cues and the actually possible actions separately? Does a map object that looks clickable, a background figure or a locked exit falsely promise an action? For a mismatch, first compare toning the cue down with making the existing action clearer. Don't bolt a new feature or tutorial onto every expectation.
- [ ] Does each response detail help read the action, the character or the emotion? Hitstop, shake and transition motion are candidates to test in context, not fixed frame rules. Cut them back if they delay input feedback or hide an important result. Not every prop needs a response.

### A4. UI cognitive load

- [ ] Use colour boldly, but is meaning carried by icon, shape or a short word too? Never split meaning by colour alone, and don't strip every word either. Screen text follows the project's text rules.
- [ ] For card games: are card type and cost read through distinct channels? Do name, art and effect text have a hierarchy and harmony that help fast identification and the feeling that a card is worth collecting? Don't create the real palette, assets or card rules here. Check that the same character reads as the same person across card, token and 3D model, using already approved assets.
- [ ] Are the cost, state and target needed for a choice close together? Do the same marks keep their meaning, and characters their identity, from screen to screen? Real card drafts and their review belong to the UI work scope.
- Numbers, state tables and evidence for reviewing an actual UI screen, card or HUD are in the `ui-craft` skill.

### A5. Loop and switching cost

- [ ] Moving between phases (for example exploration, team building and combat), how much does it cost the player to find the next goal again and see what earlier choices did? "A shared goal lowers switching cost" is a hypothesis to test. Don't force a single currency or call it the reason a particular game succeeded.
- [ ] Does the cost of re-deciding and retrying after a failure fit the intended emotion? Observe lost time, lost resources and what can be undone, but don't treat softer death penalties as a universal fix. Cost and rule changes go out only as approval candidates with evidence.

## B. Core constraint

Name five "obvious" genre elements, flip or remove one entirely, and design only what that constraint makes possible. Full checklist: [references/core-constraint.md](references/core-constraint.md).
