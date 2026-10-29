---
name: video-longform
description: Plans, scripts, cuts and judges long-form YouTube devlogs (3-15 min) for a game. Decides whether a devlog is worth making yet, writes a one-topic brief, a cold open that pays the title within 30 s, a problem-attempts-payoff structure, script and narration rules (including AI voice), retention techniques, chapters, Shorts cut from each episode, and the metrics that decide whether the series continues. Use with video-craft and video-youtube before proposing, scripting, editing or reviewing any long-form video.
license: MIT
---

# Long-form devlogs

Load `video-craft` (pipeline, tools, QA gate) and `video-youtube` (title, thumbnail, upload). This skill covers the episode itself.

## Is it worth making yet?

- Devlogs are **mid-funnel**: they deepen people who already know the game. Reported conversion is roughly 0.07-1.3% of views to wishlists, and the strongest devlog results came from years of steady uploads [PRAC]. Zukowski's survey ranks festivals, TikTok, streamers and Reddit above YouTube devlogs, and Jonas Tyroller says his own channel made no noticeable dent for Thronefall. The evidence conflicts, so run a **small, player-facing series at a pace you can hold** and judge it on weekly wishlists once the page exists.
- Start long-form only when there is enough **approved gameplay** for an episode. Until then, devlog topics become Shorts.
- **Voice**: your own voice, captions only, or an AI voice. If AI, use one approved voice and settings, and disclose it (YouTube AI use: Yes). An AI-sounding read costs trust with a dev audience, so the script and the take matter more: short lines, several takes, chosen by ear (`elevenlabs` skill, voice section).

## One episode = one topic

- A topic is a player-facing moment, not an engine topic: "This hero is hiding in a diner", not "Godot shaders". Good topics: a character or enemy reveal, a system that was broken and is fixed, a visual overhaul with before/after on approved art, a playtest invite.
- Sprint logs and bug-fix lists underperform. Tangents become notes for the next episode.
- Keep a running `devlog-notes.md`: one line and a clip path whenever something visible changes. If battles are deterministic, fixed seeds plus git history let you re-shoot any past state later instead of recording while working.

## Structure (8-12 min)

| Time | Section | Content |
| --- | --- | --- |
| 0:00-0:10 | Cold open | The moment the title and thumbnail promised, in the game. No greeting, no logo. |
| 0:10-0:30 | Stakes | One sentence on the game in plain words, naming it aloud or on screen, and this episode's problem. |
| 0:30-2:00 | Problem shown | The broken or dull version playing. Proof, not description. |
| 2:00-6:00 | Attempts (2-3) | Try → result → why it failed → an open question into the next. Failures are often the best minutes. Speed up anything that only shows time passing. |
| 6:00-8:00 | Payoff | Before/after, then the new version at full length with sound. |
| 8:00-9:00 | Meaning + ask | What it changes for the player; the one ask (follow, wishlist once the page exists) **before** the outro. |
| 9:00-10:00 | Next | The next episode's problem as a hook. End on a high moment, not a fade. |

- YouTube's **Intro** metric is the share still watching at 0:30, measured against what the title and thumbnail promised. Pay the promise inside 30 s.
- Chapters: `00:00` first, at least 3, each ≥ 10 s, named by question ("Why the fight felt dead").

## Script

- Write the body first and the cold open last, from the real payoff.
- About 120-150 spoken words a minute: 600-1,200 words for 5-10 min. Read it aloud; cut every sentence you stumble on.
- Show, then tell: wherever gameplay can replace a sentence, it does. No talking over a static screen.
- Plain, first person, no trailer voice, no invented facts or anecdotes. Run a humanizer pass for the script's language (e.g. https://github.com/blader/humanizer), and get the human's approval on the script before any paid rendering.
- Captions-only episodes: one caption per thought, ≤ 2 lines, in sync with the picture; a captions-only video has to move faster because nothing carries the gaps.

## Retention

- New visual information every 3-6 s; change the shot when the sentence changes topic.
- A pattern interrupt every 30-60 s: an angle change, B-roll, a diagram, a music change, a speed ramp, a held silence.
- Each section ends on an open question the next one answers.
- Music under speech stays low (start at −20 dB under the voice and measure, `video-craft` [tools.md](../video-craft/references/tools.md) "Measuring sound") or drops out during dense explanation.
- Narration gaps: at most 0.5 s between lines, keeping the breath at a sentence end. With TTS, take word times from the provider's timestamp response so cuts and captions never clip a word.
- One 1.5× watch-through before export: cut anything you'd skip. Write every fix in `notes.md` during that watch and fix them in one round.
- Build each chapter as its own segment and `concat` them, so a fix in one chapter re-renders only that chapter.
- After publishing, retention spikes are the next Shorts and the next thumbnail ideas.

## Every episode also makes

- 1-2 vertical Shorts (`video-short`): one moment, the hook in the first second, the game named on screen, the episode set as the Short's Related video.
- An X clip and, where it fits a sub's rules, a Reddit post, each cut for its channel.
- Later, the same topic as a Steam event post so the store page shows activity.

## Checklist (on top of the video-craft QA gate)

- [ ] The title and thumbnail promise is on screen by 0:30, and the game is named by 0:30.
- [ ] One topic; every section serves it.
- [ ] Chapters valid; the ask comes before the outro.
- [ ] Script approved; narration in the approved voice and settings; YouTube AI use set to Yes if the voice is synthetic.
- [ ] Music and SFX are your own or licensed on file; loudness −14 LUFS.
- [ ] Privacy pass on any screen capture (editor, terminal, notes, mail): names, e-mails, paths, keys and tokens blurred (`video-craft` [tools.md](../video-craft/references/tools.md) blur recipe), checked frame by frame where they move.
- [ ] An SRT is ready, plus translated titles and descriptions for your target languages (`video-youtube`).
- [ ] The Shorts cut from it are made.

## Reading the result

Read at 48 h and 7 d: Intro (% at 0:30), CTR by traffic source, average view duration, dips and spikes. Judge the series after 5-10 episodes on weekly wishlist change (0-40 a week is weak, 200+ is strong by Zukowski's benchmark), not on views. If an episode's Intro is low, the cold open didn't pay the title; fix that first.
