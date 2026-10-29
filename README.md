# gamedev-agent-skills

Agent skills and lane commands for making a game with AI coding agents: design, Godot code, characters, 3D, animation, VFX, sound, UI, story, marketing and video.

They come from the day-to-day development of **Heroes & The Horror**, a deckbuilder auto-battler (superheroes against cosmic horror) built in Godot 4 by one developer and a team of agents ([YouTube](https://www.youtube.com/@HeroesAndTheHorror)). Project-specific parts (our game's canon, internal tools, accounts) were taken out, so each skill describes a method you can apply to your own game. Where a rule only fits one genre, it says so.

## What's inside

**Skills** (`skills/<name>/SKILL.md`, with `references/` and `scripts/` where needed) teach the agent one craft: how to do it, what good looks like, and how to check it with numbers.

**Lane commands** (`commands/<lane>.md`) open a session as one member of a small game team. Each lane loads its skills, owns one area, hands other work to the right lane, and asks you before anything that needs a human call (picking between options, spending credits, publishing).

### Design and code

| Skill | What it does |
| --- | --- |
| `design-principles` | Review rules, screens, controls, feedback and card readability against the game's core experience; find a genre-breaking core constraint |
| `design-craft` | Turn a rule or level change into a spec plus a data switch, measure it with headless auto-play bots (paired seeds, standard errors), lay out stages and places. Includes TFT trait references |
| `godot-dev` | Build rules into Godot 4: logic in plain objects, numbers in `.tres`, headless tests, deterministic battles behind pinned logs, proof in the exported build |
| `skill-design` | Design the one active skill a hero, enemy or boss casts in an auto-battler: role, target shape, tell, damage measured in-game |

### Characters, 3D and animation

| Skill | What it does |
| --- | --- |
| `hero-design` | Design a hero that reads as a superhero at a glance: twist a proven cliché, look first, then the hidden everyday life |
| `enemy-design` | Design an enemy, boss or villain before any image exists: the one question it asks, its one core action, body and behaviour built around it |
| `char-3d-source` | Turn an approved design into a game-ready 3D figure: grey-mannequin 4-view sheet, image-to-3D, rig, game-camera check |
| `char-anim` | Animation that feels alive: rig check, key-pose blocking, in-betweening, Mixamo base clips, render-and-fix loops, glTF export |
| `blender-anim` | Build rigs, motion and non-human monster parts directly in Blender (Blender MCP or `blender -b`) |

### Art, effects, sound and UI

| Skill | What it does |
| --- | --- |
| `art-craft` | Non-character 3D art (grounds, places, props, maps, card art): Blender set kit, baked materials, AI image generation held to an art bible, readability and performance budgets |
| `fx-craft` | VFX, shaders and sound in Godot 4: references first, grayscale block-out, strength ladder with a frame budget, capture-and-measure scripts |
| `elevenlabs` | Sound effects and voices with ElevenLabs: pilot-then-batch credit workflow, prompt patterns, layering, loops, avoiding the "AI voice" |
| `ui-craft` | Ten-pass yardstick for game UI review: usability, readability, hierarchy, feedback timing, state matrix, consistency. Includes a WCAG contrast script |

### Story

| Skill | What it does |
| --- | --- |
| `save-the-cat` | Coach a writer through a game story with Save the Cat!, one question at a time: logline, hero, ten genres, 15 beats on two layers (campaign and scenario) |

### Marketing and video

| Skill | What it does |
| --- | --- |
| `marketing-playbook` | Indie marketing aimed at Steam wishlists: draft candidates, the human publishes; post types, channel rules for X, Reddit and YouTube, account safety, measurement |
| `post-voice` | Keep posts sounding like the developer by learning from the texts he writes himself |
| `video-craft` | Script-driven video pipeline from brief to finished candidate: tool stack, editing craft, captions, spec and loudness checks |
| `video-short` | 8–60 s clips for X, Reddit, Shorts, TikTok and Reels: hook in frame 0, payoff by 3–5 s, native 9:16 |
| `video-longform` | 3–15 min devlogs: whether one is worth making yet, cold open, problem-attempts-payoff structure, narration |
| `video-trailer` | Steam trailers and cutdowns: Valve's rules, genre-hook-content order, cutting to music, pre-publish checklist |
| `video-youtube` | YouTube packaging: titles, descriptions, thumbnails, chapters, translated metadata, AI disclosure, which numbers to read |
| `motion-graphics` | Name cards, kinetic type, title and end cards built as HTML/CSS and rendered frame-exact by script |

### Lane commands

| Command | Lane |
| --- | --- |
| `/design` | Rules, systems, levels, cards and combat; writes specs and data, measures with bots |
| `/hero` | Hero identity, combat role, concept art, 3D model and animation |
| `/enemy` | Enemies and bosses from concept to animated 3D model |
| `/art` | Sets, places, props, maps and card art |
| `/ui` | Screens, HUD, cards and UI motion |
| `/fx` | VFX, shaders, game feel and sound |
| `/dev` | Builds what design decided into the game, tests, exported builds (QA included) |
| `/story` | Story coaching: the human writes, the agent asks |
| `/marketing` | Drafts posts and clips for the human to publish |

## Install

Copy what you want into your project. Both OpenCode and Claude Code read the same `SKILL.md` format.

```sh
git clone https://github.com/twglhk/gamedev-agent-skills

# OpenCode
mkdir -p .opencode/skills .opencode/command
cp -r gamedev-agent-skills/skills/* .opencode/skills/
cp gamedev-agent-skills/commands/*.md .opencode/command/

# Claude Code
mkdir -p .claude/skills .claude/commands
cp -r gamedev-agent-skills/skills/* .claude/skills/
cp gamedev-agent-skills/commands/*.md .claude/commands/
```

Restart the agent so it picks up new skills and commands. Then open a lane, for example `/hero design a speedster who is afraid of the dark`.

## Adapting to your project

Each skill states its assumptions near the top (for example "game data in `game/data/` as Godot `.tres`" or "a headless auto-play probe script"). Change those paths to yours. The skills expect a few project docs you keep yourself: design pillars, an art bible with a written style anchor and reference images, and a decision log. Skills that use paid services (ElevenLabs, Meshy, Tripo) tell the agent to get your approval with counts and a cost estimate before spending credits. Keep API keys in an untracked `.env`.

Some skills point to third-party humanizer skills for cleaning AI-sounding text: [blader/humanizer](https://github.com/blader/humanizer) (English), [IsaacEryn/humanizer-ko](https://github.com/IsaacEryn/humanizer-ko) (Korean), [gonta223/humanizer-ja](https://github.com/gonta223/humanizer-ja) (Japanese).

To run lanes as a team with a phone-friendly review board, see [dongduni-agent-hub](https://github.com/twglhk/dongduni-agent-hub).

## License

MIT
