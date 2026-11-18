# TASKS.md — YT-Clipper 2.0 Vertical Slice Execution Ledger

---

## TASK-001: Non-Destructive Multitrack Timeline Engine (`timeline.json` & Compiler)
- **Status:** [x] DONE
- **North Star:** Define a standardized non-destructive multitrack project timeline schema (`timeline.json`) and a Python compiler that parses it into our ultra-fast NVENC FFmpeg pipeline.
- **Slice:**
  - [x] Schema: Design `timeline.json` specification supporting tracks: Video (Facecam/Gameplay), Audio, Subtitles, Emojis, and Hook Pill.
  - [x] Engine: Implement `scripts/timeline_compiler.py` that translates `timeline.json` into an optimized FFmpeg filtergraph.
  - [x] Non-Destructive Test: Edit subtitle text, emoji sticker, and color in `timeline.json` and re-compile in 2.29 seconds without touching source video.
  - [x] Edge Cases: Windows colon path escaping in subtitles filter, 60fps image input deadlock solved via `-framerate 60`.
  - [x] Verification (L3): Rendered 1080x1920 @ 60fps master short in 1.90s at ~250 FPS.

---

## TASK-002: Intelligent Editorial Director (Narrative Arc & Context Boundary Engine)
- **Status:** [ ] TODO
- **North Star:** Analyze video transcripts and audio peaks to detect complete Setup ➔ Action ➔ Reaction ➔ Payoff moments with automatic lead-in/lead-out padding.
- **Slice:**
  - [ ] Heuristic & LLM Scoring: Identify story arc boundaries rather than arbitrary time cuts.
  - [ ] Boundary Padding: Ensure payoff reaction (laughter, desk slam, victory) is never severed.
  - [ ] Transparent Rationale: Output rationale log explaining why the candidate was selected.
  - [ ] Test on real stream footage (`irNhWMG560k`).

---

## TASK-003: Gaming Intelligence HUD & Event Profiler
- **Status:** [ ] TODO
- **North Star:** Game-aware HUD recognition profiles (GTA 6, BGMI, Valorant) to trigger dynamic zooms on mini-map, scoreboard, or killfeed during high-tension gameplay.
- **Slice:**
  - [ ] Configurable Game Profiles in `resources/game_profiles/`.
  - [ ] Dynamic zoom keyframing in `timeline.json`.
  - [ ] Test on GTA 6 chase footage.
