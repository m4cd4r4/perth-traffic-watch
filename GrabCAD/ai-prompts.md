# SwanFlow AI Product Image Generation

## Google Whisk Prompts

### Prompt 1: Assembled View (Hero Image)
```
SwanFlow IoT traffic monitoring device, assembled state, horizontal orientation,
professional product photography, premium tech aesthetic, modern industrial design.

Device components visible:
- ESP32-CAM module with camera lens (center, green PCB)
- SIM7600 LTE module (green PCB with antenna)
- 12V battery pack (dark gray casing)
- Solar panel (dark blue photovoltaic cells)
- Junction box enclosure (light gray plastic)
- Professional lighting, clean white studio background
- Sharp focus, high detail, 4K quality
- Apple-style product photography
```

### Prompt 2: Exploded View
```
SwanFlow IoT traffic monitoring device, exploded view assembly diagram,
components floating and separated with clear spacing, technical illustration style.

All components visible and labeled:
- ESP32-CAM module (top, green PCB with camera)
- OV2640 camera sensor (separated above ESP32)
- SIM7600 LTE module (right side, green PCB)
- 12V battery (bottom left, dark casing)
- Solar controller (bottom center, green PCB)
- Junction box (bottom, light gray enclosure)
- Solar panel (very bottom, dark blue cells)

Professional technical photography, clean white background,
isometric perspective, components aligned vertically,
Apple-style exploded view, premium product showcase
```

## Google Veo Flow Animation Prompt

```
Smoothly transition from assembled product to exploded view assembly diagram.
Slow motion professional internal tech showcase.
Apple-style disassembly animation showing all components separating gracefully.
High quality professional 3D explosion with smooth separation of parts.
Camera remains static, components move outward from center.
Professional product photography lighting throughout.
8 seconds duration, cinematic quality.
```

## Instructions

### Phase 1: Google Whisk
1. Go to https://labs.google/fx/tools/whisk
2. Click "Create"
3. Add subject: Upload a reference image of IoT device or electronics
4. Paste Prompt 1 into the prompt field
5. Click "Shoot" and wait for generation
6. Download best result as `swanflow-assembled.png`
7. Repeat with Prompt 2, download as `swanflow-exploded.png`

### Phase 2: Google Veo Flow
1. Go to https://videofx.withgoogle.com/
2. Click "New Project"
3. Select "Frames to Video"
4. Upload `swanflow-assembled.png` as start frame
5. Upload `swanflow-exploded.png` as end frame
6. Paste animation prompt
7. Click "Shoot"
8. Download result as `swanflow-animation.mp4`

### Phase 3: EZGif Frame Extraction
1. Go to https://ezgif.com/video-to-jpg
2. Upload `swanflow-animation.mp4`
3. Set FPS to 30
4. Click "Convert to JPG"
5. Click "Split to frames"
6. Download as ZIP
7. Save to `GrabCAD/frames-ai/`

### Phase 4: Convert to WebP (Optional)
```bash
cd I:\Scratch\perth-traffic-watch\GrabCAD\frames-ai
for file in *.jpg; do
    cwebp -q 85 "$file" -o "${file%.jpg}.webp"
done
```

### Phase 5: Update Animation
Update `scroll-animation/index.html` line 252:
```javascript
framePath: 'frames-ai/assembly_',
frameExtension: '.webp', // or '.jpg'
```

## Expected Results
- 240 frames @ 30 FPS (8 seconds)
- File size: ~20-40 MB for WebP, ~60-80 MB for JPG
- Smooth Apple-style exploded view animation
- Professional product photography quality
