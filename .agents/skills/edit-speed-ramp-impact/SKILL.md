---
name: edit-speed-ramp-impact
description: Create punchy speed-ramp impact edits for car footage, product shots, action clips, launch teasers, reels, shorts, and app promos that need fast-slow-fast pacing, impact flashes, whip cuts, sharpened contrast, loudness-safe audio, and render QA. Use when the user asks for a car edit, speed ramp, impact edit, cinematic promo cut, beat-synced montage, or a reusable FFmpeg/Remotion/HyperFrames recipe for that effect.
---

# Edit Speed Ramp Impact

Use this skill to make a short, kinetic promo cut where time-remapping is the main effect. The edit should feel intentional in motion, not like random fast cuts.

## Process

1. Inspect the source.
   Run `ffprobe`, generate a contact sheet, and sample frames near likely beats, whip moves, or hero poses. Completion criterion: every selected source section has a reason such as hero framing, texture detail, motion blur, reveal, or final hold.

2. Build a tiny edit plan before rendering.
   Write the selected clips as `source_in`, `source_out`, `speed`, and `role`. Use 5-9 clips for a 10-18 second reel. Alternate holds and accelerations: hero hold, whip burst, detail hold, profile move, final hero.

3. Execute with the simplest adapter that can finish cleanly.
   Prefer FFmpeg for trim, speed, crop, grade, flash bars, loudness, and final encode. Use the repo script `scripts/render-car-edit.sh` when the request is a rainy gas-station car promo or a close variant. Use Remotion or HyperFrames only when the edit needs typography, UI, or animated graphic layers that the local FFmpeg build cannot burn in.

4. Add impact language.
   Use fast segments as transitions. Pair major changes with 2-4 frame white flashes, subtle punch-in crops, sharpened highlights, and short audio fades. Keep grades bounded so shadows stay readable and highlights do not clip.

5. QA the render.
   Run `ffprobe`, sample frames with accurate seek after input, and inspect the final video around each cut. Completion criterion: constant 9:16 output unless requested otherwise, matching audio/video duration, no render warnings, no accidental black/frozen frames, and no source transition artifact lingering longer than intended.

Read `references/recipe.md` when choosing timing, effect parameters, or troubleshooting FFmpeg constraints.
