---
name: ui-craft
description: Production-level yardstick for reviewing game UI (screens, HUDs, cards, buttons, panels, UI motion) in ten ordered passes covering usability, readability, hierarchy, feedback timing, completeness via a state matrix, consistency and fit, each with pass/fail questions, numbers (18 px text at 1080p, 4.5:1 and 3:1 contrast, 0.1 s response, 1 s transitions) and the evidence it needs, plus a WCAG contrast script. Use when making, fixing or reviewing game UI, an HTML mock or an engine screen capture, or when a UI looks generic, cluttered, unreadable, half-finished, or like it could belong to any game.
license: MIT
---

# UI craft: reviewing a screen to production level

UI makes the game's first impression, so every UI review checks quality, completeness and fit against a written yardstick.

The bar: **the player reads the state, knows what they can do, sees that it worked, and it looks like nothing but this game.** Usability first, then completeness, then fit. A screen that looks great but fails usability isn't done; a screen that works but could be any game isn't done either.

## What this skill assumes

- A Godot (or similar) project whose UI scales from a 1920×1080 design size (Godot: stretch mode `canvas_items`), a UI kit folder of shared parts, and all screen text in one data table.
- Your project's own written **UI quality bar**: an AI-tell list (defaults that make a UI look generated or generic, such as stock gradients, blur and translucent panels, default fades, mismatched icon styles, ornament competing with numbers), the project's look rules, spacing scale and motion timing sheet. Passes 1 and 8 run against it. If you have none, write one first.
- The `design-principles` skill for the cross-discipline questions (gulfs of execution and evaluation, affordance, cognitive load); pass 2 turns them into UI tests with evidence.

## Review procedure

Run passes 0 to 9 in order; questions, numbers and evidence are in [references/rubric.md](references/rubric.md). A fail in pass 1 stops the review.

0. **Set up the evidence** (below).
1. **Gate: AI tells.** Your quality bar's tell list. Any hit = fail, fix, re-run.
2. **Usability** U-1 to U-7: can a first-time player do each job the screen exists for?
3. **Readability** R-1 to R-6: text size and contrast at real display size, colour-blind safety, backing plates.
4. **Hierarchy** H-1 to H-5: one primary action, reading order = deciding order, only what the job needs.
5. **Feedback and timing** F-1 to F-6: response within 0.1 s, blocking transitions within 1 s, input never swallowed.
6. **Completeness:** the state matrix; every part and screen state has a capture or `N/A: why`.
7. **Consistency** C-1 to C-5: one mark one meaning, kit parts only, text from the data table.
8. **Fit and taste** G-1 to G-5: project look rules, transplant test, taste ledger, seed check, core verb and emotion.
9. **Verdict and record.**

Evidence rules:

- Anything without evidence is `unverified`, never a pass.
- `human` in the rubric means a real person, counted per participant and attempt. Label agent observation as such; it never stands in for a human test.
- Criteria marked mandatory fail the screen. Diagnostic criteria are measured and reported, never a fail alone. If a criterion flags something that touches an approved value (size, colour, timing), don't fix it silently: show it to the human and let them decide.

### Pass 0: set up the evidence

- **E1 Real artifact.** Review the engine scene or build, not only an HTML mock. A mock may pass passes 1, 3, 4, 7 and 8 as a direction check; it can't pass 2, 5 or 6.
- **E2 Two display sizes.** Capture at **1920×1080** and in a **1280×800 window** (Steam Deck size). With `canvas_items` stretch from 1920×1080, on-screen px = design px × min(w/1920, h/1080), 0.667 at 1280×800. Look at captures at 100 %, never scaled down.
- **E3 Same conditions as the approved reference.** Same camera, scene, seed and speed, with the approved reference image beside it.
- **E4 Motion capture.** For timing, record a movie: `godot --path game --write-movie /tmp/ui/<screen>.avi --fixed-fps 60 --quit-after <frames> <scene>`, with a preview scene that injects the input at a known frame (`Input.parse_input_event`). Count frames from input to the first visible change. Pictures need a window; headless renders none.

### Pass 9: verdict and record

- Write results in the deliverable's `review.md`, one line of evidence per verdict (where, what): mandatory or diagnostic, conditions, method, denominator, source, result, evidence path, status.
- Use one of four verdicts: **needs new work**, **not enough evidence**, **meets the bar**, **human's call** (taste or an approved value is at stake). A diagnostic that proves an approved rule broken is a defect.
- When you show the human, use one state or candidate per image, same size and camera, readable at phone width.

## Tools

- `scripts/contrast.py`: WCAG contrast between two colours, or between the farthest glyph pixel and the median background of two boxes in a capture (R-2, R-3). Box mode needs Pillow and numpy.
  - `python3 scripts/contrast.py '#1c1a17' '#e9dcc0'`
  - `python3 scripts/contrast.py shot.png --fg x,y,w,h --bg x,y,w,h` (fg box = glyph or mark, bg box = what's behind it).
- Colour-blind simulation (R-5): the Machado, Oliveira and Fernandes 2009 matrices for deutan, protan and tritan (implemented in e.g. the `colorspacious` and `daltonlens` Python packages).
- Frame counts (F-1 to F-3): the E4 movie, stepped frame by frame (e.g. `ffmpeg -i x.avi frames/%04d.png`).

## Not done

- Reviewing only a scaled-down screenshot, or only the HTML mock when the screen exists in the engine.
- Calling a check passed without its evidence line, or calling an agent run a playtest.
- Inventing taste: fit is judged against the ledger of approved and rejected examples; a new taste call goes to the human.
- Changing an approved value (size, colour, timing) to meet a criterion without the human's decision.
