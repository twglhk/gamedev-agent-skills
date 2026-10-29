# blender-anim log: what worked and what broke

Add one row after every review. Example rows from building a shadow-limbed enemy and a heavy humanoid hero:

| Subject | What was done | Result and lesson |
| --- | --- | --- |
| Enemy attack, take 1 | One bone of the load rotated by script; the body barely moved | ❌ "Looks like throwing trash." The body didn't follow and every part moved on the same curve |
| Hero, all clips | Every clip hand-keyed by numbers in one pass; plus 15 high-quality text-to-motion takes | ❌ Rejected twice; most text-to-motion credits wasted. Don't build body motion from numeric keys alone without agreed poses |
| Enemy attack, take 2 | Load attached to the body rig, linked by an ink rope, swung as mass particles | △ Close, but "don't lift the load to hit; only the shadow rises and slams." **Joining the part to the body tears the mesh** |
| Enemy attack, take 3 | Body and shadow as two separate objects; a fist rises out of the load and slams over the head | ✅ Right direction. Then polished: outlines removed from the shadow, flecks added, shadow leads the body |
| Enemy idle, walk, death | Same engine | ✅ Nothing to fix except crumpled legs in the death, solved by a floor guard that ignores arms and the chest spring turned off |
| Hero palms | Victory and death rejected; measuring showed the engine had no forearm roll, not a rig fault | ✅ `roll` channel plus three twist bones: wrist pinch 0.21 → 0.014, 0.05 at full pronation. Unlocking the elbow like a hinge made it worse and was dropped |
| Enemy glb export | Body and shadow exported as one clip, placed in the Godot battle scene | ❌→✅ Shadow chain shot thousands of metres in glTF (`inherit_scale NONE`). Reparented to the root bone and re-keyed; re-imported into Blender, it matched the source frame for frame |
| Game import audit | Every figure measured with a clip audit that reads the shipped glb | ❌ Godot resampled 24 fps clips at 30 fps and cut 9.3 degrees off an arm at the slam frame; a walk's loop seam 209 mm; hero idles' feet drifting 6 to 9 cm while enemy idles drifted 0. Bone and animation CPU cost is small; the weight is in triangles |

**Next to try:** the same engine on a crawling body with a shadow arm; calibrate the review script's thresholds against human verdicts; use the loop (pose stills → fast pass → numbers → final) for heroes too.
