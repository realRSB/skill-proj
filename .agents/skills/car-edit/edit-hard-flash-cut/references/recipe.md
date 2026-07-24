# Hard Flash Cut Recipe

## Template Position

- Template source: `download.mp4`
- Template moment: about 10.85s in the 18.1s reference
- Scaled position: `10.85 / 18.1 = 59.94%`

## Timing

- Window: `1-2%` of output duration.
- Clamp: `0.07-0.14s`.

## FFmpeg Pattern

Use a short full-frame white-black-white pulse:

```text
drawbox=x=0:y=0:w=iw:h=ih:color=white@0.92:t=fill:enable='between(t,0,first_flash)'
drawbox=x=0:y=0:w=iw:h=ih:color=black@0.58:t=fill:enable='between(t,first_flash,black_snap)'
drawbox=x=0:y=0:w=iw:h=ih:color=white@0.62:t=fill:enable='between(t,black_snap,second_flash)'
```

Pair with a crop punch if the surrounding footage has enough margin. Avoid turning this effect into blur; the flash cut must read as an impact frame.

## QA

- The flash should last only a few frames, but at least one frame should be obviously bright.
- It should signal a cut or section change more than a motion blur.
- Avoid stacking it directly on the flicker or fade out.
