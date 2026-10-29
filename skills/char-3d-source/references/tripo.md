# Tripo for main characters: access, settings, budgets, pitfalls

Tested with Tripo CLI 0.8.0 on a stylised humanoid figure. Check the docs for newer model and texture version strings.

## Access

- Use the official **Tripo CLI** (`npm install -g tripo-cli`, Node 20+). It wraps the whole API and blocks until a task ends. Agent docs ship with it: `tripo docs --llm`, `tripo docs --topic commands/process`.
- Log in once per machine: `tripo login --region ov` prints a URL and a code to approve on developers.tripo3d.ai. The key is stored in `~/.tripo/config.json` (0600). Never paste it in chat or commit it; if a script needs `TRIPO_API_KEY`, keep it in an untracked `.env`. `tripo doctor` checks login, network and balance.
- 🔴 **The CLI spends API credits, never Studio (web app) credits.** The two wallets are separate. Get the human's approval before buying API credits.
- Set `TRIPO_ANALYTICS_ENABLED=0` and `TRIPO_NO_UPDATE_CHECK=1` in scripts.
- Commercial use: paid users own their outputs, and Tripo doesn't train on them (developers.tripo3d.ai/en/terms 5.2.2). Re-check the terms for your plan.

## Settings that worked

| Step | Setting | Why |
| --- | --- | --- |
| Inputs | Views cut to one square canvas, same figure height and floor line, flat #E6E6E6, file names containing `front`/`left`/`back`/`right` | Tripo wants the same pose, light, background and scale in every view. The CLI maps file names to slots |
| Model | `--model tripo-v3.1` | Without `--model`, a face budget of 20,000 or less, or words like "game" or "low poly", route to the P1/P2 models (100 to 130 credits) |
| Triangles | `-p face_limit=30000` | Gave about 28k triangles, 17k vertices, around 100 UV islands |
| Texture | `-p texture_quality=detailed -p texture_version=v3.5-20260815 -p delight=true` | `delight` removes baked lighting (texture v3.5 only). Output: colour, normal and ORM at 4096 |
| Rig | `tripo anim rig --rig-type biped --spec mixamo --out-format fbx` | Exact Mixamo bone names (`mixamorig:*`, 65 bones with fingers), so any Mixamo-based retarget script takes it unchanged |
| Clips | `tripo anim retarget --animation preset:idle preset:walk --out-format fbx --animate-in-place` | Biped presets: idle walk run dive climb jump slash shoot hurt fall turn |

Measured prices (API credits): multi-view model with detailed texture 40, rig check 0, rig 25, retarget 10 per clip, retopology 35. Always run `tripo make … --dry-run --json` first; it returns the plan and a price estimate without uploading or spending.

## Getting the file into the game

Write one Blender script per character that:
- turns the figure from +X forward to your engine's forward on a parent root node (for Godot facing -Z, a root rotated -90 degrees about Z before export);
- scales 1 m to the character's height and puts the feet on the origin;
- takes the normal map from the model task's glb, not the rig FBX (see pitfalls);
- puts one NLA track per clip and shrinks textures to 2048.

## Budgets

- Generate at `face_limit=30000` and shrink textures to 2K in Blender. `tripo model convert --texture-size 2048` does it on Tripo's side but bills as a complex convert.
- Lower options:
  - `tripo mesh decimate <task> --model v3.0 --face-limit N`: 500 to 20,000 triangles, re-bakes textures. At 15k a figure looked the same at battle size, but the UVs split into about 2,500 islands and the vertex count went up.
  - `smart_low_poly`: 500 to 20,000 triangles, "hand-crafted" topology; complex inputs may fail. Untested.
  - P2 (Smart Mesh) with `quad=true` forces FBX. Untested.
- 🔴 Topology first, rig last. Retopology, `smart_low_poly`, quad output and segmentation rebuild the mesh and drop the skeleton (docs.tripo3d.ai rig v2.5). Retopology also invalidates UVs.

## Pitfalls

- Files are 1 m tall, +X forward. Rig, retarget and convert ignore a generation-time `export_orientation` and come out wrong while reporting success. Turn the figure in Blender, or use `convert --export-orientation` as the very last step.
- The rig FBX names its textures `<id>.fbm` and `<id>.fbm.001`. Blender's glTF exporter reads `.fbm` as the extension and writes one file for both, so the colour map lands in the normal slot. Rename images by use before exporting.
- The rig and retarget FBX embed both textures under one name, so the normal slot loads the colour picture. Take the normal map from the model task's glb (`NormalGL_*`).
- Scaling the armature object is overwritten by the sampled clip on export. Scale and turn a parent root node instead.
- A retarget FBX holds one take per preset (`Armature|Armature|idle`, `…|walk`, 30 fps). Select the take by clip name before renaming bones; a take swapped in after the rename stays on `mixamorig:` curves and freezes. Bake at a fixed fps and check every clip has more than two keys and a range above zero.
- The preset idle moves the hips off the rest pose (26 cm sideways on the test figure), so centre the figure on the posed body. It also stands bolt upright; from a high battle camera a small head sinks between the shoulders.
- A missing view is guessed. Give all four for bodies whose sides differ.
- A timeout doesn't cancel the task, and it's billed if it succeeds. Resume with `tripo task watch <id> --download`. Don't re-run `make` or `redo`.
- Clips made on another auto-rig (for example Meshy) can be retargeted onto a Tripo body frame by frame. If the other body's face was sculpted turned, put that turn back on the head or the character looks off-axis in every clip.

## Reported by others

- Shoulders deform after auto-rig: fix the weights in Blender (Tripo product doc "Rigging & Animation").
- Thin or hidden parts get simplified, and Smart Mesh can leave holes or invent detail when views conflict (r/Tripo_ai threads; Tripo staff recommend multi-view).
- A single front image of a flat shape can come back hollow (r/Tripo_ai).

## Sources

- https://developers.tripo3d.ai/en/docs/cli · /docs/generation-multiview-to-model/standard · /docs/animations-rig · /docs/mesh-decimate · /pricing · /terms
- https://studio.tripo3d.ai/cli (API credits for Studio subscribers, FAQ)
- https://www.tripo3d.ai/help: "Does Tripo Studio Membership Include API Access?", "How to Use Multi-View Images", "Commercial Use Rights"
- https://www.tripo3d.ai/product-doc: pricing-credits, p-series-smart-mesh, module-post-processing/retopo, rigging-animation
- Bundled CLI docs: `tripo docs --topic commands/generate`, `commands/process`, `examples/animation`, `examples/game-asset`
- https://docs.meshy.ai (multi-image-to-3d), https://help.meshy.ai (Multi-View Best Practices)
