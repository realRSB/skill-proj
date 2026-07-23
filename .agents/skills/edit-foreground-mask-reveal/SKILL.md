---
name: edit-foreground-mask-reveal
description: Place text, logos, UI, captions, diagrams, portals, particles, or graphic shapes behind a moving foreground subject using masks, rotoscoping, depth ordering, and compositing. Use when the user asks for text behind a person/object, subject-masked typography, foreground reveal, occluded title, behind-the-car/person graphic, depth reveal, or a reusable mask-based video edit recipe.
---

# Edit Foreground Mask Reveal

Use this skill for the classic "graphics behind the subject" move. The effect works because the audience instantly understands depth: foreground object, inserted graphic, background plate.

## Process

1. Pick the reveal window.
   Find 1-5 seconds where the subject crosses empty space or has a clean silhouette. Completion criterion: the background has enough negative space for the graphic and the subject edge is visible enough to mask.

2. Build the depth plan.
   Decide what sits behind the subject and whether it is screen-space, world-space, or depth-aware. Write a layer stack before rendering.

3. Make or obtain the matte.
   Prefer SAM 2 for promptable video masks when available. For short clips or weak hardware, create a coarse manual mask, keyframe a simple shape, or use depth maps if the subject separates cleanly. Feather edges lightly and avoid expanding the matte so far that it creates halos.

4. Render the graphic.
   Use Remotion or HyperFrames for animated typography, logos, UI, particles, and diagrams. Use FFmpeg for static overlays or final compositing. Match blur, grain, black level, and motion blur to the source.

5. Composite and check edges.
   Place the graphic between background and foreground matte. Sample frames where the subject crosses the graphic, where hair/thin edges appear, and where motion blur peaks. Completion criterion: the graphic stays behind the subject without buzzing edges, halos, or popping matte holes.

Read `references/recipe.md` for layer formulas, matte choices, and QA checks.
