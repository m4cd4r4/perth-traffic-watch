# Quick Start - Realistic PCB Rendering

Your detailed models are ready! Here's how to render them with realistic materials.

## ✅ Downloaded Models

You have these high-quality STEP models ready:
- ✅ ESP32-CAM (SnapEDA) - `models-detailed/esp32-cam.step`
- ✅ OV2640 Camera (GrabCAD) - `models-detailed/ov2640/step/OV2640_21mm-160_camera.STEP`
- ✅ SIM7600 LTE Module (SnapEDA) - `models-detailed/sim7600.step`

## 🚀 Render Now (One Command)

```bash
cd I:\Scratch\perth-traffic-watch\GrabCAD
blender --background --python render_assembly_realistic.py
```

This will:
1. Import your detailed STEP models
2. Apply realistic PCB materials (green solder mask, etc.)
3. Setup professional 3-point lighting
4. Render 120 frames to `frames-realistic/`

**Render Time**: ~2-3 minutes per frame on GPU = ~4-6 hours total

## 📊 What You'll Get

### Materials Applied:
- **ESP32-CAM & SIM7600**: Green PCB with semi-gloss finish, clearcoat protection
- **OV2640 Camera**: Black IC chip material
- **Battery**: Dark gray casing
- **Solar Panel**: Dark blue photovoltaic cells with metallic sheen
- **Enclosure**: Light gray plastic

### Lighting:
- Key light (warm, main illumination)
- Fill light (cool, soft shadows)
- Rim light (edge highlights)
- Dark studio environment

### Quality:
- Cycles renderer with denoising
- 96 samples (high quality, balanced speed)
- 1920x1080 resolution
- Transparent background

## 🎯 After Rendering

### Optimize for Web

```bash
cd scroll-animation
python optimize-frames.py --input ../frames-realistic
```

This creates:
- `frames-optimized/` - Compressed PNG (200-400KB each)
- `frames-webp/` - WebP format (100-200KB each, recommended)

### Update Animation

```bash
cd scroll-animation
# Edit index.html, change line 252:
# framePath: 'frames-optimized/assembly_',
```

Then refresh http://localhost:8081

## 🔧 Troubleshooting

### "STEP import failed"

Blender's default STL importer can't handle STEP files. You have two options:

**Option A: Convert STEP to STL** (Recommended)
Use FreeCAD (free):
```bash
# Install FreeCAD from https://www.freecad.org
# Open each STEP file and export as STL
# File → Export → STL format
```

**Option B: Install CAD Sketcher Addon**
- In Blender: Edit → Preferences → Add-ons
- Search "CAD Sketcher" and install
- This enables STEP import

### "Render too slow"

Reduce samples in `render_assembly_realistic.py`:
```python
s.cycles.samples = 64  # Instead of 96
```

### "GPU not detected"

Change to CPU rendering (slower but works everywhere):
```python
# Comment out GPU section in setup_render()
# Or just let it fall back to CPU automatically
```

## 📂 Directory Structure

```
GrabCAD/
├── models-detailed/          # Your downloaded models ✓
│   ├── esp32-cam.step
│   ├── ov2640/
│   │   └── step/OV2640_21mm-160_camera.STEP
│   └── sim7600.step
│
├── models/                   # Old simple models (fallback)
│   ├── battery-12v.stl
│   ├── solar-panel.stl
│   └── junction-box.stl
│
├── frames-realistic/         # NEW renders (will be created)
│   ├── assembly_0000.png
│   └── ...
│
└── scroll-animation/
    ├── frames-optimized/     # Web-ready frames (after optimization)
    └── index.html            # Update this to use new frames
```

## 🎨 Customization

### Change PCB Color

Edit `create_pcb_material()` in `render_assembly_realistic.py`:
```python
# Line 42, change base color:
bsdf.inputs['Base Color'].default_value = (0.05, 0.28, 0.14, 1.0)  # Green
# Try:
# (0.08, 0.08, 0.35, 1.0)  # Blue PCB
# (0.35, 0.08, 0.08, 1.0)  # Red PCB
# (0.02, 0.02, 0.02, 1.0)  # Black PCB
```

### Adjust Lighting

Edit `setup_realistic_lighting()`:
```python
# Line 187, increase brightness:
key.data.energy = 200  # Brighter (default: 150)
```

### Change Camera Angle

Edit `setup_camera()`:
```python
# Line 227, adjust position:
bpy.ops.object.camera_add(location=(0.8, -0.8, 0.6))  # Further back
```

## 💡 Tips

- **Test first**: Render just frame 60 to test:
  ```python
  # In render_frames(), change to:
  for f in [60]:  # Instead of range(FRAME_COUNT)
  ```

- **Lower resolution for testing**: In `setup_render()`:
  ```python
  s.render.resolution_x = 960   # Half size
  s.render.resolution_y = 540
  ```

- **Check progress**: Frames save as they render in `frames-realistic/`

## ✨ Expected Results

You should see photorealistic PCB boards with:
- ✅ Rich green solder mask with realistic gloss
- ✅ Visible component details from STEP models
- ✅ Professional product photography look
- ✅ Smooth shadows and highlights
- ✅ Realistic material properties

Much better than the current flat-colored shapes!
