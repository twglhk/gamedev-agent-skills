#!/usr/bin/env python3
"""fx-craft's one capture tool: record a moment, cut game-size media, measure it, run the perf check.

Global options (before the subcommand):
  --godot BIN       Godot executable (default: $GODOT or "godot")
  --project DIR     Godot project folder, the one with project.godot (default: $GODOT_PROJECT or "game")
  --size WxH        capture and analysis size (default 1920x1080)
  --font PATH       TrueType font for key-frame captions (default: Pillow's built-in font)

Assumptions: Godot 4.x with Movie Maker (--write-movie), run from the folder that holds --project.
SCENE is a res:// path to a preview scene that starts with the effect not yet visible, plays the
moment once, and accepts its own args after "--". perf needs that scene to write frame-time JSON.

  capture.py record SCENE OUT.avi [--frames N] [--pack X.pck] [-- scene args]
      Movie Maker at --size, 60 fps, in a visible window. Rejects the take when Godot's frame
      count differs from the decoded count or the log has an ERROR line.
  capture.py media CLIP --crop x,y,w,h --out DIR --name NAME [--probe x,y,w,h] [--near F] [--dark] [--contact F]
                   [--keys 0,1,2,4,7,10] [--key-box x,y,w,h] [--gray-clip CLIP] [--label TEXT]
      1:1 crops (no scaling, so sizes are game size): NAME-color.mp4, NAME-gray.mp4 and one PNG per
      key frame per colour mode. The contact frame is found in the picture (largest rise of the
      brightest 2% inside --probe), never assumed: Movie Maker frame numbers drift by one between runs.
  capture.py measure CLIP [--box x,y,w,h]
      measure.py's rubric numbers plus the peak screen area (share of the 1920x1080 frame).
  capture.py perf SCENE --out DIR --cond NAME="args" ... [--runs 5] [--off-arg --off] [--order swap|on-off]
                   [--pack X.pck] [--driver vulkan]
      Effect ON vs OFF, interleaved, several runs per condition, on a quiet machine. The scene must
      take --qa-out=PATH and write {"samples": [{"frame", "tick", "wall_ms"}], "summary": {"ticks"},
      "log_sha256"} (log_sha256 = a hash of the simulation log, so ON and OFF can be proven equal).
      Ends with perf-report. Optional: samples'
      "process_ms" and "render_cpu_ms" (game CPU column), "display": {"vsync_mode", "refresh_hz"}, and
      "events": [{"tick"}] (the effect's cues; the report then says how near each frame over 33.3 ms falls),
      samples' "gpu_ms" and "pipes" (pipelines compiled that frame: canvas, mesh, surface, draw,
      specialization) and events' "frame" (GPU and first-use diagnostics).
  capture.py perf-report DIR
      Frame-time table and the budget verdict for runs already in DIR.
  capture.py overdraw ON_DIR OFF_DIR
      The effects' own overdraw on the real stage: PNG shots of Godot's overdraw view
      (Viewport.DEBUG_DRAW_OVERDRAW) taken by your own census script, once as is and once with effects
      hidden, same file names for the same frames (step at a fixed 1/60 s). Layers per pixel read
      back from Godot's overdraw view and subtracted. Per shot: area the effects cover, their layers
      as a screen mean (1.0 = one full screen of extra fill), p99 and max where they draw.
  capture.py same CLIP_A CLIP_B [--box x,y,w,h] [--shift 10]
      Two takes of one scene frame by frame (best offset within --shift): how many frames are
      byte-identical and the largest channel difference. For changes that must not change the look.
  capture.py effect ON_CLIP OFF_CLIP [--box x,y,w,h] [--at F,F,...]
      The effect alone, from a take with it on against the same scene with it off (frame for frame,
      for an effect that never changes the scene, like a decal on a live fight): first and last frame it
      shows, frames it shows on, peak area, and the contrast of the pixels it changed against the
      same pixels without it (darkened and lightened apart, median relative-luminance ratio).
  capture.py cues CLIP --cues CUES.json
      For a moment with several sounds (a window, a chain): per cue, the frame its picture changes
      (inside the cue's box, found in the picture near the frame the scene logged) and the sound's
      onset (first clear rise of the 1 ms envelope over the 20 ms before it), their offset, how far the cue
      stands over what was already sounding (under 10 dB = buried), plus the clip's true peak and
      loudness from the first cue on. CUES.json = {"fps", "cues": [{"kind", "frame", "box": [x,y,w,h]}]}.

Needs godot, ffmpeg/ffprobe, numpy, Pillow (and pgrep for perf's quiet-machine guard).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean, median, quantiles, stdev
from typing import Any, Final

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import os

# Set from the global CLI options in main().
GODOT = os.environ.get("GODOT", "godot")
PROJECT = os.environ.get("GODOT_PROJECT", "game")
W = 1920
H = 1080
FONT: str | None = None
FPS: Final = 60
MEASURE: Final = Path(__file__).resolve().with_name("measure.py")
# Performance budget (rubric "Performance"). Frame times compare ON against OFF on the same scene.
WARMUP: Final = 120                # frames skipped at the start of each run
FRAME_MS: Final = 1000 / 60        # one refresh on a 60 Hz panel
HITCH_MS: Final = 1000 / 30        # two refreshes: a visible hitch
EXTRA_PER_1000: Final = 1.0        # ON may add at most this many frames over FRAME_MS per 1000 frames
P99_EXTRA_MS: Final = 0.5          # ON's median run p99 may exceed OFF's by at most this
# Diagnostics beside the verdict, not part of it. Under 60 Hz vsync every interval sits on 16.67 ms and
# about half read a hair over it (present jitter), so ">16.7 ms" counts nothing real there. An interval
# over MISS_MS clearly missed its refresh; game CPU (process + render CPU) over FRAME_MS is our own work
# overrunning the budget.
MISS_MS: Final = 20.0
NEAR_TICKS: Final = (0, 5)         # windows (battle ticks) for "hitch near an effect event", same tick and close
VSYNC: Final = {0: "off", 1: "on", 2: "adaptive", 3: "mailbox"}  # DisplayServer.VSyncMode
AREA_DELTA: Final = 0.1            # a pixel counts as covered when its luma moves this much from frame 0
GUARD: Final = r"(godot|Godot)( |$)|[Bb]lender -b"  # competing heavy work during perf runs

Box = tuple[int, int, int, int]
Luma = NDArray[np.float64]


def box(text: str) -> Box:
    x, y, w, h = (int(v) for v in text.split(","))
    return x, y, w, h


def luminance(rgb: NDArray[np.uint8]) -> Luma:
    """Linear relative luminance (WCAG), same formula as measure.py."""
    c = rgb.astype(np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722


def run(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(cmd, capture_output=True, check=True)


def frame_count(clip: Path) -> int:
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
               "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(clip)]).stdout
    return int(out)


# ---- record ---------------------------------------------------------------------------------

def source(pack: Path | None) -> list[str]:
    """The project folder, or an exported .pck (--pack): the build as players get it."""
    return ["--main-pack", str(pack)] if pack else ["--path", PROJECT]


def record(scene: str, out: Path, frames: int, scene_args: list[str], pack: Path | None = None) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    log = out.with_suffix(".log")
    cmd = [GODOT, *source(pack), "--resolution", f"{W}x{H}", "--position", "0,0", "--always-on-top",
           "--fixed-fps", str(FPS), "--write-movie", str(out), "--quit-after", str(frames), scene]
    if scene_args:
        cmd += ["--", *scene_args]
    with log.open("w") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True, timeout=600)
    text = log.read_text()
    said = re.search(rf"\n(\d+) frames at {FPS} FPS", text)
    decoded = frame_count(out)
    if said is None or int(said.group(1)) != decoded or "ERROR:" in text:
        sys.exit(f"take rejected: Godot said {said.group(1) if said else 'nothing'}, decoded {decoded}, see {log}")
    print(f"{out}: {decoded} frames, log {log}")


# ---- media ----------------------------------------------------------------------------------

def luma_frames(clip: Path, area: Box, scale: int = 1) -> Luma:
    """Linear relative luminance of one region for every frame, shape (frames, h, w)."""
    x, y, w, h = area
    w2, h2 = w // scale, h // scale
    vf = f"format=rgb24,crop={w}:{h}:{x}:{y}" + (f",scale={w2}:{h2}:flags=area" if scale > 1 else "")
    raw = run(["ffmpeg", "-v", "error", "-i", str(clip), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]).stdout
    rgb = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h2, w2, 3)
    return luminance(rgb)


def find_contact(clip: Path, probe: Box, near: int | None, dark: bool = False) -> int:
    """Largest rise of the brightest 2% in the probe; with dark, largest fall of the darkest 2%
    (an effect that darkens, like an ink or shadow burst)."""
    luma = luma_frames(clip, probe).reshape(-1, probe[2] * probe[3])
    core = -np.percentile(luma, 2, axis=1) if dark else np.percentile(luma, 98, axis=1)
    lo, hi = (0, len(core)) if near is None else (max(near - 8, 0), min(near + 9, len(core)))
    rise = np.diff(core[lo:hi])
    return lo + int(np.argmax(rise)) + 1


def stills(clip: Path, indices: list[int]) -> dict[int, Image.Image]:
    pick = "+".join(f"eq(n\\,{i})" for i in sorted(set(indices)))
    raw = run(["ffmpeg", "-v", "error", "-i", str(clip), "-vf", f"select='{pick}'", "-fps_mode", "passthrough",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]).stdout
    size = W * H * 3
    images = [Image.frombytes("RGB", (W, H), raw[k * size:(k + 1) * size]) for k in range(len(raw) // size)]
    return dict(zip(sorted(set(indices)), images))


def card(image: Image.Image, text: str) -> Image.Image:
    out = Image.new("RGB", (image.width, image.height + 36), "#14181c")
    out.paste(image, (0, 36))
    font = ImageFont.truetype(FONT, 22) if FONT else ImageFont.load_default()
    ImageDraw.Draw(out).text((10, 6), text, font=font, fill="white")
    return out


def gray(image: Image.Image) -> Image.Image:
    lum = luminance(np.asarray(image))
    srgb = np.where(lum <= 0.0031308, lum * 12.92, 1.055 * lum ** (1 / 2.4) - 0.055)
    return Image.fromarray((np.clip(srgb, 0, 1) * 255 + 0.5).astype(np.uint8)).convert("RGB")


def video(clip: Path, crop: Box, out: Path, to_gray: bool, audio: bool = False) -> None:
    x, y, w, h = crop
    vf = f"crop={w}:{h}:{x}:{y}" + (",format=gray" if to_gray else "")
    sound = ["-c:a", "aac", "-b:a", "192k"] if audio else ["-an"]
    run(["ffmpeg", "-y", "-v", "error", "-i", str(clip), "-vf", vf, *sound, "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "16", "-movflags", "+faststart", str(out)])


def media(a: argparse.Namespace) -> None:
    out: Path = a.out
    out.mkdir(parents=True, exist_ok=True)
    crop, key_box = a.crop, a.key_box or a.crop
    keys = [int(k) for k in a.keys.split(",")]
    modes = {"color": a.clip, "gray": a.gray_clip or a.clip}
    contacts: dict[str, int] = {}
    for mode, clip in modes.items():
        video(clip, crop, out / f"{a.name}-{mode}.mp4", to_gray=mode == "gray" and a.gray_clip is None,
              audio=a.audio and mode == "color")
        if a.probe is None and a.contact is None:
            continue
        contact = a.contact if a.contact is not None else find_contact(clip, a.probe, a.near, a.dark)
        contacts[mode] = contact
        frames = stills(clip, [contact + k for k in keys])
        x, y, w, h = key_box
        for order, k in enumerate(keys, 1):
            image = frames[contact + k].crop((x, y, x + w, y + h))
            if mode == "gray" and a.gray_clip is None:
                image = gray(image)
            card(image, f"{order}. {a.label} +{k} frames · {mode} · game size").save(out / f"{a.name}-key{order}-{mode}.png")
    info = {"clip": str(a.clip), "crop": crop, "key_box": key_box, "probe": a.probe, "keys": keys, "contact": contacts}
    (out / f"{a.name}.json").write_text(json.dumps(info, indent=2, ensure_ascii=False))
    print(json.dumps(info, ensure_ascii=False))


# ---- measure --------------------------------------------------------------------------------

def peak_area(clip: Path) -> tuple[float, int]:
    """Largest share of the whole frame whose luma moved more than AREA_DELTA from frame 0 (quarter size)."""
    w, h = W // 4, H // 4
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(clip), "-vf", f"scale={w}:{h}:flags=area",
                             "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    assert proc.stdout is not None
    first: NDArray[np.int16] | None = None
    best, best_frame, n = 0.0, 0, 0
    while chunk := proc.stdout.read(w * h):
        frame = np.frombuffer(chunk, dtype=np.uint8).astype(np.int16)
        if first is None:
            first = frame
        share = float((np.abs(frame - first) > AREA_DELTA * 255).mean())
        if share > best:
            best, best_frame = share, n
        n += 1
    proc.wait()
    return best, best_frame


def measure_cmd(a: argparse.Namespace) -> None:
    extra = ["--box", ",".join(str(v) for v in a.box)] if a.box else []
    _ = subprocess.run([sys.executable, str(MEASURE), str(a.clip), *extra], check=True)
    share, frame = peak_area(a.clip)
    print(f"area       {share * 100:6.2f} % of the frame at frame {frame} (luma moved > {AREA_DELTA}; "
          "includes moving bodies, so judge it on a still preview)")


# ---- same -----------------------------------------------------------------------------------

def rgb_frames(clip: Path, area: Box) -> NDArray[np.uint8]:
    x, y, w, h = area
    raw = run(["ffmpeg", "-v", "error", "-i", str(clip), "-vf", f"crop={w}:{h}:{x}:{y}", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-"]).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w, 3)


def same_cmd(a: argparse.Namespace) -> None:
    area = a.box or (0, 0, W, H)
    one, two = rgb_frames(a.a, area), rgb_frames(a.b, area)
    best: tuple[int, int, int] = (-1, 0, 0)  # (identical frames, offset, compared)
    for off in range(-a.shift, a.shift + 1):
        lo, hi = max(0, -off), min(len(one), len(two) - off)
        equal = sum(np.array_equal(one[i], two[i + off]) for i in range(lo, hi))
        best = max(best, (equal, off, hi - lo))
    equal, off, n = best
    lo = max(0, -off)
    diffs = [int(np.abs(one[i].astype(np.int16) - two[i + off].astype(np.int16)).max()) for i in range(lo, lo + n)]
    moved = [i for i, d in zip(range(lo, lo + n), diffs) if d]
    print(f"{a.a.name} vs {a.b.name}: {len(one)} / {len(two)} frames, best offset {off:+d}: "
          f"{equal} of {n} frames identical, largest channel difference {max(diffs, default=0)}"
          + (f", first differing frame {moved[0]}" if moved else ""))
    print("IDENTICAL" if equal == n and n > 0 else "DIFFERENT")


# ---- effect (on vs off) ---------------------------------------------------------------------

def stream_luma(clip: Path, area: Box):
    """Linear luminance of one region, one frame at a time."""
    x, y, w, h = area
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(clip), "-vf", f"crop={w}:{h}:{x}:{y}",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    assert proc.stdout is not None
    while chunk := proc.stdout.read(w * h * 3):
        yield luminance(np.frombuffer(chunk, dtype=np.uint8).reshape(h, w, 3))
    proc.wait()


def effect_cmd(a: argparse.Namespace) -> None:
    area = a.box or (0, 0, W, H)
    at = {int(v) for v in a.at.split(",")} if a.at else set()
    shown: list[int] = []
    best, best_frame = 0.0, -1
    rows: list[str] = []
    for i, (on, off) in enumerate(zip(stream_luma(a.on, area), stream_luma(a.off, area))):
        moved = np.abs(on - off) > AREA_DELTA * 0.5   # half the area step: ink on a dark floor moves little
        if not moved.any():
            continue
        shown.append(i)
        share = float(moved.sum()) / (W * H)
        if share > best:
            best, best_frame = share, i
        if i in at:
            dark = moved & (on < off)
            light = moved & (on > off)
            d = float(np.median((off[dark] + 0.05) / (on[dark] + 0.05))) if dark.any() else 0.0
            l = float(np.median((on[light] + 0.05) / (off[light] + 0.05))) if light.any() else 0.0
            rows.append(f"  frame {i:4d}: area {share * 100:5.2f} %  darkened {int(dark.sum()):6d} px at {d:4.2f} : 1"
                        f"  lightened {int(light.sum()):6d} px at {l:4.2f} : 1")
    if not shown:
        print("no difference: the effect never showed")
        return
    print(f"shows      frames {shown[0]}..{shown[-1]} ({len(shown)} frames with a difference)")
    print(f"area       {best * 100:6.2f} % of the frame at its peak, frame {best_frame}")
    print("contrast   (the changed pixels against the same pixels without the effect)")
    print("\n".join(rows))


# ---- cues -----------------------------------------------------------------------------------

AUDIO_RATE: Final = 48000
CUE_SEARCH: Final = 6          # frames either side of the logged frame to find the picture change
CHANGE: Final = 0.004          # mean luma change inside the box that counts as the picture moving
# Onset = the first millisecond that clears the loudest of the ONSET_BACK ms before it by at least
# ONSET_SHARE of the best such clearance near the cue (and ONSET_MIN_DB). Measured against the loudest
# level just before, not the level one step before, a dip-and-recover inside a ringing sound (a low
# partial's ripple, a swell inside a stamp under another's tail) is never an onset.
ONSET_BACK: Final = 20
ONSET_MIN_DB: Final = 3.0
ONSET_SHARE: Final = 0.5
# Over bed = the cue's first BED_HEAD ms against the BED_BACK ms just before its onset (energy means).
# A cue under BED_MIN_DB over what was already sounding is buried, even when its onset is on time.
BED_HEAD: Final = 12
BED_BACK: Final = (85, 3)
BED_MIN_DB: Final = 10.0


def clip_audio(clip: Path) -> NDArray[np.float64]:
    raw = run(["ffmpeg", "-v", "error", "-i", str(clip), "-vn", "-ac", "1", "-ar", str(AUDIO_RATE),
               "-f", "s16le", "-"]).stdout
    return np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0


def envelope_db(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """1 ms RMS envelope in dBFS, one value per millisecond."""
    hop = AUDIO_RATE // 1000
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
    return 20 * np.log10(np.maximum(rms, 1e-6))


def onset_ms(env: NDArray[np.float64], lo: int, hi: int) -> int:
    """First ms in [lo, hi) whose level clears the loudest of the ONSET_BACK ms before it by enough."""
    lo = max(lo, ONSET_BACK)
    clear = np.array([env[m] - env[m - ONSET_BACK:m].max() for m in range(lo, hi)])
    need = max(ONSET_MIN_DB, ONSET_SHARE * float(clear.max()))
    return lo + int(np.argmax(clear >= need))


def over_bed_db(env: NDArray[np.float64], onset: int) -> float:
    def level(a: int, b: int) -> float:
        return float(10 * np.log10(np.mean(10 ** (env[max(a, 0):b] / 10))))
    return level(onset, onset + BED_HEAD) - level(onset - BED_BACK[0], onset - BED_BACK[1])


def cues_cmd(a: argparse.Namespace) -> None:
    spec = importlib.util.spec_from_file_location("fx_measure", MEASURE)
    assert spec is not None and spec.loader is not None
    measure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(measure)
    data = json.loads(a.cues.read_text())
    fps = int(data.get("fps", FPS))
    env = envelope_db(clip_audio(a.clip))
    print("| Cue | Logged frame | Picture frame | Sound onset ms | Offset ms | Over bed dB | Verdict |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    worst, buried = 0.0, 0
    for c in data["cues"]:
        lum = luma_frames(a.clip, tuple(c["box"]))
        lo, hi = max(1, c["frame"] - CUE_SEARCH), min(len(lum) - 1, c["frame"] + CUE_SEARCH)
        moved = [f for f in range(lo, hi + 1) if float(np.abs(lum[f] - lum[f - 1]).mean()) > CHANGE]
        pic = moved[0] if moved else c["frame"]
        pic_ms = pic * 1000.0 / fps
        onset = onset_ms(env, int(max(0, pic_ms - 60)), int(min(len(env), pic_ms + 120)))
        off = onset - pic_ms
        bed = over_bed_db(env, onset)
        worst = max(worst, abs(off))
        buried += bed < BED_MIN_DB
        print(f"| {c['kind']} | {c['frame']} | {pic}{'' if moved else ' (no change found)'} | {onset} | {off:+.0f} | {bed:.1f} | "
              f"{'PASS' if abs(off) <= measure.SYNC_MS else 'FAIL'}{' · buried' if bed < BED_MIN_DB else ''} |")
    print(f"worst offset {worst:.0f} ms ({'PASS' if worst <= measure.SYNC_MS else 'FAIL'}, <= {measure.SYNC_MS:.0f})")
    print(f"over bed   {buried} cue(s) under {BED_MIN_DB:.0f} dB over what was already sounding "
          "(diagnostic, not a gate: the 10 dB line is an unvalidated proposal; cues sharing a frame share one onset)")
    start = max(0.0, min(c["frame"] for c in data["cues"]) / fps - 0.05)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        run(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", str(a.clip), "-vn", "-ac", "2",
             "-ar", str(AUDIO_RATE), "-c:a", "pcm_s16le", str(wav)])
        lufs, tp = measure.loudness(wav)
        mom = measure.momentary_max(wav)
    print(f"true peak  {tp:6.1f} dBTP {'PASS' if tp <= measure.TRUE_PEAK_MAX else 'FAIL'} (from the first cue on)")
    print(f"loudness   {lufs:6.1f} LUFS integrated · {mom:.1f} LUFS loudest 400 ms (short clip: reference only)")


# ---- perf -----------------------------------------------------------------------------------

def busy() -> list[str]:
    # macOS pgrep already takes an extended regex; it has no -E flag (it used to fail silently here).
    out = subprocess.run(["pgrep", "-fl", GUARD], capture_output=True, text=True).stdout
    return [line for line in out.splitlines() if "pgrep" not in line and "capture.py" not in line]


def perf_run(scene: str, args: list[str], json_out: Path, pack: Path | None = None, driver: str | None = None) -> None:
    waited = 0
    while busy() and waited < 300:
        time.sleep(5)
        waited += 5
    before = busy()
    cmd = [GODOT, *source(pack), *(["--rendering-driver", driver] if driver else []), "--always-on-top", "--resolution", f"{W}x{H}", "--position", "0,0",
           scene, "--", *args, f"--qa-out={json_out}"]
    during: set[str] = set()
    with json_out.with_suffix(".log").open("w") as log:
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            during.update(line for line in busy() if f"--qa-out={json_out}" not in line)
            time.sleep(0.5)
    meta = {"args": args, "waited_s": waited, "competing_before": before, "competing_during": sorted(during),
            "exit": proc.returncode}
    json_out.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2))
    print(json_out.stem, "contaminated" if before or during else "clean", flush=True)


def perf(a: argparse.Namespace) -> None:
    out: Path = a.out
    out.mkdir(parents=True, exist_ok=True)
    conds = dict(c.split("=", 1) for c in a.cond)
    for rep in range(1, a.runs + 1):
        for name, args in conds.items():
            # swap: alternate which side goes first so drift cannot favour one side.
            # on-off: always ON then OFF, so each pair rN shares its moment.
            for on in ((True, False) if a.order == "on-off" or rep % 2 else (False, True)):
                path = out / f"{name}-{'on' if on else 'off'}-r{rep}.json"
                if not path.exists():
                    perf_run(a.scene, args.split() + ([] if on else [a.off_arg]), path, a.pack, a.driver)
    perf_report(out)


@dataclass
class Side:
    runs: int = 0
    clean: int = 0
    frames: int = 0
    over_frame: int = 0
    over_hitch: int = 0
    worst_ms: float = 0.0
    p99s: tuple[float, ...] = ()
    log_sha: frozenset[str] = frozenset()
    over_miss: int = 0
    over_cpu: int | None = 0  # None once a run's samples lack process_ms or render_cpu_ms
    displays: frozenset[str] = frozenset()
    hitch_runs: dict[int, tuple[int, int]] = field(default_factory=dict)  # run -> (frames over HITCH_MS, frames)
    # (run, frame, tick, wall ms, game CPU ms or None, ticks to the nearest event or None)
    hitches: list[tuple[int, int, int, float, float | None, int | None]] = field(default_factory=list)
    near_event: dict[int, int] = field(default_factory=dict)  # window in ticks -> kept frames that near an event
    has_events: bool = True


def display_of(data: dict) -> str:
    """The run's vsync state and refresh rate, as the scene recorded them."""
    d = data.get("display")
    if not d:
        return "vsync ? · refresh ? (not recorded)"
    hz = float(d.get("refresh_hz", -1))
    return f"vsync {VSYNC.get(int(d.get('vsync_mode', -1)), '?')} · {f'{hz:.0f} Hz' if hz > 0 else 'refresh ?'}"


def perf_report(out: Path) -> None:
    sides: dict[tuple[str, str], Side] = {}
    for path in sorted(out.glob("*-r*.json")):
        if path.name.endswith(".meta.json"):
            continue
        name, side, rep = path.stem.rsplit("-", 2)
        data = json.loads(path.read_text())
        meta = json.loads(path.with_suffix(".meta.json").read_text())
        last = int(data["summary"]["ticks"])
        kept = [s for s in data["samples"] if s["frame"] > WARMUP and s["tick"] < last]
        wall = [float(s["wall_ms"]) for s in kept]
        s = sides.setdefault((name, side), Side())
        s.runs += 1
        s.clean += int(not meta["competing_before"] and not meta["competing_during"])
        s.frames += len(wall)
        s.over_frame += sum(v > FRAME_MS for v in wall)
        s.over_hitch += sum(v > HITCH_MS for v in wall)
        s.over_miss += sum(v > MISS_MS for v in wall)
        if s.over_cpu is not None and all("process_ms" in x and "render_cpu_ms" in x for x in kept):
            s.over_cpu += sum(float(x["process_ms"]) + float(x["render_cpu_ms"]) > FRAME_MS for x in kept)
        else:
            s.over_cpu = None
        s.worst_ms = max(s.worst_ms, max(wall))
        s.p99s = (*s.p99s, quantiles(wall, n=100, method="inclusive")[98])
        s.log_sha = s.log_sha | {str(data["log_sha256"])}
        s.displays = s.displays | {display_of(data)}
        run = int(rep[1:])
        s.hitch_runs[run] = (sum(v > HITCH_MS for v in wall), len(wall))
        events = sorted({int(e["tick"]) for e in data["events"]}) if "events" in data else None
        s.has_events = s.has_events and events is not None

        def nearest(tick: int) -> int | None:
            return min((abs(tick - t) for t in events), default=None) if events is not None else None

        dists = [nearest(int(x["tick"])) for x in kept]
        for window in NEAR_TICKS:
            s.near_event[window] = s.near_event.get(window, 0) + sum(d is not None and d <= window for d in dists)
        for x in kept:
            if float(x["wall_ms"]) > HITCH_MS:
                cpu = float(x["process_ms"]) + float(x["render_cpu_ms"]) if "process_ms" in x and "render_cpu_ms" in x else None
                s.hitches.append((run, int(x["frame"]), int(x["tick"]), float(x["wall_ms"]), cpu, nearest(int(x["tick"]))))
    shown = sorted({d for s in sides.values() for d in s.displays})
    print(f"Display: {' | '.join(shown) if shown else 'no runs'}")
    print(f"| Condition | Runs (clean) | Frames | >{FRAME_MS:.1f} ms | >{HITCH_MS:.1f} ms | Worst ms | Median p99 ms "
          f"| >{MISS_MS:.0f} ms (diag) | Game CPU >{FRAME_MS:.1f} ms (diag) | Display |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for (name, side), s in sorted(sides.items()):
        cpu = "n/a" if s.over_cpu is None else str(s.over_cpu)
        print(f"| {name} {side.upper()} | {s.runs} ({s.clean}) | {s.frames:,} | {s.over_frame} | {s.over_hitch} | "
              f"{s.worst_ms:.2f} | {median(s.p99s):.2f} | {s.over_miss} | {cpu} | {' / '.join(sorted(s.displays))} |")
    if any(d.startswith("vsync on") or d.startswith("vsync adaptive") for d in shown):
        print(f"Note: vsync paces intervals at the refresh, so >{FRAME_MS:.1f} ms counts present jitter; "
              f"read >{MISS_MS:.0f} ms and game CPU beside it.")
    for name in sorted({n for n, _ in sides}):
        on, off = sides.get((name, "on")), sides.get((name, "off"))
        if on is None or off is None or not on.frames or not off.frames:
            print(f"{name}: needs both ON and OFF runs")
            continue
        p99 = median(on.p99s) - median(off.p99s)
        extra = (on.over_frame / on.frames - off.over_frame / off.frames) * 1000
        checks = {
            f"added frames over {FRAME_MS:.1f} ms {extra:+.2f}/1000 (<= {EXTRA_PER_1000})": extra <= EXTRA_PER_1000,
            f"ON frames over {HITCH_MS:.1f} ms: {on.over_hitch} (= 0)": on.over_hitch == 0,
            f"p99 ON-OFF {p99:+.2f} ms (<= {P99_EXTRA_MS})": p99 <= P99_EXTRA_MS,
            "battle log ON = OFF": len(on.log_sha | off.log_sha) == 1,
            "every run clean": on.clean == on.runs and off.clean == off.runs,
        }
        verdict = "PASS" if all(checks.values()) else "FAIL"
        print(f"{name}: {verdict} - " + " · ".join(f"{k} {'ok' if v else 'NO'}" for k, v in checks.items()))
    for name in sorted({n for n, _ in sides}):
        hitch_detail(name, sides.get((name, "on")), sides.get((name, "off")))
    gpu_detail(out)


PIPE_KINDS: Final = ("canvas", "mesh", "surface", "draw", "specialization")


def gpu_detail(out: Path) -> None:
    """Diagnostics when samples carry "gpu_ms" and "pipes" (pipelines compiled that frame, PIPE_KINDS order):
    GPU time per side, pipeline compiles in and after the warmup, and every slow frame split into its parts."""
    rows: dict[tuple[str, str], list[tuple[int, dict[str, Any], set[int]]]] = {}
    for path in sorted(out.glob("*-r*.json")):
        if path.name.endswith(".meta.json"):
            continue
        name, side, rep = path.stem.rsplit("-", 2)
        data = json.loads(path.read_text())
        if not data["samples"] or "gpu_ms" not in data["samples"][0]:
            continue
        frames = {int(e["frame"]) for e in data.get("events", []) if "frame" in e}
        for s in data["samples"]:
            rows.setdefault((name, side), []).append((int(rep[1:]), {**s, "_last": int(data["summary"]["ticks"])}, frames))
    if not rows:
        return
    print("\nGPU and pipeline compiles (diag)")
    for (name, side), items in sorted(rows.items()):
        kept = [s for _, s, _ in items if s["frame"] > WARMUP and s["tick"] < s["_last"]]
        gpu = sorted(float(s["gpu_ms"]) for s in kept)
        ev = [float(s["gpu_ms"]) for _, s, fr in items if s["frame"] > WARMUP and any(0 <= s["frame"] - f <= 3 for f in fr)]
        warm = [sum(s["pipes"][k] for _, s, _ in items if s["frame"] <= WARMUP) for k in range(len(PIPE_KINDS))]
        late = [sum(s["pipes"][k] for s in kept) for k in range(len(PIPE_KINDS))]
        print(f"- {name} {side.upper()}: GPU median {median(gpu):.2f} · p99 {quantiles(gpu, n=100, method='inclusive')[98]:.2f} · "
              f"max {gpu[-1]:.2f} ms · >{FRAME_MS:.1f} ms {sum(v > FRAME_MS for v in gpu)} of {len(gpu):,}"
              + (f" · event frames +0..3: median {median(ev):.2f}, max {max(ev):.2f} ms (n={len(ev)})" if ev else ""))
        print(f"  pipelines compiled, warmup: {dict(zip(PIPE_KINDS, warm))} · after: {dict(zip(PIPE_KINDS, late))}")
        for run, s, fr in items:
            if s["frame"] > WARMUP and s["tick"] < s["_last"] and (float(s["wall_ms"]) > MISS_MS or any(s["pipes"])):
                since = min((s["frame"] - f for f in fr if f <= s["frame"]), default=None)
                print(f"  r{run} frame {s['frame']} tick {s['tick']}: wall {float(s['wall_ms']):.2f} · process {float(s['process_ms']):.2f} · "
                      f"render CPU {float(s['render_cpu_ms']):.2f} · GPU {float(s['gpu_ms']):.2f} ms · pipes {s['pipes']} · "
                      f"frames since an event {since}")


def hitch_detail(name: str, on: Side | None, off: Side | None) -> None:
    """Diagnostics beside the verdict: frames over HITCH_MS per run, ON-OFF pairs, and where they fall."""
    if on is None or off is None:
        return
    print(f"\n{name}: frames over {HITCH_MS:.1f} ms (diag)")
    for label, s in (("ON", on), ("OFF", off)):
        counts = [s.hitch_runs[r][0] for r in sorted(s.hitch_runs)]
        total = sum(counts)
        print(f"- {label}: {total} in {s.frames:,} frames ({total / s.frames * 1000:.2f}/1000) · per run {counts}")
    pairs = sorted(set(on.hitch_runs) & set(off.hitch_runs))
    diffs = [(on.hitch_runs[r][0] / on.hitch_runs[r][1] - off.hitch_runs[r][0] / off.hitch_runs[r][1]) * 1000 for r in pairs]
    if len(diffs) >= 2:
        sd = stdev(diffs)
        print(f"- ON-OFF per pair (/1000): mean {mean(diffs):+.2f} · SD {sd:.2f} · SE {sd / len(diffs) ** 0.5:.2f} · "
              f"pairs ON>OFF {sum(d > 0 for d in diffs)}, ON<OFF {sum(d < 0 for d in diffs)}, equal {sum(d == 0 for d in diffs)} (n={len(diffs)})")
    for label, s in (("ON", on), ("OFF", off)):
        for run, frame, tick, wall, cpu, near in sorted(s.hitches):
            cpu_text = "n/a" if cpu is None else f"{cpu:.2f}"
            near_text = "no events" if near is None else f"{near} ticks"
            print(f"  {label} r{run} frame {frame} tick {tick}: {wall:.2f} ms · game CPU {cpu_text} ms · nearest event {near_text}")
    for label, s in (("ON", on), ("OFF", off)):
        if not s.has_events:
            print(f"- {label}: runs record no events; nearness not measured")
            continue
        for window in NEAR_TICKS:
            near = sum(h[5] is not None and h[5] <= window for h in s.hitches)
            print(f"- {label}: hitches within {window} ticks of an event {near}/{len(s.hitches)} · "
                  f"all frames within {window} ticks {s.near_event.get(window, 0) / s.frames * 100:.1f}%")


# ---- overdraw -------------------------------------------------------------------------------

def overdraw_layers(png: Path) -> NDArray[np.float64]:
    """Layers drawn per pixel in Godot's overdraw view, from the red channel. Each layer adds
    0.04 red (linear) before a Filmic tonemap (white 1, exposure 1) and sRGB (red 102 = 2 layers).
    If your environment uses another tonemapper, replace filmic() with it."""
    a = 0.22 * 4, 0.6, 0.1, 0.2, 0.01, 0.3

    def filmic(x: NDArray[np.float64]) -> NDArray[np.float64]:
        A, B, C, D, E, F = a
        f = lambda v: ((v * (A * v + C * B) + D * E) / (v * (A * v + B) + D * F)) - E / F  # noqa: E731
        return f(x) / f(np.float64(1.0))

    n = np.linspace(0.0, 80.0, 8001)
    lin = np.clip(filmic(n * 0.04), 0.0, 1.0)
    srgb = np.where(lin < 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055) * 255.0
    red = np.asarray(Image.open(png).convert("RGB"), dtype=np.float64)[..., 0]
    return np.interp(red, srgb, n)


def overdraw_cmd(a: argparse.Namespace) -> None:
    """Effects' own overdraw: the same frames shot with effects on and off, layer counts subtracted pixel by pixel. Godot's overdraw view ignores custom shaders, so a
    quad counts whole even where its shader discards: that is the fill the GPU pays for."""
    rows = []
    for on_png in sorted(a.on.glob("*.png")):
        off_png = a.off / on_png.name
        if not off_png.exists():
            continue
        on, off = overdraw_layers(on_png), overdraw_layers(off_png)
        fx = np.clip(on - off, 0.0, None)
        # Opening (3x3 min then max) drops the 1-2 px edge lines a shaken camera leaves on every mesh.
        mask = Image.fromarray(((fx > 0.75) * 255).astype(np.uint8))
        hit = np.asarray(mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))) > 0
        fx = np.where(hit, fx, 0.0)
        rows.append((on_png.stem, hit.mean() * 100, fx.mean(), float(np.percentile(fx[hit], 99)) if hit.any() else 0.0,
                     float(fx.max()), on.mean()))
    print("| Shot | FX area % | FX layers, screen mean | FX layers p99 where drawn | FX max | All layers, screen mean |")
    print("| --- | ---: | ---: | ---: | ---: | ---: |")
    for r in rows:
        print(f"| {r[0]} | {r[1]:.2f} | {r[2]:.3f} | {r[3]:.1f} | {r[4]:.1f} | {r[5]:.2f} |")
    if rows:
        col = list(zip(*rows))
        print(f"\nshots {len(rows)} · FX area peak {max(col[1]):.2f}% mean {mean(col[1]):.2f}% · FX screen-mean layers peak "
              f"{max(col[2]):.3f} mean {mean(col[2]):.3f} · FX max layers {max(col[4]):.1f} · all layers mean {mean(col[5]):.2f}")


# ---- cli ------------------------------------------------------------------------------------

def main() -> None:
    global GODOT, PROJECT, W, H, FONT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--godot", default=GODOT, help="Godot executable")
    ap.add_argument("--project", default=PROJECT, help="Godot project folder (has project.godot)")
    ap.add_argument("--size", default=f"{W}x{H}", help="capture size WxH")
    ap.add_argument("--font", help="TrueType font for key-frame captions")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("scene")
    r.add_argument("out", type=Path)
    r.add_argument("--frames", type=int, default=600)
    r.add_argument("--pack", type=Path, help="run an exported .pck instead of the game folder")
    m = sub.add_parser("media")
    m.add_argument("clip", type=Path)
    m.add_argument("--crop", type=box, required=True)
    m.add_argument("--out", type=Path, required=True)
    m.add_argument("--name", required=True)
    m.add_argument("--probe", type=box, help="small box on the contact; finds the contact frame")
    m.add_argument("--near", type=int, help="search the contact within 8 frames of this movie frame")
    m.add_argument("--keys", default="0,1,2,4,7,10", help="key frames, counted from the contact")
    m.add_argument("--key-box", type=box, help="crop for key frames (default: --crop)")
    m.add_argument("--gray-clip", type=Path, help="a take recorded in the scene's own gray mode")
    m.add_argument("--label", default="contact", help="caption prefix on key frames")
    m.add_argument("--audio", action="store_true", help="keep the sound in the colour video")
    m.add_argument("--dark", action="store_true", help="the contact darkens the probe (find the largest fall)")
    m.add_argument("--contact", type=int, help="the contact's movie frame, already found (an ON/OFF diff); skips the search")
    c = sub.add_parser("cues")
    c.add_argument("clip", type=Path)
    c.add_argument("--cues", type=Path, required=True)
    d = sub.add_parser("same")
    d.add_argument("a", type=Path)
    d.add_argument("b", type=Path)
    d.add_argument("--box", type=box, help="compare only this region (default: whole frame)")
    d.add_argument("--shift", type=int, default=10, help="frame offsets to try either way (takes start up to 6 frames apart)")
    e = sub.add_parser("effect")
    e.add_argument("on", type=Path)
    e.add_argument("off", type=Path)
    e.add_argument("--box", type=box, help="look only here (default: whole frame)")
    e.add_argument("--at", help="frames to report contrast for, comma-separated")
    s = sub.add_parser("measure")
    s.add_argument("clip", type=Path)
    s.add_argument("--box", type=box)
    p = sub.add_parser("perf")
    p.add_argument("scene")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--cond", action="append", required=True, help='NAME="scene args", repeatable')
    p.add_argument("--runs", type=int, default=5)
    p.add_argument("--off-arg", default="--off", help="scene arg that turns the effect off")
    p.add_argument("--order", choices=("swap", "on-off"), default="swap",
                   help="swap = ON first on odd runs, OFF first on even; on-off = ON, OFF, ON, OFF ...")
    p.add_argument("--pack", type=Path, help="run an exported .pck instead of the game folder")
    p.add_argument("--driver", help="rendering driver (vulkan: GPU times are measured; Metal reads 0 in Godot 4.7)")
    q = sub.add_parser("perf-report")
    q.add_argument("out", type=Path)
    o = sub.add_parser("overdraw")
    o.add_argument("on", type=Path, help="overdraw-view PNG shots, effects on")
    o.add_argument("off", type=Path, help="the same frames with effects hidden")
    argv = sys.argv[1:]
    scene_args: list[str] = []
    if "record" in argv and "--" in argv and argv.index("record") < argv.index("--"):
        cut = argv.index("--")
        argv, scene_args = argv[:cut], argv[cut + 1:]
    a = ap.parse_args(argv)
    GODOT, PROJECT, FONT = a.godot, a.project, a.font
    W, H = (int(v) for v in a.size.lower().split("x"))
    if a.cmd == "record":
        record(a.scene, a.out, a.frames, scene_args, a.pack)
    elif a.cmd == "media":
        media(a)
    elif a.cmd == "measure":
        measure_cmd(a)
    elif a.cmd == "perf":
        perf(a)
    elif a.cmd == "cues":
        cues_cmd(a)
    elif a.cmd == "same":
        same_cmd(a)
    elif a.cmd == "effect":
        effect_cmd(a)
    elif a.cmd == "overdraw":
        overdraw_cmd(a)
    else:
        perf_report(a.out)


if __name__ == "__main__":
    main()
