---
name: video-trailer
description: Plans, captures, cuts and checks game trailers. Covers the Steam store's first trailer (gameplay, HUD on, muted autoplay, the 6 s microtrailer), the 30 s cutdown, announce, Next Fest and showcase cuts, with Valve's rules, the genre-hook-content order, showing card choices and their consequences, cutting to music, horror stings, capture features to request from dev, masters and a pre-publish checklist. Use with video-craft before planning, briefing, cutting or reviewing any trailer or showcase submission.
license: MIT
---

# Trailers

Load `video-craft` first. Beat sheets with seconds: [references/beat-sheets.md](references/beat-sheets.md).

A trailer is a project-owner decision: its brief, its music source and the final cut each need the human's approval. The first one is needed before the Steam Coming Soon page.

## Valve's rules [OFF]

- The **first trailer is gameplay**, from the player's view, **HUD visible**. Viewers in the Discovery Queue may give it under 10 s, and the store autoplays it **muted**.
- Only the first two trailers show before the screenshots.
- Steam makes a **6 s microtrailer from six random 1 s pieces of the first trailer**, and you can't choose them. Every second of trailer #1 must stand alone: no fade to black, no long title card, no near-black horror frame, no two near-identical shots.
- Spec: 1920×1080, 30 or 60 fps, ≥ 5,000 kbps, H.264 + AAC, stereo. No subtitle tracks, so burn in any text. The poster must be a frame of the video, no text.
- Name and category: `Gameplay Trailer` (category Gameplay) for slot 1. Logos and story go later in the trailer, once the player is interested.

## The order inside every trailer

**Genre (≤ 5 s) → hook (by 10-15 s, never past the halfway point) → escalation → breadth → title and one ask** [PRAC Lieu].

- The picture says the genre: the card hand, the board, the auto-fight. Shoppers read genre from familiar UI. Never "X meets Y" in text.
- The hook is your one or two real differentiators. One must land by 15 s.
- Feelings over features: title cards say what a mechanic achieves ("It can't die."), never how it works.
- Nothing repeated more than 3 times; repetition makes the game look small.
- Honest: only what is in the build. No CG-only trailer, no feature that isn't playable.

## Showing a deckbuilder or auto-battler

Auto-battlers are hard to trailer: the player acts before the fight, the fight runs itself, there are many units and the camera is far away [PRAC Lieu, GDC 2018]. The fix:

1. Hold one choice long enough to read (≥ 1.5-2 s, card art big, effect at most one line on screen).
2. Hard cut, or a match cut on the card's icon or colour, to the board where that card now acts.
3. The effect fires with exaggerated feedback (hitstop, flash, number) on a music hit.
4. Repeat 2-3 times at growing scale; the last is the biggest chain.
5. Keep eye trace: the card in screen centre → the effect's origin in screen centre.

Balatro's publisher found plain gameplay trailers didn't sell a UI-heavy deckbuilder; a voice-over that frames the one rule twist and then floods the viewer with depth did better, and streamers did most of the work [PRAC Playstack]. Default: gameplay first, with a text line (or a voice) that frames the twist.

## Capture needs (request from dev)

- A trailer camera: free camera, per-unit follow, slow motion, hitstop exaggeration, per-element UI toggles.
- Seed replay: the same fight re-shot from any angle (needs deterministic battles).
- A cheat path to late-game states so the trailer shows hours-in moments, not minute one.
- Capture with music off and SFX on, at or above 1080p, 60 fps for action.

## Music and sound

- Mark the music first: peaks (hits, drops) and troughs. Picture actions and title cards land on peaks; words go in troughs. At least one stopdown (music cut on a downbeat, masked by an SFX, with a punctuation shot), risers into new sections.
- Sync to actions more than to every beat. SFX are an extra percussion track; keep only the sounds that matter.
- Horror: ≤ 3 stings per 90 s, each after silence; the big monster withheld until the climax.
- Music must be yours or licensed for commercial use, with the licence on file (`video-craft` "Hard rules"). Picking a paid music source is the human's decision, with its cost.
- Loudness: −14 LUFS for Steam and YouTube; showcase specs vary (some ask −23 LUFS, WAV 48 kHz), so read theirs.

## Masters

Keep, per trailer: a textless master, a texted master, a logo-free version (showcases add their own), the music stem, the SFX stem, and the edit script. Showcase cutdowns (30 s, or 15 s gameplay-only, as INDIE Live Expo asks) then take hours, not days.

## Checklist (on top of the video-craft QA gate)

- [ ] Gameplay with HUD visible within 2-3 s (slot 1); genre clear by 5 s; hook by 15 s.
- [ ] Reads muted at 30% size on a phone.
- [ ] Random-scrub test: 10 random frames all show the game doing something legible (microtrailer, poster).
- [ ] No logo, slow pan or lore card before the hook; no shot used more than 3 times.
- [ ] Every choice shown with its consequence.
- [ ] Cuts and title cards on hits; ≤ 3 stings; at least one stopdown.
- [ ] Only footage from the build; music licence on file; AI-log lines for any generated audio.
- [ ] Spec: 1080p, 30/60 fps, ≥ 5,000 kbps, stereo (`check.py --channel steam`).
- [ ] Ends on the title and one ask that fits where it lives (follow now; wishlist once the page exists; "play the demo" during Next Fest).
- [ ] Steam content survey and YouTube AI disclosure answered where they apply.
