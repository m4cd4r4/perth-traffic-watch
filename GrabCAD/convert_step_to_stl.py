"""
STEP to STL Converter
Converts STEP files to STL format using available Python libraries.
"""

import os
import sys
from pathlib import Path

def convert_with_pythonocc():
    """Try using pythonocc-core library."""
    try:
        from OCC.Core.STEPControl import STEPControl_Reader
        from OCC.Core.StlAPI import StlAPI_Writer
        from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
        return True, "pythonocc"
    except ImportError:
        return False, None

def convert_with_cadquery():
    """Try using cadquery library."""
    try:
        import cadquery as cq
        return True, "cadquery"
    except ImportError:
        return False, None

def convert_step_pythonocc(step_file, stl_file):
    """Convert using pythonocc."""
    from OCC.Core.STEPControl import STEPControl_Reader
    from OCC.Core.StlAPI import StlAPI_Writer
    from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
    from OCC.Core.IFSelect import IFSelect_RetDone

    # Read STEP file
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(str(step_file))

    if status != IFSelect_RetDone:
        raise Exception(f"Error reading STEP file: {step_file}")

    step_reader.TransferRoots()
    shape = step_reader.OneShape()

    # Mesh the shape
    mesh = BRepMesh_IncrementalMesh(shape, 0.1)
    mesh.Perform()

    # Write STL file
    stl_writer = StlAPI_Writer()
    stl_writer.Write(shape, str(stl_file))

    print(f"✓ Converted: {step_file.name} -> {stl_file.name}")

def convert_step_cadquery(step_file, stl_file):
    """Convert using cadquery."""
    import cadquery as cq

    # Import STEP file
    result = cq.importers.importStep(str(step_file))

    # Export as STL
    cq.exporters.export(result, str(stl_file))

    print(f"✓ Converted: {step_file.name} -> {stl_file.name}")

def main():
    script_dir = Path(__file__).parent
    models_dir = script_dir / "models-detailed"

    # Check available libraries
    has_pythonocc, _ = convert_with_pythonocc()
    has_cadquery, _ = convert_with_cadquery()

    if not has_pythonocc and not has_cadquery:
        print("ERROR: No STEP conversion library found!")
        print("\nInstall one of:")
        print("  pip install pythonocc-core")
        print("  pip install cadquery")
        print("\nOr use online converter:")
        print("  https://www.convertio.co/step-stl/")
        print("  https://products.aspose.app/3d/conversion/step-to-stl")
        sys.exit(1)

    converter = convert_step_pythonocc if has_pythonocc else convert_step_cadquery
    library = "pythonocc" if has_pythonocc else "cadquery"

    print(f"\nUsing {library} for conversion\n")
    print("=" * 70)

    # Find all STEP files
    step_files = list(models_dir.rglob("*.STEP")) + list(models_dir.rglob("*.step"))

    if not step_files:
        print("No STEP files found in models-detailed/")
        sys.exit(1)

    print(f"Found {len(step_files)} STEP file(s)\n")

    # Convert each file
    for step_file in step_files:
        # Create output filename
        stl_file = step_file.with_suffix('.stl')

        try:
            print(f"Converting: {step_file.name}...")
            converter(step_file, stl_file)
        except Exception as e:
            print(f"✗ Failed: {e}")

    print("\n" + "=" * 70)
    print("Conversion complete!")
    print("\nNow run: blender --background --python render_assembly_realistic.py")

if __name__ == "__main__":
    main()
