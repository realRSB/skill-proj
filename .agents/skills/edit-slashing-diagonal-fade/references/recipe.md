# Slashing Diagonal Fade Recipe

## Template Position

- Template source: `car-edit.mp4`
- Template moment: about 7s
- Scaled position: `7 / 13 = 53.85%`

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

## QA

- The slash should look intentional in one or two beats.
- Avoid repeating too much of the same source moment.
- Avoid using a slash when the source is already a fast pan unless it improves readability.
