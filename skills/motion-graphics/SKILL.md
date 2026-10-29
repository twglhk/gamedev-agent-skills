---
name: motion-graphics
description: Makes motion graphics for game marketing video with an AI agent (character name cards and freeze-frame intros, kinetic type, title and end cards, logo stings, callouts, transitions), built as HTML/CSS and rendered frame-exact by a Playwright script, then laid over in-game footage with ffmpeg. Covers the tool verdicts (own renderer; HyperFrames, Remotion, After Effects MCP, Lottie/Rive weighed), timing and easing numbers, parameterised templates, rebuilding an effect from a reference clip, and a QA gate. Use with video-craft whenever a clip, Short, devlog or trailer needs on-screen graphics, or when on-screen text feels plain, cheap or "AI-made".
license: MIT
---

# Motion graphics

Bar: **a graphic earns its frames when it says something the footage can't (who this is, what this does) and moves the way the game hits.** It lands, holds still long enough to read, leaves cleanly, and has a sound on every arrival. It is rebuilt from files in the repo, never hand-keyed in an app.

Plain caption text is often the weakest part of a game clip. Introducing a character with an animated name and one line under it does more. Research behind this skill: [references/sources.md](references/sources.md).

## Hard rules

- Everything in `video-craft` "Hard rules" holds: approved in-game footage only, licensed audio, publishing only after the human approves.
- 🔴 **Text**: a name, a role line of at most 6 words, the title. No feature lists, no counts ("50 cards!"), no hype words. Character names only as the project spells them; never invent an epithet or title for a character.
- **Brand look**: copy a template in `templates/` and set your palette and fonts through its variables. Use one look per campaign, with the same palette and two font families. Paste the actual values into any brief; never just say "our brand".
- 🔴 **New tools need approval**: Remotion, HyperFrames, Lottie, any MCP server, any cloud or paid generation.
- **Deterministic**: all timing in CSS `animation`, Web Animations, or a paused GSAP timeline seeked through `window.mgSeek`; no `setTimeout`, `requestAnimationFrame` clocks or unseeded `Math.random()`. Same files, same frames.

## Stack

| Role | Tool | Verdict |
| --- | --- | --- |
| Author | HTML + CSS keyframes (Web Animations API for anything scripted) in the post folder or `templates/` | Default |
| Render | `scripts/render.py`: Playwright + Chrome, every animation paused and seeked to frame/fps, one screenshot per frame; `--alpha` for overlays, `--mov` for ProRes 4444 | Default |
| Compose | ffmpeg `concat` / `overlay` in the post's `build.sh`; full-range PNG → TV-range yuv420p | Default |
| Author + render, larger work | **HyperFrames** (HeyGen, Apache-2.0, free): the same HTML-seek idea plus GSAP, a `check` gate (layout, safe box, hold time) and about 450 registry blocks (shader transitions, kinetic type, captions). WebM/MOV alpha. See below | Good option once approved |
| Alternative | Remotion (React; free for a company of up to 3, licence counts contractors in the 5.0 draft) | React stack, licence tied to headcount |
| Rejected | After Effects MCPs (paid AE running in a GUI, not rebuildable) · Motion Canvas / Revideo (no agent tooling) · Lottie/Rive (UI motion, not titles) · ffmpeg-only text (no layout or easing) · AI video generators (not the game) | |

## HyperFrames (if adopted)

- Pin it in a tools folder (`npm install --prefix tools/motion hyperframes@<version>`), run it as `HF=tools/motion/node_modules/.bin/hyperframes` with `HYPERFRAMES_NO_TELEMETRY=1`. Never `npx hyperframes@latest`; never `cloud`/`lambda`/`publish`.
- Its agent docs ship inside the package (`node_modules/hyperframes/dist/skills/`). Read the core and CLI skill files before a HyperFrames job. The rules here win where they differ: your brand look, the text rules, licensed audio only, no cloud media.
- Which renderer: simple templates stay on `render.py`. New graphics that want a registry block (`$HF catalog --tag transition`, `$HF add <name>`) are built as a HyperFrames project in the post folder, rendered with `$HF render --format png-sequence --fps 30` (or `--format mov` for alpha), then composed in `build.sh`.
- Gate: `$HF check --json` before rendering. Intended overlap or outline text gets `data-layout-allow-overlap`; say why in `brief.md`.
- Fonts: bind every system face through `@font-face { src: local(...) }`. A bare family name can fall back to Helvetica in its Chrome.
- Registry blocks load GSAP from a CDN at render, so a render with no network fails. Stock looks (glitch, light leak, chromatic) stay banned (see "Tone").
- A ported `render.py` template rendered the same frames in HyperFrames (0.4% of pixels differed at glyph edges), 72 frames in 29 s vs 24 s.

## Making one

1. **Beat sheet first, in frames (30 fps).** Write each element's in, hold and out frame and the sound on it in `brief.md`. Storyboarding first is what separated good agent-made motion from broken renders in every tutorial reviewed.
2. **Copy a template**, set its `window.MG` vars from `build.sh`, change layout only through its CSS variables.
3. **Peek before rendering**: `render.py page.html --size WxH --still <s> --png peek.png --vars …` at the entry, the first readable frame, mid-hold and the last frame. Look at each at full size and at 360 px wide.
4. **Render** the sequence, compose in `build.sh`, run `video-craft` `check.py`.
5. **Sound pass**: a whoosh into each entry, an impact where it lands, one sting at most. Every graphic arrival has a sound; every sound has a visual twin.

```bash
MG=skills/motion-graphics   # wherever you installed this skill
python3 $MG/scripts/render.py $MG/templates/character-intro.html --size 1080x1920 --still 1.2 --png /tmp/peek.png \
  --vars '{"bg":"/abs/freeze.png","hero":"/abs/cutout.png","kicker":"UNIT 03","name":"Iron Warden","line":"Takes the hits <em>for the team.</em>","dur":2.4}'
python3 $MG/scripts/render.py page.html --size 1080x1350 --dur 2.4 --out /tmp/seq                       # opaque PNG sequence
python3 $MG/scripts/render.py page.html --size 1080x1920 --dur 3 --out /tmp/seq --alpha --mov ov.mov    # overlay
```

Needs `pip install playwright` and a Chromium (`playwright install chromium`) or an installed Chrome, plus ffmpeg for `--mov`.

## From a reference clip

When you like an effect in someone else's video, rebuild it from the clip, not from memory. A 5 s hook holds about ten separate moves (how words enter, what sits behind the subject, when the sound lands), and a description from memory misses most of them [PRAC Moran].

1. **Study copy only.** Keep the reference in `/tmp`, never in the repo or your cut; put its URL in `brief.md`. Copy the structure and timing, never its footage, art, fonts or music.
2. **Step through it**: `ffmpeg -i ref.mp4 -vf "fps=15,scale=480:-2" /tmp/ref_%03d.png`, tiled as in `video-craft` [tools.md](../video-craft/references/tools.md) "Storyboard sheet"; use the full frame rate for anything faster than 0.3 s.
3. **Write the event list** in `brief.md`: each move with its in and out frame, what moves and how far, the easing it looks like, what is in front of or behind the subject, and the sound on it.
4. **Change only what the brief names**: keep the structure and the timing, swap type, colour and devices to your look. Banned stock devices stay banned even if the reference uses them.
5. Build it with `render.py` or HyperFrames, then compare against the reference at the same moments (side-by-side recipe in `video-craft` [tools.md](../video-craft/references/tools.md)).
6. **Keep it**: if it will be used again, save it to `templates/` with a row in the table below. Over time that table becomes your library of moves.

## Craft rules

Numbers are defaults from the sources; a cut that breaks one says why in `brief.md`.

**Timing (30 fps)**
- Entry 8-12 frames (0.27-0.4 s). Exit 6-8 frames, faster than the entry.
- Hold: at least 1.5 s, or words ÷ 3 per second, whichever is longer. Name + 6-word line ≈ 2.4 s.
- Stagger: each element starts 2-4 frames after the last, while it is still settling. Things that belong together arrive together.
- Everything has left 2 frames before the cut. No half-wiped band on the next shot.
- A motion graphic is short: one idea in under 10 s. Past that it is a scene.

**Easing** (CSS cubic-bezier; GSAP names in brackets)
- Entry: snappy `cubic-bezier(.165,.84,.44,1)` [power4.out] for text; long glide `cubic-bezier(.16,1,.3,1)` [expo.out] for wipes and bands.
- Exit: `cubic-bezier(.55,.085,.68,.53)` [power2.in]. Never linear except colour fades and camera push.
- Overshoot (back, elastic) only on things with mass: a stamp, a slab hitting the ground. Never on text, numbers or UI. No bounce.

**Motion grammar**
- Land, then hold still. Nothing breathes or drifts to "feel alive"; only what is live keeps moving (a counter, the footage).
- One idea per move: rise + fade says "arriving". Spin, zoom and blur on the same text make it unreadable.
- A transition is caused by something on screen (a hit, a wipe band, a flash on impact). Never dissolve between unrelated shots. One freeze per short.
- Depth: the character cutout pushes 1.0 → 1.035 over the hold; graphics sit behind the character (band, giant name), readable text in front.

**Type and layout**
- Two families: a condensed display face for names and titles, a heavy sans for lines. Load system faces through `@font-face { src: local("...") }`; `font-stretch` alone does not pick a condensed cut.
- Name ≥ 12 vmin (≈ 130 px at 1080 wide); role line ≥ 4.5 vmin (≈ 48 px); kicker ≈ 3.6 vmin. One accent colour per line (`<em>`).
- Shorts 9:16: readable text inside x 90-900, y 250-1380 (`video-craft` channels.md). Decoration may run under the platform UI; words may not.
- High-contrast blocks (light on ink, an offset shadow) over footage; never thin text straight on the game.

**Tone**
- Match the game's tone. For horror with a heroic side: dim and desaturate the frozen world, keep the character warm with a light rim and a glow.
- One stylistic device per graphic (e.g. halftone dots, a tilted band, an offset shadow, giant outline type for a pulp-comic look). Avoid glitch, VHS, chromatic aberration, light leaks and particle swirls; they read as stock templates and say nothing about the game.

## Templates

| File | What | `window.MG` |
| --- | --- | --- |
| `templates/character-intro.html` | Freeze-frame character intro: white flash, world dims, tilted band + giant outline name behind the cutout, kicker chip, name slab, role line, all clear by the cut | `bg` `hero` `kicker` `name` `giant` `line` `dur` `origin` `cardTop` `giantTop` + colour and font vars |
| `templates/end-title.html` | End lockup over the last frame: band, title (accent via `<em>`), sub line | `bg` `title` `sub` `top` + colour and font vars |

Colour and font vars on both: `light`, `ink`, `accent`, `highlight` (intro only), `display`, `sans`. The defaults are neutral; set your palette. Both are opaque full-frame renders. For an overlay over moving footage, write the page with a transparent body and render with `--alpha`.

**Character cutout**: capture one moment twice from the same camera, once normally and once with the character alone on a flat background colour (hide the set or swap the sky). Key the flat colour to alpha (ffmpeg `colorkey` or a small numpy script), fill holes, and use the normal frame as `bg` and the keyed one as `hero`.

## QA gate (with video-craft's)

- [ ] Each readable frame passes at 360 px wide, sound off: who and what in one look.
- [ ] Entry, hold and exit match the beat sheet; nothing left on screen 2 frames before a cut.
- [ ] No overshoot on text; no element drifts during its hold.
- [ ] Words inside the safe box, in the post's language, after a humanizer pass; names as the project spells them.
- [ ] Every arrival has a sound and every sting a visual twin; music and SFX licensed and on file.
- [ ] `build.sh` rebuilds the cut from the repo alone; the graphic's HTML sits in the post folder or `templates/`.
