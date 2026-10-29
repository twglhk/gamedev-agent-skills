# Sound: building, finishing and mixing

Sources are numbered at the bottom. "Starting values" are first build values; capture, listen and retune.

## 1. One sound = three layers

- **Front (transient).** The first click or crack. This is the layer that sits on the contact frame, and it decides most of whether a sound feels strong. Heavy compression smears it, so protect it [1][2].
- **Body.** Low-mids that carry weight and material (metal, wood, flesh, stone).
- **Tail.** Space and reverb. Keep it separate so it can change per location [1].
- **Split the bands.** Each layer owns a band: lows for weight, mids for character, highs for clarity. Two layers fighting in one band turn muddy [1].
- **Size and weight.** Big things have thick lows and long tails; small things are short and mostly high. Laptop speakers barely reproduce lows, so if the thump disappears, add a high click layer to make the weight audible.
- **Same frame as the picture.** People notice sound more than 45 ms early or 125 ms late (ITU-R BT.1359) [3]. Put contact sounds much tighter: within one frame (17 ms).

## 2. Turning game rules into sound

- **A side rule by pitch** (one useful pattern): player side = pitched sounds (bells, chimes, chords), enemy and shadow side = unpitched (thuds, creaks, low rumbles, noise).
- "Bells, chimes, chords" means what gets recorded. A chord built from sine waves doesn't satisfy the rule and sounds like an old Flash game. The identity of a pitched sound is a recorded instrument (SKILL.md "What a sound is made of").
- **Period instruments (music and ambience only).** If your setting has an era, choose the instrument palette from what that era actually used, and research it like any reference. Example for a 1940s–50s setting: the Hollywood studio orchestra and radio drama (brass including muted trumpet, trombone, horn and tuba; timpani, harp, glockenspiel, cymbals, strings, upright piano) [10]. Film noir scoring was "mostly Hollywood orchestral with added dissonance"; sax and pizzicato-bass noir came in the late 1950s [11]. For eerie colour, the theremin fits the period (Rózsa's Spellbound, The Day the Earth Stood Still) [12]. Synth timbres didn't exist then. Don't put period colour on short reward, level-up, synergy or hit SFX (§8).
- **Pitched sounds share one key.** When several player-side sounds fire together they should form a chord, not a clash. Pick the key with the music; once set, record or generate every chime, bell and chord in it.
- **Endless rise.** Each level-up climbs one major-scale step (semitones 0, 2, 4, 5, 7, 9, 11, then 12 and up). Playback ratio `pitch_scale = pow(2.0, semitones / 12.0)`.
  - Shifting one sample more than double (an octave) breaks the timbre into chipmunk. Keep a sample per octave recorded at that height, or use a **Shepard tone**: layers an octave apart, the top fading out and the bottom fading in, so it circles at one height while sounding like it rises forever (Super Mario 64's endless stairs) [4].
  - Kill streaks climb the same ladder and reset when the fight ends.

## 3. Variation and fatigue

- Frequent sounds (basic hits, card plays, stacks, footsteps) get 3+ variants and never repeat back to back [1].
- Godot `AudioStreamRandomizer`: add variants with `add_stream()`, `playback_mode = PLAYBACK_RANDOM_NO_REPEATS`, `random_volume_offset_db` (start 1–2), `random_pitch_semitones` (start 0.5–1) [9]. **Never pitch-randomise pitched sounds**; it breaks the key. Vary them with separate takes.
- Play the same sound at most once per 55 ms, and cap simultaneous voices per player with `max_polyphony`.
- Long repetition fades. In Limbo the boy's footsteps grow quieter the longer he walks and come back when he stops: a 15 dB range [5].

## 4. Mixing

- **Buses.** Start with Master, Music, SFX (settings sliders usually bind to these names). To grow: Hero, Foe and UI under SFX, Ambience beside it; check the settings screen still works.
- **Priority.** Big moments (strong, max) > player actions > enemies > ambience and music. When a higher one plays, duck the lower.
- **Ducking.** `AudioEffectCompressor` on the Music and Ambience buses, `sidechain` set to the big-moment bus. Start at music −6 dB, ambience −10 dB, attack 50–100 ms [6].
- **Loudness.** Integrated −24 LUFS ±2 and true peak ≤ −1 dBTP on a recording of a typical fight: Sony ASWG-R001 for home (portable is −18) [7]. PC games have no fixed standard; if it's too quiet on laptop speakers, decide with the human how many dB to raise.
- **Per file.** True peak ≤ −1 dBTP, zero leading silence, a short fade at the end.

## 5. Music and ambience

- **Vertical layers.** Layers on one tempo switched on and off; add layers as tension rises (Inside's approach) [8]. Godot: `AudioStreamSynchronized` (`stream_count`, `set_sync_stream_volume()`).
- **Horizontal transitions.** Track to track. Godot: `AudioStreamInteractive` (`set_clip_stream()`, `set_clip_name()`, `add_transition()`); at runtime `AudioStreamPlaybackInteractive.switch_to_clip_by_name()`.
- **Horror.** Silence, low drones, unresolved chords. Limbo and Inside use a lot of silence and filter sound narrow and cold to build unease [5][8].
- **Hope.** As darkness lifts, the unresolved chord resolves to consonance, the drone drops out, highs come in and reverb shrinks so the space opens. A brief silence just before makes it land harder.

## 6. Finishing generated sound

How to generate with ElevenLabs: the `elevenlabs` skill. Never ship a raw take; go through this:

1. **Several takes.** 4 to 8 from one prompt. Generating layers (front, body, tail) separately makes picking easier.
2. **Pick.** Clear front, no band clash, right emotion.
3. **Trim.** Leading silence to 0, first peak aligned.
   `ffmpeg -i in.wav -af silenceremove=start_periods=1:start_threshold=-50dB out.wav`
4. **Layer.** Align picked layers on the front; delay body and tail a few ms for depth.
   `ffmpeg -i front.wav -i body.wav -filter_complex "[1]adelay=8|8[b];[0][b]amix=inputs=2:normalize=0" mix.wav`
5. **EQ.** Muddy: cut a little at 300–400 Hz (start −3 dB). Dull: lift highs.
   `ffmpeg -i mix.wav -af "equalizer=f=350:t=q:w=1:g=-3" eq.wav`
6. **Peak.** Measure true peak (rubric "How to measure") and set it to −1 dBTP with `volume=<dB>`.
7. **End.** Short fade-out (`afade=t=out:st=<s>:d=0.05`). For loops, enable `loop` when generating, turn Loop on in Godot's import, and listen to the seam.
8. **Format and name.** Short sounds WAV, long or looping ones OGG Vorbis. Name `<side>_<moment>_<nn>.wav` (e.g. `hero_star_up_01.wav`, `foe_death_02.wav`).

## 7. Winning moments are music (round and boss wins only)

Scope: round wins and boss deaths. Level-up, synergy, reward and hits belong to §8 and are never built as music stings (film-score stings on those read wrong).

Lengths measured from the game files (taken only to measure and then deleted, never used).

| Game | Win moment | Made of | Length |
| --- | --- | --- | ---: |
| Slay the Spire | normal fight win / boss win | SFX `SOTE_SFX_Victory` / music sting + separate SFX | 1.4 s / 20 s + 5.6 s |
| Balatro | blind won `Win`, money `Coin1~7` | one bar of music / 7 real coin recordings | 3.2 s / 0.4 s |
| Hades | `VictoryStinger`, per-layer stings (`ARStingers` stabs, strings, trombones) | live brass and string layers | 8.1 s / 3–6 s |
| Hearthstone | `Victory` (Peter McConnell) | composed orchestral | 10.6 s |
| Into the Breach | `Mus Victory` (Ben Prunty) | music | 7.5 s |
| Super Mario | Course Clear | fanfare, C major 150 BPM, rising ♭VI–♭VII–I | 4–6 s |

- **Length scales with rarity.** Frequent wins (normal fights, rounds) are 1.5–3 s; rare big wins (bosses, the end) are 8–20 s of music (Slay the Spire 1.4 vs 20 s). A medium round win: 2–3 s; a max boss death: a sting over 8 s.
- **Music closes the moment.** Hades drops the drum layer when a fight ends and plays the track's ending tag on the beat; Korb: it "conveys that feeling of victory" [13]. Into the Breach holds music back until the last mech lands: "before that you just hear ambient sound. It builds tension" [14].
- **SFX and music are one body.** Galaxy cut the sparkly part of the score so the star-bit sound could live, and Miyamoto had it fixed because "it's the most important action, but with this sound it feels really weak" [15]. Hearthstone designs sound around "what is the emotional impact of this card" (subjective sound design) and puts musical elements in SFX timed to card placement [16].
- **Material.** Most Hades SFX are layered, edited library recordings [13]. Korb first asks "what instruments would be in this place?" [13]. Your answer is your period palette (§2).
- **Harmony.** Mario's ♭VI–♭VII–I (in A major: F–G–A) borrows chords from the minor and lands on the major tonic [17]. It's the same motion as darkness into light.
- **Synth placeholder vs references, measured.** A sine-chord placeholder win measured 7 spectral peaks above −30 dB, stereo width 0, 0% below 250 Hz, 1.0 s. The references: 125–3,464 peaks, width 0.2–0.9, 12–99% below 250 Hz. Diagnostic only; it doesn't replace listening.

## 8. Level-up, synergy, reward, hit: SFX that strike on the frame

Moments where the team grows are SFX, not musical phrases. The first peak lands on the contact frame; weight and glow come from the tail after it. "Starting value (unsourced)" means capture, listen, retune.

**Measured references** (`measure.py --profile`; files measured from unofficial repositories and deleted, never used) [28]:

| Kind | Sound | Length | First peak | Hits (ms) | Brightness start→end | Width |
| --- | --- | ---: | ---: | --- | --- | ---: |
| Tier up | StS card upgrade `UpgradeCard` | 0.92 s | 6 ms | 3 (0, 290, 578) | 2.0→2.9 kHz, 67% in 2–6 kHz | 0.39 |
| Buff | StS `Buff_1~3` (three variants) | 1.3 s | 4–5 ms, top at 0.2–0.29 s | 1 | rises (4.9→6.4 kHz etc.) | 0.8–0.9 |
| Edition change | Balatro `holo1`, `foil1`, `polychrome1`, `negative` | 0.6–1.5 s | 0–3 ms | 1–2 | mostly darkens | 0–0.64 |
| Score hit | Balatro `multhit1~2`, `chips1` | 0.17–0.68 s | 0 ms | 1–2 | — | 0.2–0.44 |
| Hit | StS `FastBlunt`, `HeavyBlunt` | 0.43–0.54 s | 3–21 ms | 1–3 | 87–99% below 250 Hz | 0.1 |

- **Power moments are 0.6–1.5 s with an instant first peak.** Every measured tier and buff sound starts within 6 ms; the length is tail. Not "a sound over in under a second" but "a sound that bursts on the first frame and glows for a second or so".
- **Tiers climb in steps.** StS upgrade hits three times 0.29 s apart, brighter each time. Same idea as Peggle Blast pitching one sample up for excitement [19] and Peggle 2 climbing a diatonic scale in tune with the score [20]. Level-ups step once per tier (§2 "Endless rise"). One semitone = 2^(1/12) [21].
- **Buffs are wide and get brighter.** StS buffs have width 0.8–0.9 and rising highs; hits are width 0.1, lows only. Width and brightness let the ear tell "reward" from "got hit".
- **Generate three layers separately and stack them.** Front (click, metal strike, 0–30 ms) + body (weight: low thump or metal ring) + tail (bright rising shimmer or swell). Front narrow, tail wide. Three practitioners use the same structure (one transient, one tonal, one texture, "no more than three") [29][30]. Put pitch only in the player-side tail, in your key.
- **One identity, add layers per tier.** The WoW level-up sound stayed almost unchanged for ten years and became a memory in itself [22]. Keep one identity for every tier and synergy step; add steps, a low layer and tail length. StS rotates three variants of the same buff.
- **Don't just make it bigger.** Peggle's team kept escalating presentation, found players responded more to simpler expression, and refined that instead [23].
- **Hits are short, narrow, low, and many.** Reference hits are 0.43–0.54 s, mostly low, width 0.1. A basic hit firing hundreds of times a level should be shorter (body under 120 ms). Pitch and volume randomisation alone doesn't prevent fatigue; rotate several different takes [24]. Balatro's reverse-engineered code uses ±2% pitch (unofficial) [25]. Keep common hits quiet; only moments that carry information get loud (Vampire Survivors analysis) [26].
- **Processing.** Push lows and mids slightly and compress lightly so it sits ahead of other sounds in its band [27]. UI and reward sounds: trim the onset to 0–5 ms, dip harsh 3–6 kHz slightly, limit the peaks (sound-library vendor article) [31]. On strong and max moments with hitstop, the sound's tail covers the freeze. Sound never pauses.
- **Unresearched.** No practitioner write-up found on tier-up sound lengths or layers for TFT, Hearthstone or Marvel Snap. Riser (anticipation) length has no source either, so it isn't set. If the picture already has an anticipation beat, the sound starts at contact.

## Sources

1. Ronny Mraz (Avalanche Studios), How to design a weapon sound for video games: https://splice.com/blog/design-weapon-sound-video-games/
2. Principles of Game Audio and Sound Design, Sound design guidelines: https://ebrary.net/282895/education/sound_design_guidelines
3. ITU-R BT.1359-1, Relative timing of sound and vision for broadcasting: https://www.itu.int/rec/R-REC-BT.1359
4. Shepard tone: https://en.wikipedia.org/wiki/Shepard_tone
5. Martin Stig Andersen, Limbo interview (Designing Sound): https://designingsound.org/2011/08/01/limbo-exclusive-interview-with-martin-stig-andersen/
6. How to design a dynamic game audio mix (Splice): https://splice.com/blog/dynamic-game-audio-mix/
7. Sony ASWG-R001 loudness recommendation: https://gameaudiopodcast.com/ASWG-R001.pdf · Audiokinetic, Mastering a Game with Wwise: https://www.audiokinetic.com/en/blog/mastering-a-game-with-wwise-part1/
8. Inside: Game Audio Using Wwise (Audiokinetic): https://www.audiokinetic.com/en/blog/inside-game-audio-using-wwise/ · Audio design deep dive: Inside: https://www.gamedeveloper.com/audio/audio-design-deep-dive-using-a-human-skull-to-create-the-sounds-of-i-inside-i-
9. Godot 4 Audio buses: https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html · AudioStreamRandomizer: https://docs.godotengine.org/en/stable/classes/class_audiostreamrandomizer.html
10. Sammy Timberg (Fleischer music director): https://en.wikipedia.org/wiki/Sammy_Timberg · Bernard Herrmann (CBS Symphony, Mercury Theatre radio): https://en.wikipedia.org/wiki/Bernard_Herrmann · a free orchestral sample library with these instruments, VSCO 2 CE: https://github.com/sgossner/VSCO-2-CE
11. Film noir, "Music": https://en.wikipedia.org/wiki/Film_noir
12. Theremin, "Film music": https://en.wikipedia.org/wiki/Theremin
13. Darren Korb, The Sound of Hades (Gameplay, 2020-12-24): https://gameplay.co/hades-game-music-sound-design-darren-korb-supergiant-games/
14. Ben Prunty, How I made Into the Breach's soundtrack (PC Gamer, 2018): https://www.pcgamer.com/how-i-made-into-the-breachs-soundtrack/
15. Iwata Asks, Super Mario Galaxy vol. 3 "Sound Effects You Can Feel": https://iwataasks.nintendo.com/interviews/wii/super_mario_galaxy/2/3/
16. Meet the sound team behind Hearthstone's harmonic design (Blizzard): https://hearthstone.blizzard.com/en-gb/news/23964694/inside-battle-net-meet-the-sound-team-behind-hearthstone-s-harmonic-design
17. Course clear fanfare: https://www.mariowiki.com/Course_clear_fanfare
18. Game file lengths: khinsider game rips (Slay the Spire, Balatro, Hades, Hearthstone, Into the Breach): https://downloads.khinsider.com/
19. Audiokinetic, Real-Time Synthesis for Sound Creation in Peggle Blast! (2016-05-30): https://www.audiokinetic.com/en/blog/real-time-synthesis-for-sound-creation-in-peggle-blast/
20. Guy Whitmore, Peggle2: Sonic Joy! (GANG, 2014-01-24): https://www.audiogang.org/peggle2-sonic-joy/ · RJ Mattingly, Peggle Blast! Peg Hits and the Music System (GANG, 2015-02-11): https://www.audiogang.org/peggle-blast-peg-hits-and-the-music-system-2/
21. George Prosser, The Power of Pitch Shifting (Game Developer, 2017-01-02): https://www.gamedeveloper.com/audio/the-power-of-pitch-shifting
22. Jack Menhorn, Psychology of 10 Years of Sound in World of Warcraft (Designing Sound, 2014-12-11): https://designingsound.org/2014/12/11/psychology-of-10-years-of-sound-in-world-of-warcraft/
23. Joshua Yearsley, Form in Game Rewards (2011-07-15, quoting Peggle's development): https://joshuayearsley.com/synonyms/form-in-game-rewards-or-how-to-squeeze-out-every-last-drop-of-dopamine-from-your-brain/
24. Game Audio and Sound Design (Routledge, PDF, undated): https://www.routledge.com/rsc/downloads/GAME_AUDIO_FINAL.pdf
25. balatro-src reverse-engineering repo, `functions/common_events.lua`, commit 3a42f613 (unofficial): https://github.com/balatro-src/balatro-src-reverse-engineering/blob/3a42f613/functions/common_events.lua
26. Game Design Lab, Vampire Survivors Audio Design & Feedback (analysis, undated): https://teemo.dev/game-design/vampire-survivors/systems/audio-design-and-feedback/
27. Nathan Lovato, Squeezing more juice out of your game design! (Game Developer, 2015-04-01): https://www.gamedeveloper.com/design/squeezing-more-juice-out-of-your-game-design-
28. Measured reference files: Balatro `resources/sounds` (balatro-src-reverse-engineering, unofficial): https://github.com/balatro-src/balatro-src-reverse-engineering/tree/main/resources/sounds · Slay the Spire `SOTE_SFX_*` (EmbersKiln, unofficial copy): https://github.com/1362146771/EmbersKiln/tree/main/art/audio/sts/audio/sound
29. JJ Lyon, Funky game sounds (Krotos, 2026-10-09, tool vendor): https://krotos.studio/blog/funky-game-sounds
30. Kuba Rogut, Game sound effects (SFX Engine, 2026-02-18, tool vendor): https://sfxengine.com/blog/game-sound-effects
31. UI sound design with AI (Envato, 2026-02-05, sound-library vendor): https://elements.envato.com/learn/ui-sound-design-ai
