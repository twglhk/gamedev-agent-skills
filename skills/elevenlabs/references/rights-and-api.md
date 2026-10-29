# Rights, account settings and API

Checked against the Terms of Service (non-EEA) and ElevenCreative Terms (both "Last updated 09 October 2026"), the Voice Library Addendum (6 March 2026) and the API reference. Terms change; reopen them before any large spend. Not legal advice. Source numbers [n] refer to [sources.md](sources.md).

## Rights

- **Commercial use = paid plan only.** Free users may use the Services for non-commercial purposes only; paid users may use them commercially (Terms 1(c)) [15].
- **You keep the output.** "As between you and ElevenLabs, you retain all rights in and to your Output" (Terms 4(c)) [15]. The Text to Dialogue FAQ says the same and repeats that commercial use needs a paid plan [14].
- **Sound effects inside a game: yes. Sold or shared alone: no.** Output may go into "films, trailers, advertising, video, games, applications" combined with other material. It may not be sold, licensed or distributed on a standalone basis, as isolated audio files or samples, or in any sound, effects or music library (ElevenCreative Terms, Exhibit 4 §2) [17]. So: no sound pack, no "OST + SFX" download, no raw `.wav` folders shipped as a product.
- **ElevenLabs' licence to your content.** You grant ElevenLabs a perpetual licence to your Input and Content to provide and improve the Services (Terms 4(d)) [15]. Training use can be switched off: Terms and privacy → Data use → "Improve the models for everyone" [18].
- **The same sound can reach someone else.** Two users may get the same or similar output (Terms) [15].
- **Community Sharing.** If on, ElevenLabs may pick your sound effects for the public community library; nothing is shared while it is off (Exhibit 4 §3) [17].
- **Voice Library voices can disappear.** The owner can withdraw a shared voice; outputs made before the end of its notice period stay usable, new ones don't (Voice Library Addendum) [5].
- **Dubbing v2 only:** a separate restriction on feature films, TV and "professional audiovisual entertainment productions". It doesn't cover Sound Effects or TTS.

### Check once, before the first generation

1. Data use → "Improve the models for everyone" off.
2. Sound effects Community Sharing off.
3. Plan is paid (`tier` from `/v1/user/subscription`).

## History and logs

- Zero Retention (`enable_logging=false`) is Enterprise only [1][19].
- Sound effects are not a history source in the History API, so SFX items can't be listed or deleted one by one through the API.

## API: sound effects

| Item | Value |
| --- | --- |
| Endpoint | `POST https://api.elevenlabs.io/v1/sound-generation` [3] |
| Model | `eleven_text_to_sound_v2` (default). `eleven_text_to_sound_v3` is listed but undocumented |
| Body | `text` (required; web limit 450 characters) · `duration_seconds` 0.5–30 (the overview page says 0.1; the API rejects it) · `prompt_influence` 0–1, default 0.3 · `loop` |
| Format | Query `output_format`, default `mp3_44100_128`. `wav_*` added 2026-10-19; WAV 48 kHz for non-looping effects [1][19]. The API page says 44.1 kHz WAV/PCM needs Pro; try once, a refusal isn't billed |
| Web | Four takes per press; History tab download as MP3 44.1 kHz or WAV 48 kHz [2] |
| Cost | 40 credits per second when duration is set [1]; prompt length doesn't matter [2]. Actual bills have measured well below this; read usage after the pilot |

```bash
# Key from an untracked .env only. Never echo it.
set -a; . ./.env; set +a
curl -s -X POST "https://api.elevenlabs.io/v1/sound-generation?output_format=wav_48000" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"...","duration_seconds":1.0,"prompt_influence":0.3,"model_id":"eleven_text_to_sound_v2"}' \
  -o design/fx/<moment>/raw/<name>_01.wav
```

Worst-case estimate: seconds × 40 × takes. Six 1.5 s takes = 360 credits.

## API: music (Eleven Music)

From the API reference (https://elevenlabs.io/docs/api-reference/music/compose), pricing (https://elevenlabs.io/pricing) and Music Terms (https://elevenlabs.io/music-terms). Reread the terms before a new kind of use.

| Item | Value |
| --- | --- |
| Endpoint | `POST https://api.elevenlabs.io/v1/music`, `model_id` `music_v1` (default) · `music_v2` · `music_v2_5` |
| Length | `music_length_ms` 3,000–600,000. A 2 s sting means generating ≥ 3 s and cutting |
| Control | Prompt or `composition_plan` (sections, `positive_styles`). No key or tempo parameter: key comes only from text, so measure every take like a pitched SFX |
| Cost | 900 credits per minute (≈15 per second). One measurement: `music_v1` at `music_length_ms` 5000 billed 62 credits each and returned 6.1–7.1 s files. No cost header and the subscription counter lags; read `/v1/usage/character-stats?breakdown_type=product_type` (`Music`) |
| Rights | Depend on plan. Lower tiers have excluded film, TV, radio and "Studio Games" and defined an indie-game revenue ceiling (with a deadline to change plan once exceeded). Read the Music Terms' game clauses for your plan before shipping music |
| Format | mp3 44.1 kHz; PCM via API is listed for Pro |

## API: voices

| Item | Value |
| --- | --- |
| TTS | `POST /v1/text-to-speech/{voice_id}`, `model_id` `eleven_v4` (the default if omitted is `eleven_multilingual_v2`; always set it) [10] |
| Settings | `stability` (0.5) · `similarity_boost` (0.75) on v4; `style`, `speed`, `use_speaker_boost` on v2/v3 only [10][6] |
| Continuity | `seed` (best effort) · `previous_text` / `next_text` · `previous_request_ids` (max 3) [10] |
| Dialogue | `POST /v1/text-to-dialogue`, v4 or v3; keep all `inputs[].text` ≤ 2,000 characters per request [14] |
| Voice Design | `POST /v1/text-to-voice/design` (`voice_description`, `text` 100–1,000 chars, `guidance_scale`, `seed`, `loudness`, `model_id`), then `POST /v1/text-to-voice` with the chosen `generated_voice_id` [9] |
| Voice Changer | `POST /v1/speech-to-speech/{voice_id}`, `eleven_multilingual_sts_v2`, `remove_background_noise`; 5 min max; 1,000 characters per minute of audio [11] |
| Usage | `/v1/usage/character-stats` for credits per day; `/v1/user/subscription` for tier and slots. Listing models (`/v1/models`) needs the `models_read` key permission |
| Cost | TTS about 1 credit per character on the web for v3, cheaper via API; read the real figure from usage after the pilot |

Credits reset monthly; unused credits roll over up to two months' worth as long as the plan isn't cancelled or downgraded [21].
