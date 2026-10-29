# Sources

Read in late October 2026. Official pages were read in full from elevenlabs.io/docs. Reddit, Medium and sagaftra.org blocked direct fetches, so those lines rest on search-index excerpts (marked *index*). Vendor blogs and tool vendors (Layer, Fuser, Velven, aiproductivity) count as one-sided; a practice in the skill needs two independent backers, the official docs, or a repeatable measurement.

## Official ElevenLabs

1. Sound effects overview and prompting guide: https://elevenlabs.io/docs/overview/capabilities/sound-effects
2. Sound effects in the web app, FAQ (four takes per press, 450-character prompt, cost not tied to text, combine separate effects): https://elevenlabs.io/docs/eleven-creative/playground/sound-effects
3. Create sound effect API (`duration_seconds` 0.5–30, `prompt_influence` default 0.3, formats, `eleven_text_to_sound_v3` listed): https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
4. ElevenLabs agent skills repo, `sound-effects`, `text-to-speech`, `voice-changer` SKILL.md (last commit 2026-10-23): https://github.com/elevenlabs/skills
5. Voice Library Addendum, last updated 2026-03-06 (notice period, withdrawn voices): https://elevenlabs.io/vla
6. Eleven v4 overview (settings, accent handling, Voice Design less performative): https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4 · changelog 2026-09-28: https://elevenlabs.io/docs/changelog/2026/9/28
7. TTS best practices, "Prompting Eleven v4" (tags, punctuation, IPA): https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
8. Voice Design guide (prompt format, pitfalls, quality words, preview text, guidance scale, FAQ): https://elevenlabs.io/docs/eleven-creative/voices/voice-design
9. Design a voice API and quickstart: https://elevenlabs.io/docs/api-reference/text-to-voice/design · https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/voice-design
10. Create speech API (voice settings, `seed`, `previous_text`, request IDs): https://elevenlabs.io/docs/api-reference/text-to-speech/convert
11. Voice changer overview: https://elevenlabs.io/docs/overview/capabilities/voice-changer
12. How do audio tags work with Eleven v3 and v4: https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4
13. Text to Speech in the web app, voice settings (stability 50 start, style 0): https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech
14. Text to Dialogue overview and FAQ (ownership, free regenerations fix about half of issues, 2,000-character requests): https://elevenlabs.io/docs/overview/capabilities/text-to-dialogue
15. Terms of Service (non-EEA), last updated 2026-10-09: https://elevenlabs.io/terms-of-use
17. ElevenCreative Terms, Exhibit 4 Sound Effects, last updated 2026-10-09: https://elevenlabs.io/creative-terms
18. Is my data used to improve ElevenLabs' models (Data use toggle): https://elevenlabs.io/docs/help-center/legal/is-my-data-used-to-improve-eleven-labs-ai-models
19. Changelog 2026-10-19 (SFX `wav_*` formats, `enable_logging` Enterprise only): https://elevenlabs.io/docs/changelog/2026/10/19
21. Billing (monthly reset, two-month rollover): https://elevenlabs.io/docs/overview/administration/billing
22. Rechecked 2026-10-29: API reference still lists `eleven_text_to_sound_v3` with no description; changelog 2026-10-19 and 2026-10-26 have no v3 entry; official `sound-effects` skill still defaults to v2 and says `loop` is v2 only: https://elevenlabs.io/docs/changelog · https://raw.githubusercontent.com/elevenlabs/skills/main/sound-effects/SKILL.md
23. Showcase prompts, read 2026-10-29: video game (quest chime, level-up stinger, hitmarker) and riser pages, marketing, no settings: https://elevenlabs.io/sound-effects/video-game · https://elevenlabs.io/sound-effects/riser

## Practitioners: sound effects

- S1 AudioCipher, Ezra Sandzer-Bell, "ElevenLabs AI sound effect generator", 2024-06-03: https://www.audiocipher.com/post/elevenlabs-ai-sound-effect-generator (word sensitivity, thin output, dead air, library sounds hold up better)
- S2 Easton blog, AI game SFX prompts, 2026-05-21: https://eastondev.com/blog/en/posts/dev/20260521-ai-game-sfx-prompts/
- S3 Fuser, ElevenLabs sound effects guide, 2026-09-29: https://fuser.studio/articles/elevenlabs-sound-effects-guide (tests: auto duration 6 s door, sequence dropped a footstep, peak −21 dBFS) *tool vendor*
- S4 DevelopersIO (Classmethod), sound effects web UI trial, 2026-05-10: https://dev.classmethod.jp/articles/elevenlabs-sound-effects-web-ui-trial/
- S5 Layer Help, "Prompt ElevenLabs for sound effects", undated: https://help.layer.ai/articles/2194365955-prompt-elevenlabs-for-sound-effects *tool vendor*
- S6 Sonetho, ElevenLabs SFX tips, 2026-10-08: https://sonetho.com/en/post/75
- S7 Reddit r/ElevenLabs, "Sound effect generator cannot stop producing…", 2025-08-01: https://www.reddit.com/r/ElevenLabs/comments/1mf9o6g/sound_effect_generator_cannot_stop_producing/ *index*
- S8 PromoAmbitions, YouTube SFX tutorial, Nov 2024: https://www.youtube.com/watch?v=Eyp5c4CHWgI (partial transcript)
- S9 Interactive Audio SIG wiki, "Sound Use Cases", 2026-03-09: https://aiwg.miraheze.org/wiki/Sound_Use_Cases
- S10 Reddit r/aigamedev, AI for generating sound effects, 2026-09-26: https://www.reddit.com/r/aigamedev/comments/1wqv9bp/does_anyone_know_a_really_good_ai_for_generating/ *index*
- S11 Velven, AI sound effects for games, 2026-09-09: https://velven.ai/blog/ai-sound-effects-for-games *tool vendor*
- S12 aiproductivity.ai, ElevenLabs sound effects guide, 2026-04-11: https://aiproductivity.ai/guides/elevenlabs-sound-effects-guide/
- S13 Quantslant, prompt influence test (5 pairs, CLAP score), 2026-09-30: https://quantslant.com/elevenlabs-sound-effects-prompt-influence-test/
- S14 intrect.io, AI sound effect artifacts, 2026-10-20: https://intrect.io/blog/ai-sound-effects-artifacts/
- S15 StraySpark, AI sound design pipeline for indie games, 2026-03-24: https://www.strayspark.studio/blog/ai-sound-design-indie-games-pipeline
- S16 Reddit r/ElevenLabs, "Sound effects are always high pitched", 2026-08-02: https://www.reddit.com/r/ElevenLabs/comments/1vddje1/sound_effects_are_always_high_pitched/ *index*
- S17 gamedevaitools, ElevenLabs vs Stable Audio, read 2026-10-29: https://gamedevaitools.com/compare/elevenlabs-vs-stable-audio/ *aggregator, repeats S15*
- S18 Interactive Audio SIG wiki, "Game Development", 2026-05-06 (energy weapon prompt: very compressed, transient cut off at the start): https://aiwg.miraheze.org/wiki/Game_Development
- S19 JJ Lyon, "Funky game sounds", Krotos, 2026-10-09 (three layers: transient, pitched tone, texture; chain EQ, transient shaper or compressor, pitch, reverb): https://krotos.studio/blog/funky-game-sounds *tool vendor, not ElevenLabs-specific*
- S20 Kuba Rogut, "Game sound effects", SFX Engine, 2026-02-18 (low thump, mid body, high sizzle): https://sfxengine.com/blog/game-sound-effects *tool vendor*

Searched 2026-10-29 without a usable hit: a verbatim ElevenLabs prompt for a UI reward, power-up or level-up sound from a shipped game; any A/B of prompt influence for SFX; YouTube transcripts on ElevenLabs game SFX.

Searched without a usable hit: GDC Vault 2024–2026 talks on ElevenLabs SFX (the 2026 AI Audio Roundtable was unrecorded), Game Developer, 80.lv and A Sound Effect articles specific to ElevenLabs SFX, and any shipped commercial game documenting ElevenLabs SFX in its pipeline.

## Practitioners and news: voices

- V1 Game Developer, Danielle Riendeau, "Valve tweaks and clarifies AI disclosure rules for Steam", 2026-01-16: https://www.gamedeveloper.com/business/valve-tweaks-and-clarifies-ai-disclosure-rules-for-steam
- V2 PC Gamer, Andy Chalk, "'Unauthorized' AI-generated voices in Tomb Raider 4-6 Remastered have been removed", 2025-09-24: https://www.pcgamer.com/games/action/unauthorized-ai-generated-voices-in-tomb-raider-4-6-remastered-have-been-removed/
- V3 Engadget, Jackson Chen, "Arc Raiders replaced some of its AI-generated voice lines…", 2026-03-15: https://www.engadget.com/gaming/arc-raiders-replaced-some-of-its-ai-generated-voice-lines-with-professional-actors-184915627.html
- V4 Reddit r/ElevenLabs, u/Pronwan, "Fully voiced my indie game using ElevenLabs… 850+ players… 0 complaints", 2026-02-03: https://www.reddit.com/r/ElevenLabs/comments/1qv6qlh/fully_voiced_my_indie_game_using_elevenlabs_the/ *index, self-reported*
- V5 SAG-AFTRA, 2025 Interactive Media (Video Game) Agreement FAQ, ratified 2025-07: https://www.sagaftra.org/contracts-industry-resources/interactive/2025-interactive-media-video-game-agreement *index (403 on fetch)*
- V6 aiproductivity.ai, George Mustoe, "ElevenLabs Voice Design v3: Creating Custom AI Characters", 2026-04-03: https://aiproductivity.ai/guides/elevenlabs-voice-design-v3-guide/
- V7 ElevenLabs YouTube, "Create Custom AI Voices with ElevenLabs (Full Prompt Guide)", 2025-10-27: https://www.youtube.com/watch?v=WbNvWy4FHhg *vendor; transcript not read*
- V8 Case Analyst dev blog, Luca Panteghini, "The AI asset pipeline of a solo indie game", 2026-06-26: https://case-analyst.com/blog/07-ai-assets.html (shipped game; fixed voice IDs; short interjections pad and trim)
- V9 Anirudh Vasudevan, "How Apartment 4B Bakes an Entire Horror Game Into Static Files" and "How I Gave Four AI Characters Their Own ElevenLabs Voices", 2026-10-17: https://anirudhvasudevan.com/blog/apartment-4b-horror-game/ · https://anirudhvasudevan.com/blog/voices-of-the-last-world/
- V10 Reddit r/ElevenLabs, "How to keep the voice consistent for long scripts with v3", 2026-09-12: https://www.reddit.com/r/ElevenLabs/comments/1wdyor3/how_to_keep_the_voice_consistent_for_long_scripts/ *index*
- V11 GDC Vault, DB Cooper, "Take that! Finding, Trapping and Taming Exertion Sounds: A Vocal Work-out", date unknown: https://gdcvault.com/play/1012534/Take-that-Finding-Trapping-and *index (Vault in maintenance)*
- V12 Reddit r/ElevenLabs, u/Tomas_Fark, "Any tips on creating realistic screams with speech-to-speech?", 2025-07-30: https://www.reddit.com/r/ElevenLabs/comments/1md5s9h/any_tips_on_creating_realistic_screams_with/ *index*
- V14 Reddit r/ElevenLabs, u/KingDevyn, voice from Link's grunts and screams, 2023-03-01: https://www.reddit.com/r/ElevenLabs/comments/11evau7/i_used_links_from_zelda_grunts_screams_and_other/ *index*
- V15 Reddit r/ElevenLabs, "List of V3 audio tags" (staff reply u/J-ElevenLabs: one or two words), 2025-06-11: https://www.reddit.com/r/ElevenLabs/comments/1l8k45e/list_of_v3_audio_tags/ · "V3 reads tags instead of inflecting with them?", 2025-07-28: https://www.reddit.com/r/ElevenLabs/comments/1mb2occ/v3_reads_tags_instead_of_inflecting_with_them/ *index*
- V16 Reddit r/ElevenLabs, u/diggum, "v3 tags recently stopped working well", 2026-06-05: https://www.reddit.com/r/ElevenLabs/comments/1txpe3h/v3_tags_recently_stopped_working_well/ *index*
- V17 texttospeech.com, "ElevenLabs Eleven v3 review", 2026-09-03: https://texttospeech.com/blog/eleven-v3-review
- V19 Oğuzhan Koçaklı, "My Experience with ElevenLabs V3, What Actually Works", Medium, 2025-06-05: https://oguzhankocakli.medium.com/t-4my-experience-with-elevenlabs-v3-what-actually-works-421e7308ddb1 *index (403 on fetch)*
