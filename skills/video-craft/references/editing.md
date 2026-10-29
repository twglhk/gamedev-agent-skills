# Editing craft: picture, sound, text

Contents: How a cut is judged · Cuts that carry meaning · Rhythm · Horror, then hope · Sound · Text on screen · Phone readability · Telling an agent what to cut · Workflow

Grades: [OFF] platform doc · [SURV] study or dataset · [PRAC] working practitioner · [OPIN] opinion. Sources in [sources.md](sources.md).

## How a cut is judged

Walter Murch's Rule of Six (*In the Blink of an Eye*) [PRAC]. A cut should be true to, in order of weight:

| Criterion | Weight | Question |
| --- | --- | --- |
| Emotion | 51% | Does the viewer feel the intended feeling at this moment? |
| Story | 23% | Does it move the one message forward? |
| Rhythm | 10% | Does it land on the beat of the action or music? |
| Eye trace | 7% | Is the eye where the next shot's subject appears? |
| 2D screen plane | 5% | Left/right consistency of the two sides |
| 3D space | 4% | Spatial continuity |

Give up the bottom ones before the top. A jump in space that keeps the feeling is a good cut.

- **Blink rule**: cut where a viewer would blink, at the end of a thought, after the hit lands, not before it.
- **Do the most with the least**: suggestion beats exposition. Fewer, stronger shots.

## Cuts that carry meaning

- **Cutting on action**: start the motion in one shot and finish it in the next; the movement hides the cut. A unit leaps from its card onto the board.
- **J cut / L cut**: the next shot's sound starts before its picture (J), or the last shot's sound carries over the next (L). A monster's roar before we see it (J) builds dread; a strike's sound over the next shot (L) links two characters. Recipe in [tools.md](tools.md).
- **Match cut**: shape, motion or colour links two shots. A card icon → the same silhouette on the board; night sky → dawn.
- **Kuleshov effect**: meaning comes from the pair of shots. An ordinary face, then the monster = "they know"; the same face, then a burning street = "a hero".
- **Eye trace**: in fast cuts keep the subject at the same screen spot (Mad Max: Fury Road framed every subject centre so 1.8 s shots read). Card centre → effect centre.
- **Setup / payoff**: plant early, pay later. A weak-looking card early carries the final fight.
- **One three-act shot**: even a single take can set the scene, bring the conflict and resolve it. A fight that turns is the best first shot.

## Rhythm

- Cut on events, not a clock. Sources disagree on pace: a vendor's 50-video sample says ~2.2 s per scene; a 2026 experiment (N=242) found more transitions lowered completion; Derek Lieu tells devs to slow down. Rule: hold until the payoff lands. Typical result: 1.5-3 s per shot in a hype cut, 3-6 s for one readable mechanic.
- Vary energy: a stopdown or held beat every 10-20 s in trailers, every 30-60 s in long-form.
- Don't show the same thing more than 3 times; repetition makes the game look small.
- Watch the cut once at 1.5×. Anything you would skip, cut.

## Horror, then hope

For horror or dark-toned games, beat grammar for a 10-15 s moment [SURV + PRAC]:

1. **Normal** (0-2 s): a calm, readable state.
2. **Wrongness** (2-5 s): one detail off; sound drops to a low drone or silence.
3. **Hold** (0.5-1 s): near-stillness lets the eye find the threat.
4. **Sting** (at 60-70% of the moment): one layered transient (low boom + high metallic + reverse swell), a camera push, a 2-4-frame flash or colour drain. The muted twin must sell it alone.
5. **Response** (last 20-30%): the player's side acts. Plain horror ends on the monster; a game about fighting back ends on the fighter.

- A study of 50 horror trailers found a median of 3 startle sounds each; information placed right after a startle is remembered better [SURV Brill 2023]. Cap: 1 sting per short, 3 per 90 s, each after silence.
- Withhold the big monster: silhouette, scale cues, sound, an "it" in text before it is shown. Full reveal only at the climax.
- Small Foley gets loud in silence (cloth, breath, a creak). Misdirect with a small bump, then hit.
- Grade the two sides the same way in every video, e.g. heroes warm and saturated, horror cold and desaturated.

## Sound

- Sound is the transition. Remove the picture from a good trailer and you can still hear the sections [PRAC Lieu].
- **Mark the music first**: markers on every peak (hits, drops) and every trough. Picture events go on peaks; words go in troughs. Title cards land on hits.
- **Stopdown**: music cuts or reverbs out on a downbeat, masked by an SFX, paired with a punctuation shot (cut to black, a hit). A riser says something new is coming.
- Sync to actions more than to every beat; cutting on every beat becomes predictable.
- SFX in the final pass are an extra percussion track: keep the sound that matters (the strike that wins), drop the rest.
- Hits within 1 frame of the picture. Leave about 6 dB of headroom before a sting so the jump is felt; no music under the sting.

## Text on screen

- Only what the picture can't say, in the language of the post, in words real games and films use.
- ≤ 6 words a line, ≤ 2 lines, one line on screen at a time during action. Text and new gameplay never share the same second; put a card on a frozen or black frame.
- Say what a mechanic achieves, not how it works ("It can't die." over a health bar refilling). Feelings over features.
- Size: heavy sans, cap height ≥ 64 px at 1080 wide, dark stroke or a band (looks in `captions.py`).
- No "X meets Y", no lore card at the start, no studio or engine logo before the hook.

## Phone readability

- One focal point per shot. Keep the player side visually distinct from the threat (rim light, warm vs cold).
- About 3 characters and 1 boss in a shot meant to be read; crowd shots only as a peak.
- Main character silhouette ≥ 25% of frame height in a readable shot; a boss can exceed the frame.
- Damage numbers ≥ 70 px tall at 1080 wide, one at a time on key beats; hide minor numbers in capture.
- Hitstop and camera shake read at small size better than particles.
- Nothing important outside the safe box ([channels.md](channels.md)).
- Thumb test: watch once on a phone at arm's length, muted. If you can't say what happened, recut.

## Telling an agent what to cut

"Edit this" or "make it punchy" gets a generic cut. An agent can't hear the mix and doesn't know your look, so every instruction to an editing subagent, and every line of `edit.sh` you plan for yourself, names the move with the editor's word and gives it a number [PRAC Moran; Video editing 101]. Shared words also cost fewer turns, and a turn on video means a render.

| Move | What it is | Default number | Good for |
| --- | --- | --- | --- |
| Push-in | the shot grows slowly | +8% over 1.5 s, ease-in-out (Video editing 101 uses +20% for a talking head) | a reveal, the hook's focal point |
| Punch-in | the shot grows in one frame at a cut | +10-15%, back to 100% at the next cut | hiding a jump where waiting time was trimmed from one take |
| Crash zoom | very fast grow, 3-5 frames | +15-25% | a sting's visual twin |
| Slow creep | slow grow, linear | +3-5% over ≥ 5 s | held dread; a character cutout's hold |
| Pull-back | the shot shrinks to show more | to 100% over 1-2 s | a boss's scale |
| Easing | speed change during a move | ease-in-out on every camera move; linear only for a slow creep | |
| Speed ramp | fast, then slow on the moment | 2-4× → 0.5× on the payoff | long fights, a chain building up |
| Whip pan | fast sideways move, blur hides the change | 6-8 frames with motion blur, one whoosh | a change of place or topic only |
| Match cut, J/L cut | see "Cuts that carry meaning" | J lead 0.3-0.5 s | |
| Cutting to the beat | each cut on a beat | cuts on measured downbeats ([tools.md](tools.md)) | trailers, music-led Shorts |
| Pause | silence between narration lines | Shorts 0.25 s, devlogs ≤ 0.5 s; keep the breath at a sentence end | narration and its captions |
| Music under voice | the bed while someone speaks | about 10% of the voice (−20 dB), checked by measuring both stems | devlogs, voiced trailers |
| Sound effect | one short sound for one action | one per action, few per video | whip pans, arrivals, the hit that wins |

- **Say it all before the work starts**: message, energy, moves, numbers, brand, what not to touch. Each round trip costs a render [PRAC Moran].
- **Energy in one line**: a Short is busier than a devlog; long-form keeps graphics light because the thumbnail already won the click.
- **Never "our brand"**: paste the look's values or the template path. Told only "my brand", a model invents colours nine times in ten [PRAC Moran].
- **The gameplay does the work**: it is the A-roll. Graphics never cover the action, and a little goes a long way.
- Where the choice doesn't matter, name the allowed moves and let the agent pick ("cut or whip pan, your call"). Never leave the numbers to it.
- **Never trust a cut you didn't measure**: check loudness and where hits land ([tools.md](tools.md) "Measuring sound") before calling a mix done.
- **Liked an effect elsewhere?** Reverse-engineer it from the clip (`motion-graphics` "From a reference clip"); a description from memory misses most of its moving parts.

## Workflow

1. **Storyboard**: for any cut over 15 s, one still per beat with its seconds (`storyboard.png`, [tools.md](tools.md) "Storyboard sheet"). Fix the order and the hook on stills; a full render to find a wrong order wastes the most time [PRAC Moran: 12 stills, 4 acts, ~38 s before the build].
2. **Assembly**: placeholder title cards that describe the shots you need, in beat-sheet order.
3. **Rough**: first-pass capture, order, first music idea, rough sound.
4. **Fine**: final capture, music edit, SFX pass, text.
5. **Finish**: loudness, encode, per-channel versions, QA gate.

- Write the body first and the hook last, from the real payoff.
- **Review in one pass**: watch the whole cut once, writing each fix in `notes.md` as `mm:ss.ff · what · change`, then make every fix in one round. Drip-fed fixes re-render the cut each time.
- **Long cuts in segments**: past about 3 min, build each section as its own file and `concat` them, so a fix at 7:00 re-renders one segment.
- **Save what worked**: when a recipe or effect proves itself, add it to [tools.md](tools.md) or a `motion-graphics` template the same day.
