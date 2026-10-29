#!/usr/bin/env python3
"""Burn timed captions into a video without drawtext/libass.

Each cue is rendered from HTML to a transparent PNG the size of the video (Playwright),
then laid on with ffmpeg `overlay` between its start and end. The HTML of every cue is
kept beside the PNGs so a caption can be fixed and rebuilt.

    python3 captions.py spec.json

spec.json:
    {
      "in": "cut_9x16.mp4",            # paths relative to the spec file
      "out": "final.mp4",
      "look": "plain",                 # plain | band | panel
      "colors": {"accent": "#ffd23f"}, # optional: text, accent, bg, edge (see LOOK_COLORS)
      "font": "Inter, sans-serif",     # optional CSS font stack
      "frame": "auto",                 # auto | short (9:16 UI safe zone) | feed
      "cues": [
        {"t": [0.0, 1.8], "text": "One card.", "at": "top", "size": "l"},
        {"t": [1.8, 4.0], "text": "<em>Three</em> units move.", "at": "bottom"}
      ]
    }

`text` may hold <em> (accent colour) and <br>. `at` = top | middle | bottom, `size` = l | m | s.
Optional `top` (fraction of height) replaces the safe-zone top margin, e.g. to clear a game HUD.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

# Safe zones as fractions of width/height. "short" = the box x 90-900, y 250-1380 on
# 1080x1920, clear of the Shorts/TikTok/Reels overlays (no platform publishes official numbers;
# see video-craft references/channels.md).
SAFE = {
    "short": {"top": 250 / 1920, "bottom": 540 / 1920, "left": 90 / 1080, "right": 180 / 1080},
    "feed": {"top": 0.06, "bottom": 0.08, "left": 0.06, "right": 0.06},
}
SIZE = {"l": 0.074, "m": 0.058, "s": 0.044}  # font px as a fraction of min(w, h)
FONT = '"Hiragino Sans", "Apple SD Gothic Neo", "Helvetica Neue", "Noto Sans CJK JP", sans-serif'
SERIF = '"Hiragino Mincho ProN", "AppleMyungjo", "Didot", "Noto Serif CJK JP", serif'

# Default colours per look. Override any key with "colors" in the spec to match your brand.
LOOK_COLORS = {
    "plain": {"text": "#ffffff", "accent": "#ffd23f", "edge": "#000000", "bg": "transparent"},
    "band": {"text": "#f4f1ea", "accent": "#ff5a4a", "edge": "#c62828", "bg": "#111111"},
    "panel": {"text": "#efe9dc", "accent": "#e7b866", "edge": "#b8955a", "bg": "rgba(12, 18, 24, .82)"},
}

LOOK_CSS = {
    "plain": """
      .c { font-family: var(--font); font-weight: 800; color: var(--text);
           -webkit-text-stroke: calc(var(--fs) * 0.09) var(--edge); paint-order: stroke fill;
           text-shadow: 0 calc(var(--fs) * 0.06) calc(var(--fs) * 0.12) rgba(0,0,0,.55); }
      .c em { font-style: normal; color: var(--accent); }""",
    "band": """
      .c { font-family: var(--font); font-weight: 900; color: var(--text); background: var(--bg);
           padding: calc(var(--fs) * 0.22) calc(var(--fs) * 0.5);
           box-shadow: calc(var(--fs) * 0.12) calc(var(--fs) * 0.12) 0 var(--edge); }
      .c em { font-style: normal; color: var(--accent); }""",
    "panel": """
      .c { font-family: var(--serif); font-weight: 600; color: var(--text); letter-spacing: .02em;
           background: var(--bg); border: 2px solid var(--edge);
           padding: calc(var(--fs) * 0.25) calc(var(--fs) * 0.6); }
      .c em { font-style: normal; color: var(--accent); }""",
}

JUSTIFY = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}


def probe(path: Path) -> tuple[int, int, bool]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    streams = json.loads(out)["streams"]
    video = next(s for s in streams if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in streams)
    return int(video["width"]), int(video["height"]), has_audio


def cue_html(cue: dict, w: int, h: int, look: str, safe: dict, colors: dict, font: str) -> str:
    fs = round(min(w, h) * SIZE[cue.get("size", "m")])
    css_vars = "; ".join(f"--{k}: {v}" for k, v in colors.items())
    at = cue.get("at", "bottom")
    pad = (f"{round(h * cue.get('top', safe['top']))}px {round(w * safe['right'])}px "
           f"{round(h * safe['bottom'])}px {round(w * safe['left'])}px")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
      html, body {{ margin: 0; width: {w}px; height: {h}px; background: transparent; }}
      .z {{ box-sizing: border-box; width: {w}px; height: {h}px; padding: {pad};
            display: flex; flex-direction: column; align-items: center; justify-content: {JUSTIFY[at]}; }}
      :root {{ --font: {font}; --serif: {SERIF}; {css_vars}; }}
      .c {{ --fs: {fs}px; font-size: {fs}px; line-height: 1.22; text-align: center; max-width: 100%; }}
      {LOOK_CSS[look]}
    </style></head><body><div class="z"><div class="c">{cue['text']}</div></div></body></html>"""


def main() -> None:
    spec_path = Path(sys.argv[1]).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec_path.parent
    src, dst = base / spec["in"], base / spec["out"]
    w, h, has_audio = probe(src)
    frame = spec.get("frame", "auto")
    if frame == "auto":
        frame = "short" if h / w > 1.5 else "feed"
    safe, look = SAFE[frame], spec.get("look", "plain")
    colors = {**LOOK_COLORS[look], **spec.get("colors", {})}
    font = spec.get("font", FONT)
    work = dst.with_name(dst.stem + "_caps")
    work.mkdir(parents=True, exist_ok=True)

    pngs = []
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except PlaywrightError:  # bundled browser missing or a version mismatch: use installed Chrome
            browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": w, "height": h})
        for i, cue in enumerate(spec["cues"], 1):
            html = cue_html(cue, w, h, look, safe, colors, font)
            (work / f"{i:02d}.html").write_text(html, encoding="utf-8")
            page.set_content(html)
            page.evaluate("document.fonts.ready")
            png = work / f"{i:02d}.png"
            page.screenshot(path=str(png), omit_background=True)
            pngs.append(png)
        browser.close()

    args = ["ffmpeg", "-y", "-v", "error", "-i", str(src)]
    for png in pngs:
        args += ["-i", str(png)]
    chain, last = [], "0:v"
    for i, cue in enumerate(spec["cues"], 1):
        a, b = cue["t"]
        chain.append(f"[{last}][{i}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i}]")
        last = f"v{i}"
    chain.append(f"[{last}]scale=out_range=tv,format=yuv420p[out]")
    args += ["-filter_complex", ";".join(chain), "-map", "[out]"]
    if has_audio:
        args += ["-map", "0:a", "-c:a", "copy"]
    args += ["-c:v", "libx264", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", str(dst)]
    subprocess.run(args, check=True)
    print(f"OK {dst} ({len(pngs)} cues, look={look}, frame={frame}, {w}x{h})")


if __name__ == "__main__":
    main()
