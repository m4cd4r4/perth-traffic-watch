"""
SwanFlow Assembly Animation Renderer
Renders exploded-view assembly animation of SwanFlow hardware.

Usage: blender --background --python render_assembly.py
Output: frames/assembly_0000.png to assembly_0119.png
"""

import bpy
import os
import math
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "frames-photorealistic"
MODELS_DIR = SCRIPT_DIR / "models"
FRAME_COUNT = 120

# Components: display_name, stl_filename, exploded_pos, assembled_pos, scale, material_settings
# material_settings: (base_color, metallic, roughness, specular)
COMPONENTS = [
    ("ESP32-CAM", "esp32-cam", (0, 0, 0.12), (0, 0, 0), 0.001,
     {"pcb": (0.1, 0.4, 0.15, 1), "metal": 0.0, "rough": 0.7}),
    ("OV2640-Camera", "ov2640-camera", (0, 0, 0.20), (0, 0, 0.02), 0.001,
     {"pcb": (0.02, 0.02, 0.02, 1), "metal": 0.0, "rough": 0.4}),
    ("SIM7000-LTE", "sim7000-lte", (0.08, 0, 0.10), (0.03, 0, 0), 0.001,
     {"pcb": (0.1, 0.25, 0.4, 1), "metal": 0.0, "rough": 0.6}),
    ("Battery-12V", "battery-12v", (-0.12, 0, -0.08), (-0.05, 0, -0.03), 0.001,
     {"pcb": (0.03, 0.03, 0.03, 1), "metal": 0.0, "rough": 0.5}),
    ("Solar-Controller", "solar-controller", (0.12, 0, -0.08), (0.05, 0, -0.02), 0.001,
     {"pcb": (0.12, 0.35, 0.15, 1), "metal": 0.0, "rough": 0.6}),
    ("Junction-Box", "junction-box", (0, 0, -0.18), (0, 0, -0.06), 0.001,
     {"pcb": (0.4, 0.4, 0.4, 1), "metal": 0.0, "rough": 0.4}),
    ("Solar-Panel", "solar-panel", (0, 0, -0.30), (0, 0, -0.12), 0.001,
     {"pcb": (0.08, 0.12, 0.25, 1), "metal": 0.3, "rough": 0.2}),
]

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_material(name, settings):
    """Create photorealistic material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = settings["pcb"]
    bsdf.inputs['Metallic'].default_value = settings["metal"]
    bsdf.inputs['Roughness'].default_value = settings["rough"]
    return mat

def create_placeholder(name, size):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    return obj

def import_component(display_name, stl_name, scale, material_settings):
    """Import STL component and apply materials."""
    stl_path = MODELS_DIR / f"{stl_name}.stl"

    if stl_path.exists():
        bpy.ops.wm.stl_import(filepath=str(stl_path))
        obj = bpy.context.selected_objects[0]
        obj.name = display_name
        obj.scale = (scale, scale, scale)
        # Center the object
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    else:
        print(f"  STL not found: {stl_path}, using placeholder")
        sizes = {"Panel": (0.15, 0.10, 0.003), "Box": (0.08, 0.05, 0.03), "Battery": (0.06, 0.03, 0.04)}
        size = next((v for k, v in sizes.items() if k in display_name), (0.02, 0.02, 0.003))
        obj = create_placeholder(display_name, size)

    mat = create_material(f"Mat_{display_name}", material_settings)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

def setup_lighting():
    """Setup studio-style lighting for photorealistic render."""
    # Key light (main)
    bpy.ops.object.light_add(type='AREA', location=(0.4, -0.4, 0.5))
    key_light = bpy.context.active_object
    key_light.data.energy = 50
    key_light.data.size = 0.5
    key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

    # Fill light (softer)
    bpy.ops.object.light_add(type='AREA', location=(-0.3, -0.2, 0.3))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 20
    fill_light.data.size = 0.8

    # Rim/back light
    bpy.ops.object.light_add(type='AREA', location=(0, 0.4, 0.3))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 30
    rim_light.data.size = 0.3

    # Environment/background
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.03, 0.05, 0.08, 1.0)
        bg.inputs['Strength'].default_value = 0.5

def setup_camera():
    """Setup camera for close-up product shot."""
    bpy.ops.object.camera_add(location=(0.5, -0.5, 0.4))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(55), 0, math.radians(45))
    cam.data.lens = 85  # Portrait lens for product shots
    bpy.context.scene.camera = cam

def setup_render():
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.samples = 64
    s.render.resolution_x = 1920
    s.render.resolution_y = 1080
    s.render.image_settings.file_format = 'PNG'
    s.render.film_transparent = True

    # Enable GPU rendering
    prefs = bpy.context.preferences.addons['cycles'].preferences

    # Try to enable CUDA/OptiX (NVIDIA) or HIP (AMD)
    cuda_devices = prefs.get_devices_for_type('CUDA')
    optix_devices = prefs.get_devices_for_type('OPTIX')
    hip_devices = prefs.get_devices_for_type('HIP')

    if optix_devices:
        prefs.compute_device_type = 'OPTIX'
        for device in optix_devices:
            device.use = True
        print(f"GPU: Using OptiX ({len(optix_devices)} device(s))")
    elif cuda_devices:
        prefs.compute_device_type = 'CUDA'
        for device in cuda_devices:
            device.use = True
        print(f"GPU: Using CUDA ({len(cuda_devices)} device(s))")
    elif hip_devices:
        prefs.compute_device_type = 'HIP'
        for device in hip_devices:
            device.use = True
        print(f"GPU: Using HIP ({len(hip_devices)} device(s))")
    else:
        print("GPU: No compatible GPU found, using CPU")

    # Set scene to use GPU
    s.cycles.device = 'GPU'

def animate(objects, components):
    """Animate components from exploded to assembled positions."""
    s = bpy.context.scene
    s.frame_start, s.frame_end = 0, FRAME_COUNT - 1

    for obj, comp in zip(objects, components):
        display_name, stl_name, exploded, assembled, scale, _ = comp
        s.frame_set(0)
        obj.location = exploded
        obj.keyframe_insert(data_path="location")
        s.frame_set(FRAME_COUNT - 1)
        obj.location = assembled
        obj.keyframe_insert(data_path="location")

def render_frames():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for f in range(FRAME_COUNT):
        bpy.context.scene.frame_set(f)
        bpy.context.scene.render.filepath = str(OUTPUT_DIR / f"assembly_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"Frame {f+1}/{FRAME_COUNT}")

def main():
    print("\n=== SwanFlow Assembly Renderer (Photorealistic) ===\n")
    OUTPUT_DIR.mkdir(exist_ok=True)
    MODELS_DIR.mkdir(exist_ok=True)

    clear_scene()

    # Import all components
    objects = []
    for comp in COMPONENTS:
        display_name, stl_name, _, _, scale, mat_settings = comp
        print(f"Importing: {display_name}")
        obj = import_component(display_name, stl_name, scale, mat_settings)
        objects.append(obj)

    setup_lighting()
    setup_camera()
    setup_render()
    animate(objects, COMPONENTS)
    render_frames()
    print(f"\nDone! Frames in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
