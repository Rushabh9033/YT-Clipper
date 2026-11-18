# PRD.md — YT-Clipper 2.0: AI Video Production Studio
**Product Vision, Feature Specification, Architecture & Roadmap**

---

## 1. Product Vision & Positioning
Do not build another basic AI clipper or a direct OpusClip clone. Build an **AI video production studio** that makes stronger editorial decisions, gives creators professional editing control, and produces publish-ready content.

### Core Promise
Upload a long video, livestream recording, or gameplay session. The system understands what happened, discovers the strongest moments, creates polished edits, lets the creator refine them via a non-destructive timeline, and exports platform-ready content.

### Positioning
- **Gaming-First**: Where event detection and context-aware editing provide a focused competitive advantage.
- **Category Expansion**: Expand to podcasts, interviews, educational streams, vlogs, and commentary.
- **Competitive Edge**: Compete on content understanding, editorial quality, editability, reliability, and creator time saved — NOT on generating the largest number of mediocre, uncurated clips.

### Key Distinction
YT-Clipper 2.0 is a specialized short-form production studio. It does not need to recreate every legacy feature of DaVinci Resolve or Adobe Premiere Pro. It must provide **frame-accurate, professional-level control specifically engineered for short-form viral storytelling**.

---

## 2. Core Pillars & Differentiators

### Pillar A: Gaming Intelligence Engine
Understand what is happening in the game, not just what the streamer says:
1. **Game-State & HUD Events**: Kills, knockdowns, assists, clutches, victories, defeats, and final-circle tension.
2. **Context Transitions**: Scene shifts, scoreboard popups, intense combat vs. quiet looting periods.
3. **Emotional Calibration**: Correlate streamer facecam/mic volume spikes with in-game milestones.
4. **Configurable Game Profiles**: Customizable HUD bounding boxes (BGMI/PUBG, GTA 6, Valorant, Call of Duty).

### Pillar B: Intelligent Editorial Director
Find moments using audio, video, transcript, and game-event context:
1. **Complete Narrative Arc**: Enforce **Setup ➔ Action ➔ Reaction ➔ Payoff**.
2. **Zero Premature Cuts**: Avoid clips that begin too late (missing context) or terminate before the laughter/rage settles.
3. **Standalone Coherence**: Prefer moments that make complete sense to a first-time viewer without watching the full 4-hour VOD.
4. **Transparent Rationale**: Every selected moment provides confidence scores, editorial reasoning, and flagged risks.

### Pillar C: Premium Automatic Editing
1. **Word-Level Kinetic Captions**: Physics spring-pop on key phrases, multi-color highlighting, and verbatim sync.
2. **Intelligent Dynamic Layouts**: Game-aware framing (Facecam top + gameplay bottom with laser dividing line; dynamic zoom on mini-map during chases).
3. **Visual Punch & Overlays**: Authentic Apple iOS color emojis, retention hook badges (0.0s - 3.5s), and dynamic sound ducking.

### Pillar D: Real Professional Non-Destructive Editing Controls
Every generated effect must be independently editable via a project timeline:
1. **Multitrack Project Schema (`timeline.json`)**:
   - Track 1: Facecam video with crop/position properties.
   - Track 2: Gameplay video with zoom/reframe properties.
   - Track 3: Audio stems (speech, game audio, sound effects, ducking).
   - Track 4: Captions (word-level timestamps, styles, font parameters).
   - Track 5: Overlays & Stickers (Apple emojis, timeline keyframes).
   - Track 6: Retention Badges & Lower Thirds.
2. **Frame-Accurate Editability**: Ability to adjust cut points, replace misheard words, swap emojis, or change caption colors without re-running AI inference.

### Pillar E: Production & Autonomous Distribution Intelligence
1. **Vertical 9:16 Canvas**: 1080x1920 @ 60fps NVENC encoding in under 15 seconds.
2. **Auto-Generated Thumbnails**: Both 9:16 vertical cover (`_thumb.jpg`) and 16:9 thumbnail (`_thumb_16x9.jpg`).
3. **SEO & Publishing Package**: Viral titles, hashtag injection, description, and engagement comments.
4. **Zero-Defect Free YouTube Studio Publishing**: Headless Playwright uploader with dual-gate post-upload metadata and thumbnail verification.

---

## 3. Success Metrics for v2.0
- **Moment Retain Rate**: ≥ 85% of automatically selected moments have a complete Setup ➔ Payoff arc without manual re-trimming.
- **Render Velocity**: Full 60s 1080x1920 60fps render in under 15.0 seconds using NVENC hardware acceleration.
- **Speech Accuracy**: 100% verbatim subtitle sync (zero subtitles rendered during silent gameplay pauses).
- **Editability**: 100% of video cuts, text, and emojis editable via `timeline.json` before final render.
- **Publishing Reliability**: 100% upload completion with dual-gate verification.

---

## 4. Out of Scope for Initial v2.0 Slice
- Full web GUI / Electron desktop frontend (v2.0 engine will emit standard `timeline.json` and preview frames first).
- Cloud SaaS billing, Stripe subscriptions, or multi-tenant user authentication.
- Complex 3D particle VFX (focus strictly on viral short-form typography, overlays, and game framing).
