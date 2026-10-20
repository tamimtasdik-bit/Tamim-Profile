#!/usr/bin/env python3
"""Download licensed Unsplash photographs for Lawfinity GitHub Pages.

Photos represent London legal architecture and a historic library, not the
firm's actual premises, personnel or clients.
"""
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)

PHOTOS = [
    ("royal-courts-editorial.jpg", "https://images.unsplash.com/photo-1659274751452-2817a6dd7c0a?w=1550&q=88&fit=crop",
     "Utku Kaplan — Royal Courts of Justice, London; https://unsplash.com/photos/grand-gothic-building-on-a-rainy-day-hjSMnilsL64"),
    ("historic-library-editorial.jpg", "https://images.unsplash.com/photo-1502700807168-484a3e7889d0?w=1350&q=88&fit=crop",
     "Historic library photograph via Unsplash; https://unsplash.com/s/photos/law-library"),
]

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (compatible; LawfinitySiteAssets/1.0)"
session.headers["Accept"] = "image/jpeg,image/webp,image/*"

for filename, url, credit in PHOTOS:
    path = OUT / filename
    if path.exists() and path.stat().st_size > 10000:
        print(f"Already present: {path}")
        continue
    response = session.get(url, timeout=45)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    image = ImageOps.exif_transpose(image).convert("RGB")
    if max(image.size) > 1550:
        image.thumbnail((1550,1550), Image.Resampling.LANCZOS)
    # Subtle editorial finish; keep photographic subject faithful.
    image = ImageEnhance.Color(image).enhance(0.78)
    image = ImageEnhance.Contrast(image).enhance(1.045)
    image.save(path, "JPEG", quality=83, optimize=True, progressive=True)
    if path.stat().st_size < 10000:
        raise RuntimeError(f"Unexpectedly small image: {filename}")
    print(f"Saved {filename}: {image.size}, {path.stat().st_size} bytes; {credit}")

(OUT / "PHOTO_CREDITS.md").write_text(
    "# Photography licences and credits\n\n"
    "Photographs on the site are published under the Unsplash License. "
    "They are illustrative editorial imagery and do not depict Lawfinity Solicitors' premises or staff.\n\n"
    + "\n".join(f"- **{name}** — {credit}" for name, _, credit in PHOTOS)
    + "\n\nUnsplash License: https://unsplash.com/license\n",
    encoding="utf-8",
)
