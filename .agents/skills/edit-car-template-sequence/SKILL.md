---
name: edit-car-template-sequence
description: "Apply the exact five-effect order and pacing from the local template video `car-edit.mp4` to one raw car clip: flicker, whoosh, slashing diagonal fade, hard cut, and final fade out. Use when the user wants to upload one raw car video and have it edited like the template, with percentage-scaled timings, source footage used from beginning to end, vertical 9:16 output, and no audio."
---

# Edit Car Template Sequence

Use this skill when the user wants the reusable template derived from `car-edit.mp4`, not a generic car promo.

## Process

1. Accept exactly one raw source clip and one output path.
   If there are multiple clips, ask the user to choose one or combine them before using this skill.

2. Render with the template sequence script.
   Run:

   ```bash
   scripts/render-car-template-sequence.py input.mp4 output.mp4 --print-plan
   ```

   The script uses the full source clip from beginning to end, outputs vertical 720x1280, removes audio, and applies the five effects in order.

3. Verify the output.
   Run `ffprobe` and confirm: one video stream, no audio streams, 720x1280, 30fps, and a duration close to the source duration. Sample frames near the scaled effect positions.

4. Report the rendered output path and the scaled effect timings.
   Mention that close visual matching still depends on the raw footage containing usable car angles.

Read `references/recipe.md` for the effect timing map and implementation notes.
