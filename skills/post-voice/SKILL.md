---
name: post-voice
description: Keeps marketing posts sounding like the developer instead of AI, using a voice log in the repo that learns from texts the developer writes himself. Swap a draft for the developer's own wording when he supplies it, translate it faithfully, log what he did differently, and tune a short rule list. Use before drafting, revising or translating any X, Reddit or YouTube text, and whenever a post reads as AI-composed or generic.
license: MIT
---

# Post voice

The developer's own texts are the target. The rules you write down are only what you've learned from them so far, and they keep changing.

Keep a voice log in the repo, for example `marketing/voice.md`, with two sections: **Rules** (what his texts teach) and **His texts** (the evidence). Read both before drafting, and paste the rules plus the newest texts into any sub-agent prompt that writes post copy. Run a humanizer pass for the language afterwards, e.g. https://github.com/blader/humanizer (English), https://github.com/IsaacEryn/humanizer-ko (Korean), https://github.com/gonta223/humanizer-ja (Japanese).

## When his revision note carries his own text

A revision note may be his own words for the post rather than an instruction. Then his text is the post.

1. **Split the note.** Lines meant for posting are his text; lines like "keep the title" are instructions. If you can't tell, ask with both readings.
2. **Same language as his text:** use it word for word. Fix only obvious typos; keep his line breaks, punctuation and emoji.
3. **Another language:** translate it the way he'd say it in that language, with his sentences, his order, his tone. Add nothing, drop nothing, don't polish it into copy. A humanizer pass may change wording only.
4. **Keep what he didn't touch**: title, media, targets.
5. **If it breaks a limit** (X's 280 weighted characters, a sub's rule), don't cut on your own. Ask him, offering the shortest cut that keeps his meaning.
6. **Learn from it in the same session**: add an entry to His texts, then tune Rules.

A note that only asks for a change ("shorter") is a normal revision: do exactly that, and still record any rule it implies.

## The log

**Rules.** At most 12 bullets, each with the date or case it came from. Rewrite them as new texts arrive: sharpen one, merge two, delete one a newer text contradicts. Where they conflict with the generic advice below, the rules win. Typical things they capture: register and politeness level, punctuation habits, sentence length and how he joins clauses, how he opens and closes, how he asks for help, where the game pitch goes, words and claims he never uses.

**His texts.** Newest first, at most 6. Each entry: date, channel and post, your draft's gist in one line, his text word for word, and what he did differently in 1 to 3 points. Drop the oldest once its lessons sit in Rules; version control keeps the history. A post he wrote entirely on his own, before any draft, is the best entry you can get.

## Why drafts read as AI

- **Same shape every time.** Material, tools, pitch, CTA, one line each, in that order. Readers spot the template before any word.
- **Parallel lists.** "Tool A for the design, tool B for the 3D model, tool C for the motion."
- **Closers.** A short last line that restates instead of adding ("The failures stay in.").
- **Brochure clause.** The logline pasted in as a relative clause.
- **Stock CTA** as its own line ("Follow for more", "I'll keep posting here"). A help ask is different: it's specific to the post and he actually needs the answer.
- **Craft praise and hype** ("hand-crafted", "excited to share"), or excuses for unfinished parts.

Banned-word lists alone don't fix this. A drafting prompt full of "don't write X" primes X. Write from the rules, then audit with the lists.

## How to write

1. **Start from what he'd say.** If he writes more naturally in his first language, draft there in his register first, then put it into plain English or Japanese. Readers accept a non-native developer's translated words; they skip copy that sounds composed.
2. **Write to one reader**: a dev in that sub who has fought the same tool. Write what you'd type to them in a Discord.
3. **Lead with something they can picture**: the neck caving in, the 1 m roll. Specific beats general on every line.
4. **Fold the parts in** (material, how it was made, the help ask, and the game line; see `marketing-playbook`). They can share sentences and change order. The game line, when present, closes the post, in plain words, never the full logline.
5. 🔴 **Always ask for help**, every post, every channel. Ask about something he's really stuck on or weighing, narrow enough to answer in one comment: say what he tried or leans toward, then ask. Offer named options where it helps. Never invent a dilemma; if none is known, ask him. Patterns: "Any tips on …?", "I'm thinking of …, but I'm not sure. How would you do it?", "2D or 3D for the card art?".
6. **Uneven lines.** Mix a short sentence with a longer one. Contractions. Tool names as people type them.

## Length

- Body: about 50 words in English, about 150 characters in Japanese, Korean or Chinese, at most 4 lines. Title at most 12 words. Count before showing the candidate.
- Cut any sentence the clip already shows unless it adds a number or a reason.
- His own text is exempt. If it runs longer, it runs longer.

## Audit after drafting

- **Help-ask test.** Does it ask for help with something real, answerable in one comment, in a way that makes you want to answer?
- **Portability test.** Could the line sit under another game's post unchanged? Make it specific or cut it.
- **Read it aloud as him**, next to his newest logged text. Anything he wouldn't type goes.
- Cut on sight: not-X-but-Y, one-line closers and fragments, colon reveals ("The best part: …"), parallel triads, staged openers ("Here's the thing"), "excited to share", "journey", "dive into", marketing adjectives, -ing riders ("showcasing…"), em dashes, bold, hashtag stuffing.

## Sources

- The developer's own texts, first.
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) and [Julz7727/Stop-Slop-v3](https://github.com/Julz7727/Stop-Slop-v3) (positive routing over banned lists)
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (portability test, minimum effective edit)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), via [blader/humanizer](https://github.com/blader/humanizer)
- r/gamedev thread "Please stop using chatgpt to write your game summary" (2026-06): readers accept translated words, not composed copy.
