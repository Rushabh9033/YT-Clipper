# DECISIONS.md — Architectural & Product Decision Log

---

## DECISION-001: Autonomous Browser Playwright vs YouTube Data API v3
- **Date:** 2026-11-18
- **Context:** YouTube API v3 enforces a strict daily upload quota (10,000 units/day, where each upload costs 1,600 units = max 6 uploads/day) and requires GCP API key verification and OAuth refresh tokens that expire.
- **Options Considered:**
  - A. YouTube Data API v3 (REST OAuth2)
  - B. Third-party SaaS automation (Zapier / Make.com)
  - C. Autonomous Playwright Chrome Automation with persistent profile
- **Chosen:** Option C (Playwright Automation)
- **Reason:** Completely free, zero API quota limitations, supports unlimited daily 4K/60fps uploads, and supports direct injection of custom thumbnails and video edit page verification.
- **Tradeoffs:** Dependent on YouTube Studio web UI selectors; mitigated by Rule §7 Dual-Gate Verification.

---

## DECISION-002: Adoption of YT-Clipper 2.0 AI Video Production Studio Architecture
- **Date:** 2026-11-18
- **Context:** Basic clippers produce mediocre, black-box clips without understanding context or giving creators edit control. Creators need editorial context (Setup ➔ Payoff) and non-destructive timeline control.
- **Options Considered:**
  - A. Maintain v1.0 monolithic script (`clip_generator.py` direct hardcoded encode).
  - B. Adopt YT-Clipper 2.0: Modular Editorial Director + Multitrack `timeline.json` Project File + NVENC Timeline Compiler.
- **Chosen:** Option B (YT-Clipper 2.0)
- **Reason:** Separates AI moment discovery and layout design from the rendering step. Creators can inspect and tweak words, emojis, crops, and timing without re-running transcription or expensive AI pipelines.
- **Tradeoffs:** Requires formalizing a timeline JSON intermediate representation before calling FFmpeg.
- **Reversibility:** Easy (v1 direct render scripts remain functional as fallback).
