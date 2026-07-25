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

- cinematic grade that keeps the subject readable
- very light edge darkening only; do not bury the subject in dark borders
- `ORACLE OF THE GOLDEN SAIL` title/menu overlay based on `assets/loading-menu-reference.png`
- compact reference-style gold serif typography placed in the upper-left safe area
- stacked header matching the reference structure: large `ORACLE`, smaller centered `OF THE` between rules, large `GOLDEN SAIL`, ornate divider, italic tagline
- small circular compass/logo mark in the upper-right safe area
- transparent overlay treatment: text, ornament, selector, and a soft edge darkening only
- no boxed HUD panel, heavy black slab, neon sci-fi UI, or generic loading bar
- Continue, New Game, Settings, Exit menu options
- animated selector/highlight that visits each menu option in order
- brief click/flash accents as the selection changes

Keep overlay text inside safe margins while preserving subject readability. It should feel like the uploaded cinematic game main menu reference, not a generic HUD.

## QA

- Source audio must be absent.
- One AAC audio stream should exist with only the background song.
- Drop should occur at about `4.5s` unless the user overrides it.
- A still frame after the drop should clearly show the title/menu overlay.
- Contact sheets should show normal footage first, then selector states after the drop.
- Output should be vertical `720x1280`, `30fps`.
