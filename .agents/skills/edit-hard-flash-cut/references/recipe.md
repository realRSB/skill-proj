# Hard Flash Cut Recipe

## Template Position

- Template source: `car-edit.mp4`
- Template moment: about 10s
- Scaled position: `10 / 13 = 76.92%`

## Timing

- Window: `1-2%` of output duration.
- Clamp: `0.07-0.14s`.

## FFmpeg Pattern

Use a short full-frame flash:

```text
drawbox=x=0:y=0:w=iw:h=ih:color=white@0.34:t=fill:enable='between(t,start,end)'
```

Optional: pair with a crop punch if the surrounding footage has enough margin.

## QA

- The flash should last only a few frames.
- It should signal a cut or section change.
- Avoid stacking it directly on the flicker or fade out.
