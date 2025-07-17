# TikTok Downloader All 🎬🖼️

A powerful Python tool to download both TikTok videos and photo posts in parallel, with clean filenames and timestamps — no config file needed.

---

## ✅ Features

- Supports **TikTok video links** (`/video/...`)
- Supports **TikTok photo posts** (`/photo/...`)
- Saves files as: `username_contentID_timestamp.ext`
- Works **without a config.yaml** — all defaults are built-in
- Uses **multithreading** (default: 4 threads)
- Displays live progress: `[2/10] ✅ Downloaded: ...`
- Skips existing files automatically
- All content is saved to the `downloads/` folder

---

## ⚙️ Default settings (hardcoded)

```python
{
  "threads": 4,
  "download_folder": "downloads",
  "skip_existing": True
}
````

No external configuration file required — just run the script!

---

## 🚀 How to use

1. Install dependencies:

```bash
pip install tiktok-downloader
```

2. Create a file named `urls.txt` in the same folder.
   Add one TikTok link per line (videos and/or photo posts):

```txt
https://www.tiktok.com/@user/video/7500000000000000000
https://www.tiktok.com/@user/photo/7500000000000000001
```

3. Run the script:

```bash
python3 tiktok_downloader_all.py
```

---

## 📁 Output structure

Your downloaded content will be stored like this:

```
downloads/
├── user_7512345678901234567_20250615_101530.mp4
├── user_7512345678901234567_20250615_101530.jpg
├── user_7512345678901234567_20250615_101530_2.jpg
```

---

## 🛠 Error handling

* Invalid or missing URLs are skipped
* Unrecognized links are reported
* Failed downloads are isolated — others continue uninterrupted

---

## 📄 License

MIT License — free to use, modify, and share.

---

## 👤 Author

Built by Hubi70

