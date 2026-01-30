"""
SwanFlow 3D Model Downloader
Downloads detailed 3D models with PCB components from various sources.

Usage: python download-detailed-models.py
"""

import os
import urllib.request
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
MODELS_DIR = SCRIPT_DIR / "models-detailed"
TEXTURES_DIR = SCRIPT_DIR / "textures-pcb"

# Direct download links for models (where available without login)
MODELS = {
    # PCB-Arts shader setup
    "pcb-shader": {
        "url": "https://github.com/PCB-Arts/stylized-blender-setup/archive/refs/heads/main.zip",
        "extract": True,
        "type": "shader"
    },

    # Note: Most GrabCAD/SnapEDA models require manual download with login
    # Manual download instructions will be printed
}

MANUAL_DOWNLOADS = [
    {
        "name": "ESP32-CAM (SnapEDA)",
        "url": "https://www.snapeda.com/parts/ESP32-CAM/AI-Thinker/view-part/",
        "instructions": "Click 'Download' -> Select 'STEP' format -> Save to models-detailed/esp32-cam.step",
        "priority": "HIGH"
    },
    {
        "name": "ESP32-CAM (GrabCAD)",
        "url": "https://grabcad.com/library/esp32-cam-1",
        "instructions": "Click 'Download' -> Save to models-detailed/esp32-cam-grabcad.stl",
        "priority": "MEDIUM"
    },
    {
        "name": "OV2640 Camera (GrabCAD)",
        "url": "https://grabcad.com/library/ov2640-for-esp32-cam-1",
        "instructions": "Download and extract to models-detailed/ov2640/",
        "priority": "HIGH"
    },
    {
        "name": "SIM7600 Module (SnapEDA)",
        "url": "https://www.snapeda.com/parts/SIM7600E-H/SIMCom/view-part/",
        "instructions": "Download STEP format -> Save to models-detailed/sim7600.step",
        "priority": "HIGH"
    },
    {
        "name": "Solar Charge Controller (GrabCAD)",
        "url": "https://grabcad.com/library/solar-charge-controller-6",
        "instructions": "Download and extract to models-detailed/solar-controller/",
        "priority": "MEDIUM"
    },
    {
        "name": "BlenderKit PCB Material",
        "url": "https://www.blenderkit.com/asset-gallery-detail/e3d991d8-720f-4d01-a24e-c85887cfb5ce/",
        "instructions": "Install BlenderKit addon in Blender, search 'Procedural Circuit board'",
        "priority": "HIGH"
    }
]

def download_file(url, dest):
    """Download file with progress."""
    print(f"  Downloading: {url}")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"  [OK] Saved to: {dest}")
        return True
    except Exception as e:
        print(f"  [FAIL] Failed: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract ZIP file."""
    print(f"  Extracting: {zip_path.name}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"  [OK] Extracted to: {extract_to}")
        return True
    except Exception as e:
        print(f"  [FAIL] Failed: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("SwanFlow 3D Model & Texture Downloader")
    print("="*70 + "\n")

    # Create directories
    MODELS_DIR.mkdir(exist_ok=True)
    TEXTURES_DIR.mkdir(exist_ok=True)

    # Download automatic files
    print("\n[1/3] Downloading automatic resources...\n")

    for name, info in MODELS.items():
        dest_file = MODELS_DIR / f"{name}.zip"

        if download_file(info['url'], dest_file):
            if info.get('extract'):
                extract_dir = MODELS_DIR / name
                extract_dir.mkdir(exist_ok=True)
                extract_zip(dest_file, extract_dir)

    # Print manual download instructions
    print("\n[2/3] Manual Downloads Required (GrabCAD/SnapEDA need login)\n")
    print("-" * 70)

    for i, item in enumerate(MANUAL_DOWNLOADS, 1):
        print(f"\n{i}. {item['name']} [{item['priority']} PRIORITY]")
        print(f"   URL: {item['url']}")
        print(f"   >> {item['instructions']}")

    # Print texture download instructions
    print("\n" + "-" * 70)
    print("\n[3/3] PCB Texture Resources\n")
    print("-" * 70)

    print("\n1. PCB-Arts Shader (Already downloaded)")
    print(f"   Location: {MODELS_DIR / 'pcb-shader'}")
    print("   Contains: Complete Blender shader setup with sample PCB textures")

    print("\n2. Optional: High-res PCB textures")
    print("   - Green solder mask texture (4K)")
    print("   - Copper layer texture")
    print("   - Silkscreen overlay")
    print("   Download from: https://www.textures.com (search 'PCB circuit board')")
    print(f"   Save to: {TEXTURES_DIR}")

    # Summary
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. Download the HIGH PRIORITY models manually (requires free accounts)")
    print("2. Run the Blender setup script: blender --python setup-pcb-materials.py")
    print("3. Re-render the animation with detailed models\n")

    print(f"Models directory: {MODELS_DIR}")
    print(f"Textures directory: {TEXTURES_DIR}\n")

if __name__ == "__main__":
    main()
