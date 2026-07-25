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
   - the bundled fantasy game-menu overlay inspired by `assets/loading-menu-reference.png`
   - the title/menu aesthetic from the uploaded loading-screen reference
   - an animated selector that moves through Continue, New Game, Settings, and Exit
   - click/flash accents as the selector changes
7. During the normal lead-in, show the bundled intro caption inspired by `assets/intro-caption-reference.png`: Chinese text plus `turning myself into a video game loading screen`.
8. Verify one video stream, one audio stream, vertical `720x1280`, `30fps`, and the song trimmed/faded to the video duration.

## Renderer

Run:

```bash
.agents/skills/edit-game-loading-screen/scripts/render-loading-screen.py input.mov output.mp4 --print-plan
```

For still images, the renderer creates a short motion-video using camera drift and the song length. For videos, it plays the clip normally first, then uses the original clip in slow motion after the drop while ignoring original audio.

Read `references/recipe.md` for timing, visual rules, and QA.
