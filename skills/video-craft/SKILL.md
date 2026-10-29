---
name: video-craft
description: Script-driven marketing video pipeline for games, from brief to a finished candidate the human reviews before publishing. Covers which type skill to load next (video-short, video-longform, video-trailer, video-youtube, motion-graphics), the ffmpeg + Godot Movie Maker + Playwright tool stack, folder layout, the editing craft every cut follows, burned-in captions, spec and loudness checks, and the QA gate. Use when planning, capturing, cutting, captioning, scoring, titling or reviewing any game marketing video (clip, Short, devlog, trailer).
license: MIT
---

# Video craft: the pipeline

Bar: **a video earns its place by what a stranger feels in its first second and what it proves about the game by its last.** It is in-game, approved by the project owner, reads on a phone with the sound off, and can be rebuilt from files in the repo.

References: [sources.md](references/sources.md) (research, graded) · [tools.md](references/tools.md) (commands) · [editing.md](references/editing.md) (cutting, sound, text) · [channels.md](references/channels.md) (specs, safe zones, metadata, metrics).

This skill assumes:
- a post folder per video, e.g. `marketing/posts/<date>-<slug>/`;
- an audio library folder (e.g. `marketing/audio-library/`) with a `manifest.csv` listing each file, its source and licence;
- an AI-asset log (e.g. `ai-log.md`) with one line per generated file;
- a Godot game you can launch with a capture driver script. Adapt the paths to your project.

## Which skill next

| Making | Also load |
| --- | --- |
| A clip or Short, 8-60 s (X, Reddit, YouTube Shorts) | `video-short` |
| A YouTube devlog, 3-15 min | `video-longform` |
| A Steam, announce, Next Fest or showcase trailer | `video-trailer` |
| Anything that goes to YouTube | `video-youtube` |
| Any on-screen graphic beyond a plain caption (character name card, title, end card) | `motion-graphics` |

Post text for X and Reddit belongs to `marketing-playbook` and `post-voice`. This skill covers picture and sound.

## Hard rules

- 🔴 **Material**: approved, in-game footage only. Work-in-progress footage is fine if labelled as a dated WIP build. Never cut or scrapped content, never a feature the build doesn't have. Honesty is also a platform rule: gameplay-free CG trailers have drawn regulator action.
- 🔴 **Money**: paid SFX, music, voice or image generation needs the human's approval first, with counts and worst-case credits (`elevenlabs` skill). Every generated file used in a video gets a line in the AI log.
- 🔴 **Music and audio rights**: only the game's own audio and library files whose licence is on record in the manifest, read the day you added them. No trending or licensed tracks, no meme clips, no stock audio without its licence on file, nothing from a free plan that forbids commercial use (e.g. Suno Free/Basic). Rights per source: [tools.md](references/tools.md) "Music and SFX sources". One Content ID claim blocks a Short over 1 min worldwide.
- 🔴 **New tools**: installing ffmpeg-full, whisper.cpp, Remotion, HyperFrames or any MCP server adds a dependency. Ask the human first.
- 🔴 **Voice**: if a video uses AI narration, use only the approved voice and settings, kept in one file (e.g. `marketing/voice/narrator.md`), and get each render batch's credits approved. AI narration means YouTube's AI-use question is Yes.
- **On-screen text**: as little as possible, in the post's language, never a sentence where a picture would do. Character names exactly as the project spells them.
- 🔴 **Publishing** happens only after the human approves the finished candidate, unchanged.

## Stages

| # | Stage | Output in the post folder | Gate |
| --- | --- | --- | --- |
| 1 | Brief | `brief.md` (template below); `storyboard.png` for a cut over 15 s | One message, one feeling, one verb, proof shots named, material approved; order and hook fixed on stills before any full render |
| 2 | Material | source clips or a capture | In-game, approved, fixed seed noted; capture at or above output size |
| 3 | Edit | `edit.sh`: every ffmpeg step from source to cut | The cut rebuilds from the script alone |
| 4 | Sound | mixed audio in the cut | Hits on the frame; −14 LUFS, ≤ −1 dBTP (`check.py --fix-audio`) |
| 5 | Text | `captions.json` → `*_caps/` (HTML and PNG) | Inside the safe box, ≤ 6 words a line, target language |
| 6 | Package | one file per channel, title, description, cover frame or thumbnail | Per [channels.md](references/channels.md) and the type skill |
| 7 | QA | `hook.png`, check output | The gate below, all pass |
| 8 | Hand-off | the finished candidate with its files, text and why | The human reviews and approves before anything is published |

- Video files are usually gitignored, so `brief.md`, `edit.sh` and `captions.json` are what keep the work rebuildable. Keep them next to the outputs.
- Footage sources, in order: captures from the daily or latest build, a character viewer scene for one character in a real setting, then a dedicated Godot Movie Maker capture ([tools.md](references/tools.md) "Capture").
- Capture features only the dev lane can build (trailer camera, slow motion, UI hide toggles, a native 9:16 camera, seed replay) go to the human as one request.

## Tool stack

| Role | Tool |
| --- | --- |
| Capture | Godot Movie Maker (`--write-movie`, `--fixed-fps`) |
| Cut, crop, speed, mix, encode | ffmpeg, called from `edit.sh` |
| Captions, title cards, thumbnails | HTML → PNG with Playwright, laid on with `overlay` (`scripts/captions.py`) |
| Spec, loudness, hook sheet | `scripts/check.py` |
| SFX, stings | The game's own sounds first, then the library (e.g. Sonniss GDC picks, Kenney CC0, approved generated takes) |
| Music | Free or licensed stock from the library; the human picks tracks by ear |
| Voice | AI or recorded narration for devlogs; clips, Shorts and trailers go without unless a cut needs it |
| Word-timed captions for a voice-over | whisper.cpp + ffmpeg-full (libass), or the TTS provider's timestamps |
| Motion graphics | HTML/CSS rendered frame-exact; load `motion-graphics` |
| MCP servers | None recommended ([tools.md](references/tools.md) "MCP verdict") |

No editor app is in the loop: every cut, caption and mix is a script in the post folder, so an agent can rebuild it and the human only reviews the result. Editors weighed and dropped: DaVinci Resolve (scripting needs paid Studio, GUI-bound), CapCut and Premiere Pro (GUI subscriptions; nothing an agent can drive that ffmpeg can't), Kdenlive, Motion Canvas, Revideo, editly (stale), MoviePy (adds nothing over ffmpeg). AI tools dropped: auto-clippers and AI editors (OpusClip, Descript, Submagic) upload footage to a cloud and are built for talking heads; text-to-video generators (Runway, Sora, Veo, Kling) make footage that isn't the game, which breaks the Material rule.

Native 4:5 and 9:16 takes: Movie Maker writes the project's viewport size whatever `--resolution` says. Run the take from a throwaway project dir that symlinks your game folder and swaps only the viewport size in `project.godot`.

## Craft every video follows

Details and sources in [editing.md](references/editing.md).

1. **Frame 0 is the payoff**, not the setup. No logo, no title card, no slow pan, no greeting. The 3→5 s window must pay off or escalate what frame 0 promised.
2. **One idea per video.** A brief with two messages is two videos.
3. **Show the choice and its consequence in the same shot or the next one.** A card pick without its result on the board proves nothing.
4. **Cut on events, not on a clock.** Hold a shot until its payoff lands, then cut. Never put a text card and new gameplay in the same second.
5. **Readable on a phone with the sound off**: one focal point per shot, a small readable cast (about 3 characters and 1 boss), key numbers ≥ 70 px tall at 1080 wide.
6. **Sound on, survives muted.** Every sting has a visual twin (flash, push-in, colour drain). At most one sting in a short, three in 90 s, each after silence.
7. **For horror games: horror, then hope** (or whatever turn carries your game's main feeling). Dread, a held beat, then the player's side acts. End on the turn, not the threat.
8. **Name the move and give it a number.** Whoever cuts, a subagent or you in `edit.sh`, gets editor's words with numbers ("push-in +8% over 1.5 s, ease-in-out", "music at −20 dB under the voice"), never "make it punchy". An agent can't hear, so sound is measured, not judged by ear. Table: [editing.md](references/editing.md) "Telling an agent what to cut".

## Brief template

```
Type / channels:   (short · devlog ep N · trailer kind) → (x ja · reddit en · youtube)
Single message:    the sentence a viewer repeats to a friend: "the game where …"
Feeling:           the one feeling this cut serves
Energy:            one line of pace for the editor: "fast and busy" (Short) · "measured, the game carries it" (devlog)
Verb shown:        the core player verb on screen
Material:          files + who approved them
Proof shots:       3-6 shots, each with source, seed, camera, UI on/off
Hook:              what frame 0 shows; what 3-5 s adds
Beats:             the type skill's beat sheet with seconds; storyboard stills in the same order
Moves:             each zoom, ramp or transition by name with its numbers (editing.md table)
Sound:             game audio, SFX, sting points, music source and licence, music level under any voice
On-screen text:    each line, its language, its seconds
CTA:               one (follow · watch next · wishlist once the page exists)
Measure:           the type skill's metric, read at 24 h and 7 d
```

## QA gate (before hand-off)

- [ ] `check.py <file> --channel <ch>` prints `ALL PASS` for every channel file.
- [ ] Sound measured, not assumed: each planned hit lands within 1 frame of its picture event, and music sits about 20 LU under any voice ([tools.md](references/tools.md) "Measuring sound").
- [ ] `check.py --sheet hook.png`: frames at 0 s, 1 s and 3 s each show the game doing something, with no black frame or logo.
- [ ] Watched once at phone size (360 px wide), muted: you can say in one sentence what happened. If not, recut.
- [ ] Captions sit inside the safe box and never cover the key action. Every word is in the target language and has had a humanizer pass for that language (e.g. https://github.com/blader/humanizer for English, https://github.com/gonta223/humanizer-ja for Japanese, https://github.com/IsaacEryn/humanizer-ko for Korean).
- [ ] Every shot is approved, in-game material. No grey-box, no cut content.
- [ ] The type skill's own checklist passes.
- [ ] The hand-off note names the message and the feeling. What an agent saw in the clip is reported as an agent's observation, not as a player result.

## Scripts

```bash
S=skills/video-craft/scripts   # wherever you installed this skill
python3 $S/captions.py posts/<slug>/captions.json                # timed captions burned in (spec in the script header)
python3 $S/check.py cut.mp4 --fix-audio cut_lufs.mp4             # two-pass loudnorm to −14 LUFS, video copied
python3 $S/check.py final.mp4 --channel short --sheet hook.png   # spec + loudness + 0/1/3 s frames
```

Channels: `x`, `reddit`, `short` (YouTube Shorts, TikTok, Reels), `youtube` (long-form), `steam`. Use `--lufs -23` for festival masters that ask for it. Both scripts need `ffmpeg`/`ffprobe` on the PATH; `captions.py` also needs `pip install playwright` and a Chromium or Chrome.
