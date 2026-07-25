---
name: edit-game-loading-screen
description: "Create the 'I turned myself into a video game loading screen' trend edit from a video clip or still image. Use when the user wants normal footage to play first, then switch on the song beat drop around 4-5 seconds into a cinematic slow-motion game loading screen overlay, with source audio muted and only the bundled background song playing."
---

# Edit Game Loading Screen

Use this skill to turn a raw clip or portrait image into a vertical game-loading-screen trend edit.

## Workflow

1. Accept one input visual file and one output path.
2. Use `assets/backgroundsong.mp3` as the only audio unless the user explicitly provides another song.
3. Mute all source audio. The output should contain only the background song.
4. Place the transition at the beat drop, default `4.5s`.
5. Render a normal lead-in before the drop.
6. At the drop, switch to cinematic slow motion with:
   - darker grade and sharpening
   - letterbox bars
   - scanning/HUD styling
   - game loading text
   - animated progress bar
   - visible player/profile overlay
7. Verify one video stream, one audio stream, vertical `720x1280`, `30fps`, and the song trimmed/faded to the video duration.

## Renderer

Run:

```bash
.agents/skills/edit-game-loading-screen/scripts/render-loading-screen.py input.mov output.mp4 --print-plan
```

For still images, the renderer creates a short motion-video using the song length. For videos, it uses the original clip visually and ignores the original audio.

Read `references/recipe.md` for timing, visual rules, and QA.
