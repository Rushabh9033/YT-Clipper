---
name: yt-clipper
description: Automates viral 9:16 YouTube Shorts, Instagram Reels, and TikTok creation from livestreams and videos. Features split-screen framing, verbatim word-timed kinetic subtitles (Submagic style with dynamic colors and 3-stage physics spring pop), authentic full-color Apple iOS emojis via concat demuxer, retention hook badges, and 10-second hardware NVENC rendering. Use AUTOMATICALLY whenever the user asks to create a clip, clip a stream, make a short, cut a stream, create viral video, format YouTube Short, clip IShowSpeed, CarryMinati, or any other streamer, add submagic captions, or generate shorts.
---

# YT-Clipper — Master Viral Short Production Skill

Expert workflow for generating viral, high-retention 9:16 portrait video clips (YouTube Shorts, TikTok, Reels) from long-form livestreams and VODs.

---

## 1. Directory Structure & File Routing

Always enforce the project folder architecture:

- Final deliverables: `D:\YT-Clipper\<CreatorName>\<clip_name>.mp4`
- Permanent assets: `D:\YT-Clipper\resources\emojis\` (genuine Apple iOS 160x160 full-color PNGs)
- Intermediate / temporary files: `D:\YT-Clipper\trash\` (raw cuts, wav audio stems, ASS subtitles, sample jpgs, batch files)
- Root directory `D:\YT-Clipper\` MUST remain clean (only folders, zero loose files).

---

## 2. Core Video Architecture (1080x1920 @ 60fps)

Every short is composed of 4 key layers:

1. **Split-Screen Canvas**:
   - **Top Reaction Pane (1080x810)**: `crop=480:540:0:540,scale=1080:810,setsar=1` (zooms in on streamer facecam).
   - **Bottom Content Pane (1080x1110)**: `crop=1280:960:600:60,scale=1080:1110,setsar=1` (isolates gameplay/reaction, removing duplicate streamer facecam).
   - **Studio Neon Laser Seam**: 8px electric yellow divider (`0xFFE500`) at `y=806`.

2. **Retention Hook Pill (Active 0.0s to 3.5s)**:
   - Positioned at `(center_x, 692)` in the upper reaction pane.
   - Glassmorphism dark background with 4px neon yellow border, Impact 42pt text, and two high-res Apple emojis (e.g. `NO WAY BRO HE RETIRED?! 🇵🇹🐐`).

3. **Full-Color Apple Emojis (Floating at y=822 to 902)**:
   - Never embed emojis into ASS text (libass DirectWrite renders them as black & white monochrome glyphs).
   - Pre-render 162x80 PNG pairs of Apple emojis.
   - Use the **FFmpeg Concat Demuxer** (`-f concat -safe 0 -i emojis_timeline.txt`) to sequence emoji pairs and transparent blank gaps with zero queue deadlock.
   - Overlay at `x=459, y=822:eof_action=pass`.

4. **Kinetic Typography (Submagic Style at y=915 to 980)**:
   - Font: `Impact 64pt`, `MarginV=880`, `Alignment=2`.
   - 8px pure black outline (`&H00000000`), 4px 3D drop shadow (`&H80000000`).
   - 3-stage physics spring pop: `{\t(0,70,\fscx125\fscy125)\t(70,140,\fscx100\fscy100)}`.
   - Dynamic colors per spoken phrase:
     - Cyan: `{\c&H00E5FF&}`
     - Yellow: `{\c&HFFF500&}`
     - Crimson: `{\c&H441EFF&}`
     - Green: `{\c&H76E600&}`
     - Gold: `{\c&H00D7FF&}`
     - White: `{\c&HFFFFFF&}`
   - Verbatim spoken words (100% acoustic alignment with zero latency).

---

## 3. High-Speed Encoding Recipe

Run via NVIDIA NVENC hardware encoder:

```bash
ffmpeg -y \
  -ss 00:00:00.000 -t 60.0 -i "D:/YT-Clipper/trash/raw_cut.mp4" \
  -t 3.5 -loop 1 -i "D:/YT-Clipper/trash/hook_pill.png" \
  -f concat -safe 0 -i "D:/YT-Clipper/trash/emojis_timeline.txt" \
  -filter_complex "[0:v]crop=480:540:0:540,scale=1080:810,setsar=1[top];[0:v]crop=1280:960:600:60,scale=1080:1110,setsar=1[bot];[top][bot]vstack=inputs=2[stacked];color=c=0xFFE500:s=1080x8:r=60:d=60[seam];[stacked][seam]overlay=0:806:shortest=1[vseam];[vseam]subtitles=D\\:/YT-Clipper/trash/subtitles.ass[vsub];[vsub][1:v]overlay=236:692:eof_action=pass[vhook];[vhook][2:v]overlay=459:822:eof_action=pass[vemo];[vemo]eq=saturation=1.18:contrast=1.06:brightness=0.01[final_v]" \
  -map "[final_v]" -map 0:a \
  -c:v h264_nvenc -preset p5 -b:v 10M -maxrate 14M -bufsize 20M -r 60 \
  -c:a aac -b:a 192k \
  -t 60.0 \
  "D:/YT-Clipper/<Creator>/output.mp4"
```

**Benchmark**: Encodes a full 60.0-second 1080x1920 60fps clip in **10.7 seconds** (336 fps average).

---

## 4. Critical Engineering Rules & Bug Prevention

1. **Never Chain Multiple `-loop 1` Inputs**: Chaining multiple `-loop 1` video inputs creates queue buffer deadlocks in Windows FFmpeg (process hangs at frame 39 with 3.8GB memory). Always sequence image overlays using the `concat` demuxer.
2. **Never Use `capture_output=True` in Python**: When running FFmpeg via `subprocess.run()`, `capture_output=True` deadlocks on the 4KB Windows OS stderr pipe buffer. Redirect output to a log file or `DEVNULL`.
3. **Never Put `shortest=1` on Intermediate Overlays**: `:shortest=1` will kill the entire video the instant that overlay ends. Only use `:shortest=1` on unbounded color generators. Use `:eof_action=pass` on image overlays.
4. **Never Use `dynaudnorm` with Multi-Overlay Filtergraphs**: `dynaudnorm` looks ahead for seconds of audio, creating a cross-stream lock with the video demuxer.
5. **Keep MarginV=880**: Never place subtitles at MarginV=950 when emoji overlays are at `y=822`, otherwise two-line captions will collide with emojis. MarginV=880 leaves 15px of clean separation.
6. **Sample-Accurate Live HLS Synchronization**: When clipping live YouTube streams, never slice audio and video arrays by independent indices. Always match sequence numbers (`/sq/<id>/`) and Program-Date-Time across both manifests to guarantee sub-frame acoustic sync.

---

## 5. Mandatory Clip Delivery Package

With EVERY generated clip, the agent must ALWAYS generate and deliver:
1. **3x High-CTR Viral Titles**: Curated with emojis and curiosity hooks.
2. **Complete SEO Video Description**: Streamer credits, timestamps, algorithm keywords, and subscribe call-to-actions.
3. **Viral Hashtags**: Ready-to-use tags (#shorts, #gta6, etc.).
4. **YouTube Studio Tags Box**: Full comma-separated tag list.
5. **Pinned Engagement Comment**: Question prompt to trigger viewer discussion.
6. **Custom Thumbnail Files**:
   - **9:16 Vertical Cover** (`<clip>_thumb.jpg`, 1080×1920) for Shorts, Reels, and TikTok covers.
   - **16:9 Widescreen Thumbnail** (`<clip>_thumb_16x9.jpg`, 1280×720) for standard YouTube video uploads and community posts.

---

## 6. Mandatory Upload Completion Notification Law

Whenever an automated upload to YouTube is performed, the agent must **ALWAYS notify the user immediately upon completion**:
1. Provide the direct live clickable YouTube link (`https://www.youtube.com/shorts/<id>`).
2. Provide confirmation of video title, public visibility, and attached thumbnail.
3. Link all local deliverables.
4. Record the video ID and status in `docs/CLIPS_REGISTRY.md` and `docs/MEMORY.md`.
5. Never finish silently without presenting the final live publication report.

---

## 7. Zero-Defect Upload Verification Law (NEVER CUT OFF UPLOADS OR MISS METADATA)

To guarantee that uploads never stall mid-stream and never publish with blank descriptions or missing thumbnails:
1. **100% Raw File Streaming Guarantee**:
   - The uploader must actively poll `ytcp-video-upload-progress` and never click Publish or close browser contexts while the status indicates `Uploading X%`.
   - The browser socket must remain open until YouTube confirms `Upload complete ... Processing will begin shortly` or `Checks complete`.
2. **Mandatory Metadata & Hashtags Enforcement**:
   - Description must ALWAYS be injected with exact YouTube Studio selector targeting `div#textbox[aria-label*='Tell viewers' i]` (not just generic `description`).
   - Description must contain hook narrative, credit, subscribe CTA, and viral hashtags (`#shorts #gta6 #carryminati ...`).
3. **Mandatory Thumbnail Attachment**:
   - High-CTR custom thumbnail (`_thumb.jpg`) must ALWAYS be injected via `input#file-loader, input[accept*='image']`.
4. **Dual-Gate Post-Upload Audit**:
   - After publishing, the script must verify the video row in YouTube Studio's content list (`https://studio.youtube.com/.../videos/short`) to confirm `Public` or `Processing` status.
   - The script must automatically navigate to `https://studio.youtube.com/video/<video_id>/edit` to audit that both Description and Thumbnail are active. If missing, it immediately injects them and saves before exiting.
5. **Zero Premature Exits**: No script may exit based on reasoning or early dialogs. Only verified post-upload state confirms completion.

