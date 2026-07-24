---
name: edit-slashing-diagonal-fade
description: "Apply the car-edit.mp4 slashing fade transition: a diagonal slice/fade around a template-scaled moment, usually near 54% of a clip. Use when a car edit, transition template, reel, or promo needs the ~7s slash, diagonal wipe, slashing fade, sliced transition, or angled cut bridge."
---

# Edit Slashing Diagonal Fade

Use this skill for the third template effect from `car-edit.mp4`: the slashing diagonal fade around the 7s mark.

## Process

1. Place the slash at the requested timestamp or at about `76.52%` of output duration when matching the `download.mp4` reference template.
2. Split the source into overlapping pre/post windows around the slash or generate a visible diagonal blade over the transition window.
3. Apply a diagonal `xfade`, diagonal mask, or bright moving diagonal slash band; do not rely on tilt/blur alone.
4. QA by sampling the slash midpoint. Completion criterion: the diagonal line or wipe shape is visible in a still frame and the motion lands on the next beat cleanly.

Read `references/recipe.md` for the exact `xfade` structure.
