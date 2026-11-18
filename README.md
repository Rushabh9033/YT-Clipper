# 🎬 YT-Clipper — Autonomous Viral Shorts Creation & Publishing Engine

> **Turn any YouTube livestream or long-form video into viral, high-retention 9:16 Shorts (TikTok, Instagram Reels, YouTube Shorts) with 10-second hardware NVENC rendering and 100% free automated YouTube Studio publishing.**

---

## ⚡ Key Features

1. **Split-Screen Dynamic Framing (1080x1920 @ 60fps)**:
   - **Top Pane**: Facecam reaction crop (`1080x810`).
   - **Bottom Pane**: High-action gameplay/content crop (`1080x1110`).
   - **Studio Laser Seam**: Neon electric dividing line (`0xFFE500`).
2. **Submagic-Style Kinetic Subtitles**:
   - `Impact 64pt` font, 8px black stroke, 4px 3D drop shadow.
   - Dynamic 3-stage physics spring-pop animation on punch phrases.
   - Multi-color highlighting (Cyan, Neon Yellow, Crimson, Lime Green).
   - **100% Acoustic Speech Alignment**: Captions appear strictly when the streamer speaks. Silent gameplay pauses remain clean.
3. **Genuine Full-Color Apple iOS Emojis**:
   - High-resolution Apple emoji PNGs float above dialogue via FFmpeg's Concat Demuxer with zero buffer deadlocks.
4. **Instant 0.0s - 3.5s Retention Hook Badge**:
   - Eye-catching glassmorphism pill with neon accents grabbing viewer attention before the swipe.
5. **Ultra-Fast NVIDIA NVENC Hardware Encoding**:
   - Full 60.0-second 1080x1920 60fps master render in **10.5 seconds** (~350 FPS).
6. **Automated Free YouTube Studio Uploader (No API Quotas)**:
   - Headless Playwright automation using your persistent local Chrome profile.
   - **100% Upload Completion Guarantee**: Actively streams until YouTube confirms raw bytes are 100% uploaded before publishing.
   - **Dual-Gate Verification**: Audits and injects Title, Description with hashtags, Tags, and Custom 9:16 Cover directly into YouTube Studio.

---

## 📁 Project Architecture

```text
YT-Clipper/
├── CarryMinati/               ← Production-ready master Shorts & custom thumbnails
│   ├── carry_short_gta6_police_chase.mp4
│   ├── carry_short_gta6_police_chase_thumb.jpg
│   ├── carry_short_gta6_selfie.mp4
│   ├── carry_short_gta6_selfie_thumb.jpg
│   └── carry_short_gta6_plane_escape.mp4
├── IShowSpeed/                ← Master IShowSpeed Shorts & thumbnails
├── resources/
│   ├── emojis/                ← Genuine full-color Apple iOS emoji assets (37+ icons)
│   └── branding/              ← Channel avatars, banners, and logos
├── scripts/
│   ├── clip_generator.py          ← Core clip generation engine
│   ├── youtube_studio_uploader.py ← Automated YouTube Studio uploader
│   ├── upload_selfie_short.py     ← Dedicated short upload runner
│   └── login_youtube.bat          ← Helper to open login browser
├── docs/                      ← Master documentation
│   ├── ARCHITECTURE.md        ← Technical geometry & filtergraph architecture
│   ├── CLIPS_REGISTRY.md      ← Anti-duplication ledger & blacklisted moments
│   ├── RULES.md               ← Master engineering laws (Laws §1 to §7)
│   └── MEMORY.md              ← Current project status & live links
├── requirements.txt           ← Python dependencies
└── README.md                  ← Quick start guide
```

---

## 🚀 Quick Start Guide for Friends

### 1. Prerequisites
- **Operating System**: Windows 10/11 (or Linux/macOS with minor path adjustments).
- **Python**: Python 3.10+ ([Download Python](https://www.python.org/downloads/)).
- **FFmpeg**: Ensure FFmpeg is installed and added to your system `PATH` ([Gyan.dev FFmpeg Build](https://www.gyan.dev/ffmpeg/builds/)).
  - Verify in terminal: `ffmpeg -version`
- **NVIDIA GPU** *(Recommended)*: For instant 10s NVENC rendering (`h264_nvenc`). Fallback to CPU (`libx264`) supported.

---

### 2. Installation
Open terminal / command prompt inside the extracted folder:

```bash
# 1. Install python dependencies
pip install -r requirements.txt

# 2. Install Playwright browser binaries
playwright install chromium
```

---

### 3. One-Time YouTube Studio Login (100% Free)
Log into your YouTube channel once. Playwright saves your session securely in `resources/browser_profile/` so you never have to log in again:

```bash
python scripts/youtube_studio_uploader.py --login
```
1. A Chrome browser window will open.
2. Sign into your Google / YouTube account and navigate to YouTube Studio.
3. Close the browser window when done. Your authentication is saved!

Check your status at any time:
```bash
python scripts/youtube_studio_uploader.py --status
```

---

### 4. Uploading Any Short Automatically
To upload any vertical short with full metadata, viral hashtags, and custom cover:

```bash
python scripts/youtube_studio_uploader.py \
  --video "CarryMinati/carry_short_gta6_police_chase.mp4" \
  --thumbnail "CarryMinati/carry_short_gta6_police_chase_thumb.jpg" \
  --title "CARRYMINATI GTA 6 CRAZY POLICE CHASE ESCAPE! 🚨🏎️💨 #shorts" \
  --description "CarryMinati gets into an insane 2-star police chase in GTA 6! #shorts #gta6" \
  --tags "gta6, carryminati, gaming, shorts" \
  --visibility public \
  --headless
```

The script will:
- Stream 100% of the raw file to YouTube.
- Advance through wizard checks.
- Set Public visibility.
- Audit and save description, hashtags, and custom thumbnail on the edit page.
- Print your live clickable link (`https://youtube.com/shorts/...`).

---

## 🌟 Live Published Examples From This Engine
- **Short 7 (Police Chase Escape):** [https://youtube.com/shorts/1otgHdqrUKk](https://youtube.com/shorts/1otgHdqrUKk)
- **Short 6 (First GTA 6 Selfie):** [https://youtube.com/shorts/i8GcRlxjLJE](https://youtube.com/shorts/i8GcRlxjLJE)
- **Short 5 (Plane Crash Water Landing):** [https://youtube.com/shorts/w4yhIDy88vw](https://youtube.com/shorts/w4yhIDy88vw)

---

## 📜 Engineering Laws
Read [docs/RULES.md](docs/RULES.md) for strict architectural rules:
- **Law §3:** Vertical 9:16 Canvas, Apple iOS emojis, Concat demuxer overlays, 8px neon seam.
- **Law §5:** Clip Blacklist Non-Duplication Law (never re-clip the same timestamp range).
- **Law §6:** Mandatory Immediate Upload Notification Law.
- **Law §7:** Zero-Defect Upload Verification Law (100% file transfer + dual-gate audit).
