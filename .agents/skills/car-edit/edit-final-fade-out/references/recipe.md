# Final Fade Out Recipe

## Template Position

- Template source: `car-edit.mp4`
- Template moment: end of video.
- Scaled position: final `7-10%` of output duration.

## Timing

- Window: `9.5%` of output duration.
- Clamp: `0.70-1.30s`.

## FFmpeg Pattern

```text
fade=t=out:st=fade_start:d=fade_duration
```

For car-edit template output, fade `assets/trap-beat.mp3` with the final video fade and trim it to the render duration.

## QA

- Confirm the video has a clean ending.
- Confirm one audio stream exists with the bundled trap beat.
- Confirm the fade does not start before the final visual beat.
