---
name: fx-craft
description: Build and measure game VFX, shaders and sound in Godot 4 to a professional bar. Research references first, block out in grayscale, build on a strength ladder with a performance budget, record every moment with one capture tool (scripts/capture.py) and pass a numeric rubric for contrast, timing, sync, loudness and frame cost. Use when making, fixing or reviewing any VFX, particle, shader, screen shake, hitstop, game feel, SFX, ambience, music or loudness, or when an effect looks flat, a sound feels weak or off-sync, or effects cost frames.
license: MIT
---

# Game feel: building and measuring effects and sound

The bar: **each moment feeds one emotion, and picture and sound hit with the same strength on the same frame.** Aim for the detail a top industry designer would ship. So research before building, and measure after.

## Conventions this skill assumes

Adapt the paths to your project.

- Godot 4.x project in `game/`. Effect scenes in `game/fx/<moment>.tscn`, each started by one call, `play(strength)`. Preview scenes in `game/fx/preview/`, shaders in `game/shaders/`, tests in `game/tests/fx/`, finished audio in `game/audio/`.
- Strength, length, shake and volume values live in one tuning resource (e.g. `game/fx/fx_tuning.tres`), never in effect code.
- Working notes per moment in `design/fx/<moment>/` (`notes.md`, raw takes, prompts).
- A **moment table** in your design doc: one row per moment with its effect, sound, strength and emotion. Four strengths (weak, medium, strong, max). Pick the emotions your game needs (the examples here use thrill, hope, dread).
- A simulation that can hash its own log (`log_hash()` or similar), so you can prove effects don't change the outcome.
- `scripts/capture.py` drives the Godot binary with Movie Maker (`--write-movie`), needs ffmpeg, numpy and Pillow, and takes `--godot`, `--project`, `--size` and `--font` before the subcommand (defaults: `godot`, `game`, `1920x1080`, Pillow's font). Preview scenes must start with the effect not yet visible, play the moment once, and accept their own args after `--`. `perf` also needs the scene to take `--qa-out=PATH` and write frame-time JSON (format in the script's header). Recording opens a window: headless Godot renders no picture.

## Hard rules

- 🔴 **Determinism.** Effects and sound only watch. Hitstop pauses the view's feeding of ticks to the display, never `Engine.time_scale` or simulation code. Prove it: the sim's log hash is identical with effects on and off.
- 🔴 **Money and licences.** Ask the human before spending on sound tools, libraries or generation credits (how many, estimated cost). Load the `elevenlabs` skill before generating anything there. Keep credits in an attribution file in the game.
- 🔴 **AI generation.** Images and video only as reference and raw material, asked for each time, logged. See "Using AI" below.
- 🔴 **What a sound is made of.** The identity the ear hears (note, instrument, material) is recorded: a real instrument, a real object, a library recording, or a generated take. A code synth (sine and noise mixes) is a timing placeholder. It may sit under recorded material as support (sub thump, falling sweep) on unpitched sounds only; it is never a candidate, never the result, never in a pitched sound.
- 🔴 **Say what made it.** Every candidate states, per sound, its source in plain words (which instrument recording, which library, which generated prompt, which synth layer). Never "unchanged" or "the current sound".
- On-screen text (skill names, numbers) reads from your game's text data, not from effect code.

## Procedure: one moment, start to finish

1. **Pick the moment.** One row of the table. Its strength sets size, brightness, length and volume.
2. **Direction note.** One sentence (who, what, which emotion) plus the beats: anticipation, contact, dissipation, in 60 fps frames. Starting values in [references/vfx.md](references/vfx.md) "Beat starting values". Add one line on motion inside the beats (pop then settle, erode from inside, ease-out shards).
3. **Reference research (never skip).** Find 2 or 3 moments of the same kind in top games and step through them frame by frame. Write down frame counts, layers, how brightness and colour rise and fall, and how many sound layers. Three lines in `design/fx/<moment>/notes.md`.
   - Where: realtimevfx.com breakdowns, 80.lv, GDC Vault, ArtStation, frame-stepped gameplay video.
   - Who: cards, stacking, upgrades, synergies = Balatro, Teamfight Tactics, Marvel Snap, Slay the Spire. Hits and skills = Hades, Guilty Gear Xrd. Horror, darkness, death = Darkest Dungeon, Inside. Bosses = Hades, Darkest Dungeon. Wins and rewards = Nintendo, Hades, Hearthstone ([references/sound.md](references/sound.md) §7).
   - 🔴 **No research, no build.** If search is blocked and you would be working from memory, stop and report it as blocked. "From memory, unchecked" is not research.
4. **Grayscale first.** Build with shape, value and timing only and capture from the game camera. An effect that doesn't read in gray can't be saved by colour (Riot VFX style guide). Colour comes after, from your art palette.
5. **Build in Godot.** [references/vfx.md](references/vfx.md). Stay inside the strength's budget (live count, particles, screen area: vfx.md §5). Technique choice and Godot traps: [references/shaders.md](references/shaders.md). Frame cost and measuring it in a real fight: [references/perf.md](references/perf.md).
6. **Build the sound.** [references/sound.md](references/sound.md); generation through the `elevenlabs` skill. Raw takes and prompt logs stay in `design/fx/<moment>/`, only finished files go to `game/audio/` (Git LFS).
   - The sound contract states length, pitch, **which instrument or material it must sound like, and how the feeling moves** (dark to light, collapse). A placeholder file is not a contract: "keep the v1 chord" freezes a synth into the result.
   - An agent can't hear. Measured pitch, level and length are not evidence a sound is good. Evidence of quality is the source material and the comparison with references (layers, instruments, length). Say so in the candidate.
7. **Capture and measure.** Every moment uses the same tool: `record` (Movie Maker, frame-count check) → `media` (1:1 game-size crops, key frames from the contact found in the picture, colour and gray) → `measure` (rubric numbers and screen area) → `perf` (on/off, 5 runs each). Commands in [references/rubric.md](references/rubric.md) "How to measure". If the tool lacks something, add it to `capture.py` rather than writing a one-off script.
8. **Rubric gate.** Pass all of [references/rubric.md](references/rubric.md) before showing anyone. Fix one failure at a time and recapture; change one thing per pass so you know what worked.
9. **Ask the human.** Show the game-size clip, gray version, reference clips and key frames as separate attachments (never one collage), with the measured numbers in the text. Record feedback in `notes.md`.
10. **Hand off.** Wiring the effect into someone else's scene (the battle view) goes to the dev lane: which event triggers what, the strength name, the preview scene path. If the battle log has no list of view events yet, that list comes first.

## Principles

Evidence and numbers are in the references; this is what to keep in your head while building.

- **Three beats.** Anticipation → contact → dissipation. Contact is short (a 1 to 3 frame flash) and brightness only falls after it. Dissipation (smoke, embers, afterglow) is long and gives the eye time to read.
- **Motion inside a beat.** Never linear. Contact appears small and pops to full size in 2 frames, fast then slowing. Dissipation erodes in steps from the centre. Shards fly out with ease-out and vanish slightly after the body.
- **Value first, colour later.** In gray, centre (brightest), middle and edge must separate.
- **Shape language.** Spiky = danger and damage (enemy side). Round = safety, healing, protection (player side).
- **Hierarchy = strength.** The more important the moment, the bigger, brighter and longer. If a basic hit fills the screen, the level-up gets buried. Save hitstop, shake, flash and slow motion for strong and max; spend them on weak and strong has nothing left.
- **Budget per strength.** Strength caps live count, particles and screen area, not just size. Frequent weak moments get the tightest cap. Measure performance on and off, alternating, 5 runs each, never once.
- **Build cheap.** An effect's cost is screen pixels (overdraw) and first-draw pipeline compiles, not triangles. Fit quads to the shape, alpha scissor, `unshaded`, no shadows, `amount` sized to the strongest use, reuse existing shaders' uniforms before adding a shader, and instantiate each effect once, hidden, when the level opens ([references/perf.md](references/perf.md)).
- **One family, one grammar.** Effects of one side share beats, shapes and palette; a moment differs only in a secondary element.
- **One with the toon style** (if your game is toon-shaded). Stepped (scissored) alpha, hand-drawn texture and ink lines as thick as the bodies' instead of realistic soft smoke or normal-mapped detail (Guilty Gear Xrd). Enemy effects carve darkness with ink rather than adding light, with an eerie glow only at the edge.
- **Sound on the same frame.** The sound's first peak lands on the contact frame. One sound = three layers (front = click, body = weight, tail = space) on separate frequency bands.
- **Clear the room before a big moment.** A short silence and darkness before a boss death makes the light and harmony after it land harder (the silences of Limbo and Inside).
- **Frequent = small and varied.** Hits, card plays and stacks that fire hundreds of times a match are short and small, have several variants, and never repeat back to back.
- **Wins are music (round and boss wins only).** Use a short phrase (sting) played on real instruments. Layers and lengths in [references/sound.md](references/sound.md) §7.
- **Moments where the team grows are punchy SFX.** Level-up, synergy, reward and hits are not musical phrases. They strike on the frame (onset within 6 ms) and their tail glows bright for 0.6 to 1.5 s. Generate front, body and tail separately and layer them; raise tiers with a step (one scale degree) and an extra layer on the same sound. Measured references in [references/sound.md](references/sound.md) §8.

## Using AI

- **Code-writing AI is the main use.** Shaders, particles and capture scripts are written by the agent as code. Today that's the only AI route to shippable effects; practitioners put image generation at about 5% of the work.
- **Image and video generation only for two things:** reference sketches, and raw material (smoke and ink blobs as noise or flipbook base, cleaned up). Never the final image of a small frequent moment (hit, card, stack): at 30 to 60 px toon hits the texture drifts between frames and line weights don't match.
- 🔴 **Ask every time.** Tool, count and estimated cost go to the human first. Free tools too.
- **No one else's work as input.** No other artist's effects, textures or names in prompts or input images.
- 🔴 **AI-generation log.** Keep a log in your repo: one line per generated file used in the game or marketing (file, tool, date, prompt, where used), including ElevenLabs sounds. Steam's AI disclosure (Valve, January 2026: generated content shipped in the game or its marketing is disclosed; tools used only in the workflow are not) is filled from it. Takes looked at and dropped are logged as "not used".

## Don't

- Build without reference research, paint colour first, or judge from an isolated preview (judge at game camera, game size, game speed).
- Shake or hitstop a weak moment; make hitstop with `Engine.time_scale` or sim code.
- Pitch one sample more than an octave up to fake an endless scale (the timbre breaks; [references/sound.md](references/sound.md) "Endless rise").
- Ship a generated sound unedited, spend credits without asking, or put an API key in the repo (untracked `.env` only).
- Offer a code synth as a candidate or result, fall back to a synth when generation fails (switch to recorded instrument samples or the music route and say so), post without naming the source, or claim a sound is good from pitch and level numbers.
- Write a new capture script per moment, judge performance from one run, or show a moment that's over its strength budget.
- Quads far larger than the shape, shadow-casting effects, `preprocess`, `amount` above the strongest use, screen-reading (`hint_screen_texture`) below max strength, effects first created mid-fight (first-draw hitch), or "can't measure GPU" because Metal reports 0 (measure on Vulkan).
- Generate images or video without asking, use them as the final art of small moments, or use them without a log line.
