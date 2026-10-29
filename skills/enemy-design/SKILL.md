---
name: enemy-design
description: Design a game enemy, boss or villain before any image exists. Find the slot, write the one question it asks the player and its one core action, build body and behaviour around that, weigh it as a card enemy, boss, villain or unkillable final threat, run the readability and fear checks, name it, and hand it to art. Use when drafting, reviewing or reworking an enemy, boss, villain or eldritch-god concept or its sheet, especially for auto-battlers, card games and horror. Not for 3D source sheets (char-3d-source) or motion (char-anim, blender-anim).
license: MIT
---

# Enemy design: one question, one core action

An enemy exists to change how the player builds their team or board, and to be read in one look. This skill is the method; your project's answers (roster, roles, rules, approved looks, numbers) live in your design docs and data files, read fresh each time. Never copy a value from there into a draft or into this file. Sources: [references/sources.md](references/sources.md). Lines marked **(own view)** have no outside source yet.

The examples assume an auto-battler (the fight runs on its own after the player places units), but most steps hold for any genre.

## Read first

- Your design pillars: which verb and which emotion the enemy serves.
- Your enemy docs: roster, what the engine can already express, the gate for adding an enemy, open issues, where the numbers live.
- Your art bible: period, palette, the reject list, what is already drawn.
- If a rule doc and a newer decision disagree, the newer decision wins; fix the doc or tell its owner.

## 0. Pick the weight

Decide first how much to write, because most enemies are one card.

| Weight | Who | Method |
| --- | --- | --- |
| Card | common and elite enemies | steps 1 to 4, 9, and § Card enemy |
| Boss | stage-end bosses, mindless monster bosses | every step and the full sheet |
| Villain | bosses and mid-bosses with a will | every step, then the villain steps |
| Final threat | an unkillable god or force | steps 1 to 4 and 6 to 10, then § Unkillable final threat |

## 1. The slot

- Name the slot: the stage's roster entry, or the failed balance check that calls for a new enemy. No slot, no enemy. A missing role is not a slot: if an existing enemy already answers the brief, say so before drafting.
- Pick family, weight and exactly one role from your role list. Players learn roles on heroes; reusing them makes an enemy readable before it acts (DOOM: one demon, one job).
- Look at the stage's other enemies. Mix weak, tactical and armoured jobs so one fight asks for more than one answer (Halo's encounter mix).

## 2. The question it asks

One sentence: with this enemy in the fight, how must the player change their placement? An enemy is a number plus a keyword that changes the player's approach (MJ Newman, Arkham Horror LCG). Two questions mean the design has split. Example: "Who guards the back row when this one dives?"

## 3. Weapon, attack verbs, core action

- What it hits with (weapon or body part), two or three attack verbs, range.
- **One core action.** The single strong act that completes the character, written as a moment a camera could hold. The attack verbs, the telegraph, the three habits and the art's key pose all come out of it, so a weak core action weakens every later field.
- Test it the way the Clicker passes (The Last of Us): one act, head jerking and clicking to find its way, carries its blindness, the fungus in its skull and the rule "make noise and you die". If the core action could belong to any monster, rewrite it.
- Card enemies: take the skill from what the engine already holds before asking for a new one (see `skill-design`). Write the data path, never a number.

## 4. Behaviour loop and telegraph

- Whom it targets when the fight opens, how it moves, what it does when hurt or when a neighbour falls.
- Give the big attack its own tell (pose, sound, timing) that no other enemy uses (Hollow Knight; DOOM's exaggerated tells). Show the threat so the decision stays the player's (Into the Breach; Slay the Spire intents). **(own view)** For auto-battlers: nobody dodges, so the telegraph is how the player reads *why they lost* and changes the next placement.
- A gimmick doesn't need a greybox prototype first; test behaviour and numbers where your project tests them (usually a headless auto-play probe).

## 5. Body reason, senses, stages

- How did it get this shape, how does it move, how does it sense? Function, habitat and movement decide form (Neville Page, Ben Olsen). If your monsters are corrupted people, the reason is often how far the corruption has gone, so one family can show stages, the way the Clicker's split skull shows how far the fungus got.
- Give each type one sense the player can learn (proposal: Mark Botta, Game AI Pro 2).

## 6. Motif and period

- Mine real clothes, objects and customs of your setting's period. Show the human what you'd mix.
- Same family, same mark on the body (proposal: Darkest Dungeon II's shared faction hooks), so a new enemy is placed at once.
- For horror: fear comes from the familiar slightly off and from real things more than from the strange (Satoshi Nakai). Show half; let movement tell it before shape does in the dark (Olsen); give only a few facts, as Lovecraft does in "Pickman's Model". Keep human enemies less scary on purpose so the real monster lands (Newman).

## 7. Nature

The telegraph pose, weakness and strength, the grain of sound, smell and motion, and what you deliberately never show. Each weakness should be something a placement can exploit.

## 8. Person or instinct

Body facts (height, build, face, hair, scars), costume and build-up (layers, materials, parts), three habits (waiting, just before attacking, falling), one line or cry, back story. People and bosses get personality, want, wound, weakness, contradiction and voice; mindless monsters get instinct and the trace of who they were. Field list: [references/sheet.md](references/sheet.md).

## 9. Lore paragraph

Gather the fields into one paragraph as a first witness would see it, like a novel: look, motion, sound, smell, with the core action at the centre. Someone who doesn't know the game should picture it from the words alone.

## 10. Locks and no-go lines

Three to five fixed elements every concept must keep; enemies from other works it must not resemble (name what you borrowed and what you changed); the bible's reject list.

## 11. To art

Black silhouette thumbnails first (15 to 30 on one sheet; the human keeps 3 to 5), concepts only inside the kept silhouettes, then shrink to battle-camera size and ask whether it answers the sheet's question, not whether it's well drawn. Black silhouettes alone are hard for many people to judge, so pair a silhouette pick with a rough concept of the real look. Then `char-3d-source`, `char-anim`, and `blender-anim` for non-human parts. The lock into source image, 3D and motion is one way: new story found while drawing goes back into the sheet, and earlier steps win a conflict.

## Card enemy

A card enemy carries one identity line, a basic attack, one skill (effect plus one line of staging), a telegraph, the question, and a shape that reads from far away.

Design top-down: concept first, effect fitted to it, so the whole card feels like the concept. Name, art and effect tell one story; flavour text only fills what they couldn't (Mark Rosewater). With a borrowed folklore or literary monster, take the skill from one line of the original and avoid the ability other famous games already gave it.

Checks. Any fail goes back; write the result at the bottom of the enemy's sheet.

1. **One look.** Name and shape alone suggest what it will do.
2. **One story.** Core action and skill effect are the same act; remove the effect and the concept falls.
3. **Our world.** It touches your setting's own threats; if it fits another game unchanged, it fails.
4. **Board changes.** One placement changes, and that question fits in one sentence.
5. **Weight.** It stands without new engine work; a human enemy is less scary than the monsters.
6. **Not someone else's.** No famous enemy's signature habit; any borrowing is named.
7. **Plain words.** Run a humanizer pass on the text (e.g. https://github.com/blader/humanizer): no inflated words, forced triads or stock lines.
8. **Fear** (monsters only). Familiar but off, not fully shown, told apart by motion alone.

## Boss and villain

- A boss holds one gimmick that turns the board over. The gimmick is the boss's character, and the phases are the order its mind breaks (Hidetaka Miyazaki: a boss needs emotion and contradiction, not only fear).
- Boss fields: thesis (one emotion and its contradiction), what each phase says, how the board changes.
- Villains with a will add the eight steps and three checks in [references/villain.md](references/villain.md).
- Scenes for villain steps 3 to 5 and 7 live in levels and story; write them as a proposal for whoever owns those.

## Unkillable final threat

For cosmic horror: a god that cannot die. It is sealed, or the team holds until dawn. Its name, telegraph and behaviour must never read as something that can be knocked down. Design what it *does* to the board (calls, rings, raises) and what the team breaks or survives instead.

## Checks before showing anyone

A fail goes back to the step named.

- **Slot and question.** Slot named, one question, one role. (→ 1, 2)
- **Core action.** One act; verbs, telegraph, habits and key pose come out of it. (→ 3)
- **Read.** At battle-camera size, black-filled beside the stage's other enemies, it's told apart by shape and by motion. (→ 6, 11)
- **Colour.** None of the heroes' reserved colours (often warm and saturated); the outline melts into the dark if your bible says so. (→ 6)
- **Values.** No numbers in the draft, data paths only.
- **Pillars.** Names the verb and emotion it serves (`design-principles`). A final threat still reads as unkillable.

## Presenting

Draft the whole sheet the way you find most fun, and end it with the branches you dropped, so the human has something to pick from if they scrap it. One enemy per card or image, same size and camera. Names stay provisional until the human picks. 🔴 Paid image generation needs its own approval with a count and cost.

**Names:** make candidates with [references/naming.md](references/naming.md) and let the human pick.

## Tuning this skill

Log what the human kept or rejected and why. When two answers point the same way, change the step here. Replace **(own view)** lines when evidence arrives.
