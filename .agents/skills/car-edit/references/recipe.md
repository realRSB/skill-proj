# Car Edit Router

## Component Skill Paths

- `.agents/skills/car-edit/edit-flicker-stutter`
- `.agents/skills/car-edit/edit-whoosh-motion-blur`
- `.agents/skills/car-edit/edit-slashing-diagonal-fade`
- `.agents/skills/car-edit/edit-hard-flash-cut`
- `.agents/skills/car-edit/edit-final-fade-out`

## Timing Map

Scale these from the template duration:

- Flicker: `3 / 13 = 23.08%`
- Whoosh: `5 / 13 = 38.46%`
- Slashing fade: `7 / 13 = 53.85%`
- Hard cut: `10 / 13 = 76.92%`
- Fade out: final `7-10%`

## Renderer

```bash
scripts/render-car-template-sequence.py raw-car.mp4 edited-car.mp4 --print-plan
```

The renderer is the current executable implementation of this skill. Improve the relevant nested component skill and renderer together when tuning an effect.
