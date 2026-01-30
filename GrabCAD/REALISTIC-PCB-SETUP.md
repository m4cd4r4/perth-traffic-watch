# Realistic PCB Animation Setup Guide

Complete guide for creating photorealistic PCB assembly animations with detailed components.

## 🎯 Overview

This setup transforms simple STL models into photorealistic PCB renders with:
- ✅ Green solder mask with realistic gloss
- ✅ Metallic copper traces
- ✅ Individual component materials (ICs, capacitors, resistors)
- ✅ Realistic solder joints
- ✅ Professional 3-point lighting
- ✅ 4K textures and bump mapping

## 📦 Step 1: Download Models & Resources

### Automatic Downloads

```bash
cd I:\Scratch\perth-traffic-watch\GrabCAD
python download-detailed-models.py
```

This downloads:
- ✅ PCB-Arts shader setup (GitHub)
- ✅ Setup scripts and instructions

### Manual Downloads (Required - Need Free Accounts)

#### HIGH PRIORITY (Essential for detail):

1. **ESP32-CAM (SnapEDA)** - Best quality with PCB footprint
   - URL: https://www.snapeda.com/parts/ESP32-CAM/AI-Thinker/view-part/
   - Format: Download STEP file
   - Save to: `models-detailed/esp32-cam.step`

2. **OV2640 Camera (GrabCAD)**
   - URL: https://grabcad.com/library/ov2640-for-esp32-cam-1
   - Save to: `models-detailed/ov2640/`

3. **SIM7600 LTE Module (SnapEDA)**
   - URL: https://www.snapeda.com/parts/SIM7600E-H/SIMCom/view-part/
   - Format: STEP
   - Save to: `models-detailed/sim7600.step`

#### MEDIUM PRIORITY (Nice to have):

4. **Solar Charge Controller (GrabCAD)**
   - URL: https://grabcad.com/library/solar-charge-controller-6
   - Save to: `models-detailed/solar-controller/`

5. **ESP32-CAM Alternative (GrabCAD)**
   - URL: https://grabcad.com/library/esp32-cam-1
   - Save to: `models-detailed/esp32-cam-grabcad.stl`

#### Texture Resources:

6. **BlenderKit PCB Material** (In Blender)
   - Install BlenderKit addon
   - Search: "Procedural Circuit board"
   - Apply directly in Blender

7. **Optional: High-res PCB Textures**
   - Visit: https://www.textures.com
   - Search: "PCB circuit board green"
   - Download 4K textures
   - Save to: `textures-pcb/`

## 🎨 Step 2: Setup Blender Materials

### Option A: Using Blender GUI

1. Open Blender with your assembly scene
2. Open Scripting workspace
3. Load `setup-pcb-materials.py`
4. Click "Run Script"

### Option B: Command Line (Background)

```bash
# Windows
blender --background your-scene.blend --python setup-pcb-materials.py

# Or edit render_assembly.py to include material setup
blender --background --python render_assembly_realistic.py
```

## 🔧 Step 3: Import Detailed Models

Update `render_assembly.py` to use the new detailed models:

```python
COMPONENTS = [
    ("ESP32-CAM", "esp32-cam.step", (0, 0, 0.12), (0, 0, 0), 0.001,
     {"pcb": (0.05, 0.25, 0.12, 1), "metal": 0.0, "rough": 0.4}),

    # ... other components
]
```

Import STEP files (better than STL):
```python
def import_component(display_name, filename, scale, material_settings):
    file_path = MODELS_DIR / filename

    if filename.endswith('.step'):
        # STEP import preserves more detail
        bpy.ops.import_mesh.stl(filepath=str(file_path))
    elif filename.endswith('.stl'):
        bpy.ops.wm.stl_import(filepath=str(file_path))
```

## 🎬 Step 4: Render with New Materials

### Quick Test Render

```bash
cd I:\Scratch\perth-traffic-watch\GrabCAD
blender --background --python test-render-single-frame.py
```

### Full Animation Render

```bash
blender --background --python render_assembly_realistic.py
```

Renders 120 frames to `frames-photorealistic-detailed/`

## 📊 Material Configuration

### PCB Board Material
- **Base Color**: Dark green (0.05, 0.25, 0.12)
- **Metallic**: 0.0
- **Roughness**: 0.4 (semi-gloss solder mask)
- **Clearcoat**: 0.3 (protective coating)
- **Bump Mapping**: Procedural noise for texture

### Copper Traces
- **Base Color**: Copper (0.95, 0.64, 0.54)
- **Metallic**: 1.0
- **Roughness**: 0.3

### IC Chips
- **Base Color**: Black epoxy (0.02, 0.02, 0.02)
- **Roughness**: 0.3 (semi-glossy plastic)

### Solder Joints
- **Base Color**: Silver-gray (0.7, 0.7, 0.75)
- **Metallic**: 0.9
- **Roughness**: 0.4

## 💡 Lighting Setup

The script creates professional 3-point lighting:

1. **Key Light** (Main)
   - Position: Front-right, elevated
   - Energy: 100W
   - Color: Slightly warm (1.0, 0.98, 0.95)

2. **Fill Light** (Shadows)
   - Position: Front-left, lower
   - Energy: 40W
   - Color: Slightly cool (0.95, 0.97, 1.0)

3. **Rim Light** (Edge highlight)
   - Position: Back-left
   - Energy: 60W

## 🎯 Quality Settings

### Cycles Render Engine
- Samples: 128 (high quality, ~2-3 min per frame)
- Denoising: Enabled (reduces noise)
- Resolution: 1920x1080
- Transparent background: Enabled

### Performance Optimization
- GPU Rendering: Auto-detected (CUDA/OptiX/HIP)
- Tile-based rendering for large scenes

## 📁 Output Structure

```
GrabCAD/
├── models-detailed/           # New detailed models
│   ├── esp32-cam.step
│   ├── ov2640/
│   ├── sim7600.step
│   └── pcb-shader/           # PCB-Arts shader setup
│
├── textures-pcb/             # Optional high-res textures
│   ├── green-solder-mask-4k.jpg
│   ├── copper-layer.jpg
│   └── silkscreen.png
│
├── frames-photorealistic-detailed/  # NEW renders
│   ├── assembly_0000.png
│   └── ...
│
└── scroll-animation/
    └── frames-optimized/     # Copy here after render
```

## 🚀 Quick Start Commands

```bash
# 1. Download automatic resources
python download-detailed-models.py

# 2. Download manual models (follow printed instructions)

# 3. Setup materials in Blender
blender --background your-scene.blend --python setup-pcb-materials.py

# 4. Test render
blender --background --python test-render-single-frame.py

# 5. Full render
blender --background --python render_assembly_realistic.py

# 6. Optimize frames for web
cd scroll-animation
python optimize-frames.py --input ../frames-photorealistic-detailed
```

## 🎨 Advanced: Custom Textures

If you want even more detail:

### 1. Download PCB-Arts Sample Project
```bash
git clone https://github.com/PCB-Arts/stylized-blender-setup.git
cd stylized-blender-setup
# Open sample .blend files to see complete setup
```

### 2. Add UV-Mapped Textures
- Use texture painting in Blender
- Apply real PCB photos as textures
- Add normal maps for bump detail

### 3. Component Labels
- Add text objects for IC labels
- Use UV unwrapping for silkscreen text
- Apply decals for component markings

## 📚 Resources

- [PCB-Arts Tutorial Series](https://blog.pcb-arts.com/en/blog/blender-tutorial-1)
- [GitHub PCB Shader Setup](https://github.com/PCB-Arts/stylized-blender-setup)
- [Blender Cycles Documentation](https://docs.blender.org/manual/en/latest/render/cycles/)
- [SnapEDA 3D Models](https://www.snapeda.com)
- [GrabCAD Library](https://grabcad.com/library)

## 🐛 Troubleshooting

### Models not importing
- Check file format (STEP preferred over STL)
- Verify paths in `MODELS_DIR`
- Try manual import: File → Import → STEP/STL

### Materials look flat
- Enable Cycles render engine
- Check lighting is present
- Verify material nodes are connected

### Slow rendering
- Reduce samples (64 instead of 128)
- Enable GPU rendering
- Lower resolution for tests

## 🎉 Expected Results

After setup, you should see:
- ✅ Realistic green PCB boards with gloss
- ✅ Visible copper traces and pads
- ✅ Individual components with proper materials
- ✅ Realistic shadows and highlights
- ✅ Professional product photography look

Render time: ~2-3 minutes per frame (GPU) = 4-6 hours total for 120 frames
