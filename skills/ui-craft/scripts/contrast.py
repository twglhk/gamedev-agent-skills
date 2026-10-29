#!/usr/bin/env python3
"""WCAG 2.x contrast ratio for ui-craft R-2 (text >= 4.5:1, large >= 3:1) and R-3 (marks >= 3:1).

  contrast.py '#1c1a17' '#e9dcc0'                         two colours
  contrast.py shot.png --fg x,y,w,h --bg x,y,w,h           capture boxes

Box mode: fg = the darkest-or-lightest glyph/mark pixel in the fg box (whichever is farther in
luminance from the bg), bg = the median colour of the bg box. Measure on a 100 % capture.
Needs Pillow and numpy for box mode.
"""
import argparse
import sys


def channel(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (channel(float(v)) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hex_rgb(s):
    s = s.lstrip("#")
    if len(s) != 6:
        raise argparse.ArgumentTypeError(f"not a #rrggbb colour: {s}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def box(s):
    parts = [int(v) for v in s.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(f"box must be x,y,w,h: {s}")
    return parts


def from_capture(path, fg_box, bg_box):
    import numpy as np
    from PIL import Image

    img = np.asarray(Image.open(path).convert("RGB")).astype(np.float64)

    def crop(b):
        x, y, w, h = b
        region = img[y:y + h, x:x + w].reshape(-1, 3)
        if region.size == 0:
            sys.exit(f"empty box {b} in {path} ({img.shape[1]}x{img.shape[0]})")
        return region

    bg = np.median(crop(bg_box), axis=0)
    fg_px = crop(fg_box)
    lum = np.array([luminance(p) for p in fg_px])
    far = fg_px[int(np.argmax(np.abs(lum - luminance(bg))))]
    return tuple(int(round(v)) for v in far), tuple(int(round(v)) for v in bg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a", help="#rrggbb, or a capture path with --fg/--bg")
    ap.add_argument("b", nargs="?", type=hex_rgb, help="#rrggbb")
    ap.add_argument("--fg", type=box)
    ap.add_argument("--bg", type=box)
    args = ap.parse_args()

    if args.fg and args.bg:
        fg, bg = from_capture(args.a, args.fg, args.bg)
    elif args.b is not None:
        fg, bg = hex_rgb(args.a), args.b
    else:
        ap.error("give two colours, or a capture with --fg and --bg")

    r = ratio(fg, bg)
    verdicts = [("text 4.5:1", r >= 4.5), ("large text / mark 3:1", r >= 3.0)]
    print(f"fg #{fg[0]:02x}{fg[1]:02x}{fg[2]:02x}  bg #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}  "
          f"ratio {r:.2f}:1  " + "  ".join(f"{n} {'pass' if ok else 'FAIL'}" for n, ok in verdicts))


if __name__ == "__main__":
    main()
