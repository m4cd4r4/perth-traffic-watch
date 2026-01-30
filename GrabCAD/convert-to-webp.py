"""
Convert JPG/PNG frames to WebP format for web optimization
Usage: python convert-to-webp.py --input frames-ai --quality 85
"""

import argparse
from pathlib import Path
import subprocess
import sys

def check_cwebp():
    """Check if cwebp is installed."""
    try:
        subprocess.run(['cwebp', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_frames(input_dir, quality=85, output_dir=None):
    """Convert all JPG/PNG files to WebP."""
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Error: Directory {input_dir} not found")
        return

    # Use same directory if output not specified
    output_path = Path(output_dir) if output_dir else input_path
    output_path.mkdir(exist_ok=True)

    # Find all image files
    images = list(input_path.glob("*.jpg")) + list(input_path.glob("*.png"))

    if not images:
        print(f"No JPG or PNG files found in {input_dir}")
        return

    print(f"\nConverting {len(images)} images to WebP (quality: {quality})")
    print("=" * 70)

    converted = 0
    for img in sorted(images):
        output_file = output_path / f"{img.stem}.webp"

        try:
            result = subprocess.run(
                ['cwebp', '-q', str(quality), str(img), '-o', str(output_file)],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Get file sizes
                original_size = img.stat().st_size / 1024  # KB
                webp_size = output_file.stat().st_size / 1024  # KB
                savings = ((original_size - webp_size) / original_size) * 100

                print(f"✓ {img.name} -> {output_file.name} "
                      f"({original_size:.1f}KB -> {webp_size:.1f}KB, {savings:.1f}% savings)")
                converted += 1
            else:
                print(f"✗ Failed: {img.name}")
                print(f"  Error: {result.stderr}")

        except Exception as e:
            print(f"✗ Error converting {img.name}: {e}")

    print("=" * 70)
    print(f"\nCompleted: {converted}/{len(images)} images converted")

    # Calculate total savings
    if converted > 0:
        original_total = sum(img.stat().st_size for img in images) / (1024 * 1024)  # MB
        webp_files = list(output_path.glob("*.webp"))
        webp_total = sum(f.stat().st_size for f in webp_files) / (1024 * 1024)  # MB
        total_savings = ((original_total - webp_total) / original_total) * 100

        print(f"Total size: {original_total:.1f}MB -> {webp_total:.1f}MB ({total_savings:.1f}% savings)")

def main():
    parser = argparse.ArgumentParser(description='Convert frames to WebP format')
    parser.add_argument('--input', '-i', required=True, help='Input directory containing JPG/PNG files')
    parser.add_argument('--output', '-o', help='Output directory (default: same as input)')
    parser.add_argument('--quality', '-q', type=int, default=85, help='WebP quality (0-100, default: 85)')

    args = parser.parse_args()

    # Check if cwebp is installed
    if not check_cwebp():
        print("Error: cwebp not found!")
        print("\nInstall cwebp:")
        print("  Windows: Download from https://developers.google.com/speed/webp/download")
        print("  Mac:     brew install webp")
        print("  Linux:   sudo apt-get install webp")
        sys.exit(1)

    convert_frames(args.input, args.quality, args.output)

if __name__ == "__main__":
    main()
