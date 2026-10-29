# Sound effects with ElevenLabs

Model `eleven_text_to_sound_v2`. The API also lists `eleven_text_to_sound_v3`, but at last check it had no doc, changelog entry or price, and the vendor's own skill still defaulted to v2 [4][22]. Don't use it until it's documented and a comparison is approved. Source numbers [n] refer to [sources.md](sources.md).

## Prompt patterns

**Name the physical thing.** Source, material, action, space, shape. Concrete nouns beat adjectives: "glass shattering on concrete" beats "breaking sound"; "good attack sound" gets mush [1][S1][S2][S3].

Template:

```
[what hits what] · [material and size] · [distance and space] · [shape: one-shot, sharp attack, short tail] · [pitch if any]
```

- Pitched (player side): `Single bright brass bell strike, close and dry, sharp attack, 1.5 second ring-out, one-shot`
- Unpitched (enemy side): `Heavy wet flesh thud on wet stone, close, no tonal content, very short tail, one-shot`
- Bed (loop): `Distant harbor at night, slow water lapping against wooden pilings, faint foghorn` with `loop: true`

**Audio terms the model knows** [1]: impact, whoosh, ambience, one-shot, loop, stem, braam, glitch, drone. Use them.

**One event per prompt.** The docs and every practitioner test agree that multi-event prompts drop or mistime events (three footsteps came back as two) [1][2][S3][S5]. Generate each event and each layer separately and combine in the edit.

**Dryness.** You want dry takes so your own tail and space go on top. Two camps disagree:
- End with "dry, close-mic'd, isolated, no room reverb, no ambience, no music" [S5] (in one A/B the dry take ended a third of a second sooner).
- Avoid negative words, which can weaken the sound; say what you want: "close, dry, prominent, sharp" [S6]; "no background noise" was ignored in a forum test [S7].
- Pilot both forms on the first sound of a set and keep the winner for the rest. Positive dryness words ("dry, close-mic'd, isolated") are in both camps, so always use those.

**Quality tags** ("clean isolated professional Foley recording") are reported to help by only a few users: harmless, unproven. Use at most one.

**Long, poetic prompts pull in music beds and extra layers** [S8][S9]. Keep it to one or two lines (the web limit is 450 characters).

## Parameters

| Parameter | Do | Why |
| --- | --- | --- |
| `duration_seconds` | Always set. One-shots: final length + 0.2–0.5 s to trim (API minimum 0.5 s). Beds: 10–30 s | Auto gives odd lengths and an unknown price [2][S3][S4][S5][S10] |
| `prompt_influence` | Pilot 0.3 vs 0.7, keep the winner per sound family | Contested: practitioners push 0.6–0.8 for literal results [S6][S8][S10]; the only controlled test found no gain over 0.3 [S13]; the vendor skill uses 0.8 for a UI chime [4] |
| `loop` | Only for beds (rain, harbour, hum). Off for every one-shot | Loop makes a seamless repeat; one-shots get a smeared end [1][S10][S12] |
| `output_format` | `wav_48000` for non-looping effects if your plan allows; otherwise `mp3_44100_192` and note it | WAV 48 kHz is listed for non-looping effects [1][3]; the API page says 44.1 kHz WAV/PCM needs Pro, so try once: a refused format isn't billed |
| `model_id` | `eleven_text_to_sound_v2` | Documented model |

## Layering, variants, loops

- **Layers apart.** Front ("sharp transient click, no tail"), body and tail as three prompts. Align on the front and delay body and tail a few ms (`fx-craft` sound.md §6). Practitioners and the docs agree blends hold up better than one all-in-one take [1][S1][S5][S12][S14].
- **Blend with a real recorded layer when the take is thin.** Generated takes are often called thin; a recorded second layer carries variation and weight [S1][S14]. A code synth may sit only under recorded material as support (sub thump, falling sweep) on unpitched sounds; it's never the layer the ear identifies and never in a pitched sound.
- **Variants for frequent sounds.** 3+ per sound. Get them from separate takes of the same prompt, not by pitch-shifting one take. Pitch-shift unpitched variants by at most ±1 semitone at runtime (Godot `random_pitch_semitones`), never pitched ones.
- **Loops.** Generate with `loop: true` at 10–30 s. Import with Loop on in the engine and listen to the seam three times at game volume before keeping it [1][S12].

## Pitched sounds

If your pitched sounds must share a key, know this: nobody reports the SFX model hitting a named key reliably. The only key examples are the vendor's own [1][2], and practitioners call UI tones and chimes inconsistent or metallic [S15]. So:

1. Ask for the instrument and character, not a guaranteed note ("soft vintage celesta chord, warm, gentle attack"). Naming the key is fine; expect misses.
2. Measure every pitched take: FFT peak within ±20 cents of the target note. Drop the rest. Never shift more than a semitone.
3. If the kept rate stays low after the pilot, don't burn credits and don't fall back to a code synth. Build the tonal core from recorded, tuned instrument samples (a licensed or CC0 multisample library such as VSCO 2 CE, licence approved), or treat the moment as music (Eleven Music, or a sting played from those samples). Report the switch. Falling back to "our synth" is how a sine "ding" ends up as the win sound.
4. Only wins and losses are music (`fx-craft` sound.md §7). A level-up, synergy or reward is an SFX with its tonal colour in the tail layer (below). The SFX model can't hold a chord (a pilot got 0 of 4 chord takes), so never ask it for one; ask for a bright shimmer or a single ring and measure its strongest note.
5. A rising series (a note per tier, per unit a spark reaches) is one take played at stepped `pitch_scale` (major-scale semitones, within one octave), not one take per note. Peggle and Slay the Spire build their rises this way (`fx-craft` sound.md §8).

## Punchy game SFX (impact, power-up, reward, hit)

What exists is the vendor's showcase prompts, a handful of practitioner reports and pilots; no independent test of any one wording. Treat the recipe as the pilot's starting point.

**What the vendor shows** (marketing pages, settings not given) [23]:

- Hit: "A very short, punchy video game hitmarker sound … A sharp, dry, slightly fleshy thwack layered with a crisp, high-frequency click and subtle low-end impact … Extremely tight transient, immediate attack, rapid decay, no reverb, no echo, no voices, no music."
- Level-up: "Fantasy video game level-up stinger, a quick rising magical arpeggio … ending in a bright power chord with a shimmering sweep … short and rewarding". It asks for notes and a chord, which the model doesn't hold (above); take the shape words (quick, rising, shimmering sweep, short) and leave the notes out.
- Impact: "Epic cinematic bass impact" with a "sub-bass boom" and "metallic punch resonance".
- Words beyond the docs' term list [1]: transient, immediate attack, rapid decay, stinger, riser, sub-bass boom, shimmer, sweep.

**What practitioners report:**

- One-shots and organic sounds come out well; UI sounds (beeps, chimes, synthetic tones) are inconsistent, and very short percussive takes can carry artefacts at the very start or end [S15][S17].
- An "impactful" weapon prompt came back heavily compressed, and one take had its transient cut off at the start of the file [S18]. Check the first 10 ms of every hit take (`fx-craft` `measure.py --profile`: peak within a few ms of onset) and drop takes that start mid-sound.
- Hits and UI sounds come back at very different levels; one confirm take was too faint to use [S5][S3]. Level every take before judging it.
- Three layers, no more: one transient, one tonal, one texture or noise layer; EQ, then transient shaper or compressor, then pitch, then space [S19]. Low thump, mid body and high sizzle carved apart by EQ [S20].

**Recipe** (pilot it; one take per layer per prompt):

| Layer | Ask for | Length asked | Example |
| --- | --- | ---: | --- |
| Front | the strike: what hits what, "extremely tight transient, immediate attack, rapid decay", "dry, close-mic'd" | 0.5–1.0 s | heavy steel or bronze strike, sub-bass boom under it |
| Tail | the glow: "bright shimmering sweep rising", "sparkling", "airy", "wide"; no notes, no chord | 1.0–1.5 s | rising bright metallic shimmer that fades out |
| Step (rises only) | one short bright ping or zap, played at stepped pitch | 0.5 s | short bright metallic ping, tiny spark |

- Pitched side: the tail carries the pitch colour; measure its strongest note and keep it only within a semitone of a note in your key (then retune). Unpitched side: say "unpitched" and "no tonal content".
- Ask the frequent hit at the shortest length (0.5 s, the API floor) and cut it to its body (≤120 ms) in the edit.
- Avoid "epic", "cinematic", "orchestral", "music" and "stinger" in growth-moment prompts: they pull in music beds [S8][S9] and read as film score.

## Known failure modes

- Metallic, ringing or high-pitched hiss on top [S14][S16]. Fix in this order: regenerate with a rewritten prompt, export the best format, layer under a clean source, notch the ring with EQ. No evidence that "AI artifact remover" plugins help.
- Thin, generic results [S1][S14]. Layer; describe material and size more concretely.
- Wrong thing entirely ("fireplace" with no fire, "explosion" as a muffled thud) [S1]. Rewrite with physical nouns; don't retry the same words.
- Dead air before or after, extra hits [S1][S3]. Trim; set duration.
- Quiet takes (one test peaked near −21 dBFS) and takes far louder than their siblings [S3][S11]. Normalise every variant to the same true peak.
- Ambiences with many elements drop some and add music [S9]. Make a bed from one element and layer the rest.

## Finishing

Follow `fx-craft` [sound.md](../../fx-craft/references/sound.md) §6 for the commands. ElevenLabs-specific points:

1. Pick: clear front, no artefact on headphones, its band free, right emotion. Write the reason for each kept and dropped take in `prompts.md`.
2. Trim the onset to 0 (a late onset reads as input lag) [S6][S11]; cut trailing silence; 5–50 ms fade-out.
3. Level: true peak −1.5 dBTP per file (−1 dBTP max), same peak across a variant set.
4. Name `<side>_<moment>_el_<nn>.wav`; finals to `game/audio/<area>/`, raw stays in `design/fx/<moment>/raw/`.
5. Point a second tuning resource at the new files for A/B; touch the live resource only after approval.
6. One AI-log line per kept file.
