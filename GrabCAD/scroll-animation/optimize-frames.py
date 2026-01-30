"""
Optimize Assembly Animation Frames for Web

Compresses PNG frames for faster loading while maintaining quality.
Creates WebP versions (60-80% smaller than PNG).

Usage:
    pip install pillow
    python optimize-frames.py

Output:
    - frames-optimized/ (compressed PNG, ~200-400KB each)
    - frames-webp/ (WebP format, ~100-200KB each)
"""

import os
from pathlib import Path
from PIL import Image
import shutil

# Configuration
SOURCE_DIR = Path(__file__).parent.parent / "frames-photorealistic"
OUTPUT_PNG_DIR = Path(__file__).parent / "frames-optimized"
OUTPUT_WEBP_DIR = Path(__file__).parent / "frames-webp"

# Quality settings
PNG_OPTIMIZE = True
PNG_COMPRESS_LEVEL = 9  # Max compression
WEBP_QUALITY = 85  # Good balance of quality/size
WEBP_METHOD = 6  # Slowest but best compression

# Resize settings (optional - set to None to keep original)
TARGET_WIDTH = 1920  # None to keep original
TARGET_HEIGHT = 1080


def optimize_frames():
    print("=== SwanFlow Frame Optimizer ===\n")

    # Create output directories
    OUTPUT_PNG_DIR.mkdir(exist_ok=True)
    OUTPUT_WEBP_DIR.mkdir(exist_ok=True)

    # Get source frames
    frames = sorted(SOURCE_DIR.glob("assembly_*.png"))
    total = len(frames)

    if total == 0:
        print(f"No frames found in {SOURCE_DIR}")
        return

    print(f"Found {total} frames in {SOURCE_DIR}")
    print(f"Output PNG: {OUTPUT_PNG_DIR}")
    print(f"Output WebP: {OUTPUT_WEBP_DIR}\n")

    total_original = 0
    total_png = 0
    total_webp = 0

    for i, frame_path in enumerate(frames):
        # Load image
        img = Image.open(frame_path)

        # Resize if needed
        if TARGET_WIDTH and TARGET_HEIGHT:
            if img.size != (TARGET_WIDTH, TARGET_HEIGHT):
                img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)

        # Convert RGBA to RGB if needed (WebP can handle RGBA but smaller with RGB)
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (10, 15, 26))  # Dark background
            background.paste(img, mask=img.split()[3])  # Use alpha as mask
            img_rgb = background
        else:
            img_rgb = img.convert('RGB')

        # Get original size
        original_size = frame_path.stat().st_size

        # Save optimized PNG
        png_path = OUTPUT_PNG_DIR / frame_path.name
        img.save(
            png_path,
            "PNG",
            optimize=PNG_OPTIMIZE,
            compress_level=PNG_COMPRESS_LEVEL
        )
        png_size = png_path.stat().st_size

        # Save WebP
        webp_path = OUTPUT_WEBP_DIR / frame_path.name.replace('.png', '.webp')
        img_rgb.save(
            webp_path,
            "WEBP",
            quality=WEBP_QUALITY,
            method=WEBP_METHOD
        )
        webp_size = webp_path.stat().st_size

        # Track totals
        total_original += original_size
        total_png += png_size
        total_webp += webp_size

        # Progress
        png_reduction = (1 - png_size / original_size) * 100
        webp_reduction = (1 - webp_size / original_size) * 100
        print(f"[{i+1:3d}/{total}] {frame_path.name}: "
              f"PNG {png_size/1024:.0f}KB ({png_reduction:.0f}% smaller), "
              f"WebP {webp_size/1024:.0f}KB ({webp_reduction:.0f}% smaller)")

    # Summary
    print(f"\n=== Summary ===")
    print(f"Original total: {total_original / 1024 / 1024:.1f} MB")
    print(f"PNG total:      {total_png / 1024 / 1024:.1f} MB ({(1 - total_png/total_original)*100:.0f}% reduction)")
    print(f"WebP total:     {total_webp / 1024 / 1024:.1f} MB ({(1 - total_webp/total_original)*100:.0f}% reduction)")

    # Create manifest for preloading
    manifest = {
        "frameCount": total,
        "formats": {
            "png": {
                "path": "frames-optimized/assembly_",
                "extension": ".png",
                "totalSize": total_png
            },
            "webp": {
                "path": "frames-webp/assembly_",
                "extension": ".webp",
                "totalSize": total_webp
            }
        }
    }

    import json
    manifest_path = Path(__file__).parent / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest saved to: {manifest_path}")


if __name__ == "__main__":
    optimize_frames()
