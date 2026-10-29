# Animation craft: acting, posing, timing, game motion

SKILL.md says **in what order** to build. This file says **what good motion is**: the standards Disney, Pixar and game studio animators learn and get reviewed against, turned into checks an agent can confirm with numbers and renders. Read it before writing an acting note and before showing poses. A pose that fails the checklist at the end isn't shown.

✅ marks a source checked in the original. A number without a source is a starting value measured on test figures; don't cite it as evidence.

## 1. Acting: the thought comes before the body

- **The formula:** a character pursues a demonstrable objective, overcomes an obstacle, and acts. ✅ Ed Hooks, "Acting for Animators" masterclass, point 6.
  - Write **goal, obstacle, action** for every clip. If one is missing, don't pose.
  - Example, a victory move: goal "wants to praise his little brother"; obstacle "his hand is too big and heavy"; action "reaches to pat his head, stops, taps his shoulder instead". The obstacle creates the hesitation, and the hesitation shows the personality.
- **Thinking leads to conclusions, emotion leads to action.** ✅ Hooks point 2. The beat where the thought changes must be on screen before the body moves ("Animate the thought", Hooks 5th edition contents).
  - A figure without eyeballs or eyelids shows thought through the **head**: it looks at the target 3 to 6 frames before the body moves.
  - Give the thought change its own key pose (surprise, realisation, decision).
- **The audience empathises with emotion, not thought.** ✅ Hooks point 4. One key pose should carry the emotion at its biggest.
- **Power centre:** anxiety sits high in the body (above the shoulders); confidence is anchored in the centre. ✅ Hooks point 16.
  - Check: a confident pose has low hips and dropped shoulders (negative shrug). Fear, surprise and tension raise the shoulders toward the ears.
- **Status transactions:** eye contact, distance and bowing set relative status. ✅ Hooks point 17. A big character's warmth is bending down to the other's height; pride is staying upright and looking down. The same shoulder tap reads as a different person at a different height.
- **Blinks:** three a minute keep the eyes wet; the rest mark thought. ✅ Hooks point 18. Without eyelids, put small nods or pauses only where the thought changes; don't scatter them.
- **No stock gestures** ("sad = slumped shoulders, face in hands"). Find what only this character does in front of this obstacle. Check the character's habits in the design doc first.
- **Few ideas, smooth links:** don't cram a clip. Lay out every idea, keep the best, order them so they flow and the biggest change lands on the point. Some clips need two ideas. ✅ Victor Navone (Pixar), "Rhythm and Texture", 2009.

## 2. Posing: one frame must read

- **Silhouette:** early Disney characters were solid black, so a hand in front of the chest vanished; staging in silhouette is always better. Pixar's André scratches his side, not his belly, so the action reads outside the body. ✅ Lasseter 1987, "Principles of Traditional Animation Applied to 3D Computer Animation", 2.4.
  - Check: shrink the battle-camera strip to game size and look at it as blobs. Each key pose must be nameable in **one word**. Know which side of the body faces your fixed camera; actions on the far shoulder, far hand or in front of the body are hidden (a pack on the far shoulder read as folded arms and was dropped).
  - Check: **neighbouring key poses must differ sharply.** Overlay two; if nearly identical, drop one or push it.
  - Move hands and fists out of the torso silhouette. An arm reaching toward the camera foreshortens, so put important gestures across the screen or upward.
- **One idea at a time:** stage so the eye goes to one place. ✅ Lasseter 2.4. One pose says one thing.
- **Line of action:** hips to chest to head should read as one curve (C or S). Straight back and straight legs look stiff. (Standard posing teaching since Disney.)
  - Check: from side and battle cameras, the line through hips, spine and head bends one way. Two opposing bends? Make it one.
  - Straight against curved: if one side is straight, the other bends (straight standing leg, curved torso). Both curved or both straight has no force.
- **Centre of gravity over the support:** game readability includes centre of gravity and balance. ✅ Jonathan Cooper, "Game Anim", Readability.
  - Check (number): when standing, the hips' ground position lies near the segment between the ankles. Outside it reads as falling; fix unless the stagger or fall is intended.
  - Standing leg: the weight-bearing leg straight, the pelvis tilts toward the free side, shoulders tilt the opposite way, the head follows the weight shift. ✅ Erik Westlund, "Pushing Poses" (Williams' "Animator's Survival Kit" applied to 3D).
- **No twins:** two hands, feet or shoulders mirroring each other look mechanical. Vary height, angle and timing.
- **Push it (exaggeration):** exaggerate the essence of the idea in design and motion. ✅ Lasseter principle 9. Pixar animators following video reference push poses further and simpler. ✅ Navone, "What Is Your Favorite Part of the Animation Process?", 2009.
  - Check: does the pose read in a silhouette shrunk to game size (around 127 px tall for a typical top-down battle view)? If not, it's weak, not subtle. Raise the angles, strip the extras.
- **Pose for the game camera** ✅ Cooper, Readability, "Posing for Game Cameras": a fixed camera never orbits. A pose that works from the front but collapses at the battle camera fails.

## 3. Timing and spacing: time makes weight and personality

- **Timing** sets weight, size and personality by how many frames a move takes. ✅ Lasseter principle 2. A giant reads as a giant through time more than size: late starts and stops, long anticipation, short strike, long recovery.
- **Keys, breakdowns, in-betweens:** keys (extremes) are where direction changes; the breakdown is the first drawing between two keys, and it's where arcs come from. ✅ Williams, "The Animator's Survival Kit", extremes and breakdowns.
  - 🔴 **Don't put the breakdown in the middle.** Favouring one key shows weight and inertia; moving it off-centre makes the arc clear. ✅ Westlund, "Pushing Poses" part 2.
  - In a keyframe helper: don't set a `flow` key exactly halfway. Let heavy ends (hands, head, toes) stay near the previous pose.
- **Drag:** extremities trail toward the previous pose. Wrists point back, the head tilts back. ✅ Westlund part 2. Drag and springs handle the frame offsets; bend wrists and head in the pose yourself.
- **Overlap:** don't fully stop one action before the next. The next one starts inside the last; a character who knows what's next is already moving there (Walt Disney). ✅ Lasseter 2.5.
- **Rhythm and texture:** don't repeat the same size and beat. Start small, grow, and put the biggest shape change on the point. ✅ Navone, "Rhythm and Texture" (Sulley searching for a sound in Monsters, Inc.: eyes, then head, then torso, then arms).
- **Moving hold:** a held pose keeps breath and a slight drift. Key more at holds so the curves don't melt the pose. ✅ Navone, "Splinophilia" (key every control on a hold).
- **Squash and stretch keep volume.** ✅ Lasseter principle 1. Shrink height, grow girth.

## 4. Order of work: thumbnails, reference, blocking at real speed

- Pixar's order ✅ Navone 2009: get every idea out on paper or video → choose → order them to flow → block poses with stepped keys (complex bodies get breakdowns every 4 or 2 frames) → fix timing → switch to splines → polish.
- **The first idea is the most clichéd;** the audience thinks of it too. Thumbnail past it. ✅ Shawn Kelly (ILM), "Tips and Tricks" vol. 1, Thumbnails. Write three or more ideas in the acting note and cross out the first (cheering, fist pump, chest beating).
- **Reads without explanation:** thumbnails alone should say what happens. ✅ Alexander Williams, "How Do Pixar Animators Thumbnail Their Shots?" A move that needs a caption fails.
- **Study reference, don't copy it.** Note the frame numbers where weight or pose changes sharply, then push the poses by principle. ✅ Kelly, "5 Key Steps for Effective Blocking". Real-person mocap previews (for example Meshy's library) are the nearest source; use measured frames as starting timing for weighted beats (a knee hitting the ground, a torso falling).
- **Everything is in the blocking:** key every control on every key. Anticipation, contacts, overshoot and arcs in the blocking mean the shot is 80% done. ✅ Kelly. When the pose changes, the whole body changes; a value identical between two poses means one of them is lying. Even planted feet roll a little as weight shifts. ✅ Brian Mendenhall, "7 Things All Animators Need to Start (or Stop) Doing".
- **Two options, three at most,** only when you truly can't choose, for the director to pick. ✅ Navone, "Inside Dailies at Pixar". Don't lay out piles of still poses.
- 🔴 **A blocking you show moves at real speed.** Per option:
  - a clip with keys and breakdowns every 2 to 4 frames, rendered through at 24 fps as **battle camera, front and game-size** gifs;
  - a strip every 4 frames and the arc plate;
  - placeholder neighbours standing where they really stand, so you see whether the move works on the board.
- Splining breaks timing ✅ Navone: add easing keys before holds, slide keys to tighten, add breakdowns. In a keyframe helper, add `stop` and `flow` keys.
- Don't change big timing in polish. If you must, go back to blocking.

## 5. Game motion: Cooper's five fundamentals

The twelve principles are film basics; games add five. ✅ Cooper, "Game Anim" and "The Five Fundamentals of Video Game Animation" (gameanim.com, 2020).

| Fundamental | Contains | In practice |
| --- | --- | --- |
| Feel | Response, inertia and momentum, visual feedback | In a deterministic sim the hit tick decides contact; the clip meets that frame and builds weight around it |
| Fluidity | Blending and transitions, seamless loops, settling | End poses join the idle; hits and skills blend in and out over the idle |
| Readability | Posing for game cameras, silhouettes, centre of gravity and balance | Section 2 |
| Context | Distinct from other characters, repetition, screen position | Table below |
| Elegance | Simple design, more from less, sharing | One idea per clip; the same rig tools for every hero |

**Context: how often it's seen changes how you build it** (example for an auto-battler)

| Clip | Seen | Build |
| --- | --- | --- |
| Idle | Always | Breath and small habits. Nothing big that tires on repeat; habits as separate clips mixed in now and then |
| Attack | Often | Anticipation, strike, return. Each attack needs a clearly different anticipation shape (GDKeys, "Anatomy of an Attack") |
| Skill | Sometimes | Where personality shows biggest; there's time for a thought beat |
| Victory | Once a fight, survivors **all at once** | Must work alone; you don't know who stands next to them. A move that needs a partner gets a solo version |
| Death | Once (for good), **while the fight goes on** | Spend the time on who this person was. Too clean has no feeling; collapse is messy and broken ✅ Animotion X, "Gameplay Animation Essentials 5". The last pose stays on the board, so the silhouette alone should say who it was |

- In an auto-battler you may not need hit reactions at all; a flash or effect can show the hit. Decide per project.

**One attack that reads small** ✅ Skullgirls, "Animation Bootcamp: Fluid and Powerful Animation" (GDC; 2D 60 fps fighting game practice, not measured for 3D top-down cameras)

- Anticipation can be short and still give contrast and power; one frame of anticipation made a six-frame move read. If the game speeds attacks up to 2×, judge the anticipation time left on screen.
- **Overshoot one frame** past the last key, then settle back (a `hit` then a `flow`). Without a held impact the hit looks weak; the game's hitstop holds it, and the contact pose must be clear enough to survive the hold.
- Leaving or entering idle, use **wide spacing** near the idle pose. A slow ease out plus a 0.15 s crossfade floats.
- A one-frame snap survives only if the engine samples that frame ([game-ready](game-ready.md) section 4).

## 6. Heavy bodies, non-human bodies

- Sell size with time (section 3). Inertia: big bodies take long to change direction. ✅ Cooper, Feel, "Inertia & Momentum".
- Don't hide weight shifts: weight moves over the standing foot before the other lifts. After a landing or slam, the knees absorb it.
- Each body has poses it can't do; list them in the character's motion notes. Monster parts: the `blender-anim` skill.

## 7. AI tells in motion (any one, don't show it)

- **Pose collection:** stills that don't connect. Each is plausible but no single person moves with one thought.
- **Everything stops on the same frame:** hands, head and hips halt together. Sequence, arcs and overshoot make this impossible. ✅ Kelly, "Twinning and Why You Should (Usually) Avoid It".
- **Floaty:** right key poses, evenly sliding in between. A spacing problem. ✅ Jim van der Keyl (iAnimate), "Why does your animation feel floaty?"
- **Mirror poses:** both arms or feet the same (robot zombie). ✅ Kelly, same article.
- **Frozen or never settling:** a dead hold, or endless drifting. A moving hold passes through an overshoot pose, settles, then only breathes. ✅ Kelly, "Why All Animators Need to Master the Moving Hold".
- **Stock gestures:** cheering, fist pump, chest beat, arms-wide fall. Anyone would do them.
- **Talking to air:** a gesture aimed at someone who isn't there floats.
- **A too-clean death:** lying down straight like a log.

## Scoring table: score yourself before showing

Each item 0 (no), 1 (short), 2 (yes). **🔴 If any 🔴 item is 0 or the total is under 16, don't show it; fix.** Paste the scores with one line of reasoning each into the note, so the human can calibrate your eye.

| Item | 2 points when | Check |
| --- | --- | --- |
| 🔴 The thought reads | From the game-size gif alone, without text, you can say in one sentence what happens; the thought-change beat shows | Watch the gif with no caption |
| 🔴 It's this character | Two of the three personality words read in the body; another hero doing it would look wrong | Compare with the stock-gesture list |
| 🔴 It works in the game | Not awkward where it really plays (board, neighbours, all at once, mid-fight) | Section 5 table |
| Silhouette | Each key pose nameable in one word at game size; neighbours differ sharply; no famous cliché pose (superhero landing) | Game gif, strip |
| Weight | Matches the timing measured from the reference (knee hits ground, torso drops), or pushed on purpose; planted feet don't slide | Against reference frames |
| Spacing and arcs | Hands and head arc on the arc plate; widest at the strike, tight at anticipation and hold | Arc plate |
| Sequence | Hips → chest → head and hands, starting and stopping; no twins | First-accelerating and fastest frame per part |
| Moving hold | No frozen stretch over 12 frames (except the last pose); holds settle through an overshoot | Dead-hold count |
| Body | No tearing; nothing through floor or body | Crop and enlarge the strip |
| Rhythm | Size and beat don't repeat; the biggest change is on the point | Gif |

## Checklist before showing poses

- [ ] Every clip's acting note has goal, obstacle, action. The first idea is crossed out.
- [ ] The thought change has its own key pose.
- [ ] Important gestures aren't buried in the torso or foreshortened toward the camera.
- [ ] One line of action; straight and curved sides contrast.
- [ ] Standing poses keep the centre of gravity over the support (falls excepted).
- [ ] Power centre and body height match the personality words.
- [ ] The scoring table passes.

## Sources

- John Lasseter, "Principles of Traditional Animation Applied to 3D Computer Animation", SIGGRAPH 1987: https://courses.cs.washington.edu/courses/cse458/21au/resources/lasseter.pdf
- Ed Hooks, "Acting for Animators" masterclass outline: https://edhooks.com/wp-content/uploads/2023/05/AFA_Masterclass-Studios-game-companies-v4.pdf · 5th edition: https://www.routledge.com/Acting-for-Animators/Hooks/p/book/9781032266473
- Jonathan Cooper, "Game Anim: Video Game Animation Explained" and "The Five Fundamentals": https://www.gameanim.com/2020/04/04/the-five-fundamentals-of-video-game-animation/
- Victor Navone (Pixar): "Rhythm and Texture" http://blog.navone.org/2009/09/rhythm-and-texture.html · workflow http://www.animationtipsandtricks.com/search/label/Victor%20Navone · "Splinophilia" http://www.navone.org/HTML/Tutorial_Splines2_3.htm
- Richard Williams, "The Animator's Survival Kit" (extremes and breakdowns, the pendulum). Applied to 3D: Erik Westlund, "Pushing Poses" http://pushingposes.blogspot.com/2008/03/basic-walk-cycle-part-2.html
- GDKeys, "Anatomy of an Attack": https://gdkeys.com/keys-to-combat-design-1-anatomy-of-an-attack/
- Shawn Kelly (ILM, Animation Mentor): "Tips and Tricks" vol. 1 https://content.animationmentor.com/pdfs/TipsAndTricks_Volume1.pdf · "5 Key Steps for Effective Blocking" https://www.animationmentor.com/blog/5-key-steps-for-effective-blocking/ · "Twinning" https://www.animationmentor.com/blog/twinning-and-why-you-should-usually-avoid-it/ · "Moving Hold" https://www.animationmentor.com/blog/why-all-animators-need-to-master-the-moving-hold/
- Victor Navone, "Inside Dailies at Pixar": https://www.animationmentor.com/blog/inside-dailies-at-pixar-expressing-your-opinion-about-changes-in-animation/
- Brian Mendenhall, "7 Things All Animators Need to Start (or Stop) Doing": https://www.animationmentor.com/blog/7-things-all-animators-need-to-start-or-stop-doing-right-now/
- Animotion X, "Gameplay Animation Essentials 5: Reactions": https://www.animotionx.com/en/post/animation-gameplay-essentials-episode-5-5-reactions
- Skullgirls, "Animation Bootcamp: Fluid and Powerful Animation", GDC: https://www.gdcvault.com/play/1020575/Animation-Bootcamp-Fluid-and-Powerful · video https://www.youtube.com/watch?v=Mw0h9WmBlsw
- On agents animating: in public benchmarks, frontier models scored poorly at adding acting from scratch but did well at adding to an existing clip. What worked: small steps, a render after each, numbers for every check. Human acting is still the hardest part, so get the pose choice from a human first.

**Not yet checked in the original:** Thomas and Johnston, "The Illusion of Life"; Cooper's chapters on hits and deaths; internal Pixar and Disney material. Numbers from secondary summaries (for example "hit reactions 8 to 16 frames", "symmetry ±5 degrees") stay unused until checked.
