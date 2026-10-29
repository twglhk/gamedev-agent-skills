# Effects and shaders: principles and how to build them in Godot 4

Sources are numbered at the bottom. Numbers marked "starting value" combine several sources into a first build value; capture in your game and retune.

## 1. Beats: anticipation → contact → dissipation

- An effect has three beats [1]. Anticipation signals something is coming (gathering light, a shrinking ring, a wind-up). Contact is the brightest, strongest instant. Dissipation is where intensity falls and smoke, embers and afterglow extend the read.
- **After contact, intensity only falls** [2]. Plot brightness over time: it peaks at contact and keeps dropping. A bump back up in the middle reads as a second hit.
- Layers stagger inside one contact [2]. Flash (frame 0, 0.06 to 0.1 s) → spiky star burst (+2 frames) → streaks, rings, smoke, embers (+3 frames on, each with its own lifetime) → the point light goes out last. Fire them all on one frame and it looks flat.
- Curves are never linear [1]. Gathering accelerates (ease-in); after contact it bursts fast and slows (ease-out).

### Motion inside a beat

Linear change of size, shape or position inside a beat looks mechanical [10]. One hit moves like this:

- **Contact = pop then settle.** Appears small (about 0.6× its size) and reaches full size with ease-out within the contact frames (1 to 2). The first 3 to 4 frames are fast, then it slows.
- **Dissipation = erode from inside.** The shape doesn't blur; holes open from the centre and it erodes in steps (no soft fade, see "toon" below). While eroding it spreads outward only a little (about 1.05×).
- **Shards = ease-out.** They fly fast, slow and shrink, and disappear 1 to 2 frames after the body. Holding the last frame briefly is fine.
- **Worked example, a basic hit:** `pop_from` 0.6 → full size at `core_frames` 2 · `cavity` 0.8 (erodes from centre) · `grow_to` 1.06 · `shard_fly` 0.3 (ease-out). Curve `1 - (1 - t)^2`.
- Check by stepping key frames one at a time (`capture.py media`, frames 0, 1, 2, 4, 7, 10 from contact). If size changes by the same amount every frame, it's linear.

### Beat starting values (60 fps frames)

| Moment | Anticipation | Contact | Dissipation | Hitstop | Shake (trauma) |
| --- | --- | --- | --- | --- | --- |
| Basic hit | 0–3 | 1–2 | 6–12 | none | none |
| Critical hit | 2–4 | 2–3 | 12–20 | 2 | 0.15 |
| Hero skill | 12–20 | 3–6 | 20–40 | 2–6 | 0.2–0.35 |
| Enemy death | 0 | 3–6 | 30–60 (ink smoke) | 0 | 0 |
| Final blow | 0 | 3 | 30 + slow motion | 6 | 0.4 |
| Level-up / star-up | 6–12 | 3 | 30–45 | screen freeze 6 | 0.2 |
| Synergy activates | 4–6 staggered per unit | 3 | 30–45 | none | none |
| Team ultimate | 20–30 | 6 | 60–90 | 10 | 0.5 |
| Boss entrance | 30–60 | 10–20 | 20–40 | none | 0.6 (floor) |
| Boss death | empty 6–18 | 6 | slow motion 24 + darkness lifting 60–90 | 10 | 0.7 |

## 2. Game-feel devices

- **Hitstop.** Attacker and target freeze briefly on contact [3]. Smash Ultimate scales it with damage (a 15% move gets 15 frames) and caps at 30 [4]. An auto-battler has dozens of contacts per fight, so cap by strength: medium 2, strong 6, max 10.
  - During the freeze the hit body shakes in place, and the attack's particles keep running [4]. Freeze the particles too and the screen looks like it hung.
  - Implementation: the view stops feeding ticks to the display, puppets get `AnimationPlayer.speed_scale = 0`, effect particles keep playing. The simulation never knows.
- **Screen shake, trauma model** [5]. Keep a trauma value (0 to 1), add to it per moment, decay it linearly over time; shake amplitude is trauma squared (or cubed). So 0.3, 0.6, 0.9 give 3%, 22%, 73%: clearly different.
  - In 3D shake mostly rotation. Drive it with smooth noise (`FastNoiseLite`, fixed seed), not random values: smoother, works with pause and slow motion, and the same scene shakes the same way [5].
  - Starting values for a fixed camera that frames the whole board: max rotation 1.5°, max offset 0.1 m, decay 1.0/s.
- **Flash.** Paint the hit body white (or the side's colour) for 1 to 3 frames, one shader uniform.
- **Squash and stretch** [1]. Squash to 0.85–0.9 on contact and ease-out back over 3 to 6 frames. Stretch fast movers to 1.1–1.2. Subtle on bodies, bigger on effect blobs.
- **Damage numbers.** Rise 0.5 to 1 s from the hit point, slowing, gone in the last 0.2 s. Crits pop bigger and hold briefly.
- **Slow motion.** On the final blow and boss death, 0.3–0.5× for 0.2–0.5 s. Multiply the view's playback speed only; tick count is untouched.

## 3. Techniques that match a toon look

- **Hide the 3D** (Guilty Gear Xrd, Motomura GDC 2015) [6]. Scissored, stepped alpha edges instead of soft transparency; hand-drawn lumps instead of realistic noise smoke. Match effect line weight and colour to the bodies' ink lines.
- **Dissolve + edge glow.** Threshold a noise texture to erase the body and light only the band next to the threshold. A dying enemy breaks into ink smoke with an eerie edge glow; a fallen hero doesn't dissolve, only the warm light at its feet goes out.
- **Flipbook vs procedural.** Flipbooks are cheap, easy to edit and good for hand-drawn texture. Noise-built procedural effects are flexible but harder to art-direct. Ink and smoke lumps = flipbook; rings, beams, dissolves = shader.
- **Fresnel rim.** `pow(1.0 - dot(NORMAL, VIEW), k)` lights only the silhouette edge. For buffed units or shield shells.
- **Distortion.** Read `hint_screen_texture` with offset UVs. Max strength only (boss entrance, boss death, team ultimate).
- **Trails.** `GPUParticles3D.trail_enabled` or a ribbon mesh, thinner and fainter toward the end.
- **Soft particles.** Use `hint_depth_texture` to fade where an effect meets the floor so there's no hard cut line.
- **Readable on a dark board** [7]. Bright core + 1–2 px dark outline separates an effect from any background. Additive bright light only on the player side; enemy effects are carved dark with ink and lit only at the edge. That keeps the brightness order (heroes > enemies = background) in effects too.
- **Recipes and Godot traps.** Which job gets procedural shapes, flipbooks, UV scroll, fresnel, distortion, soft particles; scissor vs blend (ink lines, reflections); `amount_ratio`, `visibility_aabb`, instance uniforms: [shaders.md](shaders.md).
- **Whole-screen darkness.** If a post-process shader already drains saturation and darkens from the top as danger builds, drive darkness rising and lifting by curving its values, not by layering a new effect.

## 4. Godot 4 map

| Job | Use |
| --- | --- |
| Particles | `GPUParticles3D` + `ParticleProcessMaterial` (`one_shot`, strength via `amount_ratio`, `fixed_fps` and `interpolate`, game speed via `speed_scale`). `amount_ratio` only emits fewer; the cost is the full `amount`, so size `amount` to the strongest use [8] |
| Effect material | spatial shader `render_mode unshaded, shadows_disabled` + node `cast_shadow = OFF`, alpha scissor (`ALPHA_SCISSOR_THRESHOLD`) by default, billboard, `hint_depth_texture` (soft particles), `hint_screen_texture` (distortion, max only) [9] |
| Overdraw view | `Viewport.debug_draw = Viewport.DEBUG_DRAW_OVERDRAW` ignores shaders and counts whole quads. Shoot it on and off, then `capture.py overdraw` ([perf.md](perf.md)) |
| First-draw hitch | Materials built in code compile their pipeline on first draw. Instantiate each effect once, hidden, when the level opens ([perf.md](perf.md) "Shader compile stutter") |
| Hitstop | View stops feeding ticks + `AnimationPlayer.speed_scale = 0` + hit body shake. Particles keep going |
| Shake | `Camera3D` `h_offset`, `v_offset`, rotation + `FastNoiseLite` (fixed seed), trauma squared |
| One moment | `game/fx/<moment>.tscn` + `play(strength: StringName)`, reading values by strength name from the tuning resource |
| Capture | `python3 scripts/capture.py record res://fx/preview/<moment>.tscn /tmp/fx/<moment>.avi --frames <n> -- <scene args>`: Movie Maker at 1920×1080, 60 fps, sound in the same avi. Crop, key frames, measuring and perf use the same tool (rubric "How to measure") |
| Tests | Strength values come from data; `play()` doesn't change sim state; the log hash is equal with effects on and off |

## 5. Performance budget

Frequent moments add up. Cap each strength and cut at build time when over. Starting values; measure in your game and retune.

| Strength | Live at once | Particles per play | Screen area (peak, of 1080p) |
| --- | --- | --- | --- |
| Weak | 3 per body (reuse the oldest) | 8 | 0.5% |
| Medium | 1 per body | 32 | 2% |
| Strong | 2 on screen | 64 | 5% |
| Max | 1 on screen | 128 | 10%. Whole screen only through post-process values |

- **Reference point:** a well-built basic hit mark is about 60×57 px (0.17% of 1080p) with zero particles; a strong level-up peaked near 2.2%, a max moment near 2.9%.
- **Area.** `capture.py measure` reports the peak share of the frame whose luma moved more than 0.1 from frame 0. Moving bodies and shake count too, so measure on a still preview with shake and hitstop off.
- **Counts.** Cap live count with the effect scene's pool size and reuse the oldest when full. Particle count is `amount` × any amount scale.
- **Frames.** Run the worst scene (full board, every basic hit firing) at ×1 and ×2, effects on and off alternating, 5 runs each (`capture.py perf`). Count only on a machine with no other heavy Godot or Blender work (the tool waits and flags it). Metal reports GPU time 0, so use `--driver vulkan`. Verdict: rubric "Performance".
- **The real fight.** Not only previews: measure the effects' share (GPU, overdraw, particles, pipelines) in an exported build's boss fight. Commands and proposed caps in [perf.md](perf.md).

## Sources

1. Riot Games, Visual Effects Bootcamp: Artistic Principles of VFX (GDC): https://www.gdcvault.com/play/1024439/Visual-Effects-Bootcamp-Artistic-Principles · talk video https://www.youtube.com/watch?v=-L2JvngkkWw
2. RoClicks, Anatomy of an impact: https://roclicks.gg/resources/vfx/impact-recipe
3. Masahiro Sakurai, hitstop column (Famitsu 490, English translation): https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/
4. SmashWiki, Hitlag (per-game formulas, caps, shake, particles): https://www.ssbwiki.com/Hitlag · Sakurai's videos "Stop for Big Moments!" and "Eight Hit Stop Techniques"
5. Squirrel Eiserloh, Math for Game Programmers: Juicing Your Cameras With Math (GDC 2016): https://www.gdcvault.com/play/1023146/Math-for-Game-Programmers-Juicing
6. Junya C. Motomura, GuiltyGearXrd's Art Style: The X Factor Between 2D and 3D (GDC 2015): https://www.gdcvault.com/play/1022031/
7. Riot Games, League's VFX Style Guide: https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/ · Clarity in League: https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/
8. Godot 4 Particle systems (3D): https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html
9. Godot 4 Shaders: https://docs.godotengine.org/en/stable/tutorials/shaders/index.html
10. Gabriel Aguiar Prod., Frame-by-Frame Effects for Games (fast first 3–4 frames, erode from inside, hold the last frame): https://www.youtube.com/watch?v=GeCyq94tlzk
