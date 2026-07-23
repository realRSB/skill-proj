---
name: edit-game-menu-ui-composite
description: Create a video-game menu, pause-screen, inventory, character-select, racing HUD, stats overlay, or interactive UI composite on top of real or generated footage. Use when the user asks to make footage look like gameplay, a game menu, selection screen, HUD, tracked UI overlay, sci-fi interface, or app promo with persistent interactive panels.
---

# Edit Game Menu UI Composite

Use this skill when the effect is a persistent interface layered onto footage, not a one-frame glitch or ordinary lower third.

## Process

1. Classify the scene.
   Identify the subject, camera motion, stable background points, readable safe areas, and whether foreground occlusion is needed. Completion criterion: know which UI elements are screen-space, which are world-space, and which need to pass behind the subject.

2. Make the interface plan.
   Choose a game genre metaphor that fits the source: racing telemetry, pause menu, inventory, character select, mission briefing, or app dashboard. Define panels, selected states, cursor movement, bars, icons, and 2-4 ambient animations.

3. Choose adapters.
   Use HyperFrames or Remotion for UI animation, typography, scanlines, glow, and deterministic renders. Use FFmpeg for source trims, grade, final composite, and audio. Use CoTracker or planar tracking for world-locked labels. Use SAM 2 foreground masks when UI should tuck behind people, cars, hands, or products.

4. Composite with taste.
   Keep UI readable but subordinate to the footage. Match glow, blur, grain, exposure, and chromatic softness to the source. Animate selection changes and cursor moves on intentional beats.

5. Sound-design the illusion.
   Add soft hover clicks, confirm blips, low interface hum, transition whooshes, and ducking under source dialogue or music.

6. QA the render.
   Sample opening, selection change, every tracked element, and ending. Completion criterion: no drift, no matte chatter, no text outside safe areas, no unreadable UI, and no accidental imitation of a specific copyrighted game interface.

Read `references/recipe.md` for layer order, tracking choices, and source pointers.
