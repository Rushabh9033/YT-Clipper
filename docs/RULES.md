# YT-Clipper — Master Rules & Engineering Laws

## 1. Directory Structure Law (MANDATORY)
Every file in `D:\YT-Clipper` must adhere to strict hierarchical categorization:

```
D:\YT-Clipper\
├── [CreatorName]/         ← Final, production-ready master Shorts for this creator ONLY
├── resources/             ← Permanent, reusable assets (Apple color emojis, sound FX)
├── trash/                 ← ALL intermediate files (py runners, wav, ass, cut mp4s, sample jpgs)
└── docs/                  ← Project memory, PRD, architecture, workflow, and rules
```

## 2. File Organization Rules
1. **Creator-Specific Output**: Deliverables must be saved in `D:\YT-Clipper\<CreatorName>\`.
2. **Dedicated Trash Folder**: Never leave scratch scripts, intermediate cuts, wav stems, or test renders in root. Put them in `D:\YT-Clipper\trash\`. Never permanently delete raw files without user instruction.
3. **Pristine Root**: The root directory `D:\YT-Clipper` must contain ONLY directories (`CarryMinati/`, `IShowSpeed/`, `resources/`, `trash/`, `docs/`). Zero loose files.

## 3. Video & Encoding Laws
1. **Vertical 9:16 Canvas**: 1080x1920 @ 60fps progressive.
2. **No Monochrome Emojis**: Never embed raw unicode emojis into ASS subtitle dialogue lines. Use authentic Apple 160x160 PNGs from `resources/emojis/`.
3. **Concat Demuxer for Overlays**: Never chain multiple `-loop 1` video inputs. Use FFmpeg `concat` demuxer (`-f concat -safe 0 -i timeline.txt`) to sequence overlays sequentially.
4. **No Premature Stream Killers**: Never use `:shortest=1` on intermediate image overlays. Use `:eof_action=pass`.
5. **No Pipe Buffer Deadlocks**: When invoking FFmpeg via Python `subprocess.run()`, never pass `capture_output=True`. Stream output or redirect to a log file.
6. **No Cross-Stream Audio Deadlocks**: Do not insert complex lookahead filters (like `dynaudnorm=s=8`) into multi-input video overlay graphs.
7. **Accurate Verbatim Speech**: Subtitles must match 100% of spoken words with zero latency.
8. **Vertical Spacing Law**: Set ASS `MarginV=880` so subtitle text never collides with emoji pairs at `y=822`.

## 4. Mandatory Clip Delivery Metadata Law
With EVERY generated clip, the agent MUST ALWAYS automatically provide the complete YouTube publishing package:
1. **3x Viral Titles**: High CTR, emotional curiosity hooks with emojis.
2. **SEO Video Description**: Keyword-rich description, streamer credit, timestamp markers, and call-to-actions.
3. **Viral Hashtags**: 5 to 8 high-velocity tags (e.g. `#shorts`, `#gta6`, `#carryminati`).
4. **YouTube Studio Tags**: Full comma-separated tag list ready to paste directly into YouTube Studio's tag box.
5. **Pinned Engagement Comment**: Question prompt designed to provoke viewer replies and boost algorithmic distribution.
6. **Generated Thumbnail Files (MANDATORY)**: The agent must ALWAYS generate and deliver actual click-optimized thumbnail image files:
   - **9:16 Vertical Cover** (`<clip_name>_thumb.jpg` in 1080×1920) for Shorts, Reels, and TikTok covers.
   - **16:9 Widescreen Thumbnail** (`<clip_name>_thumb_16x9.jpg` in 1280×720) for standard YouTube video uploads and community posts.
   - Design: 3D high-contrast title typography, glowing neon focal rings/arrows on the action, streamer's emotional reaction, and authentic Apple emojis.

## 5. Non-Duplication & Clip Blacklist Law (NEVER REUSE THE SAME CLIP)
1. **Zero Clip Overlap**: Never extract, edit, or deliver a stream moment, timestamp range, or segment that has already been clipped.
2. **Consult `docs/CLIPS_REGISTRY.md` First**: Before clipping any source video or livestream, the agent must read `docs/CLIPS_REGISTRY.md` and verify that the target interval has not already been used.
3. **Immediate Registration**: As soon as a master Short is rendered, append its entry into `docs/CLIPS_REGISTRY.md` with: Source URL, Streamer Name, Timestamp/Sequence Range, Key Dialogue/Action, and Final Deliverable Path.
4. **Freshness Guarantee**: Every Short must deliver an unseen, high-velocity moment to keep viewer retention and channel growth maximized.

## 6. Mandatory Upload Completion Notification Law (ALWAYS NOTIFY ON UPLOAD)
Whenever an automated upload to YouTube Studio is performed, the agent must **ALWAYS notify the user immediately upon completion**:
1. **Live Short URL**: Provide the exact, direct clickable YouTube link (`https://www.youtube.com/shorts/<id>`).
2. **Publishing Confirmation**: Confirm video title, public visibility status, and thumbnail attachment.
3. **Local Deliverable Links**: Link to the final `.mp4` and both thumbnail files (`_thumb.jpg` and `_thumb_16x9.jpg`).
4. **Permanent Ledger Update**: Confirm that the video ID and status have been updated in `docs/CLIPS_REGISTRY.md` and `docs/MEMORY.md`.
5. **No Silent Finishes**: The agent must never end a turn after an upload without explicitly presenting the publication success report.

## 7. Zero-Defect Upload Verification Law (NEVER CUT OFF UPLOADS OR MISS METADATA)
To prevent uploads getting stuck mid-stream or missing metadata/thumbnails:
1. **100% Raw File Streaming Guarantee**:
   - The uploader must actively monitor `ytcp-video-upload-progress` and never click Publish or close browser contexts while the status indicates `Uploading X%`.
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


