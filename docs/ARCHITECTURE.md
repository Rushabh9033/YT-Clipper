# YT-Clipper — Technical Architecture

Detailed technical architecture and coordinate layout for the YT-Clipper video engine.

---

## 1. Coordinate & Visual Layout (1080x1920)

```
y = 0     ┌──────────────────────────────────────────────┐
          │                                              │
          │         TOP PANE: STREAMER FACECAM           │
          │              (1080x810, 60fps)               │
          │                                              │
y = 692   │      ┌───────────────────────────────┐       │
          │      │   HOOK PILL (0.0s - 3.5s)     │       │
y = 768   │      └───────────────────────────────┘       │
          │                                              │
y = 806   ╞══════════════════════════════════════════════╡  ◄── Neon Seam (8px, #FFE500)
y = 814   │                                              │
y = 822   │             ┌─────────────────┐              │
          │             │ APPLE EMOJI PAIR│              │
y = 902   │             └─────────────────┘              │
          │                                              │
y = 915   │          DYNAMIC SUBMAGIC SUBTITLES          │
y = 980   │      ("162 GOALS BRO!", Spring Pop, Tilts)   │
          │                                              │
          │        BOTTOM PANE: GAMEPLAY / SCREEN        │
          │              (1080x1110, 60fps)              │
          │                                              │
          │                                              │
y = 1920  └──────────────────────────────────────────────┘
```

---

## 2. Mathematical Geometry Breakdown

| Element | Geometry & Calculation | Coordinates | Purpose |
| :--- | :--- | :--- | :--- |
| **Top Reaction Pane** | `crop=480:540:0:540,scale=1080:810,setsar=1` | `(0, 0)` to `(1080, 810)` | Zooms and scales facecam to upper vertical third. |
| **Bottom Content Pane** | `crop=1280:960:600:60,scale=1080:1110,setsar=1` | `(0, 810)` to `(1080, 1920)` | Isolates gameplay, completely cutting out duplicate streamer corner. |
| **Studio Laser Seam** | `color=c=0xFFE500:s=1080x8:r=60:d=60` | `(0, 806)` to `(1080, 814)` | Professional 8px dividing line with 100% opacity. |
| **Glassmorphism Hook Pill** | `(text_w + 182) x 76`, radius=24, outline 4px `#FFE500` | Center-X, `y=692` | Hooks viewers during the critical 0.0s - 3.5s retention window. |
| **Apple Color Emojis** | `162 x 80` (two 76x76 emojis side by side) | `x=459, y=822` | Floats directly above subtitle text with zero overlap. |
| **Kinetic Subtitles** | `Impact 64pt, MarginV=880, Alignment=2` | Center-X, `y=915 to 980` | High-impact punch words with 3-stage physics spring pop. |

---

## 3. Concat Demuxer Engine Architecture

Chaining individual `-loop 1` inputs causes Windows FFmpeg to allocate huge FIFO buffers per input stream. When `enable` gates an input in the future, FFmpeg halts demuxing for active streams, causing a catastrophic process freeze at frame 39 (approx. 0.65s).

The **Concat Demuxer Architecture** bypasses this by feeding all emoji states through a single sequential stream:
- **Blank Gaps**: A 162x80 transparent PNG displayed for the exact duration between speech punches.
- **Active Emojis**: A 162x80 composite PNG of two authentic Apple iOS emojis displayed during the speech punch.
- **Single Demuxer Input**: FFmpeg sees `[2:v]` as a standard continuous video stream, advancing frame-by-frame with zero queue backlog.

```
Time:   0.0s ─── 2.5s ─── 4.8s ─── 7.6s ─── 10.2s ─── 12.3s ─── ... ─── 60.0s
Stream: [Blank]   [🤯💔]  [Blank]   [⚽🐐]   [Blank]    [🇵🇹🔥]           [Blank]
Dur:    2.500s    2.300s  2.800s    2.600s   2.100s     2.500s           ...
```

---

## 4. Hardware NVENC Profile

```
-c:v h264_nvenc
-preset p5
-b:v 10M
-maxrate 14M
-bufsize 20M
-r 60
-c:a aac
-b:a 192k
```
- **Throughput**: ~336 fps on modern NVIDIA RTX GPUs.
- **Speed Factor**: 5.6x real-time speed.
- **Master Duration**: Exact 60.000000s with zero audio/video timestamp drift.

---

## 5. Automated YouTube Studio Uploader & Dual-Gate Verification Architecture

```
[Raw MP4 + Thumb] ──► [Step 3: Select File] ──► [Background HTTP Stream Initiated]
                                                           │
┌──────────────────────────────────────────────────────────┘
▼
[Step 4-9: Inject Title, Tags, Visibility=PUBLIC]
│
▼
[Step 10: 100% Upload Completion Loop] ◄── Polling `ytcp-video-upload-progress`
│ (MUST reach "Upload complete ... Processing will begin shortly", never exit on "Uploading X%")
▼
[Step 11: Click Publish]
│
▼
[Step 12: Close Post-Upload Dialog & Extract Video ID]
│
▼
[Step 13: Content List Audit] ◄── Verify row status is Public / Processing on `studio.youtube.com/.../videos/short`
│
▼
[Step 14: Dual-Gate Metadata Audit] ◄── Navigate to `studio.youtube.com/video/<id>/edit`
│  ├─ Verify & Inject Description with hashtags via `div#textbox[aria-label*='Tell viewers']`
│  ├─ Verify & Set Custom 9:16 Thumbnail via `input#file-loader`
│  └─ Click Save & Verify disabled state
▼
[100% Verified Published] ──► User Notification with Live Link & Evidence Screenshot
```
