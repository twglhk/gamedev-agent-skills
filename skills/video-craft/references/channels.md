# Channels: specs, safe zones, metadata, metrics

Checked October 2026. Platform limits change; the upload screen wins. Grades: [OFF] platform · [PRAC] practitioner · [OPIN] measured by a tool vendor or convention.

## Upload specs

| | X | Reddit (native) | YouTube Shorts | YouTube long-form | Steam trailer | TikTok / Reels |
| --- | --- | --- | --- | --- | --- | --- |
| Master | 16:9 1920×1080 or 4:5 1080×1350 | 4:5 1080×1350 (16:9 for desktop subs) | 9:16 1080×1920 | 16:9 1920×1080 | 16:9 1920×1080 | 9:16 1080×1920 |
| Length to cut | 15-45 s | 15-45 s | 15-30 s (max 3 min) | 8-12 min | 30 s / 75-90 s | 9-15 s |
| Hard limit | 140 s, 512 MB, max 1920×1200 [OFF API] | 15 min, 1 GB [PRAC] | ≤ 3 min = Short, upload max 1080p [OFF] | 12 h | 30/60 fps, ≥ 5,000 kbps, H.264+AAC, stereo [OFF] | 10 min in app |
| Sound | autoplays muted | autoplays muted | sound on | sound on | autoplays muted on the store page | sound on |
| Captions | burn in (SRT track also possible) | burn in | burn in | SRT upload + translations | burn in (no subtitle tracks) | burn in |
| Clickable link | in the post | in the post | Related video only | description, end screen | n/a | bio |

- One master per moment, cut per channel. Don't post the same file everywhere: X and Reddit get 16:9 or 4:5 with their own copy, Shorts gets 9:16. Never upload a file carrying another platform's watermark.
- A 9:16 file in Reddit's mobile feed is cropped to about 4:5: keep the key content inside y 285-1635.

## Safe zones on 1080×1920

No platform publishes official organic numbers, and measured ones disagree by up to 400 px at the bottom [OPIN, five tools]. A safe house box for Shorts, TikTok and Reels: **text, logos and key action inside x 90-900, y 250-1380** (`captions.py` `frame: short`). Nothing important below y 1380 or right of x 900, where the title, handle and action buttons sit. Paid placements need the bottom 680 px clear.

## Metadata per channel

| | X | Reddit | YouTube Short | YouTube long-form | Steam |
| --- | --- | --- | --- | --- | --- |
| Title | first line of the post | the post title: plain, specific, says you made it | ~40 Latin / ~20 CJK characters visible | ~70-80 visible on a phone | trailer name: `Gameplay Trailer` etc. |
| Hashtags | JA audiences use them (`#ゲーム制作 #インディーゲーム`); EN mostly none | none | 2-3 at the end of the description | 2-3 | n/a |
| Disclosure | none | r/IndieGaming requires declaring any GenAI in the game or its promotion | Studio "AI use": No for gameplay | same | Steam content survey |
| Thumbnail | first frame | first frame | a cover frame you pick (custom only in the Partner Program) | custom 3840×2160 | a frame of the video, no text |

Reddit threads rank well on Google, so genre words belong in the Reddit title or the first comment, as long as the sub's rules allow. Some subs read any recurring series tag as an ad; check flair and title rules.

## What to read, and when

| Channel | Read first | Then | When |
| --- | --- | --- | --- |
| X | video views, % watched | likes (r = 0.86 with wishlists in one 8-game sample), profile visits | 24 h and 7 d |
| Reddit | upvotes in the first 2 h, comment quality | outbound clicks | 24 h and 7 d |
| YouTube Shorts | **stayed to watch** (viewed vs swiped away) | average % viewed, engaged views, retention curve | 7 d (Shorts seed slowly) |
| YouTube long-form | **Intro** (% still watching at 0:30), CTR by traffic source | average view duration, dips and spikes | 7 d, ≥ 100 views |
| Steam (once the page exists) | UTM visits → wishlists within 72 h | traffic sources | final after 4 days |

- Views aren't comparable over time: YouTube changed Shorts view counting on 2025-03-31 and all formats on 2026-08-24. Compare Shorts on engaged views.
- Reading a retention curve: an early cliff means the hook failed; a slow slide is pacing; a drop at the end is a dead tail, so cut it; a bump is a rewatched moment, so make more of it.
- Judge a single clip against your own running median, never on views alone. Judge a format after 8-10 posts and a channel after 30 posts or 10 weeks. Change one thing at a time. Starting targets until you have a median [OPIN]: Shorts stayed-to-watch ≥ 70%, average % viewed ≥ 80% for clips ≤ 15 s.
- Don't delete and re-upload a weak video; YouTube may read it as spam. Make a better version.
- Log the numbers in your marketing log with the post's date and slug.

## Steam UTM scheme (once the page exists)

`store.steampowered.com/app/<ID>/?utm_source={youtube|x|reddit}&utm_medium={shorts|devlog|trailer|post}&utm_campaign=<game>_<NNN>&utm_content={desc|channel|pinned|bio}&utm_term={ja|ko|en}`

Conversions count within 72 h of the click. Merge low-volume variants so they clear Steam's privacy threshold. Shorts can't carry a clickable link, so their traffic arrives through the channel's profile link (`utm_content=channel`) or the related long-form video's description.

## Expectations

Short-form views convert to wishlists at anywhere from 0.04 to 21 per 1,000 views. X has the best per-view rate in published cases (median about 7 per 1,000 in one 8-game sample); TikTok and Shorts usually sit at 0.2-2. Deckbuilders are at the low end (one $5k paid TikTok campaign: under 500 wishlists), horror at the high end. Short-form is a booster and a hook-testing lab; the demo, festivals and streamers are the engine. Until the Steam page exists, a clip's job is follows and learning which hooks hold.
