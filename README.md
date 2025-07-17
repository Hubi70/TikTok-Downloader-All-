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
