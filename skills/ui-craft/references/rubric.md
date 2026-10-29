# UI craft rubric: passes 1 to 8

Questions, numbers and evidence for the procedure in [../SKILL.md](../SKILL.md). Tags: **[M]** = mandatory, a fail fails the screen; **[QB]** = runs against your project's own quality bar; diagnostic = measured and reported, never a fail alone. Untagged rows are mandatory questions that need judgement and evidence.

## Pass 1: gate, AI tells [QB]

Run your quality bar's AI-tell list. Any hit = fail, fix, re-run.

## Pass 2: usability, can the player do the job?

Grounding: Hodent's usability pillars (signs and feedback, clarity, form follows function, consistency, minimum workload, error prevention and recovery, flexibility and accessibility) and Nielsen's heuristics applied to games. Hodent's caveat: friction the design *intends* (a hard choice) isn't a usability bug; friction in *reaching* the choice is. TFT puts it as "tough choices, not touch execution".

| ID | Pass/fail question | Evidence |
| --- | --- | --- |
| U-1 | For each job the screen exists for (write them first, e.g. "play a card onto that unit", "read which synergies are active"), can a first-time player do it without help? | **human** task test: job list, attempts, successes, help requests, wrong targets. Agent run is diagnostic only. |
| U-2 | Before acting, does the screen say what will happen? Cost, target and outcome shown at the point of decision (Slay the Spire intents include every modifier; Into the Breach previews every effect). | Capture of the pre-action state per job; list what's shown vs what the rule does in game code. Any hidden outcome = fail. |
| U-3 | Gulf of execution: does the pointer land where the player meant? A drag across a boundary snaps to the intended slot; no double trigger; no input lost during a transition. | Scripted inputs at boundaries and mid-transition (E4), result per input. |
| U-4 | Gulf of evaluation: after acting, can the player tell the new state without reading a log? | Before/after captures; one sentence of "what changed" per action. |
| U-5 | Recognition over recall: nothing the decision needs must be remembered from another screen. | Per decision: info needed, where it is. Anything only on another screen = fail. |
| U-6 | Errors prevented, not explained: invalid actions visibly unavailable before the click; irreversible actions confirmable or undoable; confirmation dialogs not overused (NN/g). | Captures of invalid targets; list of irreversible actions and their guard. |
| U-7 | Minimum workload: clicks and pointer travel per job no more than the job needs; related controls sit together (TFT moved Buy XP, Level and drop rates next to each other). | Click count and travel per job, compared with the previous version. |

## Pass 3: readability at real display size

| ID | Pass/fail question | Evidence |
| --- | --- | --- |
| R-1 [M] | Every text a decision needs is **≥ 18 px on screen at 1080p** (Xbox Accessibility Guideline 101, PC value; console is 26 px). Text inside icons counts. If smaller windows (e.g. Steam Deck) aren't in scope yet, record them without failing. | Font size × scale from E2, per text style. |
| R-2 [M] | Text contrast **≥ 4.5:1** against what's actually behind it; large text (≥ 36 px at 1080p per XAG 102) ≥ 3:1. Computed, not rounded (WCAG 1.4.3). | `contrast.py` on capture pixels (farthest glyph colour vs the backing). |
| R-3 [M] | Meaningful non-text marks (state marks, icons, active outlines) **≥ 3:1** against their background (WCAG 1.4.11). Disabled controls are exempt from the ratio but must still read as disabled. | Same method. A borderline result (e.g. 2.9 to 3.4:1 across states) goes to the human, no silent fix. |
| R-4 [QB] | Grey test (does the screen work in grayscale?), 3-second test (what does a newcomer say the screen is for after 3 s?), at most about 7 information clusters. | Grey capture; **human** 3-second test. |
| R-5 | No meaning by colour alone; check deutan, protan and tritan simulations (Machado 2009). | Simulated captures; pairs that merge must differ by shape or text. |
| R-6 [M] | Text over 3D or art always sits on a flat backing plate (RNIB guidance). | Capture over the busiest scene state (most units, darkest light). |

## Pass 4: hierarchy

| ID | Pass/fail question | Evidence |
| --- | --- | --- |
| H-1 | One primary action per screen, and it's the strongest thing in grey. | Grey capture; name the primary action and the brightest or largest element. |
| H-2 | Reading order matches deciding order: what the player checks first is seen first. | **human**: "what did you look at first, second?" Agent: squint/blur capture (diagnostic). |
| H-3 | Cards rank their information: numbers, name, art first (Hearthstone's three); ornament never competes with cost or stats. | Card capture at rest size; elements listed by grey weight. |
| H-4 | Only what the job needs is on screen (Darkest Dungeon hides gold in the dungeon). | Every element with the job it serves. An element without a job = fail. |
| H-5 | The whole battle state fits one screen with little text; animation explains changes (Hearthstone; Into the Breach's single-screen combat UI). | Capture mid-fight at worst load; count text strings needed to read the state. |

## Pass 5: feedback and timing

| ID | Pass/fail question | Evidence |
| --- | --- | --- |
| F-1 [M] | Every input gets a visible response within **0.1 s (≤ 6 frames at 60 fps)**, Nielsen's limit for "feels instant". Hover, press, pick-up and drop all count. | E4 frame count per input type. |
| F-2 [M] | A transition or decorative motion that holds up the player ends within **1 s** (Nielsen's limit for unbroken flow), unless it's a listed big moment. Waits over 10 s need progress and a way out. | E4 timing per transition. |
| F-3 [M] | Animations never swallow input. Where input must lock (a scoring cascade, as Balatro does), the lock is short and visible, and the result is never hidden. | Scripted input during each lock; log of accepted and ignored. |
| F-4 | Feedback size follows importance: small for frequent events, layered only for big moments (Balatro plays one serial sequence, one thing moving at a time). | Side-by-side captures of a common and a big moment. |
| F-5 [QB] | UI motion comes from one timing sheet; no default fades. | Motion values in one data place; capture. |
| F-6 (diagnostic) | Players can speed up or cut long UI theatre (Balatro's 0.5× to 4× game speed and reduced motion). | Settings list. |

## Pass 6: completeness, the state matrix

Before the review, write a state matrix for every interactive part and every screen: rows = parts, columns = states, each cell = a capture path or `N/A: why`. An empty cell is `unverified`; the screen isn't complete while a needed cell is empty. Approved scope sets the denominator; never drop an `N/A` silently.

**Part states:**

| State | Notes |
| --- | --- |
| rest · hover · pressed · disabled · selected | Every kit button draws all five. Disabled says *why* in a word where the player would otherwise try again. |
| drag: picked up · over valid target · over invalid target · dropped · cancelled | Hand cards, units on the board. An invalid target looks invalid before release. |
| unaffordable / not usable now | Cost shown, payable state distinct. |
| new / changed since last look | Only where the player must notice. |
| keyboard or gamepad focus | `N/A` while the game is mouse only; scope it before any Steam Deck or controller support. |

**Screen states:**

| State | Question |
| --- | --- |
| first entry | Does the screen read on first sight with no prior screen? |
| empty | No cards in hand, empty deck, no units left. Does it say so, or look broken? |
| full / overflow | Max hand, max active effects, top rank, the longest name in every shipped language, largest numbers. Nothing clips or overlaps. |
| loading / waiting | Anything slower than 1 s shows progress (F-2). |
| error | Plain words, what went wrong, what to do (Nielsen #9); text from the data table. |
| transition in / out | Enter and exit both designed; input during both checked (U-3, F-3). |
| interrupt | Window resized, focus lost, alt-tab, pause mid-transition. |
| window sizes | 1920×1080, 1280×800, 16:10, 21:9 (with `aspect="expand"` more space shows; nothing anchors off-screen). |
| dark / danger states | If the scene darkens, the UI stays readable at the darkest. |

## Pass 7: consistency

| ID | Pass/fail question | Evidence |
| --- | --- | --- |
| C-1 | Same mark, same meaning, same colour on every screen (TFT uses one colour language from trait tracker to board). | Inventory: each mark or colour, the screens it's on, its meaning there. One mark with two meanings = fail. |
| C-2 | Every part comes from the UI kit; no one-off panel or button. | Nodes per screen and their kit class. |
| C-3 [QB] | Spacing scale (e.g. 4·8·16·32), monospaced numbers, one title face and one body face. | Measure on capture. |
| C-4 | All screen text comes from the data table and uses the same word for the same thing everywhere. | Grep for UI strings outside the data table; any hit = fail. |
| C-5 | The same character is recognisable across card, portrait, token and 3D unit. | Side-by-side captures. |

## Pass 8: fit and taste

- **G-1 [QB]** The project's own look rules.
- **G-2 Transplant test.** Pasted into another game's screenshot, is it obviously yours?
- **G-3 [M] Taste ledger.** Judge taste against real approved and rejected examples, never invented ones. Keep a ledger of approved and rejected UI decisions with images and the reason. Before review, list the entries that apply and compare at the same size. A new taste call goes to the human.
- **G-4 [M] Seed check.** Hearthstone's UI team "found the seed" early (a physical box) and judged every screen against it. Name your seed (an object from your game's world) and ask of every new part: is it something that exists in that world, and does it behave like that material?
- **G-5 Fit with the core.** Which core verb and which core emotion of your design does this screen serve?

## Genre benchmarks turned into checks

Comparison references at the same size and condition, not rules to copy.

| Game | What the best do | Check |
| --- | --- | --- |
| Slay the Spire | Enemy intent always shown above the enemy, threat as escalating icons, modifiers already applied; StS2 shows several intents side by side. | U-2: is every enemy's next action visible before the player commits? |
| Into the Breach | "Sacrifice cool ideas for the sake of clarity every time"; animated previews instead of text; reliable telegraphs. | U-2, H-5: does the preview show the outcome, and does the outcome always match? |
| Hearthstone | "Our game is UI"; physicality; whole state on one screen; card info ranked numbers, name, art. | H-3, H-5, G-4. |
| TFT | Cause and effect controls adjacent; one colour language across tracker and board; limited board clutter; hover a trait to see its members. | U-7, C-1. |
| Balatro | Feedback as one serial sequence, one moving thing at a time; input lock during scoring; game speed setting. | F-3, F-4, F-6. |
| Darkest Dungeon | If everything is important, nothing is; the screen shows only what the job needs. | H-4. |
| Physical card games | A printed card's anatomy is a tested reading order. | H-3. |

## Sources

*(snippet)* = seen in search results only.

Practice and heuristics
- Celia Hodent, usability pillars and "Game UX = Usability + Engage-ability" (2019): https://celiahodent.com/understanding-the-success-of-fortnite-ux/
- Celia Hodent, 7 usability heuristics at Epic Games (2015): https://celiahodent.com/ux-practices-epic-games/
- Celia Hodent, *The Gamer's Brain*, ch. Usability (CRC Press 2017) *(snippet)*: https://www.taylorfrancis.com/chapters/mono/10.1201/9781315154725-13/usability-celia-hodent
- IxDF, The Game UX Twist *(snippet)*: https://ixdf.org/literature/article/the-game-ux-twist-usability-principles-for-games
- NN/g, 10 Usability Heuristics Applied to Video Games (2019): https://www.nngroup.com/articles/usability-heuristics-applied-video-games/
- NN/g, 10 Usability Heuristics for UI Design: https://www.nngroup.com/articles/ten-usability-heuristics/
- NN/g, Visibility of System Status (2018): https://www.nngroup.com/articles/visibility-system-status/
- NN/g, Response Times: The 3 Important Limits: https://www.nngroup.com/articles/response-times-3-important-limits/
- Pinelle, Wong, Stach, Heuristic evaluation for games (CHI 2008) *(snippet)*: https://doi.org/10.1145/1357054.1357282
- Fagerholt & Lorentzon, Beyond the HUD (Chalmers 2009) *(snippet)*: https://publications.lib.chalmers.se/records/fulltext/111921.pdf
- Game UI Database: https://gameuidatabase.com/

Studio talks
- Derek Sakamoto, Hearthstone: How to Create an Immersive User Interface (GDC 2015): https://www.gamedeveloper.com/design/video-designing-an-immersive-user-interface-for-i-hearthstone-i- · recording *(snippet)*: https://www.youtube.com/watch?v=axkPXCNjOh8
- Hearthstone GDC recap *(snippet)*: https://www.hearthpwn.com/news/797-hearthstone-ui-design-mobile-start-screens-deck
- Hearthstone critique, whole state on one screen *(snippet)*: https://anykeytostart.wordpress.com/2015/03/19/hearthstone/
- Hearthstone card priorities (fan wiki citing devs) *(snippet)*: https://hearthstone.wiki.gg/wiki/Design_and_development_of_Hearthstone
- David Candland, Tenacious Design and the Interface of Destiny (GDC 2016) *(snippet)*: https://www.gdcvault.com/play/1023460/

Accessibility and numbers
- Xbox Accessibility Guideline 101, text display: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/101
- Xbox Accessibility Guideline 102, contrast *(snippet)*: https://devdocs.xbox.com/build/game-principles/accessibility/xag-deep-dives/xag-102-contrast
- WCAG 2.2, 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
- WCAG 2.2, 1.4.11 Non-text Contrast *(snippet)*: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast
- Game Accessibility Guidelines: https://gameaccessibilityguidelines.com/full-list/
- AbleGamers APX, Clear Text: https://accessible.games/accessible-player-experiences/access-patterns/clear-text/
- RNIB, Best Practice in Accessible Gaming (third-party mirror) *(snippet)*: https://app2top.ru/wp-content/uploads/2024/12/RNIB_Best_Practice_in_Accessible_Gaming.pdf

Genre teardowns
- Slay the Spire, War Stories (Ars Technica 2019): https://arstechnica.com/video/watch/war-stories-slay-the-spire-war-stories
- Slay the Spire 2 intents *(snippet)*: https://slaythespire.wiki.gg/wiki/Slay_the_Spire_2:Intent
- Slay the Spire intent arithmetic (teemo.dev) *(snippet)*: https://teemo.dev/game-design/slay-the-spire/systems/combat-energy-block-and-enemy/
- Into the Breach, "sacrifice cool ideas for the sake of clarity" (2018): https://www.gamedeveloper.com/design/-i-into-the-breach-i-dev-on-ui-design-sacrifice-cool-ideas-for-the-sake-of-clarity-every-time-
- Into the Breach Design Postmortem (GDC 2019) *(snippet)*: https://gdcvault.com/play/1025772/-Into-the-Breach-Design
- TFT Interface Update (Riot 2019) *(snippet)*: https://teamfighttactics.leagueoflegends.com/en-us/news/game-updates/tft-interface-update/
- TFT Galaxies learnings, combat clarity (Riot 2020) *(snippet)*: https://teamfighttactics.leagueoflegends.com/en-us/news/dev/dev-teamfight-tactics-galaxies-learnings/
- TFT Fates art blast (ArtStation 2020) *(snippet)*: https://magazine.artstation.com/2020/10/riot-games-teamfight-tactics-fates-league-of-legends-art-blast/
- TFT design lessons, "tough choices, not touch execution" (Pocket Tactics on GDC 2020) *(snippet)*: https://www.pockettactics.com/teamfight-tactics-design
- Balatro game feel and juice (teemo.dev, reverse-engineered): https://teemo.dev/game-design/balatro/systems/game-feel-and-juice/
