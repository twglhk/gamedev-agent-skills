#!/usr/bin/env python3
"""Measure one FX clip (Godot Movie Maker .avi) or one sound file against fx-craft's rubric.

  measure.py clip.avi [--box x,y,w,h] [--fps 60]   picture + sound of one moment
  measure.py --wav sound.wav                        one sound file
  measure.py --profile a.ogg b.wav ...              shape of short sounds side by side: length, hits,
                                                    bands, brightness path, flatness, width, loudness

Clip mode expects the preview scene to start with the effect not yet visible: frame 0 is the
background the effect must stand out from. Writes <clip>-gray.png (grayscale contact sheet).
Needs ffmpeg, numpy, Pillow.
"""
import argparse
import math
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image

CONTRAST_MIN = 3.0   # WCAG 2.1 SC 1.4.11 non-text contrast, borrowed
BUMP_TOL = 0.05      # after the peak, brightness may rise at most 5% of the peak
SYNC_MS = 17.0       # one frame at 60 fps
TRUE_PEAK_MAX = -1.0 # dBTP, Sony ASWG-R001
ONSET_DB = -40.0     # first sample louder than this counts as the onset


def ffmpeg(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-y", *args], capture_output=True, text=True)


def luminance(rgb):
    c = rgb.astype(np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722


def loudness(path):
    err = ffmpeg("-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summary = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summary)
    p = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
    return (float(i.group(1)) if i else math.nan, float(p.group(1)) if p else math.nan)


LAPTOP = "highpass=f=250,highpass=f=250"  # rough small-speaker cut: little below 250 Hz survives


def momentary_max(path, pre=""):
    """Loudest 400 ms window (EBU momentary), padded so a sound shorter than the window still counts."""
    err = ffmpeg("-nostats", "-i", str(path), "-af", f"{pre + ',' if pre else ''}apad=pad_dur=0.5,ebur128",
                 "-f", "null", "-").stderr
    m = [float(v) for v in re.findall(r"\sM:\s*(-?[\d.]+)", err)]
    return max(m) if m else math.nan


def onset_ms(path):
    with wave.open(str(path)) as w:
        rate, ch, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if width != 2:
        sys.exit(f"{path}: need 16-bit PCM (convert: ffmpeg -i in -c:a pcm_s16le out.wav)")
    x = np.frombuffer(raw, dtype=np.int16).reshape(-1, ch).astype(np.float64) / 32768.0
    loud = np.nonzero(np.abs(x).max(axis=1) > 10 ** (ONSET_DB / 20))[0]
    return (loud[0] * 1000.0 / rate) if loud.size else math.nan


def verdict(ok):
    return "PASS" if ok else "FAIL"


def measure_wav(path):
    lufs, tp = loudness(path)
    on = onset_ms(path)
    print(f"onset      {on:7.1f} ms   (head of silence before the first peak; aim < 10 ms)")
    print(f"true peak  {tp:7.1f} dBTP {verdict(tp <= TRUE_PEAK_MAX)} (<= {TRUE_PEAK_MAX})")
    print(f"loudness   {lufs:7.1f} LUFS (integrated; judge -24 +-2 only on a long gameplay recording)")
    full, small = momentary_max(path), momentary_max(path, LAPTOP)
    print(f"momentary  {full:7.1f} LUFS (loudest 400 ms; compares short sounds by strength)")
    print(f"laptop     {small:7.1f} LUFS ({small - full:+.1f} dB with everything under 250 Hz cut; "
          "far below 0 = the thud vanishes on small speakers)")


PROFILE_RATE = 48000
BANDS = ((0, 250), (250, 2000), (2000, 6000), (6000, 24000))


def decode(path):
    """Any audio file as 48 kHz stereo float (ffmpeg), for profiles of reference files and takes."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2",
                          "-ar", str(PROFILE_RATE), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<f4").astype(np.float64).reshape(-1, 2)


def profile(path):
    """Shape numbers of one short sound, to set a take beside reference sounds of the same kind
    (rubric "Side by side with references: sound"). Diagnostics only: they say how a sound is built, not how good it is."""
    x = decode(path)
    m = x.mean(axis=1)
    hop = PROFILE_RATE // 1000
    n = len(m) // hop
    env = 20 * np.log10(np.abs(m[: n * hop]).reshape(n, hop).max(axis=1) + 1e-9)
    top = env.max()
    loud = np.nonzero(env > top - 40)[0]
    on, end = int(loud[0]), int(loud[-1])
    peak = int(np.argmax(env)) - on
    # Hits: the 5 ms envelope jumps 9 dB or more within 20 ms, at least 40 ms after the last one.
    e5 = np.convolve(10 ** (env / 20), np.ones(5) / 5, mode="same")
    e5 = 20 * np.log10(e5 + 1e-9)
    hits, last = [], -999
    for i in range(on, end):
        if i - last >= 40 and e5[i] > top - 30 and e5[i] - e5[max(i - 20, 0)] >= 9:
            hits.append(i - on)
            last = i
    seg = m[on * hop:(end + 1) * hop]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    freqs = np.fft.rfftfreq(len(seg), 1 / PROFILE_RATE)
    bands = [spec[(freqs >= lo) & (freqs < hi)].sum() / spec.sum() * 100 for lo, hi in BANDS]
    # Brightness path: spectral centroid of the first and last third of the sound (rises = gets brighter).
    def centroid(y):
        s = np.abs(np.fft.rfft(y * np.hanning(len(y)))) ** 2
        f = np.fft.rfftfreq(len(y), 1 / PROFILE_RATE)
        return float((s * f).sum() / s.sum())
    third = max(len(seg) // 3, 256)
    c0, c1 = centroid(seg[:third]), centroid(seg[-third:])
    # Tonality: in 40 ms frames within 30 dB of the top, the strongest bin over the median bin of
    # 100 Hz-12 kHz (lossy files are empty above), median over frames in dB. Rough calibration: sines and
    # held chimes 80+, struck hits and stings 35-75, noise bursts 20-35. `note` = strongest bin of the loudest frame.
    fr = 1920
    ff = np.fft.rfftfreq(fr, 1 / PROFILE_RATE)
    keep = (ff >= 100) & (ff <= 12000)
    flat, loudest, note = [], -1.0, math.nan
    for i in range(0, len(seg) - fr, fr // 2):
        lvl = np.abs(seg[i:i + fr]).max()
        if 20 * np.log10(lvl + 1e-9) < top - 30:
            continue
        s = np.abs(np.fft.rfft(seg[i:i + fr] * np.hanning(fr)))[keep] ** 2 + 1e-12
        flat.append(10 * np.log10(s.max() / np.median(s)))
        if lvl > loudest:
            loudest, note = lvl, float(ff[keep][np.argmax(s)])
    side = x[on * hop:(end + 1) * hop]
    width = float(np.sqrt(((side[:, 0] - side[:, 1]) ** 2).mean() / (((side[:, 0] + side[:, 1]) ** 2).mean() + 1e-12)))
    return dict(name=Path(path).stem, len_ms=end - on, onset_ms=on, peak_ms=peak, hits=hits,
                bands=bands, bright=(c0, c1), tonal=float(np.median(flat)) if flat else math.nan, note=note,
                width=width, mom=momentary_max(path))


def print_profiles(paths):
    print(f"{'sound':26s} {'len':>6s} {'onset':>5s} {'peak':>5s} {'hits (ms from onset)':22s} "
          f"{'<250 250-2k 2-6k >6k %':>23s} {'bright start>end Hz':>19s} {'tonal':>5s} {'note':>6s} {'width':>5s} {'M LUFS':>6s}")
    for p in paths:
        r = profile(p)
        hits = ",".join(str(h) for h in r["hits"][:5]) + ("…" if len(r["hits"]) > 5 else "")
        b = " ".join(f"{v:4.0f}" for v in r["bands"])
        print(f"{r['name'][:26]:26s} {r['len_ms']:6d} {r['onset_ms']:5d} {r['peak_ms']:5d} {hits:22s} "
              f"{b:>23s} {r['bright'][0]:8.0f}>{r['bright'][1]:<8.0f} {r['tonal']:5.0f} {r['note']:6.0f} {r['width']:5.2f} {r['mom']:6.1f}")


def measure_clip(path, box, fps):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        ffmpeg("-i", str(path), "-vf", f"fps={fps}", str(tmp / "f_%05d.png"))
        frames = sorted(tmp.glob("f_*.png"))
        if not frames:
            sys.exit(f"{path}: no frames")
        lum = [luminance(np.asarray(Image.open(f).convert("RGB"))) for f in frames]
        has_audio = ffmpeg("-i", str(path), "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le",
                           str(tmp / "a.wav")).returncode == 0
        audio_on = onset_ms(tmp / "a.wav") if has_audio else math.nan
        lufs, tp = loudness(tmp / "a.wav") if has_audio else (math.nan, math.nan)

    step = max(1, math.ceil(len(frames) / 40))
    sheet = Path(path).with_name(Path(path).stem + "-gray.png")
    ffmpeg("-i", str(path), "-vf", f"hue=s=0,select='not(mod(n\\,{step}))',scale=320:-1,tile=8x5",
           "-frames:v", "1", "-fps_mode", "vfr", str(sheet))

    h, w = lum[0].shape
    x, y, bw, bh = box or (0, 0, w, h)
    region = [l[y:y + bh, x:x + bw] for l in lum]
    # Intensity = the brightest 2% of the area, so a ring that grows while it fades reads as fading.
    core = np.array([np.percentile(r, 98) for r in region])
    impact = int(np.argmax(np.diff(core))) + 1 if len(core) > 1 else 0
    peak = int(np.argmax(core))
    bg = np.median(region[0])
    contrast = (core[peak] + 0.05) / (bg + 0.05)
    after = core[peak:]
    floor = np.minimum.accumulate(after)
    bumps = [peak + int(i) for i in np.nonzero(after - floor > BUMP_TOL * core[peak])[0]]
    sync = audio_on - impact * 1000.0 / fps

    print(f"frames     {len(frames)} @ {fps} fps   gray sheet -> {sheet}")
    print(f"impact     frame {impact} (largest jump of the brightest 2%)   peak frame {peak}")
    print(f"contrast   {contrast:7.2f} : 1  {verdict(contrast >= CONTRAST_MIN)} (>= {CONTRAST_MIN})")
    print(f"decay      {verdict(not bumps)} brightness only falls after the peak"
          + (f" - rises again at frames {bumps[:8]}" if bumps else ""))
    if has_audio:
        print(f"sync       {sync:+7.1f} ms {verdict(abs(sync) <= SYNC_MS)} (sound onset vs impact, |x| <= {SYNC_MS})")
        print(f"true peak  {tp:7.1f} dBTP {verdict(tp <= TRUE_PEAK_MAX)}")
        print(f"loudness   {lufs:7.1f} LUFS (report only)")
    else:
        print("sync       no audio track in the clip")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?")
    ap.add_argument("--wav")
    ap.add_argument("--box", help="x,y,w,h of the effect area in pixels (default: whole frame)")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--profile", nargs="+", metavar="FILE")
    a = ap.parse_args()
    if a.profile:
        print_profiles(a.profile)
    elif a.wav:
        measure_wav(a.wav)
    elif a.clip:
        measure_clip(a.clip, tuple(int(v) for v in a.box.split(",")) if a.box else None, a.fps)
    else:
        ap.error("give a clip or --wav")


if __name__ == "__main__":
    main()
