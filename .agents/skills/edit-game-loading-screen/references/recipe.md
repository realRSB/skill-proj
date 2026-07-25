# Game Loading Screen Recipe

## Timing

- Default output duration: the background song duration, capped by video source duration when the input is a video.
- Default beat drop: `4.5s`, matching the provided song's drop region.
- Before drop: normal-speed footage with minimal grading and the bilingual intro caption.
- At/after drop: cinematic slow-motion game-menu treatment.

## Audio

- Use `assets/backgroundsong.mp3` by default.
- Do not mix in source audio.
- Loop or trim song if needed.
- Fade out the song over the final `0.35-0.6s`.

## Intro Look

Use the bundled `assets/intro-caption-720x1280.png`, based on `assets/intro-caption-reference.png`.

- Keep the raw clip visible and moving.
- Place the bilingual caption in the lower-middle safe area.
- Do not use source audio; the caption should ride over the provided song only.

## Loading Screen Look

Use these visual parts after the drop:

- dark cinematic grade
- subtle vignette
- `ORACLE OF THE GOLDEN SAIL` title/menu overlay based on `assets/loading-menu-reference.png`
- Continue, New Game, Settings, Exit menu options
- animated selector/highlight that visits each menu option in order
- brief click/flash accents as the selection changes

Keep overlay text inside safe margins. It should feel like a cinematic game main menu, not a generic HUD.

## QA

- Source audio must be absent.
- One AAC audio stream should exist with only the background song.
- Drop should occur at about `4.5s` unless the user overrides it.
- A still frame after the drop should clearly show the title/menu overlay.
- Contact sheets should show normal footage first, then selector states after the drop.
- Output should be vertical `720x1280`, `30fps`.
