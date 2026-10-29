# Sources (read October 2026 unless dated otherwise)

Grades: OFF = platform or project doc · SURV = study or multi-game dataset · PRAC = working practitioner or single-game numbers · VEND = vendor. One source makes a proposal; two independent sources, an official doc or your own measurement make a rule.

## Platforms (OFF)

- Steamworks, Trailers: partner.steamgames.com/doc/store/trailer (first trailer gameplay with HUD, muted viewing, microtrailer from six 1 s clips, ≥ 5,000 kbps)
- Steamworks blog, trailer display change, 2023-05-02: steamcommunity.com/groups/steamworks/announcements/detail/5358762517221792489 (first two trailers before screenshots)
- Steamworks, Next Fest tips: partner.steamgames.com/doc/marketing/upcoming_events/nextfest/tips · Valve Next Fest Q&A, 2026-04-22: youtube.com/watch?v=tcI4jPCmH8c
- Steamworks, UTM analytics: partner.steamgames.com/doc/marketing/utm_analytics
- YouTube Help: three-minute Shorts (15424877), Shorts view counting (10059070), all-format view counting from 2026-08-24 (2991785), related video (14075157), thumbnails (72431), chapters (9884579), end screens (6388789), A/B test (16391400), altered or synthetic content (14328491), made for kids (9528076), translations (6289575), caption formats (2734698), retention key moments (9314415), descriptions (12948449), hashtags (6390658), tags (146402), CTR (7628154): support.google.com/youtube/answer/<id>
- YouTube Blog, custom Shorts thumbnails, 2026-07-24; Made on YouTube 2025-09-16; auto-dubbing 2024-12-10: blog.youtube
- X API, media subtitles: docs.x.com/x-api/media/media-subtitles-create · large video upload sample: github.com/xdevplatform/large-video-upload-python
- Instagram for Creators, originality and watermarks, 2024-04-30 and 2025-02-26: creators.instagram.com/blog
- TikTok for Business, Creative Codes: tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads
- Godot docs, creating movies: docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html
- ffmpeg filters (loudnorm, ebur128, ass): ffmpeg.org/ffmpeg-filters.html
- Remotion pricing and terms v5.0, 2026-10-26: remotion.dev/docs/license/pricing, remotion.dev/docs/terms
- Homebrew formulae ffmpeg-full (libass), whisper.cpp: formulae.brew.sh
- ElevenLabs music terms, updated 2026-10-09: elevenlabs.io/music-terms · Suno terms, effective 2026-09-03: suno.com/terms-of-service
- ElevenLabs API, create speech with timing: elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps (per-character start and end times)

## Trailers and editing (PRAC unless marked)

- Derek Lieu blog: first shot (2022-08-01), hook timing (2022-10-24), social optimisation (2023-02-12), trailer length (2018-12-20), simplest Steam trailer (2021-04-18), announce trailer (2021-02-28), sound editing (2020-11-24), dialogue to music (2022-03-14), editing workflow (2022-10-24): derek-lieu.com/blog
- Derek Lieu, GDC: Capturing Great Footage (2018), Make the Trailer Before the Game (2024); Lieu & Trebella, More Feelings, Fewer Features (2019)
- Derek Lieu, Sheepherds re-cut (first herding shot 8 s → 2 s, 25k → 100k views), 2026-08-27: youtube.com/watch?v=jwB1jO7X9O4
- Kert Gartner, Making entertaining game trailers: kertgartner.com
- Playstack on Balatro's marketing (gameplay trailer not enough; VO plus ~300 small streamers): gamedeveloper.com, 2025
- Walter Murch, *In the Blink of an Eye* (Rule of Six), 1995/2001
- SURV: Brill 2023, startle events in 50 horror trailers (median 3); Schubert 2025, suspense in 30 horror trailers
- SURV: Dost & Huang 2026, transition frequency vs engagement (N=242), Marketing Trends Congress

## Briefing an agent editor (read 2026-10-28)

- Peter Yang with Jake Moran (HeyGen, HyperFrames launch videos), "Video editing 101" interview, 2026-10-25: youtube.com/watch?v=MC1g2fHYC88. PRAC, and VEND where he describes HyperFrames Studio. Claims used: name moves in editor's words with numbers (pauses ≈ 0.25 s for short-form, music at 10% of the voice); everything in one brief; storyboard stills before the build (12 stills, 4 acts, ~38 s); "my brand" alone gets invented colours; energy words; let the A-roll work; rebuild a liked effect from a reference clip and keep a library; batch review notes; split long videos into segments; blur private details. 20:30 raw → 18:11 cut, 390 silences trimmed.
- Video editing 101 companion page: video-editing-101.vercel.app. PRAC. Term list: punch-in +15%, push-in +20% over 1.5 s, crash zoom in a few frames, slow creep over 5 s, ease-in-out as default, pauses over 0.5 s cut, one whoosh per whip pan, −14 LUFS.
- Josh's newsletter summary of the interview, 2026-10-28: maily.so/josh/posts/knrjk2l0zld (secondary).
- HyperFrames media-use docs (audio, operations; shipped inside the npm package): Parakeet 6.05% vs whisper.cpp 7.44% WER.

Not taken: AI avatars and AI-made B-roll (break the Material rule), HeyGen cloud features.

## Short-form and wishlists

- Zukowski, 2026 tips for viral tweets (IndieGameJoe, 8 games, median ~7 wishlists / 1,000 views; horror travels best), 2026-05-07: howtomarketagame.com. SURV (small)
- Zukowski, TikTok tips 2022-02-07 and viral TikTok cases 2022-02-14; Steam user observation 2019-09-06 (gamedeveloper.com); FAQ with wishlist-source survey 2023-03-14; Jonas Tyroller case 2024-10-07; Merchant 64 2025-07-08. PRAC/SURV
- GameDiscoverCo: CloverPit 100k wishlists in a week (2025-04-29) and 750k sales (2025-10-14); Backpack Battles 650k (2024-04-24). PRAC
- Future Friends (Abi Le Guilcher), How to TikTok for Indie Games, IMPACT! 2025. PRAC
- Studio Ortica, Loan Shark TikTok postmortem, 2025-10-15; PC Gamer, Quarantine Zone on TikTok, 2025-07-26. PRAC
- r/IndieDev, Dead Spin $5k TikTok campaign under 500 wishlists, 2026-08-04. PRAC
- AUTOMATON, 15-second trailer and 1-minute dev-process trends on Japanese X, 2025-02-05 and 2025-02-20. PRAC
- Safe-zone measurements: ShortFormVideo.co (2026-07), KeyframeKit (2025-03), Xyla, ToolkitsLab. VEND, disagree

## YouTube packaging

- Paddy Galloway, Creator Science #152 (2023-06-13) and 3.3B-view Shorts study (2023-04). PRAC
- Retube, title truncation measured per surface, 2026-10-21. VEND (measured)
- Sebastian Lague on his devlog process, 2023. PRAC

## Tools and repos (state in October 2026)

- whisper.cpp (MIT, active), WhisperX (BSD-2), mlx-whisper repetition-loop report (curtis.engineer), Apple Silicon ASR benchmark (pareido.jp, 2025-10-19)
- Remotion (source-available), Motion Canvas, Revideo, editly (last push 2025-05-12), MoviePy, auto-editor (Unlicense)
- MCP repos: burningion/video-editing-mcp, samuelgursky/davinci-resolve-mcp, legionsound/open-fusion-mcp, elevenlabs/elevenlabs-mcp (archived), kajisho5/ffmpeg-skill, kyanitelabs/kinocut
- DaVinci Resolve 21.1 Studio-only scripting and built-in MCP: nordlys.io, 2026-10-13. PRAC, not confirmed by Blackmagic

## Not verified yet

YouTube's official loudness page (−14 LUFS is practitioner consensus) · YouTube Audio Library licence · Udio terms · X video alt text · whether a digit hashtag `#N` in a YouTube title becomes a link · Reddit native video thumbnail choice.
