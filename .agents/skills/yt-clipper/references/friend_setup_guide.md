# Antigravity Viral Shorts Studio — Setup & Usage Guide for Friends

Welcome! This guide explains how to set up the exact **YT-Clipper** viral shorts engine inside your own Google Antigravity setup so you can produce studio-grade 9:16 vertical clips (YouTube Shorts, TikTok, Reels) in **10 seconds** flat.

---

## 1. What This System Does

When you give Antigravity a stream URL or raw video, it automatically:
1. **Cuts & crops** the stream into a 1080x1920 vertical split-screen (facecam on top, gameplay/content on bottom) separated by a glowing neon laser seam.
2. **Generates verbatim word-timed kinetic subtitles** with Submagic styling (Impact font, multi-color dynamic words, 3-stage elastic physics spring pop, and micro-tilts).
3. **Overlays authentic full-color Apple iOS emojis** (`😭🐐`, `⚽🐐`, `🤯💔`) floating above words using a high-speed zero-lag demuxer.
4. **Adds a glassmorphism retention hook pill** at the top during the first 3.5 seconds.
5. **Renders via NVIDIA NVENC hardware acceleration** in ~10 seconds for a full 60-second video at 60fps.
6. **Organizes deliverables** cleanly into creator-specific folders (`CarryMinati/`, `IShowSpeed/`, etc.).

---

## 2. Prerequisites & Installation (One-Time Setup)

Open **PowerShell as Administrator** on your Windows PC and install the tools below:

### Step 1: Install FFmpeg (with NVENC & libass support)
If using Chocolatey:
```powershell
choco install ffmpeg -y
```
Or with Winget:
```powershell
winget install Gyan.FFmpeg
```
*Verify*: Run `ffmpeg -version` in PowerShell. Ensure `h264_nvenc` and `libass` are listed in configurations.

### Step 2: Install Python & Required Libraries
Ensure Python 3.10+ is installed:
```powershell
pip install pillow openai-whisper yt-dlp
```

### Step 3: Install the Impact Font
The default viral typography uses **Impact**. It is pre-installed on Windows at `C:\Windows\Fonts\impact.ttf`. If missing, install it from Windows Settings > Personalization > Fonts.

---

## 3. Installing the `yt-clipper` Skill into Your Antigravity

Antigravity uses Agent Skills to teach the AI assistant specialized workflows.

1. Navigate to your user's Antigravity skills directory:
   ```
   C:\Users\<YourUsername>\.gemini\config\skills\
   ```
   *(If the `skills` folder doesn't exist, create it).*

2. Create a folder named `yt-clipper`:
   ```
   C:\Users\<YourUsername>\.gemini\config\skills\yt-clipper\
   ```

3. Inside that folder, create `SKILL.md` and paste the following content:

```markdown
---
name: yt-clipper
description: Automates viral 9:16 YouTube Shorts, Instagram Reels, and TikTok creation from livestreams and videos. Features split-screen framing, verbatim word-timed kinetic subtitles (Submagic style with dynamic colors and 3-stage physics spring pop), authentic full-color Apple iOS emojis via concat demuxer, retention hook badges, and 10-second hardware NVENC rendering. Use AUTOMATICALLY whenever the user asks to create a clip, clip a stream, make a short, cut a stream, create viral video, format YouTube Short, clip IShowSpeed, CarryMinati, or any other streamer, add submagic captions, or generate shorts.
---

# YT-Clipper Production Skill

Follow the master workflow:
1. Output final video ONLY into `<CreatorName>/<clip_name>.mp4`.
2. Keep all scratch files (audio wavs, ASS scripts, raw cuts) in `trash/`.
3. Use Apple emojis from `resources/emojis/` via FFmpeg concat demuxer (`-f concat -safe 0 -i timeline.txt`).
4. Keep subtitle MarginV=880 so text sits at y=915 to 980 and emojis float at y=822.
5. Render via NVIDIA NVENC (`h264_nvenc -preset p5 -b:v 10M -maxrate 14M -bufsize 20M -r 60`) for 10-second encodes.
```

4. Refresh your Antigravity IDE (or click the refresh icon in the Skills sidebar). Antigravity will now automatically know this skill!

---

## 4. Workspace Folder Setup

In whatever folder you want to do your video clipping (e.g. `D:\YT-Clipper` or `C:\YT-Clipper`), create this clean folder structure:

```
Your-Clipper-Folder/
├── resources/
│   └── emojis/        ← Copy genuine Apple iOS PNG emojis here (160x160)
├── trash/             ← Where all temporary build/test files will live
├── docs/              ← Guides and notes
└── scripts/           ← Helper automation scripts
```

### Apple Emojis Pack:
Grab genuine Apple PNG emojis (160x160 transparent PNGs) and drop them into `resources/emojis/`:
- `goat.png`, `crying.png`, `pray.png`, `fire.png`, `skull.png`, `broken_heart.png`, `red_heart.png`, `soccer.png`, `crown.png`, `lightning.png`, `muscle.png`, `portugal.png`, etc.

---

## 5. How to Tell Antigravity to Make Clips for You

Once this is set up, you don't need to write manual FFmpeg commands or Python scripts. You simply open your workspace in Antigravity and prompt it like a $1,000,000,000 salary editor:

### Example Prompts:

#### Example 1: Stream URL with Timestamps
> *"Clip this stream from 15:02 to 16:02 for IShowSpeed: https://www.youtube.com/live/9aPR9UXI1kY. Make a 60-second viral YouTube Short with Submagic dynamic subtitles, Apple emojis, a hook badge, and save it in the IShowSpeed folder."*

#### Example 2: From a Local Video
> *"Take the file `trash/raw_gameplay.mp4`. It has CarryMinati reacting to a jumpscare from 00:30 to 01:00. Create a 30s viral short with facecam on top, gameplay on bottom, neon laser seam, animated captions, and save it in CarryMinati folder."*

Antigravity will automatically:
1. Cut the segment.
2. Transcribe verbatim with Whisper.
3. Build the ASS kinetic subtitle script.
4. Composite the Apple emojis using the concat demuxer.
5. Run the NVENC master render in ~10 seconds.
6. Deliver a clickable video link and YouTube viral title/tags!

---

## 6. Golden Rules & Traps to Avoid

If you or your Antigravity ever run into issues, remember these 5 engineering laws:

1. **Why multiple image loops freeze FFmpeg**: Never chain multiple `-loop 1 -i image.png` inputs in FFmpeg. It causes memory buffer deadlocks on Windows and freezes at frame 39. Always use the **Concat Demuxer** (`-f concat -safe 0 -i timeline.txt`).
2. **Why Python scripts hang on FFmpeg**: When calling FFmpeg from Python `subprocess.run()`, never pass `capture_output=True`. The Windows stderr pipe is only 4KB and deadlocks when FFmpeg prints frame progress. Always redirect to a log file (`stdout=f, stderr=f`).
3. **Why emojis look black & white**: libass on Windows DirectWrite does not render color glyphs in fonts like Impact. Never put emoji unicode in ASS dialogue lines. Always composite Apple PNG emojis as transparent image overlays.
4. **Intermediate overlay `:shortest=1` trap**: Never put `:shortest=1` on an intermediate overlay filter—it kills the entire video stream when that overlay ends! Use `:eof_action=pass`.
5. **Collision prevention**: Subtitles should have `MarginV=880` in ASS so they sit at `y=915 to 980`. Apple emoji pairs sit at `y=822 to 902`. This gives 15px of clean separation so they never overlap.
