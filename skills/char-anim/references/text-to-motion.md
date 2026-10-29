# Text to motion: the fallback path

Text-to-motion services (Meshy Text to Motion, Hunyuan HY-Motion, Uthana and similar) rarely produce a clip that passes the quality gate for a signature move. In one trial most of about 166 credits of output was rejected. Use them for rough reference or background motion, and test on the cheap mode before the expensive one.

## Steps

1. **Acting note.** Read the character's design doc (three mood words, personality, weakness, attack, habits, signature skill staging) and write one sentence per clip: *who, does what, in what mood, how it ends*. Translate personality into **timing and body cues** (tables below).
2. **Prompt.** One English paragraph from the template below. Log every prompt in `<character>/motion/prompts.md` (note, prompt, length, result, verdict) so no prompt is repeated.
3. **Generate and apply.** One take on the cheap mode first (Meshy: `swift`, about 6 credits). Only a prompt that passes steps 4 and 5 is re-run unchanged on the high-quality mode (Meshy: `prime`, about 13 credits). 🔴 Say how many takes and roughly how many credits before generating. Apply the clip to your rigged body and run your rig fix on it right away. Meshy deletes generated motion after 3 days, so download the applied glb immediately.
4. **Render** at the battle camera and a side camera with your sheets script: battle gif, game-size gif, side gif, side arc plate (red right hand, blue left hand, yellow head, white hips; wider gaps mean faster). Keep frame PNGs in a temp folder; keep only gif, jpg and glb in the repo.
5. **Gates.** Pass the defect gate, then the quality gate in SKILL.md. On a failure, don't show it; change **one** thing in the prompt and regenerate, so you know what worked. Regenerating costs credits too; say so first.
6. **Show** battle, game-size, side and arc plate to the human; log the verdict in `prompts.md`.
7. **Touch-ups:** fix flaws in a chosen clip (long holds, sliding feet, a weapon through the body) with Blender scripts. Don't rebuild the body motion.

## Prompt template: principles in body language

```
A [weight and build in a few words], [body cues that show personality]. In place.
[Anticipation: slow/deep + which foot carries the weight] → then [strike: fast/explosive + what leads, what follows]
→ [short hold after contact] → then [end: back to a ready stance].
```

- 🔴 **One clip, one action; keep it short (under 60 words).** An attack is anticipation → strike → short hold → ready stance. Don't chain a stagger, a look at the fist, a shake and a chest puff; habits are separate clips. Four actions in one prompt twisted the body, laid it flat on the floor and dropped one action (HY-Motion README: "60 words, one action").
- 🔴 **No turning, direction or camera words** ("turns to his side", "glances back over his shoulder", "the swing carries him around", "facing the camera"). Every clip with such words turned the body and showed its back for over a second. Keep the body facing forward, "in place" (HY-Motion doesn't support camera or viewpoint words).
- 🔴 **Don't ask for poses the body can't do.** List them at the top of `prompts.md` (for example: fist no higher than the head because the armpit stretches; no big back arch). Clasped hands fail without finger bones.
- **Gestures at someone who isn't there** (patting an ally's shoulder) rarely work. Say where the hand goes and how many times, by body part; if that fails, use a preset plus touch-ups.
- **Describe only the body.** Clothes, dirt, colour and backstory don't affect motion (Hunyuan Motion, Uthana).
- **Body cues over adverbs:** "chest out, chin up, shoulders back" rather than "proudly" (Uthana, "Write direction, not just an action label").
- **Order words set the beat:** then, pauses, holds for a beat, before, after.
- **Name side and hand:** "right fist" is the character's right. Use the arm on the camera's side for big gestures. "In place" for stationary clips.
- **Set the end:** "then returns to a ready stance", so it joins the idle.
- Under 400 characters, 30 to 60 words. Earlier words weigh more; put build and personality first.
- Words aren't numbers: "slowly" doesn't become exact seconds (Uthana). Set length with the duration parameter.

### Principles to prompt words

| Principle | Words in the prompt |
| --- | --- |
| Anticipation opposite, big and slow | "winds up slowly", "draws back", "sinks low first", "weight on the back foot" |
| A pause at the top (moving hold) | "pauses at the top for a beat" |
| Short, explosive strike | "then explodes", "slams down fast", "whips across" |
| Joint sequence and drag | "hips and shoulders turn first, the arm whips after", "the fist trails behind the body" |
| Weight and planted feet | "feet planted", "knees bend deep", "shifts his whole weight onto the front foot" |
| Hold after contact | "holds the impact for a moment" |
| Overshoot, stagger, settle | "the momentum carries him a half step forward", "staggers, catches himself" |
| Head aims first | "looks at the target first" |
| Break symmetry | Describe the two hands and feet differently ("left foot forward, right arm back") |
| A living idle | "breathes slowly and deeply, shifts weight from foot to foot, small restless movements" |

### Personality in the body

| Quality | Anticipation | Strike | Recovery | Body cues |
| --- | --- | --- | --- | --- |
| Heavy, steadfast | Long and deep | Short and explosive | Long and weighty | knees bend deep, feet planted |
| Proud | Bigger than needed | No hesitation | Holds, then puffs the chest | chest out, chin up |
| Doesn't know his strength | | | Overshoots, staggers, looks at his hand | staggers, looks at his fist |
| Agile, cold | Short and low | Very short and straight | Cuts off at once | low crouch, minimal wasted motion |
| Playful, showman | Exaggerated delay | A big curving arc | Shows off a finishing pose | flourish, a showy pose at the end |

(sunstrikestudios "Timing in animation" · Riot "Character animation" · Overwatch GDC 2017)

### Duration: include the recovery, keep it short

| Clip | Seconds |
| --- | --- |
| Attack (heavy character) | 2.5 to 3.5. A 4 s slam spent too long bent over |
| Attack (light character) | 2 to 2.5 |
| Skill, victory | 3 to 4.5 |
| One habit | 2 to 3 |
| Idle (loop) | 6 to 8 |
