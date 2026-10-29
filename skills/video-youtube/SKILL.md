---
name: video-youtube
description: Packages and publishes game videos on YouTube. Covers what the algorithm actually reads (and the myths to drop), titles, descriptions, hashtags and tags, Shorts cover frames and long-form thumbnails, chapters, Related video, translated metadata, the AI-disclosure and made-for-kids answers, a field-by-field Studio upload recipe, multilingual keywords, and which numbers to read when. Use with video-craft before writing YouTube metadata, uploading in Studio, or reading YouTube analytics for a game channel.
license: MIT
---

# YouTube

Load `video-craft` first, and `video-short` or `video-longform` for the video itself. This skill decides what goes into each field. 🔴 Nothing is uploaded or made public until the human has approved the finished candidate (file, title, description, thumbnail).

## What YouTube actually reads [OFF]

- **Shorts feed**: shown → stayed or swiped → % watched → satisfaction. The title is a small overlay; the first second is the thumbnail. Metadata barely matters there.
- **Search**: the words in the title and the first lines of the description, plus the video's content (YouTube transcribes speech).
- **Home and Up next**: viewer history and satisfaction. The title and thumbnail decide the click. High CTR with low view duration reads as clickbait and gets shown less.
- Myths to drop: tags as SEO (they only help with misspellings), `#Shorts` in the title (any vertical or square upload ≤ 3 min is a Short), "uploaded captions boost ranking" (unproven; upload them for muted viewers and translation), "1280×720, 2 MB thumbnails" (outdated ceiling).

## Title

- Clear before clever: plain words a non-native English reader understands. Front-load the hook or the main search word.
- What shows: about 40 Latin or 20 CJK characters on a Short's overlay, about 70-80 on a phone's Home feed, the full title in desktop search.
- No series tag on YouTube: the whole visible title goes to the hook; the game name sits in the description's first line.
- Shorts: `<one concrete moment>` with a genre word if it fits. Long-form: `<conflict or outcome>`, with "devlog" in it, since people search for devlogs. Trailers: game name and trailer kind lead, genre words after (`<Game>: Gameplay Trailer | Deckbuilding Auto Battler`).
- Never repeat the thumbnail's words in the title; the two split the work.

## Description

- Line 1: what happens in the video, in plain words, with the main keyword.
- Line 2 (long-form): one ask and a link with UTM once the Steam page exists (`video-craft` [channels.md](../video-craft/references/channels.md) "Steam UTM scheme"). Before the page exists there is no link; don't invent one.
- Then one or two sentences on the game, chapters for long-form (`00:00` first, ≥ 3, each ≥ 10 s), and 2-3 hashtags at the end (e.g. `#indiegame #deckbuilder #cosmichorror`, or the equivalents for that audience). More than 60 hashtags voids all of them.
- Links in Shorts descriptions and comments aren't clickable. A Short's bridge is the **Related video** field (needs advanced features) and the channel's profile links.

## Thumbnail and cover frame

- Shorts: custom thumbnails are for Partner Program channels only (since 2026-07-24). Build a clean cover frame into the cut (`video-craft` [tools.md](../video-craft/references/tools.md) "Thumbnails and cover frames") and pick it in Studio; keep the subject inside the centre 4:5, which is how Home and Subscriptions crop it.
- Long-form: 3840×2160 PNG (≥ 1280×720), one situation about to happen, a large character or monster face as the focal point, 0-3 words, a bright subject with a rim light against a dark background, the same layout zone and type every episode.
- Test & Compare (up to 3 titles or thumbnails, desktop, long-form only) picks by watch-time share. Use it once eligible, with really different ideas; expect "inconclusive" while views are low.

## Languages

One channel can serve several languages. Set the video language and the title/description language, then add the others as translated **title & description** (Studio → Subtitles → Add language). Translated metadata shows in search for those languages. Run each translation through a humanizer for its language (e.g. https://github.com/gonta223/humanizer-ja for Japanese, https://github.com/IsaacEryn/humanizer-ko for Korean). Set auto-dubbing, if offered, to review before publishing.

## Studio recipe

1. Upload, on the game's own channel, the file that passed `check.py --channel short` or `--channel youtube`.
2. Title and description exactly as the human approved them.
3. Thumbnail: the cover frame (Short) or the custom thumbnail (long-form).
4. Playlist: the series playlist (devlogs) or the Shorts playlist.
5. Audience: **No, it's not made for kids** (unless it is). No age restriction unless the content needs it.
6. Show more → Paid promotion No · **AI use (altered or synthetic): No** for gameplay footage; **Yes** when the video has AI narration, a realistic synthetic person or event, or a main focus on AI-generated music · Tags: the game's name and its common misspellings, nothing else · Language set · Category **Gaming** · Comments on, held for review · Shorts remixing allowed · Embedding on.
7. Long-form: upload the SRT; end screen in the last 5-20 s (best next video + subscribe); 1-2 cards (playlist, a related devlog). Short: **Related video** = the matching devlog or trailer once one exists.
8. The copyright check must be clean. Visibility Public, at the slot the human chose.
9. After publishing: add the translated titles and descriptions; pin a comment (on a Short it points to the Related video in words).

## Keywords

Check phrasing in YouTube search autocomplete signed out, per region, and in Steam tag names per language. Seed terms for English and Japanese; build the same table for any other language you target:

| Concept | EN | JA |
| --- | --- | --- |
| Deckbuilder | deckbuilder, roguelike deckbuilder | ローグライクデッキ構築, デッキ構築 |
| Auto battler | auto battler, auto chess | オートバトル, オートバトラー |
| Horror | cosmic horror, lovecraftian, eldritch | コズミックホラー, クトゥルフ |
| Dev | indie game devlog, solo dev | 個人開発, インディーゲーム, ゲーム開発 |

Name comparable games only where the comparison is honest.

## Numbers

| Format | Read | When |
| --- | --- | --- |
| Short | stayed to watch, average % viewed, engaged views | 7 d |
| Long-form | Intro (% at 0:30), CTR by traffic source, average view duration, dips and spikes | 48 h and 7 d, ≥ 100 views |

Views changed definition on 2025-03-31 (Shorts) and 2026-08-24 (all formats); don't compare raw views across those dates. CTR for half of all channels sits at 2-10%; there is no official Shorts benchmark, so build your own median. Judge a Shorts format after 10-20 uploads and long-form after 5-10. Never delete and re-upload a weak video; make a better one.
