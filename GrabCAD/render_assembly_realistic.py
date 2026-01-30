"""
SwanFlow Assembly Animation Renderer - REALISTIC VERSION
Renders photorealistic exploded-view assembly with detailed STEP models and PCB materials.

Usage: blender --background --python render_assembly_realistic.py
Output: frames-realistic/assembly_0000.png to assembly_0119.png
"""

import bpy
import os
import math
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "frames-realistic"
MODELS_DIR = SCRIPT_DIR / "models-detailed"
FRAME_COUNT = 120

# Components: display_name, model_file, exploded_pos, assembled_pos, scale, material_type
COMPONENTS = [
    ("ESP32-CAM", "esp32-cam.step", (0, 0, 0.15), (0, 0, 0), 0.001, "pcb"),
    ("OV2640-Camera", "ov2640/step/OV2640_21mm-160_camera.STEP", (0, 0, 0.25), (0, 0, 0.03), 0.001, "ic"),
    ("SIM7600-LTE", "sim7600.step", (0.12, 0, 0.12), (0.04, 0, 0.01), 0.001, "pcb"),
    # Placeholders for other components (using existing STL files)
    ("Battery-12V", "../models/battery-12v.stl", (-0.15, 0, -0.10), (-0.06, 0, -0.04), 0.001, "battery"),
    ("Solar-Controller", "../models/solar-controller.stl", (0.15, 0, -0.10), (0.06, 0, -0.03), 0.001, "pcb"),
    ("Junction-Box", "../models/junction-box.stl", (0, 0, -0.22), (0, 0, -0.08), 0.001, "enclosure"),
    ("Solar-Panel", "../models/solar-panel.stl", (0, 0, -0.35), (0, 0, -0.15), 0.001, "solar"),
]

# ============================================================================
# SCENE SETUP
# ============================================================================

def clear_scene():
    """Remove all objects from scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("Scene cleared")

# ============================================================================
# REALISTIC PCB MATERIALS
# ============================================================================

def create_pcb_material(name="PCB_Material"):
    """Realistic PCB with green solder mask."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = (0.05, 0.28, 0.14, 1.0)  # Rich green
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.35  # Semi-gloss
    # Specular removed in Blender 5.0 - now controlled by IOR
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = 0.6
    bsdf.inputs['Coat Weight'].default_value = 0.4  # Protective coating (renamed from Clearcoat in 5.0)
    bsdf.inputs['Coat Roughness'].default_value = 0.08

    # Bump for PCB texture
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -200)
    bump.inputs['Strength'].default_value = 0.15

    # Noise for surface detail
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, -200)
    noise.inputs['Scale'].default_value = 120.0
    noise.inputs['Detail'].default_value = 16.0
    noise.inputs['Roughness'].default_value = 0.6

    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def create_ic_material(name="IC_Chip"):
    """Black IC chip material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.015, 0.015, 0.015, 1.0)  # Matte black
    bsdf.inputs['Roughness'].default_value = 0.25
    # Specular removed in Blender 5.0
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = 0.4

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_battery_material(name="Battery"):
    """Dark battery casing."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.08, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.5

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_enclosure_material(name="Enclosure"):
    """Light gray plastic enclosure."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.75, 0.75, 0.75, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.4

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_solar_material(name="Solar_Panel"):
    """Dark blue solar cell material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.04, 0.08, 0.25, 1.0)  # Dark blue
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.2  # Glossy solar cells

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

# ============================================================================
# IMPORT MODELS
# ============================================================================

def import_component(display_name, filename, scale, material_type):
    """Import STEP or STL model and apply material."""
    file_path = MODELS_DIR / filename if not filename.startswith('../') else SCRIPT_DIR / filename.replace('../', '')

    print(f"  Importing: {display_name} from {file_path}")

    if not file_path.exists():
        print(f"  WARNING: File not found: {file_path}")
        print(f"  Creating placeholder cube")
        bpy.ops.mesh.primitive_cube_add(size=0.02)
        obj = bpy.context.active_object
        obj.name = display_name
    else:
        # Import based on file type
        if str(filename).lower().endswith('.step'):
            try:
                # Try importing STEP file (requires CAD Sketcher addon or similar)
                bpy.ops.import_mesh.stl(filepath=str(file_path))
                obj = bpy.context.selected_objects[0]
                obj.name = display_name
                print(f"    [OK] Imported as STL fallback")
            except:
                print(f"    [INFO] STEP import requires CAD addon, trying alternate method")
                # Fallback: User should convert STEP to STL manually
                print(f"    [INFO] Please convert {filename} to STL format")
                bpy.ops.mesh.primitive_cube_add(size=0.02)
                obj = bpy.context.active_object
                obj.name = display_name
        elif str(filename).lower().endswith('.stl'):
            bpy.ops.wm.stl_import(filepath=str(file_path))
            obj = bpy.context.selected_objects[0]
            obj.name = display_name
            print(f"    [OK] Imported STL")
        else:
            print(f"    [ERROR] Unknown file format")
            bpy.ops.mesh.primitive_cube_add(size=0.02)
            obj = bpy.context.active_object
            obj.name = display_name

    obj.scale = (scale, scale, scale)

    # Apply material
    material_funcs = {
        "pcb": create_pcb_material,
        "ic": create_ic_material,
        "battery": create_battery_material,
        "enclosure": create_enclosure_material,
        "solar": create_solar_material,
    }

    mat_func = material_funcs.get(material_type, create_pcb_material)
    mat = mat_func(f"Mat_{display_name}")

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return obj

# ============================================================================
# LIGHTING
# ============================================================================

def setup_realistic_lighting():
    """Professional 3-point product photography lighting."""
    print("\nSetting up realistic lighting...")

    # Key light (main, warm)
    bpy.ops.object.light_add(type='AREA', location=(0.6, -0.6, 0.7))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 150
    key.data.size = 1.0
    key.data.color = (1.0, 0.98, 0.96)
    key.rotation_euler = (math.radians(50), 0, math.radians(45))

    # Fill light (soft, cool)
    bpy.ops.object.light_add(type='AREA', location=(-0.5, -0.4, 0.5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 60
    fill.data.size = 1.5
    fill.data.color = (0.96, 0.98, 1.0)

    # Rim/back light
    bpy.ops.object.light_add(type='AREA', location=(0.3, 0.7, 0.5))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = 80
    rim.data.size = 0.6
    rim.rotation_euler = (math.radians(130), 0, math.radians(-30))

    # World environment
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.04, 0.06, 0.10, 1.0)
        bg.inputs['Strength'].default_value = 0.25

    print("  [OK] Lighting setup complete")

# ============================================================================
# CAMERA
# ============================================================================

def setup_camera():
    """Product photography camera setup."""
    bpy.ops.object.camera_add(location=(0.6, -0.6, 0.5))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(60), 0, math.radians(45))
    cam.data.lens = 90  # Slightly telephoto
    bpy.context.scene.camera = cam
    print("[OK] Camera setup complete")

# ============================================================================
# RENDER SETTINGS
# ============================================================================

def setup_render():
    """High-quality Cycles render settings."""
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.samples = 96  # Good quality, reasonable speed
    s.cycles.use_denoising = True
    s.render.resolution_x = 1920
    s.render.resolution_y = 1080
    s.render.image_settings.file_format = 'PNG'
    s.render.film_transparent = True

    # GPU rendering
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'OPTIX'  # Try CUDA if this fails
        for device in prefs.devices:
            device.use = True
        s.cycles.device = 'GPU'
        print("[OK] GPU rendering enabled")
    except:
        print("[INFO] Using CPU rendering")

# ============================================================================
# ANIMATION
# ============================================================================

def animate(objects, components):
    """Create exploded view animation."""
    s = bpy.context.scene
    s.frame_start, s.frame_end = 0, FRAME_COUNT - 1

    for obj, comp in zip(objects, components):
        _, _, exploded, assembled, _, _ = comp

        s.frame_set(0)
        obj.location = exploded
        obj.keyframe_insert(data_path="location")

        s.frame_set(FRAME_COUNT - 1)
        obj.location = assembled
        obj.keyframe_insert(data_path="location")

    print("[OK] Animation keyframes set")

# ============================================================================
# RENDER FRAMES
# ============================================================================

def render_frames():
    """Render all frames."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"\nRendering {FRAME_COUNT} frames to: {OUTPUT_DIR}\n")

    for f in range(FRAME_COUNT):
        bpy.context.scene.frame_set(f)
        bpy.context.scene.render.filepath = str(OUTPUT_DIR / f"assembly_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"  [{f+1}/{FRAME_COUNT}] Frame rendered")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*70)
    print("SwanFlow Realistic Assembly Renderer")
    print("="*70 + "\n")

    print("[1/7] Clearing scene...")
    clear_scene()

    print("\n[2/7] Importing components...")
    objects = []
    for comp in COMPONENTS:
        display_name, model_file, _, _, scale, mat_type = comp
        obj = import_component(display_name, model_file, scale, mat_type)
        objects.append(obj)

    print("\n[3/7] Setting up lighting...")
    setup_realistic_lighting()

    print("\n[4/7] Setting up camera...")
    setup_camera()

    print("\n[5/7] Configuring render settings...")
    setup_render()

    print("\n[6/7] Creating animation...")
    animate(objects, COMPONENTS)

    print("\n[7/7] Rendering frames...")
    render_frames()

    print("\n" + "="*70)
    print("RENDER COMPLETE!")
    print("="*70)
    print(f"\nOutput: {OUTPUT_DIR}")
    print(f"Frames: {FRAME_COUNT} @ 1920x1080")
    print("\nNext step: Optimize for web")
    print("  cd scroll-animation")
    print("  python optimize-frames.py --input ../frames-realistic\n")

if __name__ == "__main__":
    main()
