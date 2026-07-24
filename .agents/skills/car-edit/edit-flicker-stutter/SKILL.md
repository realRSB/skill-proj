---
name: edit-flicker-stutter
description: "Apply the car-edit.mp4 flicker/stutter hit: fast alternating white and black exposure pulses around a template-scaled moment, usually near 23% of a clip. Use when a car edit, transition template, teaser, reel, or promo needs the ~3s template flicker, impact stutter, flash flicker, exposure blink, or pre-transition glitch hit."
---

# Edit Flicker Stutter

Use this skill for the first template effect from `car-edit.mp4`: the fast visual flicker around the 3s mark.

## Process

1. Place the flicker at the requested timestamp or at `23.08%` of the output duration when matching `car-edit.mp4`.
2. Build 3 alternating white pulses and 3 black/dim pulses across a short window.
3. Keep the pulses brief enough to read as an impact, not a fade.
4. QA by sampling frames before, during, and after the flicker. Completion criterion: the effect is visible in motion but does not obscure the car for more than a few frames.

Read `references/recipe.md` for exact timing and FFmpeg expressions.
