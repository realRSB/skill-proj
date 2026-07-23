# Game Menu UI Composite Recipe

## Layer Order

1. Base footage, stabilized or trimmed.
2. World-space tracked UI: labels, brackets, selection rings, item stats attached to scene points.
3. Behind-subject UI, masked by foreground matte when needed.
4. Screen-space menu: left/right panels, selected item, top status, bottom prompts.
5. Finish: scanlines, bloom, subtle blur, grain, chromatic softness, vignette.

## UI Patterns

- Racing/product footage: speed, mode, lap, boost, torque, damage, selector cursor.
- Person/fashion footage: character select, outfit stats, inventory carousel, skill bars.
- App promo footage: dashboard as a game objective, checklist, reward screen, mission complete.

Use 2-4 animated elements. Good defaults: pulsing selected row, cursor travel, tiny progress bar fill, ambient particle/scanline drift.

## Tracking Choices

- Locked camera: screen-space UI is enough.
- Handheld with stable background: track 4-12 points and smooth the transform.
- Moving subject occlusion: create a foreground matte and composite the UI behind it.
- Planar screen or sign: use four-corner tracking and match blur/noise.

## Failure Checks

- UI drifts from the object it claims to label.
- Bright panels cover the strongest facial/product detail.
- The interface looks like a flat sticker because it lacks grain, blur, or exposure matching.
- The design copies a real game HUD too closely.
- Every element animates at once, making the footage unreadable.

## Source Pointers

- Project brief example: Instagram Reel `DYQ2TyWAy22`, publicly described in the pasted research as a video-to-game-menu edit.
- HyperFrames agent video framework: https://github.com/heygen-com/hyperframes
- HyperFrames quickstart: https://hyperframes.heygen.com/quickstart
- Remotion agent skills: https://www.remotion.dev/docs/ai/skills
- CoTracker point tracking: https://github.com/facebookresearch/co-tracker
- SAM 2 video mask propagation: https://github.com/facebookresearch/sam2
