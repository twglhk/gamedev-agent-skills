# Tools and commands

Contents: Capture · Cut recipes · Storyboard sheet · Captions and cards · Sound · Measuring sound · Thumbnails and cover frames · When a voice exists · MCP verdict · Music and SFX sources

Homebrew's default ffmpeg may lack freetype/libass, so `drawtext`, `subtitles` and `ass` filters may be missing. These recipes never need them: text is always HTML → PNG → `overlay`.

## Capture

- Godot Movie Maker: `godot --path game --write-movie /abs/out.avi --fixed-fps 60 --resolution 1920x1080 -s DRIVER`. `--fixed-fps` gives every frame the same `delta`, so footage is frame-accurate on any machine. Writers: AVI (MJPEG + PCM, 4 GB limit), PNG sequence + WAV (lossless), OGV. Transcode to H.264 afterwards. Movie Maker needs a real window, never `--headless`. [Godot docs, creating_movies]
- Audio is mixed at 48 kHz, locked to frames, so loudness measures are repeatable.
- **Capture bigger than the output.** Raise `Rendering > Scaling 3D > Scale` above 1.0 for supersampling, or set the viewport above the screen size; crop and scale down in the edit. A 9:16 crop of 16:9 keeps only 31.6% of the frame, so a vertical video should come from a **native 1080×1920 camera** (viewport override under the `movie` feature tag), not a crop.
- If your battles are deterministic, fix a seed per shot so the same fight can be re-shot after an art change or from another angle. Note the seed in `brief.md`.
- Capture with in-game music off and SFX on when the edit will carry its own music; keep a second take with full game audio.
- UI: off by default for social cuts, except the one element the clip is about. HUD **on** for the Steam slot-1 trailer.
- Capture features (trailer free camera, per-unit follow camera, slow motion, hitstop exaggeration, per-element UI toggles, vertical camera) are dev work: request them as one item.

## Cut recipes

```bash
# trim
ffmpeg -ss 12.0 -to 27.5 -i src.mp4 -c:v libx264 -crf 18 -c:a aac cut.mp4
# 4:5 centre crop from 16:9
ffmpeg -i src.mp4 -vf "crop=ih*4/5:ih,scale=1080:1350" cut_4x5.mp4
# 9:16 with a blurred fill behind the 16:9 picture (wide shots only; reads like a repost)
ffmpeg -i src.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" fill.mp4
# half speed (picture and sound)
ffmpeg -i a.mp4 -filter_complex "[0:v]setpts=2*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" slow.mp4
# concat cuts that share codec and size (list.txt: file 'a.mp4' per line)
ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4
# hard cut on a hit with a 2-frame white flash (30 fps)
ffmpeg -i a.mp4 -vf "fade=t=in:st=0:d=0.066:color=white" a_flash.mp4
# freeze the last frame 0.6 s (a held beat before a sting)
ffmpeg -i a.mp4 -vf "tpad=stop_mode=clone:stop_duration=0.6" a_hold.mp4
# push-in 0→8% over 1.5 s from 4.0 s, ease-in-out, centred
ffmpeg -i a.mp4 -vf "zoompan=z='1+0.08*(1-cos(PI*min(max((it-4)/1.5,0),1)))/2':d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=1080x1920:fps=30" push.mp4
# blur a region (a name, an e-mail, a path in a screen capture) for the whole clip: w:h:x:y of the box
ffmpeg -i a.mp4 -filter_complex "[0:v]split[a][b];[b]crop=600:120:100:900,boxblur=20:2[bl];[a][bl]overlay=100:900" -c:a copy blurred.mp4
# before/after side by side
ffmpeg -i before.mp4 -i after.mp4 -filter_complex "[0:v]scale=960:-2[a];[1:v]scale=960:-2[b];[a][b]hstack" -an ba.mp4
# stacked 9:16 from one 16:9 source: boss region on top, team region below (x,y,w,h per shot)
ffmpeg -i src.mp4 -filter_complex "[0:v]split[t][b];[t]crop=960:540:480:0,scale=1080:960[top];[b]crop=960:540:480:540,scale=1080:960[bot];[top][bot]vstack,format=yuv420p" stack.mp4
# J cut: shot b's sound arrives 0.4 s before its picture (a = 5 s; b's picture from src 12 s, its sound from 11.6 s)
ffmpeg -i a.mp4 -ss 12 -t 4 -i src.mp4 -ss 11.6 -t 4.4 -i src.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v];[0:a]atrim=0:4.6[aa];[aa][2:a]concat=n=2:v=0:a=1[a]" -map "[v]" -map "[a]" j.mp4
# full-range Godot capture → TV range (X rejects yuvj420p)
ffmpeg -i in.mp4 -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -c:a copy out.mp4
```

Encoding defaults: `-c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart`, AAC 192k 48 kHz. Steam needs ≥ 5,000 kbps; YouTube re-encodes everything, so feed it a high-quality file.

The push-in eases in and out (slow, faster, slow); on a test chart the edge moved 5, 10, 12, then 5 px per quarter. Use the linear form only for a slow creep.

## Storyboard sheet

One still per beat at each beat's planned in-point, tiled into `storyboard.png`. Write each still's seconds and beat in `brief.md` in the same order (without `drawtext`, the labels live in the brief).

```bash
i=0; for t in 0.5 2 4 6.5 9 11; do i=$((i+1))
  ffmpeg -v error -ss $t -i src.mp4 -frames:v 1 -vf scale=480:-2 -y sb_$(printf %02d $i).png; done
ffmpeg -v error -i sb_%02d.png -vf "tile=3x2:padding=8:color=black" -frames:v 1 storyboard.png
```

Numbered names keep the order (a glob would sort `11` before `2`). For a graphic that doesn't exist yet, the still is a `render.py --still` peek.

## Captions and cards

`scripts/captions.py` renders each cue from HTML to a transparent PNG the size of the video and overlays it between its start and end. Looks: `plain` (heavy sans, dark stroke), `band` (solid band with an offset shadow), `panel` (dark translucent panel, thin frame, serif). Override colours with `colors` in the spec to match your brand. `frame: short` uses the 9:16 safe box; `feed` uses 6% margins.

- Fonts: the default stack uses macOS faces with CJK coverage (Hiragino Sans, Apple SD Gothic Neo). Set `font` in the spec on other systems (e.g. `"Noto Sans CJK JP", sans-serif`). Wrap a word in `<em>` for the accent colour, one word per line at most.
- Full-screen title cards: a cue with `at: middle`, `size: l`, on a black or frozen frame (`tpad`) so text and new gameplay never share a second.
- The PNGs and HTML stay in `<out>_caps/`; fix a line in `captions.json` and rerun.
- X also accepts an SRT track (web composer, `POST /2/media/subtitles`). Burned-in captions stay the default because X doesn't auto-caption and every feed autoplays muted.

## Sound

- Targets: −14 LUFS integrated, true peak ≤ −1 dBTP for X, Reddit, YouTube and Steam. Festival masters often ask −23 LUFS (read their spec). `check.py --fix-audio` runs two-pass `loudnorm` with `linear=true` and copies the video.
- Mix order: the sound that carries the moment (the hit, the sting), then SFX, then music. Duck music −6 dB under hits (`sidechaincompress`) or cut it.
- Making and finishing a sound: `fx-craft` and `elevenlabs` skills.
- Lay an SFX at a time: `ffmpeg -i cut.mp4 -i sting.wav -filter_complex "[1:a]adelay=6200|6200[s];[0:a][s]amix=inputs=2:normalize=0[a]" -map 0:v -map "[a]" -c:v copy out.mp4`. The hit must land within 1 frame of the picture (more than 45 ms early or 125 ms late reads as off).
- A clip with no audio stream is fine muted on X and Reddit; Shorts and trailers want sound.
- Music under a voice: start the bed at `volume=0.1` (−20 dB) against the voice, then measure both stems. An agent that only "adds music" usually lays it louder than the voice [PRAC Moran].

## Measuring sound

An agent can't hear, so it measures. ffmpeg alone covers the essentials:

```bash
ffmpeg -nostats -i cut.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12        # integrated LUFS, true peak
ffmpeg -i cut.mp4 -af silencedetect=n=-40dB:d=0.3 -f null - 2>&1 | grep silence_  # silent spans
ffmpeg -i vo.wav -af ebur128 -f null - 2>&1 | grep "I:"; ffmpeg -i bed.mp3 -af ebur128 -f null - 2>&1 | grep "I:"   # voice/music gap in LU
```

For hit times (onsets), BPM, downbeats and sections, use an audio analyser. One option is the HyperFrames CLI (`hyperframes audio <file> --only loudness,silence,onsets` or `--only bpm,downbeats,sections`), which runs locally on any audio or video file. Set `HYPERFRAMES_NO_TELEMETRY=1`, keep the default `--quality local` (🔴 `--quality best` uploads to a cloud service and may bill), and pin the version. librosa (`onset_detect`, `beat_track`) is a Python alternative.

- Use it to mark the music before cutting, to check that every hit lands within 1 frame of its picture event, and to read the voice/music gap.
- Beat trackers guess. Check the first downbeat by eye on the waveform before cutting a trailer to it.
- `check.py` stays the delivery gate for loudness; the analyser is for finding where things are.

## Thumbnails and cover frames

- Long-form thumbnail: HTML → PNG with Playwright at 3840×2160 (min 1280×720). One focal point (a character's or monster's face), 0-3 words that don't repeat the title, strong value contrast, same layout zone and type every episode.
- Shorts cover frame: custom Shorts thumbnails need the Partner Program, so build a clean 0.5-1 s frame into the cut (key pose, no UI clutter, important part inside the centre 4:5) and pick it in Studio.
- Steam poster: must be a frame of the video, 1920×1080, no text.
- Glance test: look at it at 168×94 and 360×202 px. If the subject doesn't read, change the image, not the text.

## When a voice exists (new installs need approval)

```bash
brew install ffmpeg-full    # keg-only: call /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg by full path
brew install whisper.cpp    # whisper-cli with Metal; download a ggml model separately (large-v3-turbo)
whisper-cli -m <model> -f vo.wav -ml 1 -oj    # word-level timings as JSON
```

- **If the narration is TTS, ask the provider for timings instead of transcribing.** ElevenLabs `POST /v1/text-to-speech/{voice_id}/with-timestamps` returns the audio plus each character's start and end time for that exact take, so word times for captions and cut points need no ASR step. Transcribe only a recorded human voice.
- Bad timestamps are how an agent's silence cut chops half a word [PRAC Moran]. If whisper misplaces word edges, try NVIDIA Parakeet (local, ~640 MB; HyperFrames' audio docs rank it above whisper.cpp, 6.05% vs 7.44% WER). Any model download is a new dependency: ask first.

Word timings → an ASS file with `\kf` karaoke tags → `ffmpeg-full -vf ass=captions.ass`. Edit the ASS `Style:` line, not `force_style` (commas break `-vf`). Upload a plain SRT to YouTube as well. WhisperX (wav2vec2 alignment) only if whisper.cpp timing misses fast speech. mlx-whisper is faster but has a documented repetition-loop failure: diff its output against whisper.cpp. `auto-editor` (Unlicense) can cut silences in a voice-over.

## MCP verdict

No MCP server is needed. Agents call ffmpeg, Godot, Playwright and TTS APIs directly through the shell, which is reproducible and keeps footage on your machine.

| Server | Why not |
| --- | --- |
| burningion/video-editing-mcp | Front end for Video Jungle, a paid cloud service that uploads footage |
| DaVinci Resolve MCPs (samuelgursky, luquimbo, open-fusion-mcp, Resolve built-in) | Need paid Resolve Studio running in a GUI; `run_script` executes arbitrary Python |
| Thin ffmpeg wrappers (none-stack, kevinten-ai, yubraaj11, ff-toolkit) | Duplicate the CLI with less control |
| elevenlabs/elevenlabs-mcp | Archived; call the API |
| Remotion skills repo | No licence stated; read the docs' `.md` pages instead |

Worth a look after a licence and code read: `kajisho5/ffmpeg-skill` (delivery checks, karaoke) and `kyanitelabs/kinocut` (render provenance logs).

## Music and SFX sources

Licences as read in October 2026. Re-read before first use and record the date in the manifest.

| Source | OK for marketing video? |
| --- | --- |
| Your game's own audio and SFX | Yes. Preferred: it is also the brand |
| Mixkit Stock Music Free License | Yes for marketing: social posts, online ads and YouTube allowed; not inside the game, TV or CDs; no remixing into a music-only track; contributors may not register tracks with Content ID (`mixkit.co/license/modal/musicFree/`) |
| Sonniss GDC bundles | Yes: royalty-free, commercial, no attribution, lifetime; no redistribution as SFX, no AI/ML training (`sonniss.com/gameaudiogdc`) |
| Kenney audio packs | Yes: CC0 (`License.txt` in each pack) |
| Pixabay music and SFX | Read the licence and Content ID pages in a browser before first use |
| Incompetech, Free Music Archive | Only with a credit line (CC BY), and creators report Content ID claims on these tracks. Avoid if a no-credit source covers the need |
| Paid stock (Uppbeat, Epidemic, Artlist) | A spend decision for the human. Uppbeat's free and Essentials tiers cover only individuals' own channels |
| ElevenLabs SFX (paid plan) | Yes, with approved spend and an AI-log line. About 200 credits a generation |
| ElevenLabs Music (paid plan) | Starter: individuals only, online commercial use and sync to video allowed, no attribution, monthly generation and download caps, no music-streaming release, no lossless WAV. About 900 credits a minute. Check the current Music Terms for your plan |
| Suno Free/Basic | No (non-commercial). Pro/Premier downloads are commercial; a spend decision |
| Trending or licensed tracks | No: TikTok business accounts can't use them; a Content ID claim blocks Shorts over 1 min |
| YouTube Audio Library | Copyright-safe on YouTube only; Creative Commons tracks need credit in the description. No guidance for use off YouTube, so not for X or Reddit |
