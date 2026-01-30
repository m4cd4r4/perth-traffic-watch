"""
STEP to OBJ Converter for SwanFlow CAD Models
Uses cadquery/OCP (OpenCASCADE) to convert STEP files to OBJ format.

Usage: python convert_step_to_obj.py
"""

import os
from pathlib import Path
import sys

# Add OCP to path
try:
    from OCC.Core.STEPControl import STEPControl_Reader
    from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
    from OCC.Core.StlAPI import StlAPI_Writer
    from OCC.Core.IFSelect import IFSelect_RetDone
    HAS_OCC = True
except ImportError:
    HAS_OCC = False
    print("OCC not available, trying cadquery...")

try:
    import cadquery as cq
    HAS_CQ = True
except ImportError:
    HAS_CQ = False

SCRIPT_DIR = Path(__file__).parent
EXTRACTED_DIR = SCRIPT_DIR / "extracted"
MODELS_DIR = SCRIPT_DIR / "models"

# Mapping: output name -> STEP file path (relative to extracted)
COMPONENTS = {
    "esp32-cam": "1-esp32-cam-1.snapshot.3/ESP32-cam/ESP3-CAM v4.step",
    "ov2640-camera": "2-ov2640-for-esp32-cam-1.snapshot.1/step/OV2640_21mm-160_camera.STEP",
    "sim7000-lte": "3-sim7000-1.snapshot.1/SIM7000.step",
    "battery-12v": "6-battery-12v-7ah-150-x-65-x-100-mm-1.snapshot.6/Batería 12V-7Ah 150mm x 65mm x 100mm v5.step",
    "solar-controller": "7-solar-charge-controller-6.snapshot.2/Solar Charger Controller.STEP",
    "junction-box": "10-ip65-ip67-electrical-enclosures-2.snapshot.56/IP65 Electrical Enclosure, 200 mm x 155 mm x 80 mm/IP65 Electrical Enclosure, 200 mm x 155 mm x 80 mm.STEP",
    "solar-panel": "11-solar-panel-114.snapshot.4/PANEL SOLAR/PANEL SOLAR.STEP",
}


def convert_with_cadquery(step_path: Path, stl_path: Path) -> bool:
    """Convert STEP to STL using cadquery."""
    try:
        result = cq.importers.importStep(str(step_path))
        cq.exporters.export(result, str(stl_path))
        return True
    except Exception as e:
        print(f"  cadquery error: {e}")
        return False


def convert_with_occ(step_path: Path, stl_path: Path) -> bool:
    """Convert STEP to STL using OCC directly."""
    try:
        step_reader = STEPControl_Reader()
        status = step_reader.ReadFile(str(step_path))

        if status != IFSelect_RetDone:
            print(f"  Failed to read STEP file")
            return False

        step_reader.TransferRoots()
        shape = step_reader.OneShape()

        # Mesh the shape
        mesh = BRepMesh_IncrementalMesh(shape, 0.1)
        mesh.Perform()

        # Write STL
        stl_writer = StlAPI_Writer()
        stl_writer.Write(shape, str(stl_path))
        return True
    except Exception as e:
        print(f"  OCC error: {e}")
        return False


def main():
    print("\n=== STEP to STL Converter ===\n")

    MODELS_DIR.mkdir(exist_ok=True)

    if not HAS_CQ and not HAS_OCC:
        print("ERROR: Neither cadquery nor OCC available!")
        print("Install with: pip install cadquery")
        sys.exit(1)

    converter = "cadquery" if HAS_CQ else "OCC"
    print(f"Using converter: {converter}\n")

    for name, rel_path in COMPONENTS.items():
        step_path = EXTRACTED_DIR / rel_path
        stl_path = MODELS_DIR / f"{name}.stl"

        print(f"Converting: {name}")
        print(f"  From: {step_path}")
        print(f"  To:   {stl_path}")

        if not step_path.exists():
            print(f"  SKIP: STEP file not found")
            continue

        if HAS_CQ:
            success = convert_with_cadquery(step_path, stl_path)
        else:
            success = convert_with_occ(step_path, stl_path)

        if success:
            print(f"  OK: {stl_path.name}")
        else:
            print(f"  FAILED")
        print()

    print(f"\nConverted files in: {MODELS_DIR}")
    print("Note: STL files can be imported directly into Blender")


if __name__ == "__main__":
    main()
