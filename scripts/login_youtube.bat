@echo off
title YouTube Studio Login Setup
color 0b
echo ============================================================
echo   YOUTUBE STUDIO AUTOMATION LOGIN SETUP (100%% FREE)
echo ============================================================
echo.
echo Opening browser window for one-time YouTube authentication...
echo Please log in with the channel account where you publish clips.
echo Once you see YouTube Studio dashboard, your login is saved!
echo.
python D:\YT-Clipper\scripts\youtube_studio_uploader.py --login
echo.
pause
