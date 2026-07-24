# Slashing Diagonal Fade Recipe

## Template Position

- Template source: `download.mp4`
- Template moment: about 13.85s in the 18.1s reference
- Scaled position: `13.85 / 18.1 = 76.52%`

## Timing

- Window: `3-4.5%` of output duration.
- Clamp: `0.28-0.48s`.

## FFmpeg Pattern

Create overlapping sections:

```text
[0:v]trim=start=0:end=slash_end,setpts=PTS-STARTPTS[pre]
[0:v]trim=start=slash_start:end=duration,setpts=PTS-STARTPTS[post]
[pre][post]xfade=transition=diagbr:duration=slash_d:offset=slash_start[slashed]
```

Use `diagbr`, `diagbl`, `wipetl`, or `wipetr` depending on source movement direction.

For FFmpeg-only renders where the source angles are too similar for `xfade` to read, add a generated diagonal slash band:

```text
format=rgb24,geq=r='if(between(X-Y+(W+H)*T/d,H*0.18,H*0.34),255,r(X,Y))':g='...':b='...'
```

Use a bright leading band and a darker trailing band so the slash is visible even on static footage.

## QA

- The slash should look intentional in one or two beats.
- A still frame at the slash midpoint should show a diagonal shape, not just blur.
- Avoid repeating too much of the same source moment.
- Avoid using a slash when the source is already a fast pan unless it improves readability.
