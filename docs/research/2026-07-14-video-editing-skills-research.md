# Video Editing Skills Research

Pasted research transcript supplied by the user. It is kept here as source context for the video-agent skill library and the Instagram loading-screen effect direction.

ChatGPT Plus

















This is a copy of a shared ChatGPT conversation

Report conversation
Tue, Jul 14 at 4:36 PM
Can you search for the best video editing skills written for claude or Codex right now 
- we want to start writing skills for a claude SDK agent so that it can do really cool edits on top of AI generated videos or real footage 
But there may already be great skills on how to do really cool edits and transitions online as well as how to use things like ffmpeg well already
so lets do a thorough search

especially for libraries of skills to do specific high quality edits 
here are two example instagram videos:
https://www.instagram.com/reel/DZI7RSwsF3L/
https://www.instagram.com/reel/DYQ2TyWAy22/

In general we think it is possible to be able to pull in tutorials (articles or video transcripts) of how to do these edits and create great skills out of them too so research that too 

Worked for 30m 55s
Research conclusion
As of July 14, 2026, there are already several strong foundations, but no single skill library covers all four things you need:

Editorial decisions on real footage.

High-end motion graphics and transitions.

Tracking, masking, depth, and compositing.

Visual-taste judgment and quality control.

The strongest practical combination is:

OpenMontage as the architecture and reference-video-analysis model.

HyperFrames as the primary library of named motion effects, UI treatments, and transitions.

browser-use/video-use as the real-footage editing and FFmpeg execution backbone.

Remotion’s official skills as a second compositor for React/WebGL effects.

SAM 2, CoTracker, and Video Depth Anything for subject mattes, object tracking, occlusion, and parallax.

That is a substantially better starting point than writing one giant “video editing” skill.

Ranked findings
1. OpenMontage — best overall architecture to study
calesthio/OpenMontage is the repository closest to your full vision. It treats video creation as a set of pipelines with dedicated stage-director skills, structured artifacts, schemas, review gates, resumable state, provider selection, cost tracking, and post-render QA. Its README describes 12 production pipelines and claims more than 400 production, creative, review, and technical skills.

Its Video Reference Analyst is particularly relevant to your Instagram examples. It distinguishes “this is footage to edit” from “this is a stylistic reference,” analyzes transcript, pacing, scenes, keyframes, motion type, framing, camera language, overlays, and transition patterns, then maps the reference against available production capabilities. It explicitly forbids producing a carbon copy and instead generates differentiated concepts that retain selected characteristics from the reference.

OpenMontage also contains one of the better attempts at encoding taste rather than just commands. Its taste profile includes a written “design read,” visual variance, motion intensity, information density, palette discipline, layout variation, anti-patterns, and quality gates. Its reviewer checks those choices at every production stage rather than only validating whether the video rendered.

Verdict: this is the best architectural reference and probably the best existing prototype of a reference-driven video agent.

Important caution: OpenMontage is AGPLv3. For a proprietary Claude SDK product, study its architecture and patterns carefully rather than copying or embedding it wholesale without a licensing review.

2. HyperFrames — best current library of specific motion effects and transitions
heygen-com/hyperframes is the best ready-made answer to “libraries of skills for specific high-quality edits.” It is explicitly built for coding agents, renders deterministic MP4 video from HTML/CSS/media, and ships a router plus approximately 20 workflow and domain skills. Its workflows include talking-head graphic treatments, embedded captions, motion graphics, product launches, music-driven video, website-to-video, and general compositions.

Its animation skill is organized correctly: atomic rules, multi-stage blueprints, transition recipes, broader techniques, and runtime adapters for GSAP, Lottie, Three.js, Anime.js, CSS, the Web Animations API, and WebGPU. The intended workflow is to compose two to four small motion rules rather than loading one giant prompt.

Examples already encoded as named recipes include:

Kinetic beat slams.

Hacker/decryption text reveals.

ASR-synchronized keyword glows.

Slot-machine text tickers.

Virtual-camera zooms and focus locks.

Depth-of-field rack focus.

3D webpage scrolls.

AI tracking-box overlays.

3D scatter-and-assemble effects.

Reactive collision transitions.

Card-morph transitions.

Motion-blur streaks.

Spring-pop entrances.

SVG drawing and animated icon internals.

Its transition catalog includes push and elastic transitions, irises, diagonal splits, 3D flips, zoom-throughs, focus pulls, color dips, blinds, blocks, light leaks, film burns, glitches, chromatic aberration, ripples, VHS treatments, shutter effects, clock wipes, grid dissolves, directional blur, and page burns. It also leaves room for custom CSS and GLSL effects.

Verdict: use HyperFrames as the default engine for UI composites, kinetic typography, motion graphics, HUDs, animated diagrams, social overlays, and custom transitions.

Limitation: HyperFrames’ own router says that footage retiming, reordering, recoloring, and other traditional NLE work are outside its talking-head workflows. It needs to sit on top of a separate footage-editing layer.

HyperFrames is Apache 2.0, making it a more straightforward foundation than OpenMontage for a commercial agent.

3. browser-use/video-use — best lightweight real-footage and FFmpeg backbone
browser-use/video-use is the most practical small skill I found for editing actual footage. It combines:

Transcript-led cutting.

Dead-space and filler-word removal.

An edit-decision list.

FFmpeg rendering.

Small fades at cut boundaries.

Grading.

Styled captions.

Generated overlays through HyperFrames, Remotion, Manim, or PIL.

Cut-boundary visual QA.

Persistent project memory.

Its pipeline is clean: transcribe once, pack the transcript, let the model create an EDL, render, inspect cut boundaries, and retry only a bounded number of times. It also explicitly separates exploratory previews from final rendering.

Verdict: this is the best small repository to fork for your core “edit source footage correctly” loop. Combine its EDL/FFmpeg workflow with HyperFrames rather than replacing either one.

It is MIT-licensed and supports Claude Code and Codex. 

4. Remotion’s official skills — best React/WebGL effects implementation library
remotion-dev/skills is now an official skill repository rather than a collection of third-party prompts. It is particularly useful when you want reusable typed components, React composition, custom shaders, data-driven layouts, and a large JavaScript ecosystem.

Its effect guidance covers brightness and contrast, color keying, duotone, blur, glow, light trails, venetian blinds, mirrors, barrel distortion, chromatic aberration, fisheye, corner pinning, waves, halftone, noise, pixel dissolves, scanlines, television shutdowns, light leaks, starbursts, 3D, audio visualization, sound effects, and captions.

The transition skill includes fades, slides, wipes, flips, clock wipes, spring timing, linear timing, and correct overlap/duration semantics.

The effects system also documents custom WebGL2 effect factories, so a skill can contain an actual shader-backed implementation instead of merely describing an effect in natural language.

Verdict: use Remotion when the composition naturally wants React components, charts, product UI, or reusable WebGL effects. Use HyperFrames when the work is more naturally HTML/GSAP motion design.

License caution: Remotion is not a plain permissive-license assumption for every commercial use case. Verify its current license and any company-license requirements before standardizing on it. 

5. FireRed OpenStoryline — best existing “turn an edit style into a new skill” idea
FireRedTeam/FireRed-OpenStoryline is notable for two reasons.

First, it can archive a completed editing workflow as a reusable skill. Its style-creation meta-skill examines pacing, narrative logic, sound density, subtitle treatment, color, transitions, and recurring preferences, then writes a new skill into the editing skill library.

Second, it recently added generated bridge shots: it can use the outgoing frame, incoming frame, and a natural-language description to generate an intermediate transition clip. The project correctly warns that this can be expensive and unpredictable.

Verdict: study this for your future “learn my editing style” or “save this edit as a reusable profile” functionality.

It is Apache 2.0.

6. Vex — strongest advanced architecture study, but noncommercial
AKMessi/vex is one of the more ambitious systems technically. It combines natural-language editing, FFmpeg and MoviePy, semantic video analysis, generated visuals, evidence contracts, pairwise judging, anti-repetition checks, typed design intermediate representations, and multimodal visual verification. Its effect schema includes punch-ins, slow pushes, reframes, freeze accents, impact pulses, shakes, vignettes, blur, flashes, and subtitle emphasis.

Verdict: mine it for verification and evidence-backed decision patterns, not as the commercial foundation.

The repository uses a PolyForm noncommercial license.

7. maxazure/video-editing-skill — strong production and QA, less useful for high-end effects
This is a very large artifact-first workflow aimed at talking heads, screen recordings, tutorials, interviews, podcasts, and Chinese social platforms. It covers transcription, long-video highlight selection, hook generation, B-roll planning, screen focus, picture-in-picture, bounded grading, rendering, QA, review proxies, subtitles, multi-platform export, and EDL/FCPXML/OTIO output.

Its author explicitly frames complex handcrafted VFX, detailed grading, and advanced motion work as outside the automated core.

Verdict: excellent source material for production gates, exports, provenance, and social-video operations; not the strongest source for the visual effects you are prioritizing. Treat its code as study-only until its licensing is confirmed.

Where the best effect recipes actually live
Motion graphics and UI composites
HyperFrames is currently the best agent-oriented collection. Its organization into atomic rules and blueprints is also the right structure for your own library. An effect should be something like card-morph-anchor or kinetic-beat-slam, not “make it more dynamic.”

Remotion is the strongest secondary source for componentized WebGL, corner pinning, light leaks, dissolves, distortions, and generative overlays.

FFmpeg-native editing and transitions
FFmpeg’s official xfade filter already includes many production-ready transitions: fades, wipes, slides, circles, dissolves, pixelization, slices, zooms, winds, covers, reveals, and custom expressions. A robust skill must enforce its input constraints—matching frame rate, dimensions, pixel format, and time base—rather than blindly constructing a filter graph. 

Useful adjacent primitives include:

perspective for four-corner screen replacements and planar inserts. 

minterpolate for motion interpolation and smoother slow motion. 

The gl-transitions collection for reusable GLSL transition kernels. 

ffmpeg-gl-transition when you accept maintaining a custom FFmpeg build. 

FFmpeg is strongest for deterministic cutting, transforms, grading, audio, encoding, and simpler transitions. It is not the ideal authoring language for complex, stateful UI animation.

Real-footage tracking, mattes, and depth
This is the biggest missing layer in almost every current editing skill repository.

SAM 2 can take point or box prompts and propagate object masks through video, including multiple tracked objects. That enables subject-behind-text compositions, foreground wipes, object isolation, selective grades, and more convincing overlay occlusion.

CoTracker3 tracks arbitrary points or quasi-dense point grids through video. It is well suited to attaching HUD elements to objects, reconstructing planar motion, estimating camera drift, and deriving corner-pin motion.

Video Depth Anything produces temporally consistent depth for long video sequences. That enables depth-aware fog, 2.5D parallax, text passing behind foreground objects, simulated camera pushes, and depth-based grading. Its small model is Apache 2.0, while the larger models have noncommercial licensing, so model selection matters.

ProPainter can fill regions after an object has been masked out, making it relevant for object removal and clean-plate generation. It is GPU-heavy and should be an optional specialist tool rather than a mandatory dependency.

Recommended architecture for your Claude SDK agent
I would use six layers:

Reference or source footage
        ↓
1. Perception and analysis
        ↓
2. Editorial plan / typed timeline
        ↓
3. Real-footage NLE execution
        ↓
4. Motion/VFX composition
        ↓
5. Audio finishing
        ↓
6. Render QA and critique
1. Perception
Produce a durable analysis artifact containing:

Media metadata and time base.

Transcript with word timestamps.

Scene boundaries.

Keyframes and contact sheets.

Audio waveform, beats, silence, and peaks.

People, faces, screens, products, and salient objects.

Camera-motion estimate.

Optional point tracks, masks, and depth maps.

Existing on-screen text and graphics.

A shot-by-shot visual-language description.

The OpenMontage five-aspect structure—subject, subject motion, scene, spatial framing, and camera—is a good starting vocabulary.

2. Typed editorial plan
Do not allow each skill to edit media files directly in an ad hoc manner. First emit a source-of-truth edit plan.

OpenTimelineIO is useful here because it models timelines, tracks, clips, transitions, markers, and metadata independently from the media files themselves. A simpler versioned JSON EDL is also reasonable initially. 

The plan should contain:

timeline:
  fps: 30
  aspect: 9:16
  clips:
    - source: input.mp4
      source_in: 4.120
      source_out: 7.830
      timeline_in: 0
      speed: 1.0

effects:
  - id: game-menu-ui
    start: 0.250
    duration: 4.800
    targets: [subject, background]
    parameters:
      menu_position: left
      selected_item: continue
      tracking_mode: camera
      occlusion_mode: subject_matte

audio:
  dialogue_lufs: -16
  music_cues: []
  sfx_cues: []

qa:
  expected_reference_frames: []
  checks: []
3. Real-footage engine
Use FFmpeg for:

Trim, concat, speed, and frame-rate work.

Crop, scale, stabilization, and social reframing.

Color normalization and LUT application.

Audio mixing, ducking, loudness, and fades.

Subtitle burn-in.

Final encoding and delivery variants.

Follow the video-use principle: one planned graph and as few destructive re-encodes as possible.

4. Compositor adapters
Each effect recipe can expose one or more adapters:

ffmpeg       deterministic footage operations
hyperframes  HTML/GSAP/UI/kinetic type/transition work
remotion     React components/WebGL/data-driven graphics
vision       tracking, masks, depth, clean plates
The effect skill should select the adapter. The adapter scripts should perform the operation. The language model should not manufacture a new 500-character FFmpeg filter graph every time.

5. Audio finishing
Visual-only effect libraries routinely underestimate sound. Every effect recipe should optionally define:

Entry transient.

Movement whoosh.

Interface click or confirmation sound.

Low-frequency impact.

Background texture.

Ducking envelope.

Pre-lap or post-lap.

Maximum peak and loudness expectations.

A mediocre animation with tightly synchronized sound often feels more polished than a technically sophisticated silent animation.

6. QA
Every render should generate:

ffprobe report.

Contact sheet across the finished video.

Extra frames around every cut or transition boundary.

Black-frame and frozen-frame checks.

Audio clipping, silence, and channel checks.

Caption-safe-area checks.

Comparison against expected reference frames.

A concise multimodal critique with concrete corrective actions.

A bounded revision count.

OpenMontage’s reviewer is valuable here because it requires findings to be accurate, complete, and constructive, and it limits endless revision loops.

The first skill library I would write
These should be separate skills or small coherent families, not sections inside one enormous document.

Foundation skills
reference-video-analyzer
Converts a Reel, Short, TikTok, YouTube video, or local reference into a shot map, pacing profile, transition map, visual-language profile, and replication guidance.

footage-ingest-and-index
Generates transcript, keyframes, scene boundaries, waveform, beat grid, detections, and media inventory.

video-edit-director
Chooses the editorial structure and emits the versioned edit plan.

video-render-and-qa
Executes the plan, produces proxies, samples boundaries, validates output, and manages bounded revisions.

High-value effect skills
edit-game-menu-ui-composite
Turns footage into an interactive-looking game menu or character-select screen with tracked UI, selection highlights, scanlines, ambient animation, and sound cues.

edit-object-tracked-hud
Tracks a person or object and attaches labels, bounding boxes, stats, arrows, or diagrams.

edit-screen-replacement-corner-pin
Finds a screen or planar surface, tracks it, inserts content, matches blur/exposure/noise, and handles foreground occlusion.

edit-foreground-mask-reveal
Places typography or graphics behind a moving person or foreground object.

edit-speed-ramp-impact
Combines retiming, optical-flow interpolation, directional blur, impact frames, camera shake, and audio accents.

edit-whip-pan-match-transition
Detects or creates directional motion at both clip boundaries, aligns direction and exposure, adds blur, and hides the cut.

edit-freeze-frame-poster
Freezes a strong frame, isolates the subject, adds typography or outlines, then transitions back into motion.

edit-depth-parallax-2-5d
Uses depth maps and layered warping to add controlled camera movement to real or generated footage.

edit-clone-echo-trail
Uses temporal masks and offset copies to create subject trails, echoes, and repeated silhouettes.

edit-seamless-loop
Finds compatible entry/exit regions and constructs crossfaded, optical-flow, or object-matched loops.

edit-kinetic-captions
Builds word-accurate captions with semantic emphasis, rhythmic movement, occlusion, and safe-area awareness.

edit-beat-synced-montage
Detects musical structure, assigns cut density by section energy, and permits intentional off-beat cuts rather than mechanically cutting on every beat.

edit-color-match-and-look
Normalizes source shots first, then applies a bounded creative look with scopes and skin-tone protection.

edit-sound-design-pass
Reads visual events and creates a cue sheet for transitions, interactions, impacts, ambience, and music ducking.

This library covers considerably more useful territory than having 100 different named wipes.

How to turn tutorials into reliable skills
Yes, this is feasible, and the emerging research is directionally encouraging.

The recent RESOURCE2SKILL work constructs hierarchical, provenance-aware skill collections from tutorial videos, repositories, articles, and reference artifacts. It emphasizes that video carries procedural order, before/after state, layout, and tacit design information that transcript summaries often lose. VISUALSKILL similarly reports that agents benefit from retrieving visual references alongside textual instructions. These are recent preprints and are not specifically validated for professional editing, but the design direction is highly applicable. 

Do not build a transcript-only extractor
For an editing tutorial, the useful information is distributed across:

Spoken explanation.

Timeline and node-graph state.

Mouse operations.

Parameter values.

Before/after frames.

Motion curves.

Project files.

Hidden assumptions such as frame rate, color space, and layer order.

Failures demonstrated visually but never described.

A good extractor needs transcript plus sampled video frames and, where possible, an inspectable project file.

Highest-value tutorial corpora
Blackmagic Design’s official DaVinci Resolve training is probably the best initial corpus. It includes official videos and downloadable project or lesson files across editing, variable-speed effects, traveling mattes, green screen, sign replacement, tracking, Fusion compositing, object removal, color, and sound design. The project files give you a ground-truth result rather than only a verbal explanation. 

Adobe Learn for After Effects is valuable for motion blur, easing, stabilization, typography, title animation, and compositing fundamentals. 

Apple’s Final Cut Pro guide is useful for object tracking, masks, keying, compositing, transitions, generators, color tools, and LUT workflows. 

Official FFmpeg, Remotion, and HyperFrames documentation should be the executable reference layer. Creator tutorials can explain taste; official documentation should define parameter and runtime behavior.

Public video captions can be collected first, with ASR used only as a fallback. The claude-video project follows that pattern for URL analysis: use available captions, scene-aware frame selection, and Whisper when captions are absent.

Proposed tutorial-to-skill pipeline
Ingest and record provenance
Store source, creator, title, publication date, access date, license or usage status, and relevant timestamps.

Segment by technique
One tutorial may contain three different skills. Split “track the screen,” “insert the graphic,” and “match the grade” rather than making one monolithic tutorial skill.

Align transcript and frames
Sample aggressively around parameter changes, before/after comparisons, timeline edits, masks, and node-graph changes.

Extract an engine-neutral recipe
Capture:

Intent.

Preconditions.

Layer structure.

Timing.

Tracking or masking requirements.

Parameter ranges.

Easing curves.

Audio cues.

Failure modes.

Verification frames.

Implement adapters
Translate the recipe into FFmpeg, HyperFrames, Remotion, or a vision-tool pipeline. Some tutorials will only have one valid adapter.

Create a clean-room fixture
Use your own test footage and assets. Do not make the original creator’s paid project file or footage part of the distributed skill.

Render multiple parameter variants
Compare subtle, medium, and strong versions. Store which ranges remain visually stable.

Run visual and structural evaluations
Test whether the correct skill triggers, whether the plan validates, whether it renders, whether it visibly produces the intended effect, and whether it avoids common artifacts.

Publish a compact skill
Keep the main SKILL.md short. Put detailed explanations, troubleshooting, and source notes in references; executable operations belong in scripts.

Maintain provenance and versions
A tutorial-derived skill should say which information is extracted knowledge, which code is original, which implementation is adapted from an open-source project, and which model or application versions it was tested against.

How to package these for Claude SDK and Codex
Claude Code and Codex both support the open Agent Skills structure. Claude’s Agent SDK loads filesystem configuration and can use skills under .claude/skills/*/SKILL.md; it also supports subagents, which map naturally to perception, edit direction, compositing, audio, and QA roles. 

Use a router plus progressive disclosure:

.claude/skills/
  video-director/
    SKILL.md

  edit-game-menu-ui/
    SKILL.md
    references/
      recipe.md
      failure-modes.md
      provenance.md
    scripts/
      analyze.py
      render_hyperframes.ts
      render_remotion.ts
      composite_ffmpeg.py
      verify.py
    assets/
      expected-frames/
The open Agent Skills guidance recommends keeping the primary skill concise—roughly under 500 lines and 5,000 tokens—and loading supporting references and scripts only when needed. It also warns that excessively comprehensive skills can perform worse than short, procedural skills with a working example. 

The name and especially the description should be treated as routing code, because they are the primary trigger signals. Test both positive and negative triggering, expected tool calls, output artifacts, and style conventions. 

A good effect description looks like:

Use when footage should resemble a video-game pause, inventory, character-select, or menu screen, including persistent HUD panels, selection highlights, tracked interface elements, scanlines, and UI sound cues. Do not use for a brief one-frame glitch or a normal title card.

That is much more reliable than:

Helps create cool game effects.

What I could verify about the two Instagram examples
Instagram throttled direct playback in the research environment, so I could not perform a trustworthy frame-by-frame examination of either Reel from the links alone. citeturn760386view0turn760386view1

Reel 2: DYQ2TyWAy22
The publicly indexed description identifies this as turning a video into a game menu screen. 

For that class of effect, I would route to edit-game-menu-ui-composite:

Analyze whether the source camera is locked, drifting, or moving.

Track stable scene points with CoTracker.

Generate a person or foreground matte with SAM 2.

Construct menu panels, labels, selection states, bars, icons, and ambient animations in HyperFrames or Remotion.

Attach world-space UI to tracked coordinates while keeping screen-space menu elements fixed.

Composite selected elements behind the person using the matte.

Match the UI to the footage with glow, blur, grain, scanlines, bloom, and chromatic separation.

Add cursor movement, selection pulses, menu clicks, confirm sounds, and a low ambient interface bed.

Inspect sampled frames for tracking drift, matte chatter, unreadable UI, and excessive effects.

This is primarily a persistent layered composite, not merely a transition.

Reel 1: DZI7RSwsF3L
The available search result references a “Strawberry Full Moon,” but it does not expose enough visual information to classify the actual edit, transition, or compositing method responsibly. 

Uploading the two Reels as MP4 files would enable a frame-accurate breakdown into cuts, masks, tracks, layer ordering, timing curves, sound cues, and draft effect-skill specifications.

Recommended starting plan
Phase 1: adopt and study the strongest foundations
Install the two most useful effect libraries:

npx skills add heygen-com/hyperframes --full-depth --yes
npx skills add remotion-dev/skills
HyperFrames documents the agent install and its on-demand skill router directly; Remotion provides its own official agent skills. 

Clone OpenMontage into a separate research workspace and use it to study:

Reference-video analysis.

Taste profiles.

Pipeline manifests.

Stage-specific director skills.

Reviewer and slideshow-risk checks.

Artifact schemas.

Do not make it an embedded dependency until the AGPL implications are resolved.

Phase 2: build the proprietary core
Use:

A video-use-style transcript/EDL/FFmpeg pipeline.

OTIO or a versioned JSON edit-plan schema.

HyperFrames as the default motion compositor.

Remotion as an optional adapter.

PySceneDetect plus your own keyframe/contact-sheet analysis.

SAM 2 and CoTracker as optional GPU workers.

A mandatory render-QA skill.

Phase 3: implement five showcase effects
Start with:

Game-menu UI composite.

Object-tracked HUD.

Foreground mask reveal.

Speed-ramp impact.

Screen replacement and corner pin.

These collectively force the system to solve UI design, tracking, masks, retiming, blur, audio, compositing, and QA—the important infrastructure that simpler wipes do not exercise.

Phase 4: build the tutorial extractor
Begin with ten official Resolve or After Effects lessons that include project files. Produce one small, tested skill per technique, then compare the tutorial-derived implementations against hand-authored skills. Only after that should the extractor be allowed to acquire large numbers of public tutorials automatically.

The key strategic decision is to build a verified effect-recipe library with multiple rendering adapters, not a large text collection of editing advice. That is the difference between an agent that talks convincingly about editing and one that repeatedly produces polished edits.




Sources
