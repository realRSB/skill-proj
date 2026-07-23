# Foreground Mask Reveal Recipe

## Layer Formula

Use this mental model:

```text
base footage
+ inserted graphic
+ foreground subject matte from the same footage
= graphic appears behind subject
```

If using FFmpeg, generate an alpha matte or foreground RGBA clip first, then overlay graphic and foreground in order. If using Remotion, treat the foreground matte as a top layer and the title/graphic as the middle layer.

## Matte Choices

- SAM 2: best default for people, cars, hands, products, or irregular objects when a GPU or hosted worker is available.
- Coarse rotoscope: acceptable for 1-2 second clips with large simple subjects.
- Depth map: useful when the foreground/background separation is strong and the graphic should react to distance.
- Manual holdout shapes: useful for simple car hood, phone, laptop, or product silhouettes.

## Graphic Choices

- Big typography behind a person or car.
- App UI panels tucked behind a hand, phone, or product.
- Diagram arrows passing behind an object.
- Particles, smoke, portals, or light ribbons partially occluded by the subject.

Keep graphic motion simpler than subject motion. If both move aggressively, the edge read collapses.

## Edge QA

- Inspect high-motion frames, hair/fingers/mirrors/wheels, and high-contrast intersections.
- Feather `1-3px` for clean 720p/1080p social output; adjust upward only for soft or heavily compressed footage.
- Add matching blur/noise to the inserted graphic before compositing.
- If the matte chatters, smooth masks temporally or shorten the effect window.

## Source Pointers

- SAM 2 overview: https://ai.meta.com/research/sam2/
- SAM 2 repository video prediction: https://github.com/facebookresearch/sam2
- Video Depth Anything project: https://videodepthanything.github.io/
- CoTracker point tracking: https://github.com/facebookresearch/co-tracker
- Remotion effects docs: https://www.remotion.dev/docs/effects
