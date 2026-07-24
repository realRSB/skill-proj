---
name: car-edit
description: "Apply the reusable car-edit template to one raw car clip using the five nested effect skills in reference order plus the bundled trap beat background music. Use when the user wants any raw car video edited like the download.mp4 reference template, with vertical output, percentage-scaled pacing, and background audio trimmed to the video length."
---

# Car Edit

Use this top-level skill as the entrypoint for the reusable car edit template. The five component skills live inside this folder and must be loaded before rendering.

## Component Order

1. `./edit-flicker-stutter` at about `13%`
2. `./edit-whoosh-motion-blur` at about `37%`
3. `./edit-hard-flash-cut` at about `60%`
4. `./edit-slashing-diagonal-fade` at about `77%`
5. `./edit-final-fade-out` at the end

## Process

1. Accept one raw car clip and one output path.
2. Read each nested component skill's `SKILL.md` and `references/recipe.md` in the order above.
3. Split the raw clip into the same template beat structure before applying effects; the reference is not one continuous shot with overlays.
4. Apply exactly those five components: no extra promo bars, text overlays, logos, UI graphics, or unrelated effects unless the user explicitly asks.
5. Use `scripts/render-car-template-sequence.py input.mp4 output.mp4 --print-plan` for the deterministic FFmpeg implementation of the five skills.
6. Verify one video stream, one audio stream, 720x1280, 30fps, and sampled frames at the scaled effect times.
7. Confirm the bundled `assets/trap-beat.mp3` is looped or trimmed to the exact video duration and fades out with the final visual beat.

Read `references/recipe.md` for the timing map and nested component paths.
