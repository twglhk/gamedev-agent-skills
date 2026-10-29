# Rubric: the gate before anyone sees it (one failure = redo)

Pass all of it for every moment. "Measured" items are judged by numbers, "Look" and "Listen" items by opening the scene yourself. Fix failures one at a time and recapture.

## How to measure

`C=scripts/capture.py` (path relative to this skill). Add `--godot`, `--project`, `--size` before the subcommand if your setup differs from the defaults.

1. **Preview scene.** `game/fx/preview/<moment>.tscn`, using the game's battle camera and the real location set. It starts with a few frames of no effect, then plays the moment once. Frame 0 is the background the effect has to beat.
2. **Record.** One tool takes picture and sound together; a window opens.
   `python3 $C record res://fx/preview/<moment>.tscn /tmp/fx/<moment>.avi --frames <n> -- <scene args>`
   Discard the take if Godot's reported frame count differs from the decoded count or the log has an ERROR. Record the same scene again at ×2 (and ×4 if your game has it). Record the worst crowd (full board, everyone hitting at once) separately.
3. **Measure.** `python3 $C measure /tmp/fx/<moment>.avi --box x,y,w,h`
   - `--box` is where the effect fires (pixels); contrast and brightness curve are measured inside it.
   - Output: contact frame, peak frame, contrast, decay, sync, true peak, loudness, peak screen area (compare with vfx.md §5).
   - One sound file: `python3 scripts/measure.py --wav <file>.wav` gives leading silence, true peak, loudness.
4. **Media to show.** `python3 $C media /tmp/fx/<moment>.avi --crop x,y,w,h --out design/fx/<moment>/<take> --name <name> --probe x,y,w,h [--near <frame>] [--key-box x,y,w,h]`
   - Video: `<name>-color.mp4` and `<name>-gray.mp4`, 1:1 crops at game size (no scaling).
   - Key frames: 0, 1, 2, 4, 7, 10 from contact, one PNG each, colour and gray (`--keys` to change). The contact is found from brightness inside `--probe`. Movie Maker frame numbers drift by one between runs, so never trust them.
   - If the scene has its own gray mode, pass that take with `--gray-clip`; otherwise gray is computed from the colour take's luminance.
5. **Determinism.** A test runs the same seed and team with effects on and off and compares the sim's log hash. In Godot headless on macOS a failing run can still exit 0, so check the runner's final pass line, not the exit code.
6. **Performance.** `python3 $C perf res://fx/preview/<moment>.tscn --out /tmp/fx/perf-<moment> --cond 'crowd-x1=<scene args>' --cond 'crowd-x2=<scene args> --speed=2'` (5 runs each by default, on and off alternating). The scene must take `--qa-out=<path>` and write frame-time JSON (format in `capture.py`'s header). Recount with `python3 $C perf-report <dir>`.

## Picture

- [ ] **Three gray layers** (look). At the contact frame of the gray key frame, centre (brightest), middle and edge separate. If gray doesn't read, colour won't save it (Riot VFX style guide).
- [ ] **Contrast** (measured). Brightest 2% at the contact peak vs frame-0 background relative luminance, **at least 3:1**. Borrowed from WCAG 2.1 SC 1.4.11 (non-text contrast). Enemy effects never outshine the heroes.
- [ ] **Brightness only falls** (measured). After the peak, zero frames rise more than 5% of the peak. A deliberate double hit must be written as two beats in the direction note.
- [ ] **Beats** (measured). Anticipation, contact and dissipation frame counts within ±2 of the direction note.
- [ ] **Motion inside beats** (look). Step through key frames: contact pops then settles, dissipation erodes from inside, shards ease out. Nowhere does size or brightness change by the same step every frame (vfx.md "Motion inside a beat").
- [ ] **Strength order** (look). Side by side, one side's moments rise weak < medium < strong < max in size, brightness, length and shake. Zero cases of weak beating strong.
- [ ] **Game size** (look). In the game-size clip the one key thing (hit point, star, linking beam) reads.
- [ ] **Speed** (look). At ×2 and ×4 the contact still reads and dissipation doesn't hide the next moment.
- [ ] **Crowd** (look). In the worst scene strong and max moments aren't buried and basic hits don't cover the screen. You can say in one sentence what happened and why.
- [ ] **Light rule** (look). Warm light only on the player side; enemy and shadow side use cold, ink and eerie light (or whatever split your art direction sets).
- [ ] **One with the toon look** (look). No realistic soft smoke or normal-mapped detail; reads as one picture with the ink lines and stepped shading (Guilty Gear Xrd).
- [ ] **Budget** (measured). Live count, particles (by `amount`) and peak screen area within the strength's cap (vfx.md §5). In the real fight, overdraw, shadow-casting effects and effect shader count within [perf.md](perf.md) "Proposed effect budget" (census + `capture.py overdraw`, same frames on and off).
- [ ] **First draw** (measured). From 2 s after the level opens, the frame an effect first appears has zero Surface or Draw pipeline compiles (if the off run has them too, it's not the effect).
- [ ] **Ink lines** (look). Blended effects get no post-process ink line, so they draw their own rim in the shader; scissored effects don't get a doubled line (shaders.md "Godot behaviour that bites").
- [ ] **Performance** (measured). Worst scene ×1 and ×2, on and off 5 runs each (`capture.py perf`), all four hold. Off runs also have frames over 16.7 ms, so always compare with off.
  - Frames over 16.7 ms (one refresh) added by effects: at most 1 per 1,000.
    - Report vsync state and refresh rate every time. With vsync on at 60 Hz, intervals sit on 16.67 ms and about half read a hair over, so read this line only as on-minus-off, beside "frames over 20 ms" and "game CPU over 16.7 ms".
  - Zero frames over 33.3 ms (two refreshes, a visible hitch) with effects on.
  - Median p99 of five runs at most 0.5 ms above off.
  - Battle log on = off, and every run clean (no competing Godot or Blender work).
  - Measure GPU share on Vulkan (`capture.py perf --driver vulkan`). Per-tier frame ceilings are your project's call; until agreed, report them as reference, not verdict.

## Sound

- [ ] **Onset** (measured). The contact sound file's first sound starts within 10 ms (no leading silence).
- [ ] **Sync** (measured). In the clip, sound onset vs contact frame **within 17 ms (one frame)**. Tighter than the human detection limit (ITU-R BT.1359: sound 45 ms early, 125 ms late).
- Diagnostic, not a gate: **buried.** `capture.py cues` reports how many dB a cue rises over what was already sounding. Under 10 dB is flagged "buried" (an unvalidated threshold; ducking typically lifts a buried cue from about 5 dB to 15 dB).
- [ ] **True peak** (measured). Each file and the worst-crowd clip **at or below −1 dBTP** (Sony ASWG-R001). Zero clipping.
- [ ] **Loudness** (measured). A long recording (10+ min) of a typical fight integrates to **−24 LUFS ±2** (ASWG-R001, home). Short clips are reference only.
- [ ] **Strength order** (measured + listen). Strong and max moments are clearly louder (momentary loudness) than basic hits, and you hear music and ambience duck.
- [ ] **Side rule** (listen). If your game splits sides by pitch: player side pitched and in one key, enemy side unpitched.
- [ ] 🔴 **Source** (look). Every sound's source (which instrument or object recording, library name and licence, generation prompt, synth layer) is written in `notes.md` and the candidate. If the identity the ear hears is a code synth, fail.
- [ ] **Side by side with references: sound** (measured). Compare with at least 2 reference files of the same kind of moment by the same method (`measure.py --profile ref.ogg ours.wav …`: length, first peak, hits, bands, brightness path, pitch, width, momentary loudness): length, layer count, instrument family, spectral peak count (above −30 dB), stereo width (side/mid), share below 250 Hz. Put the table in `notes.md`. "Ten times fewer peaks or zero width = thin" is a proposed diagnostic threshold. Numbers catch thinness; they are not evidence it sounds good.
- [ ] **Threshold sources** (look). Every numeric threshold used to fail something has a source (literature or reference measurement). An unsourced threshold is a proposal and never a reason to drop recorded material and keep a synth. (A "keep only above 6 kHz" rule once cut a real coin sound to 12 ms; Balatro's coin has 87% of its energy above 6 kHz anyway.)
- [ ] **Variation** (look). Frequent sounds have 3+ variants, never the same one twice in a row, and the same sound never twice within 55 ms.
- [ ] **Three speakers** (listen). Audible on laptop speakers, headphones and mono (`ffmpeg -i x.wav -af "pan=mono|c0=.5*c0+.5*c1" mono.wav`). If the thump vanishes on a laptop, add a high click layer.
- [ ] **Fatigue** (listen). Ten typical fights in a row with nothing grating. The human's ears make the final call.

## Together

- [ ] **Determinism** (measured). Log hash equal with effects and sound on and off.
- [ ] **Emotion** (look). The emotion in the moment table shows and sounds. Thrill bursts and rises; hope is warm light pushing back darkness; dread drains light and saturation.
- [ ] **Side by side with references** (look). Reference clip and ours at the same size and speed. Our detail layers (flash, shards, smoke, afterglow, light change, screen device, sound layers) are not fewer than the reference's. Write any missing layer in `notes.md` and add it.
- [ ] **Clearing** (look). Before a max moment, 0.1 to 0.3 s of space (sound dipped, light pressed down).
- [ ] **One frame** (measured). Picture contact, sound front, hitstop start and shake start are the same frame.
