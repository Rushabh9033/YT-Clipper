#!/usr/bin/env python3
"""
YT-Clipper Master Automation Script
Automates viral 9:16 Shorts generation with NVENC hardware acceleration,
genuine Apple color emoji overlays, Submagic kinetic typography, and glassmorphism hook badges.
"""

import os
import sys
import argparse
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

RESOURCE_DIR = "D:/YT-Clipper/resources/emojis"
TRASH_DIR = "D:/YT-Clipper/trash"
FONT_PATH = "C:/Windows/Fonts/impact.ttf"

def render_hook_pill(text: str, emoji_names: list, out_path: str):
    """Renders a glassmorphism retention badge with neon yellow outline and Apple emojis."""
    font = ImageFont.truetype(FONT_PATH, 42)
    emojis = [Image.open(os.path.join(RESOURCE_DIR, f"{e}.png")).convert("RGBA").resize((56, 56), Image.Resampling.LANCZOS)
              for e in emoji_names if os.path.exists(os.path.join(RESOURCE_DIR, f"{e}.png"))]
    
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    pill_w = text_w + len(emojis) * 60 + 60
    pill_h = 76
    
    img = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, pill_w, pill_h], radius=24, fill=(10, 10, 16, 230), outline=(255, 229, 0, 255), width=4)
    d.text((24, 14), text, font=font, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    
    cur_x = 24 + text_w + 14
    for em in emojis:
        img.alpha_composite(em, (cur_x, 10))
        cur_x += 62
        
    img.save(out_path)
    pill_x = (1080 - pill_w) // 2
    return pill_w, pill_h, pill_x

def build_concat_timeline(events: list, blank_path: str, out_timeline: str):
    """
    Builds the FFmpeg concat demuxer timeline for Apple color emojis.
    events: list of tuples (start_sec, end_sec, em1_name, em2_name)
    """
    lines = ["ffconcat version 1.0\n"]
    cur_time = 0.0
    
    for idx, (s, e, em1_name, em2_name) in enumerate(events):
        p1 = os.path.join(RESOURCE_DIR, f"{em1_name}.png")
        p2 = os.path.join(RESOURCE_DIR, f"{em2_name}.png")
        em1 = Image.open(p1).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
        em2 = Image.open(p2).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
        
        pair = Image.new("RGBA", (162, 80), (0, 0, 0, 0))
        pair.alpha_composite(em1, (0, 2))
        pair.alpha_composite(em2, (82, 2))
        
        pair_path = os.path.join(TRASH_DIR, f"em_pair_{idx:02d}.png").replace("\\", "/")
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

def render_short(input_raw: str, hook_pill: str, pill_x: int, timeline: str, ass_path: str, output_path: str, duration: float = 60.0):
    """Executes high-speed NVENC master encode in ~10 seconds."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
    
    fc = [
        "[0:v]crop=480:540:0:540,scale=1080:810,setsar=1[top]",
        "[0:v]crop=1280:960:600:60,scale=1080:1110,setsar=1[bot]",
        "[top][bot]vstack=inputs=2[stacked]",
        "color=c=0xFFE500:s=1080x8:r=60:d=60[seam]",
        "[stacked][seam]overlay=0:806:shortest=1[vseam]",
        f"[vseam]subtitles={ass_escaped}[vsub]",
        f"[vsub][1:v]overlay={pill_x}:692:eof_action=pass[vhook]",
        f"[vhook][2:v]overlay=459:822:eof_action=pass[vemo]",
        f"[vemo]eq=saturation=1.18:contrast=1.06:brightness=0.01[final_v]"
    ]
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:00.000", "-t", str(duration), "-i", input_raw,
        "-t", "3.5", "-loop", "1", "-i", hook_pill,
        "-f", "concat", "-safe", "0", "-i", timeline,
        "-filter_complex", ";".join(fc),
        "-map", "[final_v]", "-map", "0:a",
        "-c:v", "h264_nvenc", "-preset", "p5", "-b:v", "10M", "-maxrate", "14M", "-bufsize", "20M",
        "-r", "60", "-c:a", "aac", "-b:a", "192k",
        "-t", str(duration),
        output_path
    ]
    
    print(f"Encoding master short to {output_path}...")
    t0 = time.time()
    log_path = os.path.join(TRASH_DIR, "render.log")
    with open(log_path, "w", encoding="utf-8") as f:
        res = subprocess.run(cmd, stdout=f, stderr=f)
        
    if res.returncode != 0:
        print("FFmpeg error! Check", log_path)
        sys.exit(1)
        
    print(f"Master short rendered in {time.time() - t0:.2f} seconds!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YT-Clipper Viral Short Generator")
    parser.add_argument("--creator", default="IShowSpeed", help="Creator folder name")
    parser.add_argument("--input", required=True, help="Path to raw cut mp4")
    parser.add_argument("--output", required=True, help="Output short mp4 path")
    parser.add_argument("--hook-text", default="NO WAY BRO HE RETIRED?!", help="Hook text")
    parser.add_argument("--hook-emojis", default="portugal,goat", help="Hook emojis comma-separated")
    parser.add_argument("--ass", required=True, help="Path to ASS subtitles file")
    parser.add_argument("--timeline", required=True, help="Path to emojis_timeline.txt")
    parser.add_argument("--duration", type=float, default=60.0, help="Duration in seconds")
    
    args = parser.parse_args()
    
    os.makedirs(TRASH_DIR, exist_ok=True)
    hook_pill_path = os.path.join(TRASH_DIR, "hook_pill.png")
    emojis = [e.strip() for e in args.hook_emojis.split(",")]
    pw, ph, px = render_hook_pill(args.hook_text, emojis, hook_pill_path)
    
    render_short(args.input, hook_pill_path, px, args.timeline, args.ass, args.output, args.duration)
