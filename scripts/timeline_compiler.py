#!/usr/bin/env python3
"""
YT-Clipper 2.0 — Non-Destructive Multitrack Timeline Compiler
Translates a human/AI-editable `timeline.json` project file into an ultra-fast
NVENC-accelerated FFmpeg pipeline with Submagic kinetic captions, Apple emoji
concat overlays, and glassmorphism hook badges.
"""

import os
import sys
import json
import argparse
import subprocess
import time
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont

RESOURCE_DIR = "D:/YT-Clipper/resources/emojis"
TRASH_DIR = "D:/YT-Clipper/trash"
FONT_PATH = "C:/Windows/Fonts/impact.ttf"

def render_hook_badge(badge_config: Dict[str, Any], out_path: str) -> int:
    """Generates the glassmorphism retention badge PNG and returns its centered X coordinate."""
    text = badge_config.get("text", "")
    emoji_names = badge_config.get("emojis", [])
    font = ImageFont.truetype(FONT_PATH, 42)
    
    loaded_emojis = []
    for em in emoji_names:
        p = os.path.join(RESOURCE_DIR, f"{em}.png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA").resize((56, 56), Image.Resampling.LANCZOS)
            loaded_emojis.append(im)
            
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    pill_w = text_w + len(loaded_emojis) * 60 + 60
    pill_h = 76
    
    img = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, pill_w, pill_h], radius=24, fill=(10, 10, 16, 230), outline=(255, 229, 0, 255), width=4)
    d.text((24, 14), text, font=font, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    
    cur_x = 24 + text_w + 14
    for em_im in loaded_emojis:
        img.alpha_composite(em_im, (cur_x, 10))
        cur_x += 62
        
    img.save(out_path)
    pill_x = (1080 - pill_w) // 2
    return pill_x

def generate_ass_subtitles(captions: List[Dict[str, Any]], out_ass_path: str) -> None:
    """Generates Submagic-style ASS kinetic captions with physics spring pop keyframing."""
    header = """[Script Info]
Title: YT-Clipper 2.0 Submagic Kinetic Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Submagic,Impact,64,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,4,2,40,40,880,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    
    for c in captions:
        s = c["start"]
        e = c["end"]
        text = c["text"]
        color = c.get("color", "&H00FFFFFF")
        spring = c.get("spring_pop", True)
        
        # Convert seconds to 0:00:00.00
        def fmt(t):
            m, sec = divmod(t, 60)
            h, m = divmod(m, 60)
            return f"{int(h)}:{int(m):02d}:{sec:05.2f}"
            
        start_str = fmt(s)
        end_str = fmt(e)
        
        if spring:
            anim = r"{\t(0,70,\fscx125\fscy125)\t(70,140,\fscx100\fscy100)}"
        else:
            anim = ""
            
        line = f"Dialogue: 0,{start_str},{end_str},Submagic,,0,0,0,,{anim}{{\\c{color}}}{text}\n"
        lines.append(line)
        
    with open(out_ass_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def build_emoji_timeline(overlays: List[Dict[str, Any]], blank_path: str, out_timeline: str) -> None:
    """Builds FFmpeg concat demuxer sequence for emoji stickers."""
    lines = ["ffconcat version 1.0\n"]
    cur_time = 0.0
    
    for idx, ov in enumerate(overlays):
        s = ov["start"]
        e = ov["end"]
        emojis = ov.get("emojis", [])
        if not emojis:
            continue
            
        # Composite emoji pair
        p1 = os.path.join(RESOURCE_DIR, f"{emojis[0]}.png")
        em1 = Image.open(p1).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
        
        pair = Image.new("RGBA", (162, 80), (0, 0, 0, 0))
        pair.alpha_composite(em1, (0, 2))
        
        if len(emojis) > 1:
            p2 = os.path.join(RESOURCE_DIR, f"{emojis[1]}.png")
            if os.path.exists(p2):
                em2 = Image.open(p2).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
                pair.alpha_composite(em2, (82, 2))
                
        pair_path = os.path.join(TRASH_DIR, f"v2_em_pair_{idx:02d}.png").replace("\\", "/")
        pair.save(pair_path)
        
        gap = s - cur_time
        if gap > 0.001:
            lines.append(f"file '{blank_path.replace(chr(92), '/')}'\n")
            lines.append(f"duration {gap:.3f}\n")
            
        dur = e - s
        lines.append(f"file '{pair_path}'\n")
        lines.append(f"duration {dur:.3f}\n")
        cur_time = e
        
    lines.append(f"file '{blank_path.replace(chr(92), '/')}'\n")
    lines.append("duration 5.000\n")
    lines.append(f"file '{blank_path.replace(chr(92), '/')}'\n")
    
    with open(out_timeline, "w", encoding="utf-8") as f:
        f.writelines(lines)

def compile_and_render(project_path: str, out_video_path: str) -> None:
    """Parses project_timeline.json and compiles it directly into high-speed NVENC encode."""
    print(f"Loading project timeline: {project_path}")
    with open(project_path, "r", encoding="utf-8") as f:
        proj = json.load(f)
        
    os.makedirs(TRASH_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(out_video_path)), exist_ok=True)
    
    raw_video = proj["media_sources"]["raw_video"]
    canvas = proj.get("canvas", {"width": 1080, "height": 1920, "fps": 60, "duration": 60.0})
    duration = canvas.get("duration", 60.0)
    tracks = proj["tracks"]
    
    # 1. Render Hook Badge
    badge_config = tracks.get("hook_badge", {})
    hook_badge_png = os.path.join(TRASH_DIR, "v2_hook_badge.png").replace("\\", "/")
    pill_x = render_hook_badge(badge_config, hook_badge_png)
    
    # 2. Render ASS Subtitles
    captions = tracks.get("captions", [])
    ass_path = os.path.join(TRASH_DIR, "v2_captions.ass").replace("\\", "/")
    generate_ass_subtitles(captions, ass_path)
    
    # 3. Render Blank PNG & Emoji Timeline
    blank_png = os.path.join(TRASH_DIR, "v2_blank.png").replace("\\", "/")
    Image.new("RGBA", (162, 80), (0, 0, 0, 0)).save(blank_png)
    
    overlays = tracks.get("emoji_overlays", [])
    emoji_timeline = os.path.join(TRASH_DIR, "v2_emojis_timeline.txt").replace("\\", "/")
    build_emoji_timeline(overlays, blank_png, emoji_timeline)
    
    # 4. Construct Modular FFmpeg Filtergraph
    vtop = tracks.get("video_top", {})
    crop_top = vtop.get("crop", {"w": 480, "h": 540, "x": 0, "y": 540})
    scale_top = vtop.get("scale", {"w": 1080, "h": 810})
    
    vbot = tracks.get("video_bottom", {})
    crop_bot = vbot.get("crop", {"w": 1280, "h": 960, "x": 600, "y": 60})
    scale_bot = vbot.get("scale", {"w": 1080, "h": 1110})
    
    seam = tracks.get("laser_seam", {"enabled": True, "y": 806, "height": 8, "color": "0xFFE500"})
    grading = tracks.get("color_grading", {"saturation": 1.18, "contrast": 1.06, "brightness": 0.01})
    
    # Use relative path to avoid Windows drive letter colon issue in FFmpeg subtitles filter
    cwd = os.getcwd()
    try:
        rel_ass = os.path.relpath(ass_path, cwd).replace("\\", "/")
    except ValueError:
        rel_ass = ass_path.replace("\\", "/").replace(":", "\\:")
    
    filter_complex = [
        f"[0:v]crop={crop_top['w']}:{crop_top['h']}:{crop_top['x']}:{crop_top['y']},scale={scale_top['w']}:{scale_top['h']},setsar=1[top]",
        f"[0:v]crop={crop_bot['w']}:{crop_bot['h']}:{crop_bot['x']}:{crop_bot['y']},scale={scale_bot['w']}:{scale_bot['h']},setsar=1[bot]",
        "[top][bot]vstack=inputs=2[stacked]",
        f"color=c={seam['color']}:s=1080x{seam['height']}:r={canvas['fps']}:d={duration}[seam]",
        f"[stacked][seam]overlay=0:{seam['y']}:shortest=1[vseam]",
        f"[vseam]subtitles='{rel_ass}'[vsub]",
        f"[vsub][1:v]overlay={pill_x}:{badge_config.get('y', 692)}:eof_action=pass[vhook]",
        f"[vhook][2:v]overlay=459:822:eof_action=pass[vemo]",
        f"[vemo]eq=saturation={grading['saturation']}:contrast={grading['contrast']}:brightness={grading['brightness']}[final_v]"
    ]
    
    badge_start = badge_config.get("start", 0.0)
    badge_end = badge_config.get("end", 3.5)
    
    filter_complex = [
        f"[0:v]crop={crop_top['w']}:{crop_top['h']}:{crop_top['x']}:{crop_top['y']},scale={scale_top['w']}:{scale_top['h']},setsar=1[top]",
        f"[0:v]crop={crop_bot['w']}:{crop_bot['h']}:{crop_bot['x']}:{crop_bot['y']},scale={scale_bot['w']}:{scale_bot['h']},setsar=1[bot]",
        "[top][bot]vstack=inputs=2[stacked]",
        f"color=c={seam['color']}:s=1080x{seam['height']}:r={canvas['fps']}:d={duration}[seam]",
        f"[stacked][seam]overlay=0:{seam['y']}:shortest=1[vseam]",
        f"[vseam]subtitles='{rel_ass}'[vsub]",
        f"[vsub][1:v]overlay={pill_x}:{badge_config.get('y', 692)}:enable='between(t,{badge_start},{badge_end})':eof_action=pass[vhook]",
        f"[vhook][2:v]overlay=459:822:eof_action=pass[vemo]",
        f"[vemo]eq=saturation={grading['saturation']}:contrast={grading['contrast']}:brightness={grading['brightness']}[final_v]"
    ]
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(proj.get("time_offset", 0.0)),
        "-t", str(duration),
        "-i", raw_video,
        "-framerate", str(canvas['fps']), "-loop", "1", "-i", hook_badge_png,
        "-f", "concat", "-safe", "0", "-i", emoji_timeline,
        "-filter_complex", ";".join(filter_complex),
        "-map", "[final_v]",
        "-map", "0:a?",
        "-c:v", "h264_nvenc",
        "-preset", "p5",
        "-b:v", "12M",
        "-maxrate", "16M",
        "-bufsize", "24M",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-r", str(canvas['fps']),
        "-t", str(duration),
        out_video_path
    ]
    
    print("\n--- Executing Hardware NVENC Compiler ---")
    t0 = time.time()
    log_path = os.path.join(TRASH_DIR, "compiler_render.log")
    with open(log_path, "w", encoding="utf-8") as f_log:
        res = subprocess.run(cmd, stdout=f_log, stderr=f_log)
    t1 = time.time()
    
    if res.returncode != 0:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f_log:
            err_output = f_log.read()
        print(f"Compiler Error:\n{err_output[-1500:]}")
        sys.exit(res.returncode)
        
    print(f"Compilation Complete in {t1 - t0:.2f}s!")
    size_mb = os.path.getsize(out_video_path) / (1024 * 1024)
    print(f"Master Deliverable: {out_video_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YT-Clipper 2.0 Timeline Compiler")
    parser.add_argument("--project", required=True, help="Path to project_timeline.json")
    parser.add_argument("--output", required=True, help="Path to output .mp4 deliverable")
    args = parser.parse_args()
    
    compile_and_render(args.project, args.output)
