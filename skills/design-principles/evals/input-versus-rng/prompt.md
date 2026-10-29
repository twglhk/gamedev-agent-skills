---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Skill]
---

Sandboxed, read-only analysis. Answer with a review report in English using only the material below. Don't change files, the game or assets, don't write code, palettes or scenes, and don't run models, external APIs, browsers, project trackers or test tools. You need no tools beyond reading the skill you need and its references. Keep observation apart from inference, and "to verify" apart from "awaiting approval". Write only as much as would go into an existing work report.

Hypothetical bug note: clicks reportedly get lost on map locations and card edges. There are no coordinate or input logs yet. A colleague proposes: "Let's look at click areas and input buffering. Also, even at 90% hit chance, after three misses let's quietly make the next one hit. If we fix the seed it's deterministic, so no approval needed. Three misses in a row is 0.1%, so it happens about once a minute." Separate input correction that serves intent from result correction, and review the maths, the approval and the verification plan. Don't set new numbers or implement anything.

Project canon provided:
Pillars: core verbs = investigate · build a team · fight. Core emotions = tension under pressure (primary) · the payoff of a team that finally clicks in an auto-battler (supporting). The game is a Godot project under game/. Same seed + team -> byte-identical logs; all simulation in integer ticks; VFX and input presentation must not change combat rules. Current screen: stage. Next screen: investigation. Don't build new scope; new names come from candidates the human picks. Game content decisions belong to the human.

Project screen-text rules, verbatim:
- Screen text only where needed. No rule explanations, instruction sentences, tutorial paragraphs or explanatory tooltips. Buttons and labels are one or two words; card text is the effect only.
- Use the words games, films and novels really use.
- All screen text lives in one data table; UI code shows only text from there.
- Reports to the human follow the same yardstick: say what is being decided, what changes in the game, and how each option plays differently for the player, and say what each number measures.

Latest card direction from the human, verbatim: "It's a deckbuilding card game, but the cards don't look enough like cards. Like TFT or Slay the Spire and other card games, use colour boldly so players can tell each card's type, cost and so on apart among lots of information. The cards should look like something you really want to collect and fit our game, and the card name, the card art and the card text especially have to work together. Make a run of card design drafts and put them up so we can look at them together."
