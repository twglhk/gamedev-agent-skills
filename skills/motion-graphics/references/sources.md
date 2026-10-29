# Motion graphics: research behind the skill (October 2026)

Grades: **A** primary source read (docs, licence, repo) · **B** read in part or through a reliable summary · **C** title, description or chapter list only (the video itself was not watched).

## Tools

| Tool | Facts | Grade | Source |
| --- | --- | --- | --- |
| HyperFrames (HeyGen) | HTML/CSS/GSAP/WAAPI/Lottie seeked frame by frame in headless Chrome, encoded by FFmpeg; "same input, same frames". Apache-2.0, no per-render fees. Agent install `npx hyperframes skills update` or `claude plugin install hyperframes@hyperframes`; core skills `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry` (about 450 blocks: transitions, titles, kinetic type, captions, charts). Transparent output: `--format webm` or `--format mov` (ProRes 4444); check alpha with `ffmpeg -c:v libvpx-vp9 -i x.webm` | A | github.com/heygen-com/hyperframes (README, docs/guides/rendering.mdx, docs/guides/motion-graphics.mdx, docs/prompting/motion.mdx) |
| HyperFrames motion guide | Elements land and hold; overlap, don't queue; one idea per move; overshoot only for physical objects, never text or numbers; move the camera only to get somewhere; no fade-out-then-fade-in; transitions caused by something on screen, 3-5 kinds per film. Ease words: smooth power2.out · snappy power4.out · bouncy back.out · dramatic expo.out. Timing: 0.2 s energy · 0.4 s professional · 0.6 s luxury. Motion graphics live under 10 s, up to about 30 | A | docs/prompting/motion.mdx, docs/guides/motion-graphics.mdx |
| Remotion | React components rendered frame by frame. Free for individuals and companies of up to 3 employees, company licence above; 5.0 licence draft (PR 3750) counts contractors. Official agent skills `remotion-dev/skills` (no licence file). Alpha via ProRes 4444 or VP8/VP9 WebM | A | github.com/remotion-dev/remotion LICENSE.md, PR 3750, remotion.dev/docs/transparent-videos |
| GSAP | Free for commercial use including former Club plugins (SplitText, MorphSVG) since 2025-04-30; only no-code builders competing with Webflow are excluded | B | gsap.com/standard-license |
| After Effects MCP | Dakkshin/after-effects-mcp and others drive AE through ExtendScript; needs a paid AE running in a GUI | B | github.com/Dakkshin/after-effects-mcp |
| Motion Canvas / Revideo | MIT; Motion Canvas last release v3.17.2 (2024-12); no agent skills found | B | GitHub repos |
| lottie-web / Rive MCP | lottie-web MIT, quiet since 2025-09; Rive MCPs are small community projects | B | GitHub repos |
| `scripts/render.py` | Same principle as HyperFrames with only Playwright + Chrome: `document.getAnimations()` paused and `currentTime` set per frame | A | this skill |

## Craft and platform

| Source | Takeaway | Grade |
| --- | --- | --- |
| Steamworks "Trailers" (partner.steamgames.com/doc/store/trailer) | Viewers may give under 10 s and watch muted: the video must read with no sound; first trailer = gameplay | A |
| Apple HIG "Motion" (developer.apple.com/design/human-interface-guidelines/motion) | Motion with a purpose only; brief and precise feedback; never the only carrier of information | A |
| easings.net | Curve families; back/elastic are the overshoot families, bounce reads as a cliché on titles | A |
| Derek Lieu, "How to Make a Game Trailer With Great Title Cards" (youtu.be/zzYDjjRww2Y) | Try the cut without cards first; cards must be specific to this game; don't list or count features | C |
| Derek Lieu, "How to Edit a Game Trailer That Keeps Viewers Hooked" (youtu.be/jwB1jO7X9O4) | Common mistake: too many title cards too soon; slower edits that let the game show perform better | C |
| Joshua Craigie, "10 Motion Design Principles Every Animator Needs" (youtu.be/Cz-GcIITNrs) | Timing and spacing, easing, mass and weight, anticipation, arcs, follow-through, overlap, secondary motion | C |
| Tudor Baba, "The FASTEST Freeze Frame Character Intro Effect" (youtu.be/mp7eu7AlxxM); Enam Alamin, Snatch-style freeze (youtu.be/j_UOvUeZEjI) | The freeze intro recipe: freeze cut, subject mask with a border, ink or colour field behind, text, flash transition out | C |

## Agents making motion graphics (YouTube, 2025-2026)

All grade C unless marked: title, description and chapters read, videos not watched.

| Video | Lesson in its description |
| --- | --- |
| Matt Loui, "Claude Opus 5.5 Animated Every Motion Graphic in This Video" (youtu.be/Ll45R_Z8tQc) | Prompt from real recordings, screenshots or a reference clip, not from words alone; finish with a sound pass (whooshes, pops) |
| Sanji Nai-Chien, "I Turned Claude Into a $880/Day Motion Graphics Skill" (youtu.be/D5qpBbEWTxo) | Scene-by-scene storyboard, brand fonts and colours, vector UI; the first render was broken and one-sentence fixes per bug repaired it; "a storyboard makes or breaks AI motion graphics" |
| Jad M.H, "How to Make Viral Motion Graphics With AI With 0$" (youtu.be/zke3bTtvmLo) | A one-line prompt gives the same look everyone else gets; sound design and a story lifted the later versions |
| Jack Roberts, "Claude Video 2.0 Just Changed Everything" (youtu.be/KphrV76DJoI) | Pick a style, find real references, write the brief, check the finished frames |
| MoSidd, "I Made Vox-Style Motion Graphics Using Only Claude Code & Remotion" (youtu.be/7wuYBfE131U) | Plan script and visual style before building scenes; cuts land on the word |
| Zinho Automates, "Create Motion Graphics with Claude Code + Remotion" (youtu.be/MAhkbZHcbLA) | Setup, pro tips and mistakes to avoid (chapters) |
| Moe Lueker, "I Built a Claude Skill That Makes Videos (HyperFrames + HeyGen)" (youtu.be/UGYfVzV8jHc, sponsored by HeyGen) | HyperFrames as the free agent renderer; two custom skills on top made the difference |
| Aidan Stanik, "Claude Code + After Effects MCP" (youtu.be/YTOwQj-n7ME); Luke Byrne (youtu.be/iRGsj8H6DSs) | AE MCP builds editable comps and expressions; still needs AE open and a human finishing pass |
| Futurepedia, "Claude Makes a New Kind of Video" (youtu.be/Ge1B-Ok1Pfk) | A style atlas of reusable prompt looks; time animations to a voice-over |
| Peter Yang with Jake Moran (HeyGen), "Video editing 101" (youtube.com/watch?v=MC1g2fHYC88, 2026-10-25; full transcript read, grade B) | Storyboard stills before the build; rebuild a liked hook from a 5 s reference clip, prompting only what to change (type, colour, icon); about ten moves in one hook; keep reverse-engineered moves as a reusable library |

## Open

- Transcripts of the videos above and fighting-game intro references (Street Fighter 6, Guilty Gear Strive, Overwatch) were not read.
- HyperFrames registry blocks and GSAP timelines were tested on one card only.
