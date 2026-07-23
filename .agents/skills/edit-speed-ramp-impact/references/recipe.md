# Speed Ramp Impact Recipe

## Effect Anatomy

- Intent: compress raw action or product footage into a high-energy promo by alternating brief slow hero moments with fast transition bursts.
- Good inputs: cars, devices, sports, launch demos, fashion details, app UI captures with strong gestures, or any footage with obvious hero frames.
- Weak inputs: static talking-head footage, low-light clips with no highlight detail, or source with heavy built-in transitions that cannot be trimmed around.

## Plan Shape

Use a compact EDL:

```yaml
timeline:
  fps: 30
  aspect: 9:16
  clips:
    - source: input.mp4
      source_in: 0.20
      source_out: 1.75
      speed: 0.82
      role: hero-open
    - source: input.mp4
      source_in: 1.80
      source_out: 3.20
      speed: 1.90
      role: whip-transition
effects:
  grade: contrast-medium, saturation-plus, readable-shadows
  impacts:
    - flash at cut boundaries for 2-4 frames
    - crop punch-ins on detail clips
audio:
  loudness: -16 LUFS integrated, -1.5 dB true peak
qa:
  sample: open, every cut, ending
```

## Timing Heuristics

- Slow hero: `0.75x-0.95x`, 1.4-3.5s on timeline.
- Fast whip: `1.6x-2.4x`, 0.4-0.9s on timeline.
- Detail hold: `0.85x-1.05x`, 1.0-2.5s.
- Final hold: 2.0-4.0s, usually slower than real time.
- Flash: 0.06-0.12s. Use fewer flashes than cuts.

## FFmpeg Constraints

- Force constant frame rate, matching dimensions, `setsar=1`, and `format=yuv420p` before final encode.
- For concat, every video segment must have the same resolution, pixel format, frame rate, time base, and sample aspect ratio.
- Rebuild audio timestamps after speed changes with `aresample=async=1:first_pts=0,asetpts=N/SR/TB`.
- If `drawtext` is unavailable, use simple bars in FFmpeg or switch typography to Remotion, HyperFrames, or image overlays.

## Reusable Renderer

Use this command for arbitrary raw car clips:

```bash
scripts/render-speed-ramp-impact.py input-car-video.mp4 output-car-edit.mp4
```

The script:

- probes the input duration and audio presence;
- builds a seven-part fast-slow-fast EDL from proportional source windows;
- samples nearby candidate frames for brightness so it avoids black/source-transition moments;
- keeps source ranges mostly chronological;
- renders vertical 720x1280 H.264/AAC with impact flashes, punch-in crops, grade, sharpening, and loudness normalization.

Use `--target-duration 15` to ask for a longer reel. Use `--print-plan` when debugging the generated EDL.

## Local Fixture

The first validated reusable fixture is `/Users/bedir/Downloads/download.mp4`, rendered by `scripts/render-speed-ramp-impact.py` into `/Users/bedir/Documents/Codex/2026-07-23/can/outputs/car-edit-reusable.mp4`.

The hand-tuned fixture remains `scripts/render-car-edit.sh`, which renders `/Users/bedir/Documents/Codex/2026-07-23/can/outputs/car-edit.mp4`.

Observed source issue: the raw car footage contains a built-in vertical strip transition around 13.2s. Trim around it unless the user explicitly wants that glitch-like moment.

## Source Pointers

- FFmpeg filter docs: https://ffmpeg.org/ffmpeg-filters.html
- FFmpeg xfade notes: https://trac.ffmpeg.org/wiki/Xfade
- CapCut speed-ramp car-edit framing: https://www.capcut.com/explore/speed-ramp-car-edit
- Project brief reference: viral car speed-ramp edits and rainy gas-station car footage.
