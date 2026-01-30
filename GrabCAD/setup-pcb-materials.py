"""
SwanFlow PCB Material Setup for Blender
Automatically sets up realistic PCB materials based on PCB-Arts methodology.

Usage: blender --background --python setup-pcb-materials.py
       or run directly in Blender's scripting tab
"""

import bpy
import os
import math
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
MODELS_DIR = SCRIPT_DIR / "models-detailed"
TEXTURES_DIR = SCRIPT_DIR / "textures-pcb"
SHADER_DIR = MODELS_DIR / "pcb-shader" / "stylized-blender-setup-main"

# ============================================================================
# PCB MATERIAL CREATION (Based on PCB-Arts methodology)
# ============================================================================

def create_pcb_material(name="PCB_Material"):
    """
    Create photorealistic PCB material with:
    - Green solder mask
    - Copper traces (procedural)
    - Realistic roughness and specular
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)

    # Green solder mask base color
    bsdf.inputs['Base Color'].default_value = (0.05, 0.25, 0.12, 1.0)  # Dark green
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.4  # Semi-gloss finish
    bsdf.inputs['Specular'].default_value = 0.5
    bsdf.inputs['Clearcoat'].default_value = 0.3  # Protective coating
    bsdf.inputs['Clearcoat Roughness'].default_value = 0.1

    # Add bump for PCB texture
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -200)
    bump.inputs['Strength'].default_value = 0.1

    # Noise texture for subtle surface variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, -200)
    noise.inputs['Scale'].default_value = 100.0
    noise.inputs['Detail'].default_value = 16.0

    # Connect nodes
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def create_copper_material(name="Copper_Traces"):
    """Create realistic copper trace material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)

    # Copper color
    bsdf.inputs['Base Color'].default_value = (0.95, 0.64, 0.54, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.3
    bsdf.inputs['Specular'].default_value = 0.8

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def create_component_material(name, color, metallic=0.2, roughness=0.6):
    """Create material for electronic components (capacitors, resistors, etc)."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)

    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness

    nodes["Principled BSDF"].node_tree.links.new(
        bsdf.outputs['BSDF'],
        output.inputs['Surface']
    )

    return mat

def create_solder_material(name="Solder"):
    """Create realistic solder joint material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)

    # Lead-free solder appearance
    bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.75, 1.0)  # Silver-gray
    bsdf.inputs['Metallic'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.4
    bsdf.inputs['Specular'].default_value = 0.7

    links = mat.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def create_ic_chip_material(name="IC_Chip"):
    """Create material for IC chips (black epoxy body)."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)

    # Black plastic/epoxy
    bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.3  # Semi-glossy
    bsdf.inputs['Specular'].default_value = 0.4

    links = mat.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

# ============================================================================
# APPLY MATERIALS TO OBJECTS
# ============================================================================

def apply_materials_to_objects():
    """Apply realistic materials to imported objects."""

    print("\nApplying PCB materials to objects...")

    # Create materials
    pcb_mat = create_pcb_material()
    copper_mat = create_copper_material()
    solder_mat = create_solder_material()
    ic_mat = create_ic_chip_material()

    # Component materials
    capacitor_mat = create_component_material("Capacitor", (0.8, 0.6, 0.3, 1.0))  # Tan
    resistor_mat = create_component_material("Resistor", (0.15, 0.12, 0.1, 1.0))  # Dark brown

    # Apply to objects based on name patterns
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue

        name_lower = obj.name.lower()

        # Apply PCB material to boards
        if any(keyword in name_lower for keyword in ['esp32', 'pcb', 'board', 'sim7000', 'sim7600']):
            if obj.data.materials:
                obj.data.materials[0] = pcb_mat
            else:
                obj.data.materials.append(pcb_mat)
            print(f"  ✓ Applied PCB material to: {obj.name}")

        # Apply IC material to chips/modules
        elif any(keyword in name_lower for keyword in ['chip', 'ic', 'module', 'camera', 'ov2640']):
            if obj.data.materials:
                obj.data.materials[0] = ic_mat
            else:
                obj.data.materials.append(ic_mat)
            print(f"  ✓ Applied IC material to: {obj.name}")

        # Solar panel - blue/metallic
        elif 'solar' in name_lower or 'panel' in name_lower:
            solar_mat = create_component_material("Solar_Cell", (0.05, 0.1, 0.3, 1.0), metallic=0.6)
            if obj.data.materials:
                obj.data.materials[0] = solar_mat
            else:
                obj.data.materials.append(solar_mat)
            print(f"  ✓ Applied solar material to: {obj.name}")

        # Battery - dark gray/black
        elif 'battery' in name_lower:
            battery_mat = create_component_material("Battery", (0.1, 0.1, 0.1, 1.0), roughness=0.5)
            if obj.data.materials:
                obj.data.materials[0] = battery_mat
            else:
                obj.data.materials.append(battery_mat)
            print(f"  ✓ Applied battery material to: {obj.name}")

        # Enclosure/box - light gray
        elif 'box' in name_lower or 'enclosure' in name_lower or 'junction' in name_lower:
            box_mat = create_component_material("Enclosure", (0.7, 0.7, 0.7, 1.0), roughness=0.4)
            if obj.data.materials:
                obj.data.materials[0] = box_mat
            else:
                obj.data.materials.append(box_mat)
            print(f"  ✓ Applied enclosure material to: {obj.name}")

# ============================================================================
# IMPROVED LIGHTING SETUP
# ============================================================================

def setup_realistic_lighting():
    """Setup 3-point lighting for PCB photography."""

    print("\nSetting up realistic lighting...")

    # Remove existing lights
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj)

    # Key light (main, slightly warm)
    bpy.ops.object.light_add(type='AREA', location=(0.5, -0.5, 0.6))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 100
    key.data.size = 0.8
    key.data.color = (1.0, 0.98, 0.95)  # Slight warm tint
    key.rotation_euler = (math.radians(50), 0, math.radians(45))

    # Fill light (softer, cooler)
    bpy.ops.object.light_add(type='AREA', location=(-0.4, -0.3, 0.4))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 40
    fill.data.size = 1.2
    fill.data.color = (0.95, 0.97, 1.0)  # Slight cool tint

    # Rim light (highlights edges)
    bpy.ops.object.light_add(type='AREA', location=(0.2, 0.6, 0.4))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = 60
    rim.data.size = 0.5
    rim.rotation_euler = (math.radians(130), 0, math.radians(-30))

    # Environment lighting
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.05, 0.08, 0.12, 1.0)  # Dark blue-gray
        bg.inputs['Strength'].default_value = 0.3

    print("  ✓ 3-point lighting setup complete")

# ============================================================================
# MAIN SETUP FUNCTION
# ============================================================================

def main():
    print("\n" + "="*70)
    print("SwanFlow PCB Material Setup")
    print("="*70 + "\n")

    # Check if we have objects
    if len([obj for obj in bpy.data.objects if obj.type == 'MESH']) == 0:
        print("WARNING: No mesh objects found!")
        print("Import your 3D models first, then run this script.")
        return

    # Apply materials
    apply_materials_to_objects()

    # Setup lighting
    setup_realistic_lighting()

    # Configure render settings for high quality
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128  # Higher quality
    scene.cycles.use_denoising = True

    print("\n" + "="*70)
    print("Setup Complete!")
    print("="*70)
    print("\nMaterials created:")
    print("  ✓ PCB_Material (green solder mask)")
    print("  ✓ Copper_Traces (metallic copper)")
    print("  ✓ Solder (lead-free solder joints)")
    print("  ✓ IC_Chip (black epoxy)")
    print("  ✓ Component materials (capacitors, resistors)")
    print("\nNext: Render your animation!")
    print("  blender --background --python render_assembly.py\n")

if __name__ == "__main__":
    main()
