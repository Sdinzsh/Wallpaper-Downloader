#!/usr/bin/python3
import os
import sys
import requests
import random
import pathlib
import string

DOWNLOAD_DIR = pathlib.Path.home() / "pix" / "wall"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_WALLPAPERS = 15

RES_OPTIONS = {
    "1": "1920x1080",
    "2": "2560x1440",
    "3": "3840x2160",
    "4": ""
}

def generate_id(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_ext(url):
    return os.path.splitext(url)[1]

def download_wallpaper(url):
    try:
        print(f"Downloading {url}")
        res = requests.get(url, allow_redirects=True, timeout=10)
        filename = generate_id() + get_ext(url)
        filepath = DOWNLOAD_DIR / filename
        with open(filepath, 'wb') as f:
            f.write(res.content)
        print(f"Saved to {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def wallpaper_search_api(query, resolution):
    base_url = f"https://wallhaven.cc/api/v1/search?q={query}&purity=100&categories=111"
    if resolution:
        base_url += f"&at_least={resolution}"
    try:
        res = requests.get(base_url, timeout=10)
        data = res.json()["data"]
        return [wall["path"] for wall in data][:MAX_WALLPAPERS]
    except Exception as e:
        print(f"API error: {e}")
        return []

print("Choose resolution:")
print("1) Full HD (1080p)  - 1920x1080")
print("2) 2K (1440p)       - 2560x1440")
print("3) 4K (2160p)       - 3840x2160")
print("4) Mixed")
res_choice = input("Enter your choice (1–4): ").strip()
resolution = RES_OPTIONS.get(res_choice, "")

query = input("Enter your wallpaper search keyword: ").strip().replace(' ', '+')

wallpapers = wallpaper_search_api(query, resolution)
if not wallpapers:
    print("No wallpapers found.")
    sys.exit()

print(f"Found {len(wallpapers)} wallpapers. Starting download...")
for url in wallpapers:
    download_wallpaper(url)