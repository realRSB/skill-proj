---
name: edit-hard-flash-cut
description: "Apply the car-edit.mp4 hard cut hit: a brief white flash or impact cut around a template-scaled moment, usually near 77% of a clip. Use when a car edit, transition template, reel, or promo needs the ~10s hard cut, flash cut, impact cut, punch cut, or final-section accent."
---

# Edit Hard Flash Cut

Use this skill for the fourth template effect from `car-edit.mp4`: the hard flash cut around the 10s mark.

## Process

1. Place the cut at the requested timestamp or at about `59.94%` of output duration when matching the `download.mp4` reference template.
2. Add a short white-black-white impact pulse with a crop punch so the beat reads as a cut, not a blur.
3. Keep the cut shorter than the flicker and visually stronger than the whoosh.
4. QA the before/after frames. Completion criterion: at least one sampled frame in the cut window is clearly flashed or snapped, and the following frame lands on a different crop.

Read `references/recipe.md` for timing and FFmpeg expressions.
