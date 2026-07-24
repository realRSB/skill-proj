---
name: edit-slashing-diagonal-fade
description: "Apply the car-edit.mp4 slashing fade transition: a diagonal slice/fade around a template-scaled moment, usually near 54% of a clip. Use when a car edit, transition template, reel, or promo needs the ~7s slash, diagonal wipe, slashing fade, sliced transition, or angled cut bridge."
---

# Edit Slashing Diagonal Fade

Use this skill for the third template effect from `car-edit.mp4`: the slashing diagonal fade around the 7s mark.

## Process

1. Place the slash at the requested timestamp or at `53.85%` of output duration when matching `car-edit.mp4`.
2. Split the source into overlapping pre/post windows around the slash.
3. Apply a diagonal `xfade` or an equivalent diagonal mask transition.
4. QA by sampling the slash midpoint. Completion criterion: the diagonal transition is visible and lands on adjacent moments from the same source order.

Read `references/recipe.md` for the exact `xfade` structure.
