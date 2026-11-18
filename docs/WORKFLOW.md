# YT-Clipper — Master Production Workflow

The definitive guide to generating viral, high-retention 9:16 YouTube Shorts, Instagram Reels, and TikToks from livestreams and long-form videos. Built for speed, flawless execution, and cinema-grade aesthetics.

---

## 1. Pipeline Overview

```
[Raw Stream / VOD] 
       │
       ▼ (yt-dlp cut)
[Raw Cut (trash/raw_*.mp4)] ──► [Whisper Word-Level Alignment]
       │                                     │
       ▼                                     ▼
[Split-Screen Crop & Stack]         [Kinetic ASS Subtitles (Multi-color + Spring Pop)]
       │                                     │
       ├─────────────────────────────────────┘
       ▼
[Apple Color Emoji Concat Demuxer (resources/emojis/)]
       │
       ▼
[NVIDIA NVENC Hardware Master Encode (10.7s render @ 336 fps)]
       │
       ▼
[Creator Folder Output: D:\YT-Clipper\<Creator>\<clip>.mp4]
```

---

## 2. Directory Architecture & Hygiene

All files strictly follow this hierarchy:

```
D:\YT-Clipper/
├── <CreatorName>/             # Final production-ready master deliverables ONLY
│   ├── CarryMinati/
│   │   ├── short_1_mummy_grenade.mp4
│   │   ├── short_2_jumpscare_rage.mp4
│   │   └── short_60s_mummy_clutch_complete.mp4
│   └── IShowSpeed/
│       ├── speed_short_1_ronaldo_retires.mp4
│       └── speed_short_2_zelda_chicken_death.mp4
│
├── resources/                 # Permanent, reusable production assets
│   └── emojis/                # 36+ authentic Apple iOS 160x160 full-color PNGs
│       ├── goat.png, crying.png, fire.png, skull.png, ...
│
├── trash/                     # ALL intermediate and build files (never in root)
│   ├── *.py                   # Build scripts & scratch runners
│   ├── *.bat                  # Generated FFmpeg execution batches
│   ├── *.ass                  # Subtitle files
│   ├── *.wav                  # Extracted audio stems for Whisper
│   ├── *.txt                  # Concat demuxer timelines
│   ├── raw_*.mp4              # Raw downloaded cuts
│   └── *.jpg / *.png          # Verification frames & emoji pair composites
│
└── docs/                      # Documentation, memory, and specifications
    ├── WORKFLOW.md            # This master guide
    ├── ARCHITECTURE.md        # Technical engine specifications
    ├── RULES.md               # Folder and execution constraints
    └── MEMORY.md              # Live project snapshot
```

---

## 3. The 7-Step Production Workflow

### Step 1: Viral Moment Identification
Look for high-arousal emotional peaks:
- **Unhinged Rage / Screaming**: Streamer slamming desk, dying to weak mobs (e.g. Zelda chicken).
- **Deep Emotional Tribute**: Streamer breaking into tears over their idol (e.g. Speed crying for Ronaldo).
- **Clutch or Epic Fail**: Last-second bomb defusal, team wipe, accidental teamkill.
- **Duration**: Uncapped up to 60.0 seconds. 60 seconds maximizes YouTube Shorts algorithm watch time.

### Step 2: High-Quality Stream Cutting
Extract exact section at 1080p60:
```powershell
yt-dlp -f "bv*[height<=1080]+ba/b" --downloader ffmpeg --downloader-args "ffmpeg_i:-ss 00:15:02.000 -to 00:16:02.000" "https://www.youtube.com/live/..." -o "D:/YT-Clipper/trash/raw_speed.mp4"
```

### Step 3: Verbatim Acoustic Transcription (Zero Latency)
Extract audio and run Whisper with word-level timestamps:
```python
import whisper
model = whisper.load_model("base")
result = model.transcribe("trash/audio.wav", word_timestamps=True)
```
- **Rule**: Never summarize, clean up, or alter spoken grammar. Verbatim speech preserves authentic streamer charisma.
- **Microsecond Timing**: Anchor subtitle start times to the acoustic rise edge of the first word.

### Step 4: Kinetic Typography (Submagic Style)
Author `.ass` subtitles with dynamic styling:
- **Font**: Impact (bold, condensed, maximum readability). Size: 64pt.
- **Thick Stroke & Shadow**: 8px pure black outline (`&H00000000`), 4px 3D drop shadow (`&H80000000`).
- **Dynamic Palette**: Vary colors per punch word:
  - Cyan: `{\c&H00E5FF&}` (emphasis / technical terms)
  - Yellow: `{\c&HFFF500&}` (high-energy words)
  - Crimson: `{\c&H441EFF&}` (rage, intensity, names)
  - Green: `{\c&H76E600&}` (country, money, success)
  - Gold: `{\c&H00D7FF&}` (GOAT, tribute, glory)
  - White: `{\c&HFFFFFF&}` (base connector words)
- **3-Stage Elastic Spring Pop**:
  `{\t(0,70,\fscx125\fscy125)\t(70,140,\fscx100\fscy100)}`
- **Micro-Tilts**:
  `{\frz-2}` or `{\frz2}` on energetic phrases.
- **Vertical Spacing**: Set `MarginV=880` (Alignment 2) so text stays in `y=915 to 980`, leaving `y=822 to 902` clear for emojis.

### Step 5: Full-Color Apple Emojis via Concat Demuxer
*Never use libass text glyphs for emojis*—DirectWrite renders them monochrome black and white.

1. Pre-render 162x80 transparent PNG pairs of genuine Apple iOS emojis from `resources/emojis/`.
2. Generate an `emojis_timeline.txt` using the FFmpeg `concat` demuxer:
```
ffconcat version 1.0
file 'D:/YT-Clipper/trash/blank_pair.png'
duration 2.500
file 'D:/YT-Clipper/trash/em_pair_00.png'
duration 2.300
file 'D:/YT-Clipper/trash/blank_pair.png'
duration 2.800
...
file 'D:/YT-Clipper/trash/blank_pair.png'
duration 5.000
file 'D:/YT-Clipper/trash/blank_pair.png'
```
3. Overlay onto the video stream with `overlay=459:822:eof_action=pass`.
- **Result**: Exactly ONE stream input. Zero memory buffer bloat. No multi-input deadlocks.

### Step 6: Split-Screen Canvas & Retention Hook
- **Canvas Resolution**: 1080x1920 (9:16 vertical).
- **Top Reaction Pane**: `crop=480:540:0:540,scale=1080:810,setsar=1` (facecam zoomed to fill top).
- **Bottom Stream Pane**: `crop=1280:960:600:60,scale=1080:1110,setsar=1` (screen content without duplicate streamer).
- **Studio Neon Seam**: 8px electric yellow laser divider (`0xFFE500`) at `y=806`.
- **Glassmorphism Hook Pill**: Active for first 3.5s at `(pill_x, 692)`:
  - Dark glass background `(10, 10, 16, 230)` with neon yellow border `(255, 229, 0)`.
  - Impact 42pt hook text + Apple emojis (e.g. `NO WAY BRO HE RETIRED?! 🇵🇹🐐`).
  - Overlay: `overlay=pill_x:692:eof_action=pass`.

### Step 7: Hardware NVENC Encode
Encode the master video at maximum speed:
```bash
ffmpeg -y \
  -ss 00:00:00.000 -t 60.0 -i raw_cut.mp4 \
  -t 3.5 -loop 1 -i hook_pill.png \
  -f concat -safe 0 -i emojis_timeline.txt \
  -filter_complex "[0:v]crop=...[top];[0:v]crop=...[bot];[top][bot]vstack[stacked];color=...[seam];[stacked][seam]overlay=0:806:shortest=1[vseam];[vseam]subtitles=subtitles.ass[vsub];[vsub][1:v]overlay=...:eof_action=pass[vhook];[vhook][2:v]overlay=459:822:eof_action=pass[vemo];[vemo]eq=saturation=1.18:contrast=1.06:brightness=0.01[final_v]" \
  -map "[final_v]" -map 0:a \
  -c:v h264_nvenc -preset p5 -b:v 10M -maxrate 14M -bufsize 20M -r 60 \
  -c:a aac -b:a 192k \
  -t 60.0 \
  "D:/YT-Clipper/<Creator>/output.mp4"
```
**Performance Benchmark**: 60-second video rendered in **10.7 seconds** (336 fps average).

---

## 4. Critical Engineering Laws & Trap Prevention

| Issue | Root Cause | Golden Rule Solution |
| :--- | :--- | :--- |
| **FFmpeg Freezes on Frame 39** | Chaining multiple `-loop 1 -i image.png` inputs without consumed timestamps causes demuxer FIFO buffer overflow (3.8GB RAM deadlock). | **Use the `concat` demuxer (`-f concat -safe 0 -i timeline.txt`).** Generates a single, lightweight stream with zero buffer bloat. |
| **Monochrome Emojis (B&W Glyphs)** | `libass` on Windows with DirectWrite strips color bitmap layers from fonts like Impact and tints them white. | **Never put emoji characters in ASS dialogue.** Pre-render Apple iOS PNGs and overlay via `concat`. |
| **Premature Video Termination** | Using `:shortest=1` on an intermediate overlay filter terminates the entire graph when that overlay window ends. | **Only use `shortest=1` on infinite sources (like `color`).** On image/emoji overlays, use `:eof_action=pass`. |
| **Python Script Deadlock** | `subprocess.run(cmd, capture_output=True)` fills the 4KB Windows OS pipe buffer when FFmpeg writes frame progress to `stderr`. | **Redirect stdout and stderr to a log file or `DEVNULL`:** `with open("render.log", "w") as f: subprocess.run(cmd, stdout=f, stderr=f)`. |
| **Audio Filter Deadlock** | `dynaudnorm` looks ahead for `s=8` seconds of audio, stalling video packets and creating cross-stream filter deadlock. | **Do not chain `dynaudnorm` inside complex multi-overlay filtergraphs.** Keep stream audio clean with standard `aac` encoding. |
| **Overlay Overlapping Subtitles** | Placing emojis at `y=825` when subtitles are at `MarginV=950` causes 2-line subtitles to collide with the emojis. | **Set `MarginV=880` in ASS.** Subtitles sit comfortably at `y=915 to 980`, while emojis sit at `y=822 to 902`. |
