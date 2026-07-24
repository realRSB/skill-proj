# Whoosh Motion Blur Recipe

## Template Position

- Template source: `car-edit.mp4`
- Template moment: about 5s
- Scaled position: `5 / 13 = 38.46%`

## Timing

- Window: `6-8%` of output duration.
- Clamp: `0.42-0.90s`.

## FFmpeg Pattern

Use blur during the whoosh:

```text
boxblur=lr=8:lp=1:cr=4:cp=1:enable='between(t,start,end)'
```

When safe crop margins exist, animate crop position through the same window. Keep expressions simple; FFmpeg escaping gets fragile inside crop expressions.

## Better Adapters

- Remotion/HyperFrames: use directional blur, streaks, and easing.
- FFmpeg-only: use `boxblur`, `gblur`, `tblend`, or a fast crop sweep.

## QA

- The whoosh should feel like a fast pass, not soft focus.
- Do not blur for so long that the viewer loses the car.
