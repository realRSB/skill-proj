# Flicker Stutter Recipe

## Template Position

- Template source: `download.mp4`
- Template moment: about 2.35s in the 18.1s reference
- Scaled position: `2.35 / 18.1 = 12.98%`

## Timing

- Window: `2.5-3.5%` of output duration.
- Clamp: `0.22-0.42s`.
- Pulse count: 6 total pulses, alternating bright/dark.

## FFmpeg Pattern

Use `drawbox` over the full frame:

```text
drawbox=x=0:y=0:w=iw:h=ih:color=white@0.40:t=fill:enable='pulse_1+pulse_3+pulse_5'
drawbox=x=0:y=0:w=iw:h=ih:color=black@0.40:t=fill:enable='pulse_2+pulse_4+pulse_6'
```

Generate pulses as short `between(t,start,end)` ranges.

## QA

- The flicker should be a stutter hit, not a slow dissolve.
- Avoid long black frames.
- Avoid placing it over an already-black source moment.
