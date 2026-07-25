# Game Loading Screen Recipe

## Timing

- Default output duration: the background song duration, capped by video source duration when the input is a video.
- Default beat drop: `4.5s`, matching the provided song's drop region.
- Before drop: normal-speed footage with minimal grading.
- At/after drop: cinematic slow-motion loading screen treatment.

## Audio

- Use `assets/backgroundsong.mp3` by default.
- Do not mix in source audio.
- Loop or trim song if needed.
- Fade out the song over the final `0.35-0.6s`.

## Loading Screen Look

Use these visual parts after the drop:

- dark cinematic grade
- subtle vignette
- top and bottom letterbox bars
- thin frame/corner boxes
- `LOADING PLAYER` title
- `PLAYER 01` and `STATUS: CINEMATIC MODE`
- animated loading bar
- small flavor text such as `PRESS START WHEN READY`

Keep overlay text inside safe margins. It should feel like a video game UI, not a poster or meme caption.

## QA

- Source audio must be absent.
- One AAC audio stream should exist with only the background song.
- Drop should occur at about `4.5s` unless the user overrides it.
- A still frame after the drop should clearly show the loading-screen overlay.
- Output should be vertical `720x1280`, `30fps`.
