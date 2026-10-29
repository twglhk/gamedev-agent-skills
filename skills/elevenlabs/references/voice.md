# Character voices with ElevenLabs

How to do voices well if you decide to have them. This file authorises nothing. Source numbers [n] refer to [sources.md](sources.md).

## Before any voice work

Put these to the human as one decision before the first credit:

- **Voice at all, and how much?** Barks and efforts only (attack, hurt, death, victory), or lines too. In an auto-battler barks carry most of the feel; lines bring cost, localisation and backlash risk.
- **Disclosure.** Steam requires disclosing generated content that ships in the game or its marketing (rules rewritten 2026-01-16) [V1]. The backlash cases found came mostly from undisclosed use or from replacing known actors: Tomb Raider IV–VI Remastered removed AI lines after a week (2025-09) [V2]; Arc Raiders re-recorded some TTS lines with actors (2026-03) [V3]. One indie reported no complaints from 850+ players with full TTS voicing, self-reported [V4].
- **Whose voice.** Use only voices you design (Voice Design) or your own performance through Voice Changer. A Voice Library voice is a real person's model: the owner can withdraw it after a notice period, after which new lines are impossible (Voice Library Addendum, 2026-03-06) [5]. The SAG-AFTRA 2025 Interactive Media Agreement governs replicas built from a covered performer's work; a designed voice built from no performer appears to be outside that definition, but that is a reading, not legal advice [V5].

## Model choice

- **Eleven v4 (`eleven_v4`) is current** (2026-09-28) and ElevenLabs calls it a net upgrade over v3 for character voiceover [6][7]. Only two settings: stability and similarity. No style, no speed, no SSML [6][4].
- **But Voice Design voices "may not be as performative" on v4** [6][8]. For each designed character, render the same three test lines on `eleven_v4` and `eleven_v3` and pick per character.
- Text to Dialogue only for multi-speaker scenes; barks are single TTS requests.
- Multilingual v2 is the fallback when a long line must stay steady.

## Designing a voice

Voice Design (`POST /v1/text-to-voice/design`, model `eleven_ttv_v3` or `eleven_multilingual_ttv_v2`) returns three previews per call; you pay for the preview text once [8][9].

**Description format** (official [8]):

```
Native <language and region>. <Gender>, <age range>. <Quality level>.
Persona: <2–5 words>. Emotion: <2–3 adjectives>.
<1–2 sentences on timbre, pacing, delivery>
```

- Be concrete on age, timbre (deep, gravelly, breathy, thin, booming), pacing and emotion [8][V6][V7]. Say "thick" rather than "strong" for accent strength [8].
- Say "intonation" when you mean intonation; "accent" triggers a dialect shift [8].
- 🔴 No effect words ("reverb", "echo", "phone", "tape", "radio") [8]. Period sound (old radio, gramophone) is post-processing, below.
- Quality words ("studio quality") help clean output but can blur a niche character [8]. Leave them out for monsters.
- **Preview text matches the character.** A shouting drill sergeant with a gentle preview line sounds wrong; longer previews (100–1,000 characters, a full paragraph) are steadier [8][9][V7].
- **Guidance scale:** low for performance and audio quality, high when accent or tone accuracy matters most; high values can sound robotic [8][9]. The doc examples sit around 20–40%.
- Set a `seed` and record it with the description, model, guidance scale and preview text in a per-character file (e.g. `design/voice/<character>/voice.md`) so the design can be repeated.

**Saving.** Pick one preview with `POST /v1/text-to-voice` and record the `voice_id`. Each saved voice uses one of your plan's voice slots.

## Keeping a character the same

- **One `voice_id` per character, frozen.** Never edit the voice after its first approved line; store the ID and settings next to the script in the repo [V8][V9].
- **Same model and settings** for every line of that character. Mixing v3 and v4 lines of one voice sounds like two people [6].
- **`seed` is best effort, not a lock** [10][V10]. Keep the takes, not the hope of re-rolling them.
- For lines cut from a longer read, pass `previous_text` / `next_text` (or `previous_request_ids`) so the joins sound continuous [10].

## Barks and efforts vs lines

Short interjections are TTS's weak point [V8], and good exertion sounds are hard even for actors [V11]. Try three routes in the pilot and keep the best per character:

1. **TTS with a tag and a padded line:** `[shouting] Hah, now!` Pad very short barks with punctuation and trim afterwards [V8].
2. **The SFX model for wordless sounds** (grunts, breaths, monster roars and gurgles), as `sfx.md` describes.
3. **Voice Changer on your own performance** (`/v1/speech-to-speech`, `eleven_multilingual_sts_v2`, `remove_background_noise`), costing 1,000 characters per minute of audio [11][4]. It keeps timing and emotion [11], but one tester found screams came out robotic [V12]. Test a scream before relying on it.

Monsters: use routes 2 and 3 as raw layers and process them. A voice built from someone's grunts came out mediocre and picked up stray accents in one test [V14], so don't expect a finished monster from Voice Design.

## Audio tags and text

- Tags are short instructions in square brackets where delivery changes: `[whispers]`, `[shouts]`, `[sighs]`, `[laughs]`, `[curious]` [7][12].
- One or two words per tag; longer tags make the voice unstable or get read aloud [V15].
- Describe voice quality, not a sound cue: `[low, gravelly voice]`, because v4 can read a tag as a sound effect [7].
- Match tags to the voice: a measured voice won't shout well [7].
- Punctuation shapes delivery: ellipses add weight, CAPS add emphasis, a dash cuts off [7].
- Tags fail sometimes: users report ignored tags and tags spoken aloud [V15][V16]. Listen for both on every take.
- Stability: lower is more expressive and less predictable, higher is steady and can go flat; 0.5 is the documented start [13]. For a character, pilot 0.35 and 0.5 and keep one value for all its lines.

## Avoiding the "AI voice" sound

Common complaints: flat, predictable delivery over long listening; over-clean studio air; clicks; skipped syllables; loudness jumps; ignored tags [V17][V19].

- Keep lines short: under about 200 characters each, never long paragraphs.
- Direct with tags and punctuation rather than raising stability.
- Generate several takes per line and choose. Regenerations fix roughly half of quality problems [14].
- Post-process like a recording: high-pass, gentle de-ess, light compression, the same room as the scene. Era colour (old radio, gramophone) is a band-pass and saturation chain you build and A/B, not words in the prompt.
- Check name pronunciation with IPA in slashes on v4 (`"/ˈɡɑːrɡɔɪl/"`) and lock what works [7].

## Other languages

v4 covers many languages [6]. When a voice speaks a language different from its reference, v4 drops the foreign accent on purpose [6]; if a character's accent matters, design the voice in that language. Native speakers have called output in some languages unusable [V17]; have a native speaker check every non-English line before shipping.
