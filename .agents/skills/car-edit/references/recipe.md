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

The renderer is the current executable implementation of the five nested skills. It should only render:

1. flicker stutter
2. whoosh motion blur
3. slashing diagonal fade
4. hard flash cut
5. final fade out

Improve the relevant nested component skill and renderer together when tuning an effect. Do not add unrelated graphic overlays or extra promo effects to the template renderer.
