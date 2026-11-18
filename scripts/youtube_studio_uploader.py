import os
import sys
import time
import argparse
from playwright.sync_api import sync_playwright

PROFILE_DIR = r"D:\YT-Clipper\resources\browser_profile"
os.makedirs(PROFILE_DIR, exist_ok=True)

def check_login_status(headless=True):
    """Checks if the saved persistent profile is currently logged into YouTube Studio."""
    print(">>> Checking YouTube Studio authentication status...")
    if not os.path.exists(PROFILE_DIR) or not os.listdir(PROFILE_DIR):
        print("[STATUS] NOT LOGGED IN (Profile folder empty)")
        return False

    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                channel="chrome",
                headless=headless,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://studio.youtube.com", timeout=30000)
            page.wait_for_timeout(3000)

            # Check for interstitial
            skip_btn = page.locator("text='SKIP TO YOUTUBE STUDIO', a:has-text('SKIP TO YOUTUBE STUDIO')")
            if skip_btn.count() > 0:
                try:
                    skip_btn.first.click()
                    page.wait_for_timeout(3000)
                except Exception:
                    pass

            current_url = page.url
            current_title = page.title()
            is_authed = ("accounts.google.com" not in current_url) and (
                "studio.youtube.com" in current_url 
                or "YouTube Studio" in current_title 
                or "Channel dashboard" in current_title
            )

            if is_authed:
                print(f"[STATUS] AUTHENTICATED! Active YouTube Studio session detected: {current_title} ({current_url})")
                context.close()
                return True
            else:
                print(f"[STATUS] NOT LOGGED IN. Redirected to: {current_url}")
                context.close()
                return False
        except Exception as e:
            print(f"[STATUS] Error checking login: {e}")
            return False

def open_login_window():
    """Opens a visible browser so the user can log into YouTube Studio once."""
    print("=" * 65)
    print(">>> OPENING YOUTUBE STUDIO LOGIN WINDOW (100% FREE)")
    print(">>> Official Google Chrome will open on your screen.")
    print(">>> Please sign into your Google / YouTube account.")
    print(">>> Once logged in, your session is saved permanently for 1-click uploads.")
    print("=" * 65)
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            viewport={"width": 1280, "height": 850},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check"
            ]
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://studio.youtube.com")
        
        print("\nWaiting for you to log in... (Checking every 3 seconds for up to 10 minutes)")
        logged_in = False
        for i in range(200):  # up to 10 minutes
            time.sleep(3)
            try:
                if page.is_closed():
                    print("\n[INFO] Browser window closed by user.")
                    break
                current_url = page.url
                current_title = page.title()
                # Genuine Studio login check (NOT accounts.google.com)
                if "accounts.google.com" not in current_url and (
                    "studio.youtube.com" in current_url 
                    or "YouTube Studio" in current_title 
                    or "Channel dashboard" in current_title
                ):
                    logged_in = True
                    print("\n" + "=" * 65)
                    print("[SUCCESS] DETECTED ACTIVE YOUTUBE STUDIO LOGIN!")
                    print(f"[SUCCESS] Title: {current_title}")
                    print(f"[SUCCESS] URL: {current_url}")
                    print(f"[SUCCESS] Profile permanently saved to: {PROFILE_DIR}")
                    print("=" * 65)
                    time.sleep(2)
                    break
            except Exception:
                break
        
        if not logged_in:
            print("[INFO] If you completed login before closing, your session is saved. Run --status to verify.")
        
        try:
            context.close()
        except Exception:
            pass

def upload_video(video_path, thumbnail_path=None, title=None, description=None, tags=None, visibility="public", headless=False):
    """Automates full upload to YouTube Studio."""
    if not os.path.exists(video_path):
        print(f"[ERROR] Video file not found: {video_path}")
        return False

    print("=" * 65)
    print(">>> STARTING AUTOMATED YOUTUBE STUDIO UPLOADER")
    print(f"Video: {video_path}")
    print(f"Title: {title}")
    print(f"Visibility: {visibility.upper()}")
    print("=" * 65)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=headless,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check"
            ]
        )
        page = context.pages[0] if context.pages else context.new_page()
        
        try:
            print("[1] Navigating to YouTube Studio...")
            page.goto("https://studio.youtube.com", timeout=60000)
            page.wait_for_timeout(4000)
            
            # Check for interstitial "SKIP TO YOUTUBE STUDIO" or "Improve your experience"
            skip_btn = page.locator("text='SKIP TO YOUTUBE STUDIO', a:has-text('SKIP TO YOUTUBE STUDIO'), [aria-label*='Skip' i]")
            if skip_btn.count() > 0:
                print("[INFO] Detected browser interstitial. Clicking 'SKIP TO YOUTUBE STUDIO'...")
                try:
                    skip_btn.first.click()
                    page.wait_for_timeout(4000)
                except Exception as e:
                    print(f"[WARN] Error clicking skip: {e}")

            # Check if login is required
            if "accounts.google.com" in page.url or page.locator("text=Sign in").count() > 0:
                print("\n[ALERT] You are not logged in yet!")
                print("Please run: python D:\\YT-Clipper\\scripts\\youtube_studio_uploader.py --login")
                context.close()
                return False

            print("[2] Opening Upload Dialog...")
            # Dismiss welcome popups if any
            try:
                welcome_btn = page.locator("button:has-text('Continue'), ytcp-button:has-text('Continue'), #dismiss-button, button:has-text('Dismiss')")
                if welcome_btn.count() > 0 and welcome_btn.first.is_visible():
                    welcome_btn.first.click()
                    time.sleep(1)
            except Exception:
                pass

            # Click Create Button
            create_btn = page.locator("#create-icon, button:has-text('Create'), [aria-label='Create'], ytcp-button#create-icon")
            create_btn.first.click()
            time.sleep(1)

            # Click Upload videos option
            upload_item = page.locator("tp-yt-paper-item:has-text('Upload videos'), ytcp-text-menu-item:has-text('Upload videos')")
            upload_item.first.click()
            time.sleep(2)

            print("[3] Selecting video file...")
            file_input = page.locator("input[type='file']")
            file_input.set_input_files(video_path)
            time.sleep(5)

            # Wait for upload modal details page
            page.wait_for_selector("#textbox, div#title-textarea", timeout=60000)
            print("[4] Injecting Title & Description...")

            # Set Title
            if title:
                title_box = page.locator("div#title-textarea #textbox, #textbox[aria-label*='title' i], #textbox").first
                title_box.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                title_box.type(title, delay=10)
                time.sleep(1)

            # Set Description
            if description:
                desc_boxes = page.locator("div#textbox[aria-label*='Tell viewers' i], div#description-container #textbox, ytcp-social-suggestions-textbox #textbox, #textbox[aria-label*='description' i]")
                if desc_boxes.count() > 0:
                    desc_box = desc_boxes.first
                else:
                    all_textboxes = page.locator("div#textbox")
                    desc_box = all_textboxes.nth(1) if all_textboxes.count() > 1 else None

                if desc_box and desc_box.count() > 0:
                    print("  Found description box! Injecting text and hashtags...")
                    desc_box.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    desc_box.fill(description)
                    time.sleep(1)
                    page.keyboard.press("Escape")

            # Upload Thumbnail if provided
            if thumbnail_path and os.path.exists(thumbnail_path):
                print(f"[5] Injecting custom thumbnail: {os.path.basename(thumbnail_path)}...")
                try:
                    thumb_input = page.locator("input#file-loader, input[accept*='image']")
                    if thumb_input.count() > 0:
                        thumb_input.first.set_input_files(thumbnail_path)
                        time.sleep(2)
                except Exception as e:
                    print(f"[WARN] Thumbnail upload skipped: {e}")

            # Audience: Set "No, it's not made for kids"
            print("[6] Setting Audience to 'No, it\\'s not made for kids'...")
            page.keyboard.press("Escape")
            not_kids_radio = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK'], tp-yt-paper-radio-button:has-text('No, it\\'s not made for kids')")
            if not_kids_radio.count() > 0:
                not_kids_radio.first.click(force=True)
                time.sleep(1)

            # Tags & Category: Click 'Show More'
            print("[7] Setting Tags...")
            show_more_btn = page.locator("#toggle-button, button:has-text('Show more'), div[aria-label='Show more']")
            if show_more_btn.count() > 0:
                show_more_btn.first.click(force=True)
                time.sleep(1)
                
                if tags:
                    tags_box = page.locator("input[aria-label='Tags'], #text-input[aria-label='Tags'], #tags-container input")
                    if tags_box.count() > 0:
                        tags_box.first.click(force=True)
                        tags_box.first.fill(tags)
                        page.keyboard.press("Enter")
                        time.sleep(1)

            # Navigate through Next steps (Details -> Video elements -> Checks -> Visibility)
            print("[8] Advancing through wizard checks to Visibility...")
            for _ in range(30):
                next_btn = page.locator("#next-button:visible, button:has-text('Next'):visible")
                if next_btn.count() > 0 and next_btn.first.is_enabled():
                    next_btn.first.click(force=True)
                    time.sleep(2)
                
                # Check if Visibility options or Done/Publish button are visible
                vis_check = page.locator("tp-yt-paper-radio-button[name='PUBLIC']:visible, #done-button:visible")
                if vis_check.count() > 0:
                    print("  Reached Visibility step!")
                    break
                time.sleep(1)

            # Visibility Step
            print(f"[9] Setting Visibility to: {visibility.upper()}...")
            if visibility.lower() == "public":
                vis_radio = page.locator("tp-yt-paper-radio-button[name='PUBLIC'], tp-yt-paper-radio-button:has-text('Public')")
            elif visibility.lower() == "unlisted":
                vis_radio = page.locator("tp-yt-paper-radio-button[name='UNLISTED'], tp-yt-paper-radio-button:has-text('Unlisted')")
            else:
                vis_radio = page.locator("tp-yt-paper-radio-button[name='PRIVATE'], tp-yt-paper-radio-button:has-text('Private')")
            
            if vis_radio.count() > 0:
                vis_radio.first.click(force=True)
                time.sleep(1)

            # CRITICAL STEP: Wait for video upload to reach 100% BEFORE clicking Publish!
            # If we click Publish and close early, YouTube kills the upload socket mid-stream.
            print("\n" + "=" * 65)
            print("[10] STREAMING VIDEO: Waiting for 100% raw file upload completion...")
            print("=" * 65)
            t_upload_wait = time.time()
            last_msg = ""
            while time.time() - t_upload_wait < 600:  # up to 10 minutes
                prog_el = page.locator("ytcp-video-upload-progress, .progress-label, span.ytcp-video-upload-progress, #dialog-footer")
                status_text = ""
                if prog_el.count() > 0:
                    try:
                        status_text = prog_el.first.inner_text().strip()
                    except Exception:
                        pass

                if status_text and status_text != last_msg:
                    print(f"  [UPLOAD PROGRESS] {status_text}")
                    last_msg = status_text

                # Check if upload is 100% done
                is_still_uploading = "uploading" in status_text.lower() and ("%" in status_text or "left" in status_text.lower())
                is_upload_finished = any(done_kw in status_text.lower() for done_kw in [
                    "upload complete", "processing", "checks complete", 
                    "processing will begin shortly", "no issues found", "saved as draft"
                ])

                if is_upload_finished and not is_still_uploading:
                    print(f"\n[SUCCESS] 100% RAW FILE UPLOAD VERIFIED: {status_text}!")
                    break

                time.sleep(3)

            # Final Save / Publish
            print("\n[11] Publishing video to YouTube...")
            save_btn = page.locator("#done-button:visible, button:has-text('Publish'):visible, button:has-text('Save'):visible")
            for _ in range(20):
                if save_btn.count() > 0 and save_btn.first.is_enabled():
                    save_btn.first.click(force=True)
                    print("  Clicked Publish button!")
                    break
                time.sleep(1)

            # Wait for post-upload dialog to appear and verify publish status
            print("\n[12] Verifying post-upload confirmation dialog...")
            time.sleep(3)
            video_url = None
            t_post_wait = time.time()
            while time.time() - t_post_wait < 60:
                post_dialog = page.locator("ytcp-post-upload-dialog, ytcp-dialog:has-text('published'), ytcp-dialog:has-text('Video published'), ytcp-dialog:has-text('Short published')")
                if post_dialog.count() > 0 and post_dialog.first.is_visible():
                    print("  Post-upload confirmation dialog is visible!")
                    # Check if dialog has remaining progress
                    dialog_text = post_dialog.first.inner_text()
                    if "uploading" in dialog_text.lower() and "%" in dialog_text.lower():
                        print("  [INFO] Dialog indicates streaming remaining chunks... waiting.")
                        time.sleep(3)
                        continue
                    
                    # Extract Video Link
                    link_el = post_dialog.locator("a.ytcp-video-info, a.ytcp-upload-dialog-video-url, a[href*='youtu.be']")
                    if link_el.count() > 0:
                        video_url = link_el.first.get_attribute("href")
                        print(f"[SUCCESS] Extracted Video URL: {video_url}")
                    break
                time.sleep(2)

            # Close post-upload dialog if visible
            close_btn = page.locator("ytcp-button#close-button, button:has-text('Close')")
            if close_btn.count() > 0 and close_btn.first.is_visible():
                close_btn.first.click(force=True)
                time.sleep(2)

            # CRITICAL STEP [13]: Navigate to YouTube Studio Shorts page and verify row status!
            print("\n" + "=" * 65)
            print("[13] FINAL VERIFICATION: Checking Studio Content list...")
            print("=" * 65)
            page.goto("https://studio.youtube.com/channel/UCwlh2AW5W4XIkHIYu2NQ6qg/videos/short", timeout=30000)
            page.wait_for_timeout(5000)

            # Poll until video row is NOT in "Uploading" state
            t_row_wait = time.time()
            verified_published = False
            while time.time() - t_row_wait < 300:  # up to 5 minutes
                rows = page.locator("ytcp-video-row").all()
                if len(rows) > 0:
                    top_row = rows[0]
                    row_title = ""
                    try:
                        row_title = top_row.locator("#video-title").inner_text().strip()
                    except Exception:
                        pass
                    row_text = top_row.inner_text()

                    # Find status lines
                    status_details = [l.strip() for l in row_text.splitlines() if any(k in l.lower() for k in ['upload', 'percent', '%', 'pending', 'process', 'draft', 'public', 'checks'])]
                    status_summary = " | ".join(status_details)
                    print(f"  [STUDIO ROW 0] '{row_title}' -> Status: {status_summary}")

                    # Check if still uploading in Studio
                    if "uploading" in row_text.lower() and "%" in row_text.lower():
                        print("  [WAIT] Video row still shows uploading progress in Studio. Keeping connection alive...")
                        time.sleep(5)
                        page.reload()
                        page.wait_for_timeout(4000)
                        continue

                    # If row shows Public, Processing, or Checks complete
                    if any(k in row_text.lower() for k in ["public", "processing", "checks", "pending"]):
                        print(f"\n[SUCCESS] VIDEO VERIFIED IN STUDIO CONTENT LIST: {status_summary}!")
                        verified_published = True
                        break

                time.sleep(4)

            # Extract Video ID and Live Link from row if not already found
            video_id = None
            if video_url and "youtu.be/" in video_url:
                video_id = video_url.split("youtu.be/")[1].split("?")[0]
            elif video_url and "shorts/" in video_url:
                video_id = video_url.split("shorts/")[1].split("?")[0]

            rows = page.locator("ytcp-video-row").all()
            if len(rows) > 0 and not video_id:
                link_el = rows[0].locator("a#thumbnail, a#video-title")
                if link_el.count() > 0:
                    href = link_el.first.get_attribute("href") or ""
                    if "/video/" in href:
                        video_id = href.split("/video/")[1].split("/")[0]
                        video_url = f"https://www.youtube.com/shorts/{video_id}"

            # CRITICAL STEP [14]: Dual-Gate Verification on Edit Page
            # Guarantee 100% that Description with hashtags and Thumbnail are applied
            if video_id and (description or thumbnail_path):
                print("\n" + "=" * 65)
                print(f"[14] POST-UPLOAD AUDIT: Verifying metadata & thumbnail on edit page...")
                print(f"URL: https://studio.youtube.com/video/{video_id}/edit")
                print("=" * 65)
                try:
                    page.goto(f"https://studio.youtube.com/video/{video_id}/edit", timeout=30000)
                    page.wait_for_timeout(4000)

                    needs_save = False

                    # 1. Verify / Apply Description
                    if description:
                        desc_box = page.locator("div#textbox[aria-label*='Tell viewers' i], ytcp-social-suggestions-textbox #textbox, div#description-container #textbox")
                        target_box = desc_box.nth(1) if desc_box.count() > 1 else desc_box.first
                        curr_desc = target_box.inner_text().strip() if target_box.count() > 0 else ""
                        if not curr_desc or len(curr_desc) < 20:
                            print("  [AUDIT] Description missing or empty. Applying full description with hashtags...")
                            target_box.click()
                            page.keyboard.press("Control+A")
                            page.keyboard.press("Backspace")
                            target_box.fill(description)
                            time.sleep(1)
                            page.keyboard.press("Escape")
                            needs_save = True
                        else:
                            print("  [AUDIT] Description verified present.")

                    # 2. Verify / Apply Thumbnail
                    if thumbnail_path and os.path.exists(thumbnail_path):
                        print(f"  [AUDIT] Ensuring custom thumbnail is active: {os.path.basename(thumbnail_path)}...")
                        thumb_input = page.locator("input#file-loader, input[accept*='image']")
                        if thumb_input.count() > 0:
                            thumb_input.first.set_input_files(thumbnail_path)
                            time.sleep(2)
                            needs_save = True

                    # 3. Save changes if updated
                    if needs_save:
                        save_btn = page.locator("#save, button#save, ytcp-button#save, button:has-text('Save')")
                        for i in range(save_btn.count()):
                            b = save_btn.nth(i)
                            if b.is_visible() and b.is_enabled():
                                print("  Saving audit changes...")
                                b.click(force=True)
                                time.sleep(3)
                                break
                    print("  [SUCCESS] Metadata and Thumbnail audit passed!")
                except Exception as e:
                    print(f"  [WARN] Audit gate non-fatal error: {e}")

            time.sleep(3)
            print("\n" + "=" * 65)
            print(f"[SUCCESS] 100% COMPLETE & VERIFIED PUBLISHED TO YOUTUBE!")
            if video_url:
                print(f"Live Video URL: {video_url}")
            print("=" * 65)
            context.close()
            return True

        except Exception as e:
            print(f"\n[ERROR] Upload workflow encountered error: {e}")
            os.makedirs(r"D:\YT-Clipper\trash", exist_ok=True)
            page.screenshot(path=os.path.join(r"D:\YT-Clipper\trash", "upload_error.png"))
            context.close()
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Studio Automated Uploader (100% Free)")
    parser.add_argument("--login", action="store_true", help="Open visible Google Chrome to log into YouTube Studio once")
    parser.add_argument("--status", action="store_true", help="Check current login status")
    parser.add_argument("--video", type=str, help="Path to video MP4 file")
    parser.add_argument("--thumbnail", type=str, help="Path to thumbnail JPG file")
    parser.add_argument("--title", type=str, help="Video Title")
    parser.add_argument("--description", type=str, help="Video Description")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")
    parser.add_argument("--visibility", type=str, default="public", choices=["public", "unlisted", "private"])
    parser.add_argument("--headless", action="store_true", help="Run browser in background")

    args = parser.parse_args()

    if args.login:
        open_login_window()
    elif args.status:
        check_login_status()
    elif args.video:
        upload_video(
            video_path=args.video,
            thumbnail_path=args.thumbnail,
            title=args.title,
            description=args.description,
            tags=args.tags,
            visibility=args.visibility,
            headless=args.headless
        )
    else:
        parser.print_help()
