#!/usr/bin/env python3
"""Render an HTML/CSS motion graphic frame by frame, frame-exact, with headless Chrome.

Every CSS animation and transition (and any Web Animation) in the page is paused and seeked to
frame / fps, then the frame is screenshotted. Same input = same frames, so a cut rebuilds
from the repo. If the page defines `window.mgSeek(seconds)` (GSAP: `gsap.globalTimeline.seek`),
that is called instead of the built-in seek.

    python3 render.py page.html --size 1080x1920 --dur 2.4 --out /tmp/seq            # opaque PNGs
    python3 render.py page.html --size 1080x1920 --dur 2.4 --out /tmp/seq --alpha    # transparent PNGs
    python3 render.py page.html --size 1080x1920 --still 1.2 --png /tmp/peek.png     # one frame
    python3 render.py page.html ... --vars '{"name": "IRON WARDEN"}'                  # -> window.MG

Then lay it on with ffmpeg: `-framerate 30 -i /tmp/seq/%04d.png` (alpha PNGs keep their alpha;
use `overlay`), or `--mov out.mov` to also write a ProRes 4444 file with alpha.

Page rules: size the body to --size, put every timing in CSS `animation` (delay + duration) or
Web Animations, no `setTimeout`/`requestAnimationFrame` clocks and no unseeded `Math.random()`.
`window.MG` holds --vars before any page script runs; paths in it are relative to the page.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

SEEK = """t => {
  if (window.mgSeek) return window.mgSeek(t);
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
}"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--size", required=True, help="WxH, e.g. 1080x1920")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--dur", type=float, help="seconds to render")
    ap.add_argument("--out", help="directory for 0000.png …")
    ap.add_argument("--alpha", action="store_true", help="transparent background")
    ap.add_argument("--mov", help="also write ProRes 4444 (alpha) here")
    ap.add_argument("--still", type=float, help="render one frame at this second")
    ap.add_argument("--png", help="path for --still")
    ap.add_argument("--vars", default="{}", help="JSON put on window.MG")
    a = ap.parse_args()
    w, h = (int(x) for x in a.size.lower().split("x"))
    page_path = Path(a.page).resolve()

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except PlaywrightError:  # bundled browser missing: use the installed Chrome
            browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        page.add_init_script(f"window.MG = {a.vars};")
        page.goto(page_path.as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(150)  # images decoded, styles resolved, animations created

        def shot(t: float, path: Path) -> None:
            page.evaluate(SEEK, t)
            page.screenshot(path=str(path), omit_background=a.alpha)

        if a.still is not None:
            shot(a.still, Path(a.png))
            print(f"OK {a.png} @ {a.still}s")
        else:
            out = Path(a.out)
            if out.exists():
                shutil.rmtree(out)
            out.mkdir(parents=True)
            n = round(a.dur * a.fps)
            for i in range(n):
                shot(i / a.fps, out / f"{i:04d}.png")
            print(f"OK {n} frames {w}x{h} @ {a.fps} fps -> {out}")
        browser.close()

    if a.mov and a.still is None:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(a.fps), "-i", f"{a.out}/%04d.png",
                        "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", a.mov], check=True)
        print(f"OK {a.mov}")


if __name__ == "__main__":
    main()
