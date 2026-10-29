# Readability at battle size: method and traps

The art bible says what must read (brightness order, a calm play area, the brightest place beside the characters). This page is how to check it on a shot, and the traps that skew the numbers.

## Why value, measured on the edge

- A unit reads when its outline differs in lightness from what is right behind it. Hue alone fails in the dark and in grayscale, so measure lightness first (CIE L*, 0 to 100, perceptual) [5, 6, 7].
- A whole-body average hides a lost edge: a white costume on a pale patch can have a good mean and no outline. So the measure compares the local mean just inside and just outside along the silhouette, and reports the median step (edge dL) and the share of outline under 8 L* (weak edge).
- Units standing together count as one group; overlapping characters count as one shape.
- Grayscale is a proxy, not a verdict: it knows nothing about motion, focus or intent [18]. It catches the common failure (a unit sinking into the ground); a person at battle size judges the rest.

## The shot set for one proposal

Same camera, cells, reference characters and seed in every shot; only the thing under test changes.

1. Baseline: the approved set through the same scene.
2. Each option in the main battle light, with a character mask and a units mask.
3. The darkest state (e.g. max danger): does the world fall to black while the character light pools stay?
4. Any other light state the place ships.
5. The HUD composite of each: what sits under each HUD panel.
6. Grayscale copies when value is the question.

Measure 2 and 3 for the baseline and every option, and put the numbers side by side in the report, each with what it measures.

## Reading the numbers

- **Character edge dL** up or equal versus baseline: the set doesn't hurt the characters. Report the mean and the weakest unit, since the weakest unit is the one a player loses.
- **Enemy edge dL**: lower than heroes by design if your brightness order says so, but the weakest enemy must not vanish. Rows far from the camera, under a darkening screen band, are the usual worst case.
- **Brightest tile**: on a hero's light pool is right. If the brightest tile away from heroes beats the heroes' pools, a lamp or window is too loud.
- **Ground under the board**: darker and calmer than the ring around the characters. A rise when board marks are on shows how loud the board is on this floor.
- Without an approved pass mark, write "versus baseline", never "passes".

## Traps

- **Different lamp reach.** If the check scene lights the baseline and the new set with different reach, the comparison measures the lamp, not the set. Pass the reach explicitly in every comparison.
- **Random clip start.** An idle clip that starts at a random frame can spread edge dL by about ±1.5 L* between identical runs. Take three runs and report the spread before calling a difference real.
- **Board drawn differently.** An art scene that draws the board through a different path than the game (e.g. a transparent viewport) under-draws it. Compare board looks in a game capture.
- **Lift one thing at a time.** A floor too dark loses enemy outlines; lift it in steps until it matches the baseline, measuring each step with nothing else changed.
- **The HUD covers landmarks.** The best spots in a clean shot often sit under a HUD panel. Plan landmarks against the composite.

## What the numbers don't tell you

- The set's frame time in the game.
- How it looks to a person at battle size; an agent's observation never stands in for that.
- Taste and fit (era, mood, "is this our game"): show those to the human as images.
