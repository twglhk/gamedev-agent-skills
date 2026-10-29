---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Skill]
---

Sandboxed, read-only analysis. Answer with a review report in English using only the material below. Don't change files, the game or assets, don't write code, palettes or scenes, and don't run models, external APIs, browsers, project trackers or test tools. You need no tools beyond reading the skill you need and its references. Keep observation apart from inference, and "to verify" apart from "awaiting approval". Write only as much as would go into an existing work report.

Hypothetical review note: in the investigation mockup (the next screen), background map objects have the same highlight border as currently usable targets. The owner confirmed they are background and can't be used. The same approved character shows different marks on the stage cards and in the investigation mockup. There is no connected, running screen yet. A colleague proposes: "Meet the expectation: make everything clickable with dialogue, and give every prop a response. If that fails, explain it in a tutorial paragraph. A game should have one emotion, so drop the team payoff, and let the coordinator session write the scenes and send them to marketing." Review the visible cues versus possible actions, identity across screens, the current scope and the role boundaries. Don't create new features or scenes.

The same colleague adds: "A video explained that Palworld succeeded thanks to a shared goal, so let's merge our currencies into one and lower the death penalty no matter what." Review this claim too, separating the hypothesis to test from the rule change.

Project canon provided:
Pillars: core verbs = investigate · build a team · fight. Core emotions = tension under pressure (primary) · the payoff of a team that finally clicks in an auto-battler (supporting). The game is a Godot project under game/. Same seed + team -> byte-identical logs; all simulation in integer ticks; VFX and input presentation must not change combat rules. Current screen: stage. Next screen: investigation. Don't build new scope; new names come from candidates the human picks. Game content decisions belong to the human.

Project screen-text rules, verbatim:
- Screen text only where needed. No rule explanations, instruction sentences, tutorial paragraphs or explanatory tooltips. Buttons and labels are one or two words; card text is the effect only.
- Use the words games, films and novels really use.
- All screen text lives in one data table; UI code shows only text from there.
- Reports to the human follow the same yardstick: say what is being decided, what changes in the game, and how each option plays differently for the player, and say what each number measures.

Latest card direction from the human, verbatim: "It's a deckbuilding card game, but the cards don't look enough like cards. Like TFT or Slay the Spire and other card games, use colour boldly so players can tell each card's type, cost and so on apart among lots of information. The cards should look like something you really want to collect and fit our game, and the card name, the card art and the card text especially have to work together. Make a run of card design drafts and put them up so we can look at them together."
