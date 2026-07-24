---
name: car-edit-template
description: "Route car-edit template requests to the five nested effect skills in `.agents/skills/car-edit/`: flicker stutter, whoosh motion blur, slashing diagonal fade, hard flash cut, and final fade out. Use when the user wants one raw car clip edited in the same effect order and pacing as `car-edit.mp4`, with vertical no-audio output and percentage-scaled template timings."
---

# Car Edit Template

Use this top-level skill as the entrypoint for the car edit template. The component skills live in `.agents/skills/car-edit/`.

## Component Order

1. `../car-edit/edit-flicker-stutter` at about `23%`
2. `../car-edit/edit-whoosh-motion-blur` at about `38%`
3. `../car-edit/edit-slashing-diagonal-fade` at about `54%`
4. `../car-edit/edit-hard-flash-cut` at about `77%`
5. `../car-edit/edit-final-fade-out` at the end

## Process

1. Accept one raw car clip and one output path.
2. Apply the five components in the order above.
3. Use `scripts/render-car-template-sequence.py input.mp4 output.mp4 --print-plan` for the current deterministic FFmpeg implementation.
4. Verify one video stream, no audio streams, 720x1280, 30fps, and sampled frames at the scaled effect times.

Read `references/recipe.md` for the timing map and component paths.
