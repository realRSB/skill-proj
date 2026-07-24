# Car Template Sequence Recipe

## Template Timing Map

Source template: `/Users/bedir/Documents/Codex/2026-07-23/can/outputs/car-edit.mp4`.

The template is treated as 13 seconds. Scale these positions to the uploaded raw clip duration:

- Flicker: `3 / 13 = 23.08%`
- Whoosh: `5 / 13 = 38.46%`
- Slashing fade: `7 / 13 = 53.85%`
- Hard cut: `10 / 13 = 76.92%`
- Fade out: final `7-10%` of the output

## User Choices Baked In

- Input: one raw video clip.
- Source usage: beginning to end, in order.
- Output: vertical 9:16, 720x1280, 30fps.
- Audio: removed.
- Matching goal: same effect order and pacing, with timings scaled by percentage.

## Renderer

Use:

```bash
scripts/render-car-template-sequence.py raw-car.mp4 edited-car.mp4 --print-plan
```

The script:

- probes the input duration and dimensions;
- creates a vertical crop, including horizontal-to-vertical reframing;
- applies the flicker near 23%;
- applies a blurred visual whoosh near 38%;
- applies a diagonal `xfade` slash around 54%;
- applies a hard flash cut around 77%;
- fades out at the end;
- drops all audio with `-an`.

## QA

Sample frames at the scaled effect times from the printed plan:

- `flicker`
- `whoosh`
- `slash`
- `cut`
- `fade_start`

Confirm there is no audio:

```bash
ffprobe -hide_banner -v error -select_streams a -show_entries stream=index -of csv=p=0 output.mp4
```

The command should print nothing.
