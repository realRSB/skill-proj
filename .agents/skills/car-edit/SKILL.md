---
name: car-edit
description: "Apply the reusable car-edit.mp4 template to one raw car clip using the five nested effect skills in order: flicker stutter, whoosh motion blur, slashing diagonal fade, hard flash cut, and final fade out. Use when the user wants any raw car video edited like the car-edit template, with vertical no-audio output and percentage-scaled pacing."
---

# Car Edit

Use this top-level skill as the entrypoint for the reusable car edit template. The five component skills live inside this folder.

## Component Order

1. `./edit-flicker-stutter` at about `23%`
2. `./edit-whoosh-motion-blur` at about `38%`
3. `./edit-slashing-diagonal-fade` at about `54%`
4. `./edit-hard-flash-cut` at about `77%`
5. `./edit-final-fade-out` at the end

## Process

1. Accept one raw car clip and one output path.
2. Apply the five components in the order above.
3. Use `scripts/render-car-template-sequence.py input.mp4 output.mp4 --print-plan` for the current deterministic FFmpeg implementation.
4. Verify one video stream, no audio streams, 720x1280, 30fps, and sampled frames at the scaled effect times.

Read `references/recipe.md` for the timing map and nested component paths.
