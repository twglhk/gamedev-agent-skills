# Measuring frame cost

Budgets come from your build guide; this file is how to measure against them.

## Tools

- **A frame probe script** that opens a screen, lets it settle, then averages CPU and GPU frame time, draw calls, primitives and objects per step, and prints video memory at the end. Example call:

  ```sh
  godot --path game --position 20000,20000 --resolution 1920x1080 --rendering-driver vulkan \
    -s res://tools/perf_probe.gd -- screen=stage stages=plan,fight,boss frames=600 quality=high
  ```

  Give it switches like `off=sun_shadow` that turn one feature off; that is how you isolate a cost. If `quality=` writes the player config the way the settings menu does, back up the `user://` config first.
- **A whole-run frame logger** that plays a full stage in the real main scene at a player's pace and logs every drawn frame (wall time, process time, render CPU, pipeline compiles, what was happening). Interleave conditions so machine drift can't favour one, and report slow frames, worst frames, their causes, and whether battle logs matched.
- **Godot's profiler and monitors** in the editor for a function-level look when a probe shows a CPU cost you can't place.

## Method

1. **Name the question.** "Does the sun shadow cost more than 2 ms GPU at high?", not "is it fast?".
2. **Same conditions.** Same seed, steps, quality, resolution and frame count before and after. Disable vsync so frame time is real.
3. **One change per run.** Switch one thing off or on and measure; that is the Godot docs' hypothesis testing. When you don't know where the time goes, turn off half and halve again.
4. **CPU or GPU.** The frame takes as long as the slower of the two; speeding up the faster one changes nothing. Read both columns before choosing what to fix.
5. **Spikes are their own problem.** A steady 10 ms and one 479 ms hitch are different bugs. Report averages, worst frame and the count of frames over 16.6 ms; name a likely cause for each spike (often a shader compile the first time something is drawn).
6. **Profile again** after the fix; the bottleneck moves.

## Traps

- macOS Metal reports GPU time as 0. Use `--rendering-driver vulkan` (MoltenVK) for GPU numbers.
- `--headless` draws nothing, so render numbers there are meaningless. Probes run windowed, off screen.
- Other jobs (Blender, another Godot, exports) share the machine. Note the load average with every table; have the logger wait for competing jobs. Rerun when load was high.
- Mesh traps that look like perf bugs: vertex compression on environment meshes can drop omni-light shadows, and meshes whose shadow mesh lacks LODs were seen crashing on macOS. Guard both with an import test.
- Movie Maker (`--write-movie`) runs at fixed fps and hides real frame cost. Never measure while recording.

## Reporting

A table per condition: quality and size, step, GPU ms, CPU ms, slow frames, worst frame, before → after. Under it: machine, renderer and driver, load, frames per step, and what the change was.
