# Sources

*checked* = page or text opened; *excerpt* = seen in a search excerpt, a table of contents or a transcript excerpt only, so treat wording as approximate. **Strength** as used in `SKILL.md`: **rule** = two independent sources, an official doc, or repeated field practice; **proposal** = one source. Tune proposals when play disagrees.

## Testing a change and handoff

| Source | Author | URL / ISBN | Published | Claim it supports | Seen |
| --- | --- | --- | --- | --- | --- |
| The Art of Game Design, 3rd ed., ch. 8 | Jesse Schell | https://www.oreilly.com/library/view/the-art-of/9781351803632/xhtml/C11_chapter8.xhtml | 2019 | "Prototyping Tip #1: Answer a Question" | excerpt (contents) |
| Game Design Workshop, 4th ed., ch. 7 | Tracy Fullerton | ISBN 978-1-138-09877-0 | 2018 | Decide what a prototype is for: "Are you trying to answer game design or technical questions?" | excerpt (publisher preview) |
| Designing Games, ch. 11 "Grayboxing" | Tynan Sylvester | https://www.oreilly.com/library/view/designing-games/9781449338015/ch11.html ; quote via https://blog.punygames.com/designing-games-book/ | 2013 | What runs, not a design doc, is the design's real spec | excerpt (secondary quote) |
| Design Logs | Daniel Cook | https://lostgarden.com/2011/05/03/game-design-logs/ | 2011 | "Make something you can play as soon as humanly possible." | excerpt |
| Visualizing the Creative Process | Daniel Cook | https://lostgarden.com/2010/08/17/visualizing-the-creative-process/ | 2010 | "Make your ideas real as quickly as possible." | excerpt |
| One Page Designs (GDC 2010 slides) | Stone Librande | http://www.stonetronix.com/gdc-2010/ | 2010 | Keep the written part short: "Most people don't read past the first page" | excerpt (slide text) |

**Strength:** one question per change = **rule** (Schell + Fullerton). Try it in the running game, keep the written part short = **rule** (Sylvester + Cook, with Librande on short docs). Switch with default unchanged, measure line in the handoff = **rule** by field practice.

## Reading the auto-play

| Source | Author | URL / ISBN | Published | Claim it supports | Seen |
| --- | --- | --- | --- | --- | --- |
| Automated Playtesting with Procedural Personas through MCTS with Evolved Heuristics | Holmgård, Green, Liapis, Togelius | https://arxiv.org/abs/1802.06881 | 2018 | Bot personas are a tool "when human feedback is not readily available" | checked (abstract) |
| AI-based playtesting of contemporary board games (FDG 2017) | de Mesentier Silva, Lee, Togelius, Nealen | https://dl.acm.org/doi/10.1145/3102071.3102105 | 2017 | Agents with different play styles give a profile that characterises the content | excerpt (abstract) |
| Simulating Mechanics to Study Emergence in Games (AIIDE 2011) | Joris Dormans | https://doi.org/10.1609/aiide.v7i3.12477 | 2011 | 1,000 simulated runs per setting; sim tweaks don't prove "a perfectly balanced game" | excerpt (paper text) |
| 'Slay the Spire': Metrics Driven Design and Balance (GDC 2019) | Anthony Giovannetti | https://www.gdcvault.com/play/1026309/-Slay-the-Spire-Metrics | 2019 | Balance aim is a place for every card, "not … making every card equally good" | excerpt (transcript) |
| Champion Balance Framework | Riot Games | https://www.leagueoflegends.com/en-us/news/dev/dev-champion-balance-framework/ | 2019 | Win rate is the main power signal; play rate is not; small samples at the top limit the reading | checked |
| Experimental Design for Simulation (WSC 2003) | W. David Kelton, Russell R. Barton | https://dl.acm.org/doi/pdf/10.5555/1030818.1030828 | 2003 | Common random numbers "can sometimes greatly reduce the variance" of a comparison | excerpt |
| Variance-Reduction Techniques (course slides) | W. David Kelton | https://www3.cs.stonybrook.edu/~cse529/chap11.pdf | undated | Compare alternatives on the same random inputs, streams kept in sync | excerpt |
| NIST/SEMATECH e-Handbook 7.2.4.1 | NIST | https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm | undated | Standard error and interval of a proportion | excerpt |

**Strength:** same seeds, paired difference = **rule** (Kelton & Barton). ± standard error on every rate = **rule** (NIST). A bot is not a playtest = **rule** (Holmgård + Dormans). Policy spread as the sign that decisions matter = **proposal** (de Mesentier Silva). Win rate as the main signal = **rule** (Riot + Giovannetti).

## Level beats

| Source | Author | URL / ISBN | Published | Claim it supports | Seen |
| --- | --- | --- | --- | --- | --- |
| The secret to Mario level design | Christian Nutt, interviewing Koichi Hayashida | https://www.gamedeveloper.com/design/the-secret-to-i-mario-i-level-design | 2012 | Stages follow kishōtenketsu: introduce, develop, twist, conclude | excerpt |
| Super Mario 3D World's 4 Step Level Design | Mark Brown (Game Maker's Toolkit) | https://www.youtube.com/watch?v=dBmIkEvEBtA | 2015 | "Stages are four-part self-contained showcases for new ideas" | excerpt (transcript) |
| The AI Systems of Left 4 Dead (GDC 2009) | Michael Booth | https://steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf | 2009 | Build up, sustain peak, peak fade, relax; relax keeps the threat low for a while | excerpt (slide text) |
| Level Up!, 3rd ed., "The Beat Chart" | Scott Rogers | ISBN 978-1-394-29877-8 | 2024 | A beat chart is a standard planning step | excerpt (contents) |
| An Architectural Approach to Level Design, 2nd ed. | Christopher W. Totten | https://www.routledge.com/Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367 | 2019 | Pacing as a level workflow | excerpt (contents) |
| Hades' Level Design Is Less Random Than It Seems | Nathan Grayson, quoting Ed Gorinstein | https://kotaku.com/hades-level-design-is-less-random-than-it-seems-1845254545 | 2020 | Room-to-room pacing shaped the encounter design | excerpt |

**Strength:** introduce, develop, twist, conclude = **rule** (Hayashida + Brown). Saw-tooth with rests = **rule** (Booth + Hades). Beat chart table = **rule** (Rogers + Totten).

## Not found (left out)

- A Riot TFT post defining a top-4 rate framework; only "4th place or higher should feel like a win" (TFT Set 1 Learnings, 2019). Not used.
- Supercell's prototype pipeline from Supercell itself; only press coverage. Not used.
- The full Giovannetti transcript; only the opening and one passage.
