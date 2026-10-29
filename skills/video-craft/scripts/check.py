#!/usr/bin/env python3
"""Check a finished video against a channel profile, and optionally fix its loudness.

    python3 check.py final.mp4 --channel short            # spec + loudness report, exit 1 on any FAIL
    python3 check.py final.mp4 --channel x --sheet hook.png  # also save frames at 0 / 1 / 3 s for the hook check
    python3 check.py cut.mp4 --fix-audio cut_lufs.mp4       # two-pass loudnorm to -14 LUFS / -1 dBTP, video copied

Channels: x, reddit, short (YouTube Shorts / TikTok / Reels), youtube (long-form), steam.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

# min/max seconds, max bytes, allowed aspect ratios (w/h) with 2% tolerance, min height.
PROFILES = {
    "x":       {"dur": (0.5, 140), "bytes": 512 << 20, "aspects": [16/9, 1, 4/5, 9/16], "min_h": 720},
    "reddit":  {"dur": (1, 900),   "bytes": 1 << 30,   "aspects": [16/9, 1, 4/5, 9/16], "min_h": 720},
    "short":   {"dur": (1, 180),   "bytes": 4 << 30,   "aspects": [9/16, 1],            "min_h": 1080},
    "youtube": {"dur": (1, 43200), "bytes": 256 << 30, "aspects": [16/9],               "min_h": 1080},
    "steam":   {"dur": (1, 600),   "bytes": 4 << 30,   "aspects": [16/9],               "min_h": 1080,
                "min_kbps": 5000},
}
LUFS_TOL, TRUE_PEAK = 1.5, -1.0


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)


def probe(path: Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    return json.loads(out.stdout)


def moov_first(path: Path) -> bool:
    with path.open("rb") as f:
        while head := f.read(8):
            size, kind = struct.unpack(">I4s", head)
            if kind == b"moov":
                return True
            if kind == b"mdat":
                return False
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0] - 8
            f.seek(size - 8, 1)
    return False


def loudness(path: Path) -> tuple[float, float] | None:
    err = run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    return (float(i[-1]), float(tp[-1])) if i and tp else None


def fix_audio(src: Path, dst: Path, lufs: float) -> None:
    target = f"I={lufs}:TP={TRUE_PEAK - 0.5}:LRA=11"
    err = run(["ffmpeg", "-nostats", "-i", str(src), "-af", f"loudnorm={target}:print_format=json",
               "-f", "null", "-"]).stderr
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    measured = (f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
                f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-c:v", "copy",
                    "-af", f"loudnorm={target}:{measured},aresample=48000", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(dst)], check=True)
    print(f"OK {dst}")


def sheet(src: Path, dst: Path) -> None:
    frames = []
    for t in (0, 1, 3):
        frame = dst.with_name(f"{dst.stem}_{t}s.png")
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1",
             "-vf", "scale=-2:540", str(frame)])
        if frame.exists():
            frames.append(frame)
    inputs = sum((["-i", str(f)] for f in frames), [])
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", f"hstack=inputs={len(frames)}", str(dst)])
    for f in frames:
        f.unlink()
    print(f"SHEET {dst} (0 s · 1 s · 3 s)")


def check(path: Path, channel: str, lufs: float) -> bool:
    p, info = PROFILES[channel], probe(path)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    w, h = int(v["width"]), int(v["height"])
    dur, size = float(info["format"]["duration"]), int(info["format"]["size"])
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    fps = num / den
    rows = [
        ("container mp4", "mp4" in info["format"]["format_name"], info["format"]["format_name"]),
        ("video h264", v["codec_name"] == "h264", v["codec_name"]),
        ("yuv420p", v.get("pix_fmt") == "yuv420p", v.get("pix_fmt")),
        ("tv range", v.get("color_range", "tv") == "tv", v.get("color_range", "unset")),
        ("fps 24-60", 23.9 <= fps <= 60.01, f"{fps:.2f}"),
        ("aspect", any(abs(w / h - r) / r < 0.02 for r in p["aspects"]), f"{w}x{h}"),
        ("short side", min(w, h) >= p["min_h"], f"{min(w, h)} (min {p['min_h']})"),
        ("duration", p["dur"][0] <= dur <= p["dur"][1], f"{dur:.1f}s (max {p['dur'][1]})"),
        ("size", size <= p["bytes"], f"{size / 1e6:.1f} MB"),
        ("faststart", moov_first(path), "moov before mdat"),
    ]
    if "min_kbps" in p:
        kbps = int(info["format"]["bit_rate"]) / 1000
        rows.append(("bitrate", kbps >= p["min_kbps"], f"{kbps:.0f} kbps (min {p['min_kbps']})"))
    if a:
        rows.append(("audio aac", a["codec_name"] == "aac", a["codec_name"]))
        lt = loudness(path)
        if lt:
            i, tp = lt
            rows.append(("loudness", abs(i - lufs) <= LUFS_TOL, f"{i:.1f} LUFS (target {lufs})"))
            rows.append(("true peak", tp <= TRUE_PEAK, f"{tp:.1f} dBTP (max {TRUE_PEAK})"))
    ok = all(r[1] for r in rows)
    for name, good, got in rows:
        print(f"{'PASS' if good else 'FAIL'}  {name:14} {got}")
    if not a:
        print("WARN  audio          none (fine muted on X/Reddit; Shorts and trailers want sound)")
    print(f"{'ALL PASS' if ok else 'FAILED'}  {path.name} for {channel}")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--channel", choices=sorted(PROFILES))
    ap.add_argument("--sheet", type=Path)
    ap.add_argument("--fix-audio", type=Path)
    ap.add_argument("--lufs", type=float, default=-14.0, help="-14 social and Steam; festivals often -23")
    args = ap.parse_args()
    if args.fix_audio:
        fix_audio(args.video, args.fix_audio, args.lufs)
    if args.sheet:
        sheet(args.video, args.sheet)
    if args.channel and not check(args.fix_audio or args.video, args.channel, args.lufs):
        sys.exit(1)


if __name__ == "__main__":
    main()
