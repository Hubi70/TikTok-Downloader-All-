from tiktok_downloader import snaptik
import re
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Default configuration (no external config.yaml needed)
DEFAULT_CONFIG = {
    "threads": 4,
    "download_folder": "downloads",
    "skip_existing": True
}

# Utility functions
def extract_timestamp_from_id(content_id):
    try:
        timestamp = int(content_id) >> 32
        return timestamp
    except:
        return 0

def format_timestamp(unix_timestamp):
    try:
        return datetime.utcfromtimestamp(unix_timestamp).strftime("%Y%m%d_%H%M%S")
    except:
        return "unknown_time"

# Download logic for videos
def download_tiktok_video(url, index, total, config):
    username_match = re.search(r'/@([^/]+)', url)
    username = username_match.group(1) if username_match else "unknown"

    video_id_match = re.search(r'/video/(\d+)', url)
    video_id = video_id_match.group(1) if video_id_match else "unknown"

    ts = format_timestamp(extract_timestamp_from_id(video_id))
    try:
        downloader = snaptik(url)
        if not downloader:
            print(f"[{index}/{total}] ⚠️ No download links found for {url}")
            return

        video = downloader[0]
        fname = f"{username}_{video_id}_{ts}.mp4"
        fname = re.sub(r'[^\w\-_\.]', '_', fname)
        path = os.path.join(config['download_folder'], fname)

        if config['skip_existing'] and os.path.exists(path):
            print(f"[{index}/{total}] ⏭️ File {fname} already exists")
            return

        video.download(path)
        print(f"[{index}/{total}] ✅ Video saved: {fname}")
    except Exception as e:
        print(f"[{index}/{total}] ❌ Error with video: {e}")

# Download logic for photos
def download_tiktok_photo(url, index, total, config):
    username_match = re.search(r'/@([^/]+)', url)
    username = username_match.group(1) if username_match else "unknown"

    photo_id_match = re.search(r'/photo/(\d+)', url)
    photo_id = photo_id_match.group(1) if photo_id_match else "unknown"

    ts = format_timestamp(extract_timestamp_from_id(photo_id))
    try:
        downloader = snaptik(url)
        if not downloader:
            print(f"[{index}/{total}] ⚠️ No images found for {url}")
            return

        for i, item in enumerate(downloader, start=1):
            ext = ".jpg"
            try:
                url_attr = getattr(item, 'url', None)
                if url_attr:
                    ext = os.path.splitext(url_attr)[1] or ".jpg"
            except:
                pass

            base = f"{username}_{photo_id}_{ts}"
            fname = f"{base}_{i}{ext}" if len(downloader) > 1 else f"{base}{ext}"
            fname = re.sub(r'[^\w\-_\.]', '_', fname)
            path = os.path.join(config['download_folder'], fname)

            if config['skip_existing'] and os.path.exists(path):
                print(f"[{index}/{total}] ⏭️ File {fname} already exists")
                continue

            item.download(path)
            print(f"[{index}/{total}] ✅ Image saved: {fname}")
    except Exception as e:
        print(f"[{index}/{total}] ❌ Error with image: {e}")

# Main processing
def process_url_file():
    config = DEFAULT_CONFIG
    if not os.path.exists(config['download_folder']):
        os.makedirs(config['download_folder'])

    urls_file = os.path.join(os.path.dirname(__file__), 'urls.txt')
    if not os.path.exists(urls_file):
        print("⚠️ urls.txt not found.")
        return

    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [url.strip() for url in f if url.strip()]

    total = len(urls)
    print(f"Found links: {total}\n")

    with ThreadPoolExecutor(max_workers=config['threads']) as executor:
        futures = []
        for idx, url in enumerate(urls):
            if '/video/' in url:
                futures.append(executor.submit(download_tiktok_video, url, idx+1, total, config))
            elif '/photo/' in url:
                futures.append(executor.submit(download_tiktok_photo, url, idx+1, total, config))
            else:
                print(f"[{idx+1}/{total}] ⚠️ Unknown TikTok link format: {url}")

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[Thread Error] {e}")

    print("\n✅ All content has been processed.")

if __name__ == "__main__":
    process_url_file()

