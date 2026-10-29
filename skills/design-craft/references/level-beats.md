# Level beats

How to lay out a stage's rounds, an exploration, a location's choices or a whole run so it rises, rests and ends on a test. Your project's decided level rules and stage pass criteria live in your design doc; this file is the method.

## 1. Yardstick before layout

1. Name the unit: a stage (rounds between stops and the boss), a leg (one exploration), a location (its choices), the run.
2. Collect what three or more games in the genre do for the same unit: length, where the stops are, what the first and last beats ask. Cite each line; mark anything from memory as recall and don't build a number on it.
3. Turn that into pass criteria with numbers you can read from auto-play (round win rate, HP left, idle rounds, minutes). Write them down before building.

## 2. Beat chart

Draw it as a table in the report before editing data. One row per beat.

| Beat | Player meets | New this beat | Intended intensity | Measured (smart) | Rest after? |
| --- | --- | --- | --- | --- | --- |
| R1 | | | low | round win %, HP left | |
| … | | | | | |
| Boss | | | test | | |

- "Intended" is a word (low, rising, peak, rest, test); "Measured" is the auto-play number for it. A beat whose number doesn't match its word gets reworked, not relabelled.
- One new thing per beat at most. If a beat has two, split it or move one.
- Count rests: every stop (exploration, shop, road event) should be followed by a lower beat before the next climb.

## 3. Introduce, develop, twist, conclude

Nintendo's stages teach one idea in four steps (Hayashida; Brown's analysis):

- **Introduce:** the new enemy, card or choice appears alone, where failing is cheap.
- **Develop:** it combines with things the player already knows.
- **Twist:** it turns once in a way the player didn't expect (a pairing, a timing, a place).
- **Conclude:** the beat closes on a test that uses what was learned.

For a round-based stage: a new common enemy shows alone in the first rounds, mixes with known ones before the midpoint stop, gets its pairing turn after it, and the boss round tests the team that answered it. The same four steps fit one location's chain of choices.

## 4. Saw-tooth intensity

- Intensity should climb across the unit with drops after each stop, not in a straight line. Valve's Left 4 Dead director cycles build-up, peak, peak fade and relax; the relax window is what makes the next peak read as a peak (Booth).
- A flat or falling back half is padding. In the numbers it shows as many rounds won with high HP, or many rounds where the player has nothing worth playing; count both in your lane probe.
- If the back half is soft, check first whether it is content (enemy groups) or economy (nothing left to spend on). They have different fixes.

## 5. Locations and choices

- Keep each location to the few things worth trying.
- Each choice should change something later the player can see (a unit found, a fight changed, a place revealed). If a choice changes nothing measurable, merge or cut it.
- Show what opened by what appears on the map, not by a message.
- If time of day or risk level changes the reward, check that in the numbers per condition, not by reading the data.

## 6. Check the layout

- Run a lane probe that keeps only the seeds whose route is the stage in question, at the N in [reading-probe.md](reading-probe.md). A stage the game can't play yet is asked of dev first (`SKILL.md` §3).
- Fill the "Measured" column, compare with the criteria from §1, and change one thing at a time.
- A stage's total difficulty belongs to combat balance. Level work changes the shape (which round is hard) and keeps the stage's average where it was unless the task says otherwise.
