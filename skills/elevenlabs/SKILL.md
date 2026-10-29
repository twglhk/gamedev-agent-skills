---
name: elevenlabs
description: Generate game sound effects, music stings and character voices with ElevenLabs without wasting credits or shipping the "AI sound". Covers the hard rules (paid plan for commercial use, human approval of take counts and a credit estimate, an AI-generation log, keys in .env), the pilot-then-batch workflow, SFX prompt patterns, layering, loops, pitched sounds, finishing takes for the game, and voice work (model choice, Voice Design, consistency, barks, audio tags, disclosure). Use before planning, estimating, prompting, generating or reviewing anything made with ElevenLabs (Sound Effects, Music, Text to Speech, Text to Dialogue, Voice Design, Voice Changer).
license: MIT
---

# ElevenLabs: sound effects and voices

Every practice here is backed by two or more independent sources, by the official docs, or by a measurement you can repeat. Where sources disagree, the skill says so and tells you to A/B it in the pilot rather than pick a side. Sources with dates: [references/sources.md](references/sources.md).

The bar: **ElevenLabs gives raw takes, never finished sounds. Every take is chosen, cut, layered and measured like a recording, and nothing reaches the game without the human's approval and a line in the AI-generation log.**

The craft of sound itself (three layers, bands, frame sync, mixing, loudness) lives in the `fx-craft` skill ([sound.md](../fx-craft/references/sound.md)). This skill covers getting good raw material out of ElevenLabs.

Conventions assumed: raw takes and prompt logs in `design/fx/<moment>/`, finished audio in `game/audio/`, gains in a tuning resource. Adapt to your project.

## Hard rules

- 🔴 **Paid plan only for anything shipped.** Output made on a Free plan never goes into the game or marketing (Terms 1(c): free = non-commercial). Check your tier with `GET /v1/user/subscription` before the first batch.
- 🔴 **Ask before spending.** Every generation, pilot included, goes to the human first with: what, how many takes, settings, and estimated credits, worst case. Estimate SFX at the documented 40 credits per second; real bills often come in lower. After each batch read the actual cost from `/v1/usage/character-stats` and write it down.
- 🔴 **AI-generation log.** Keep an AI-generation log in your repo. Every file used in the game or marketing gets a line (file, tool, date, prompt, where used). Takes looked at and dropped are logged as `not used`. Steam's AI disclosure is filled from this log.
- 🔴 **Key only in an untracked `.env`** (`ELEVENLABS_API_KEY`). Never in the repo, notes, logs, or a command echoed into a report.
- **fx-craft's determinism and mixing rules hold.** Sound only watches the game. Gains live in data.
- **No one else's work as input.** No artist, game or library names in prompts, no reference audio you don't own.
- **Voice is a separate decision each time.** Character voices touch actors, disclosure and player trust. Never generate a voice, design a voice, or use a Voice Library voice without its own explicit approval. See [references/voice.md](references/voice.md) "Before any voice work".

Rights, terms and the API tables: [references/rights-and-api.md](references/rights-and-api.md).

## Workflow: pilot, then batch

Takes vary a lot and the parameters that matter (prompt influence, negative words) are contested, so learn on a small pilot and spend on the batch only after.

1. **Contract per sound.** Before any prompt, write what the sound must keep: length, pitched or not, the band it owns, the moment and its strength, what it must sound like it's made of (instrument or material), and the feeling it moves through. A placeholder file is never the contract: "keep the v1 chord" freezes a code synth into the result.
   - **SFX or music is set by the moment, not by how big it feels.** Round wins, boss wins and losses can be music stings (Eleven Music). Every moment where the team grows (level-up, synergy, reward) and every hit is an SFX: it strikes on the frame and glows for 0.6–1.5 s. A synergy written as film score reads wrong.
2. **Prompts.** One sound event per prompt; front, body and tail as separate prompts. Patterns in [references/sfx.md](references/sfx.md), punchy game sounds in its "Punchy game SFX".
3. **Pilot plan, approved.** 2 takes × 2 settings per sound (prompt influence 0.3 and 0.7, or with and without the negative tail), explicit duration, worst-case credits. Usually under 10% of the batch.
4. **Pilot.** Raw takes to `design/fx/<moment>/raw/`; every prompt, setting, take count and credit cost to `design/fx/<moment>/prompts.md`. Listen at game volume, measure (onset, true peak, pitch for pitched sounds), keep or drop each take with one reason.
5. **Batch plan, approved.** Use the winning settings and fix the prompts that failed. Report the pilot's kept rate (kept ÷ takes) and size the batch from it: takes needed = sounds × variants ÷ kept rate. Cap it. Get approval, then generate.
6. **Finish.** Trim, layer, EQ, peak, fade, name: [references/sfx.md](references/sfx.md) "Finishing". Finals to `game/audio/`, a second tuning resource for A/B, log lines.
7. **A/B for the human.** Same scene, same capture, old and new as separate clips (`fx-craft` "Capture and measure"). The live game resource changes only after approval.

Credit savers the sources agree on:

- **Always set `duration_seconds`.** Auto picks odd lengths (dead air, 6 s for one door hit) and you can't price it in advance.
- **Change one thing per retry.** Rewording and a parameter change in the same retry tell you nothing.
- **Stop at 3 to 5 usable candidates** per sound; editing beats more generating.
- **Never rerun an identical prompt hoping for luck after two misses.** Rewrite it concretely (source, material, action, space).
- **Text costs nothing in SFX** (cost depends on duration only), so a precise prompt is free; a vague one costs retries.
- **Voice Design charges the preview text once for three voices**; TTS in the web app gives two free regenerations of identical input (dashboard only, not API).

## Don't

- Use a take straight from the download, or pitch-shift a tonal take more than a semitone to fit the key.
- Ask the SFX model for a sequence ("footsteps, then a door") and keep it; it drops events. Generate parts and combine.
- Write a level-up, synergy or reward as a music prompt or cut it from a music take. Music starts soft and resolves over seconds; these moments must hit on the frame.
- Fall back to a code synth when a take fails, or keep a synth as the part the ear hears. Use recorded samples or the music route instead ([references/sfx.md](references/sfx.md) "Pitched sounds").
- Show a candidate without saying, per sound, what made it (which ElevenLabs takes, which library recording, which synth layer).
- Trust the SFX model to hit a musical key. No practitioner reports it reliably; measure every pitched take (FFT within ±20 cents) or build the tonal core another way.
- Put effect words in a Voice Design description ("reverb", "echo", "phone", "tape", "radio"); they degrade the voice. Era colour is post-processing.
- Use a Voice Library voice of a real person for a character, or clone anyone without written consent.
- Leave Community Sharing or model-training data use on (check both once, see [references/rights-and-api.md](references/rights-and-api.md)).
- Generate anything in a task that wasn't approved for it, including "just one test take". A no-credit call (one that fails validation, `/v1/user/subscription`) is fine.
