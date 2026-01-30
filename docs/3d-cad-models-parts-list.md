# SwanFlow 3D CAD Models - Parts List

This document contains download links for photorealistic 3D CAD models of all SwanFlow hardware components. These models can be used for:

- **Hero section scroll animation** (exploded view assembly)
- **Documentation renders**
- **3D printing enclosures**
- **Technical illustrations**

---

## Quick Start

1. Create a free account at [GrabCAD.com](https://grabcad.com/register)
2. Download STEP files for each component below
3. Import into Blender (via [BlenderBIM add-on](https://blenderbim.org/) or convert to OBJ first)
4. Apply materials and render

---

## Component Downloads

### Core Electronics

| # | Component | Download Link | Format | Dimensions |
|---|-----------|---------------|--------|------------|
| 1 | **ESP32-CAM Board** | [GrabCAD](https://grabcad.com/library/esp32-cam-1) | STEP | 40.5 x 27 x 4.5mm |
| 2 | **OV2640 Camera Module** | [GrabCAD](https://grabcad.com/library/ov2640-for-esp32-cam-1) | STEP | Plugs into ESP32 |
| 3 | **ESP32-CAM** (alternative) | [Sketchfab](https://sketchfab.com/3d-models/esp32-cam-dummy-7d7a983f89734c3dbf4bd7ceb06be00f) | GLTF/OBJ | With textures |
| 4 | **ESP32-CAM + SD Card** | [3D ContentCentral](https://www.3dcontentcentral.com/download-model.aspx?catalogid=171&id=1048064) | STEP | Complete assembly |

### Cellular Modem

| # | Component | Download Link | Format | Notes |
|---|-----------|---------------|--------|-------|
| 5 | **SIM7000A LTE Module** | [GrabCAD](https://grabcad.com/library/sim7000-1) | STEP | 4G NB-IoT/Cat-M |
| 6 | **SIM7600 Module** | [GrabCAD](https://grabcad.com/library/sim7600-module-1) | STEP | 4G LTE Cat4 |
| 7 | **SIM7600 STEP file** | [GitHub](https://github.com/brunoeagle/kicad-open-3d/blob/master/SIM7600.step) | STEP | Direct download |
| 8 | **SIM7600G-H 4G HAT** | [GrabCAD](https://grabcad.com/library/sim7600g-h-4g-hat-b-1) | STEP | Raspberry Pi HAT style |

### Power System

| # | Component | Download Link | Format | Notes |
|---|-----------|---------------|--------|-------|
| 9 | **12V 7Ah Battery** | [GrabCAD](https://grabcad.com/library/12v-7ah-sealed-lead-acid-battery-1) | STEP | Sealed lead acid |
| 10 | **12V 7Ah Battery** (alt) | [GrabCAD](https://grabcad.com/library/battery-12v-7ah-150-x-65-x-100-mm-1) | STEP | 150 x 65 x 100mm |
| 11 | **18650 Li-ion Cell** | [GrabCAD](https://grabcad.com/library/18650-li-ion-battery) | STEP | Alternative power |
| 12 | **18650 Battery** | [Printables](https://www.printables.com/model/54312-18650-battery) | STEP | With STEP CAD file |

### Solar Components

| # | Component | Download Link | Format | Notes |
|---|-----------|---------------|--------|-------|
| 13 | **Solar Charge Controller** | [GrabCAD](https://grabcad.com/library/solar-charge-controller-6) | STEP | PWM/MPPT style |
| 14 | **Solar Charge Controller** (alt) | [3D ContentCentral](https://www.3dcontentcentral.com/download-model.aspx?catalogid=171&id=1531172) | STEP | PCB-8 model |
| 15 | **Victron Controllers** | [TraceParts](https://www.traceparts.com/en/search/victron-energy-solar-solar-charge-controllers) | STEP | Professional grade |
| 16 | **Solar Panels** | [GrabCAD](https://grabcad.com/library/tag/solarpanel) | STEP | Various sizes |
| 17 | **Solar Panels** | [TraceParts](https://www.traceparts.com/en/search/traceparts-classification-electrical-power-generation-solar-panels) | STEP | Manufacturer-certified |
| 18 | **Solar Panel** | [Free3D](https://free3d.com/3d-models/solar-panel) | OBJ/FBX | Ready for Blender |

### Enclosure

| # | Component | Download Link | Format | Notes |
|---|-----------|---------------|--------|-------|
| 19 | **IP65 Junction Box** | [GrabCAD](https://grabcad.com/library/ip65-waterproof-electronic-junction-box-enclosure-case-outdoor-terminal-cable-ip65-4n45799-1) | STEP | Weatherproof |
| 20 | **IP65/IP67 Enclosures** | [GrabCAD](https://grabcad.com/library/ip65-ip67-electrical-enclosures-2) | STEP | Multiple sizes |
| 21 | **Junction Box with Lock** | [GrabCAD](https://grabcad.com/library/ip65-junction-box-with-lock-300-mm-x-200-mm-x-170-mm-1) | STEP | 300x200x170mm |
| 22 | **ESP32-CAM Case** | [GrabCAD](https://grabcad.com/library/esp32-cam-case-2) | STEP | 3D printable |

### Small Components

| # | Component | Download Link | Format | Notes |
|---|-----------|---------------|--------|-------|
| 23 | **MicroSD Card** | [GrabCAD Search](https://grabcad.com/library?query=microsd) | STEP | Various models |
| 24 | **USB-to-TTL Programmer** | [GrabCAD Search](https://grabcad.com/library?query=usb%20ttl) | STEP | FTDI/CH340 style |

---

## File Format Compatibility

### For Blender (Photorealistic Rendering)

| Format | Import Method |
|--------|---------------|
| **STEP** | Install [BlenderBIM add-on](https://blenderbim.org/) or convert first |
| **OBJ** | File → Import → Wavefront (.obj) |
| **FBX** | File → Import → FBX (.fbx) |
| **GLTF/GLB** | File → Import → glTF 2.0 (.glb/.gltf) |

### Converting STEP to OBJ

**Option 1: Online Converter**
- [imagetostl.com/convert/file/step/to/obj](https://imagetostl.com/convert/file/step/to/obj)

**Option 2: FreeCAD (Free Software)**
```bash
# Install FreeCAD
# Open STEP file
# File → Export → OBJ format
```

**Option 3: Blender with BlenderBIM**
```bash
# Install BlenderBIM add-on
# File → Import → IFC/STEP
# Direct STEP import support
```

---

## Recommended Download Priority

For the hero section assembly animation, download these first:

1. **ESP32-CAM** - The star of the show
2. **OV2640 Camera** - Plugs into ESP32
3. **Junction Box IP65** - Main enclosure
4. **Solar Panel** - Most visually striking
5. **12V Battery** - Power source
6. **Solar Charge Controller** - Completes the system

---

## Material Guide for Blender

When rendering, apply these materials for photorealism:

| Component | Material | Colour | Properties |
|-----------|----------|--------|------------|
| PCB Board | Matte | Green `#1a5c1a` | Roughness: 0.8 |
| Copper Traces | Metallic | Gold `#d4af37` | Metallic: 1.0 |
| IC Chips | Glossy Plastic | Black `#1a1a1a` | Roughness: 0.3 |
| Camera Lens | Glass | Dark | IOR: 1.5 |
| Solar Panel | Glass + Metal | Blue `#1a2a4a` | Two-layer material |
| Battery | Matte Plastic | Black | Roughness: 0.7 |
| Junction Box | ABS Plastic | Grey `#4a4a4a` | Roughness: 0.5 |
| Metal Pins | Metallic | Silver | Metallic: 1.0 |

---

## Animation Sequence

For scroll-driven assembly animation:

| Scroll % | Assembly Step |
|----------|---------------|
| 0% | All parts exploded/floating |
| 20% | OV2640 camera connects to ESP32-CAM |
| 40% | ESP32-CAM + SIM7000A positioned |
| 60% | Electronics enter junction box |
| 80% | Junction box lid closes |
| 100% | Solar panel + battery connect |

---

## Resources

### Account Registration (Free)
- [GrabCAD Register](https://grabcad.com/register)
- [3D ContentCentral](https://www.3dcontentcentral.com/)
- [TraceParts](https://www.traceparts.com/)

### Software
- [Blender](https://www.blender.org/) - Free 3D rendering
- [BlenderBIM](https://blenderbim.org/) - STEP import add-on
- [FreeCAD](https://www.freecadweb.org/) - Free CAD software

### Tutorials
- [Blender Product Animation](https://www.skillshare.com/en/classes/product-animation-in-blender-bring-your-3d-renders-to-life/1954902863)
- [Apple-style Scroll Animation](https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/)

---

## License Notes

Most GrabCAD community models are shared for personal and educational use. Check individual model pages for specific license terms before commercial use.

---

*Last Updated: January 2026*
