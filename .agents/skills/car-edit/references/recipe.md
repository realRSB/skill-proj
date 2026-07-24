# Car Edit Router

## Component Skill Paths

- `.agents/skills/car-edit/edit-flicker-stutter`
- `.agents/skills/car-edit/edit-whoosh-motion-blur`
- `.agents/skills/car-edit/edit-hard-flash-cut`
- `.agents/skills/car-edit/edit-slashing-diagonal-fade`
- `.agents/skills/car-edit/edit-final-fade-out`

## Timing Map

Scale these from the actual reference template duration, `18.1s`:

- Flicker: `2.35 / 18.1 = 12.98%`
- Whoosh: `6.65 / 18.1 = 36.74%`
- Hard cut: `10.85 / 18.1 = 59.94%`
- Slashing fade: `13.85 / 18.1 = 76.52%`
- Fade out: final `7-10%`

## Beat Structure

The template is an edited sequence, not a continuous source clip with effects on top. Preserve this structure when adapting one raw clip:

- opening hold
- flicker/glitch smear into a new crop/angle
- short black pause
- low-angle hold
- whoosh/warp into another crop/angle
- rear/close hold
- hard smear cut
- close hold
- slashing/tilted fade
- wide/front hold
- final fade

## Renderer

```bash
scripts/render-car-template-sequence.py raw-car.mp4 edited-car.mp4 --print-plan
```

By default the renderer adds `assets/trap-beat.mp3` as background music. Loop or trim the beat to the final video duration, fade it out with the ending, and encode AAC audio in the MP4 output.

The renderer is the current executable implementation of the five nested skills. It should only render:

1. flicker stutter
2. whoosh motion blur
3. hard flash cut
4. slashing diagonal fade
5. final fade out

Improve the relevant nested component skill and renderer together when tuning an effect. Do not add unrelated graphic overlays or extra promo effects to the template renderer.
