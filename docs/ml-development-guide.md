# ML Development Guide: Vehicle Detection on ESP32-CAM

## Goal: "See Only Rectangles"

The ESP32 should detect vehicles as **centroids or bounding boxes** - not "understand" what it's seeing like human vision. This is computationally simpler and privacy-preserving.

---

## Recommended Approach: Edge Impulse FOMO

### Why FOMO (Faster Objects, More Objects)?

| Feature | FOMO | Traditional Object Detection |
|---------|------|------------------------------|
| Model size | < 100KB | 1-10MB |
| Inference time | ~100ms | 4-5 seconds |
| RAM usage | ~200KB | 1-4MB |
| ESP32 compatible | Yes | Barely/No |
| Output | Centroids | Bounding boxes |
| Accuracy | Good for counting | Better for identification |

**FOMO outputs centroids (x, y coordinates), not bounding boxes.** This is perfect for counting - you don't need the box size, just the location.

### How FOMO Works

1. Divides image into grid cells (e.g., 6x6 on 96x96 image)
2. Each cell predicts: "Is there a vehicle here? Yes/No"
3. Returns list of (x, y) centroids where vehicles detected
4. You count centroids crossing a virtual line

---

## Development Workflow

### Phase 1: Data Collection (1-2 days)

**Option A: Record from test location**
```
1. Mount ESP32-CAM temporarily at Mounts Bay Rd
2. Capture 500-1000 frames over 2-3 hours
3. Capture varied conditions: sun angles, shadows, rain
4. Download via SD card or WiFi
```

**Option B: Use existing datasets + augmentation**
```
- COCO dataset (filter for car, truck, bus, motorcycle)
- UA-DETRAC (traffic surveillance dataset)
- Augment with Perth-specific lighting/angles
```

**Minimum requirements:**
- 100+ images with vehicles labeled
- 20-30 background images (empty road)
- Varied lighting conditions

### Phase 2: Labeling (2-4 hours)

Use Edge Impulse's built-in labeling tool:
1. Upload images to Edge Impulse Studio
2. Draw bounding boxes around each vehicle
3. Label as single class: `vehicle` (don't distinguish car/truck/bus)
4. Include partial vehicles at frame edges

### Phase 3: Training (30 minutes - 2 hours)

**Edge Impulse Settings:**

```
Image size: 96x96 (smallest, fastest)
Color depth: Grayscale (reduces data, sufficient for shapes)
Model: FOMO MobileNetV2 0.1 (smallest variant)
Training cycles: 30-50
Learning rate: 0.001
```

**Expected results:**
- Model size: 50-100KB
- Inference: ~100ms per frame
- Accuracy: 85-95% (depends on training data quality)

### Phase 4: Export & Deploy

1. **Export from Edge Impulse:**
   - Deployment → Arduino Library
   - Target: ESP32
   - Quantization: INT8
   - Enable EON Compiler (optimizes for microcontrollers)

2. **Integrate with firmware:**
   ```cpp
   #include <vehicle_detection_inferencing.h>

   // Capture frame
   camera_fb_t* fb = esp_camera_fb_get();

   // Run inference
   ei_impulse_result_t result;
   run_classifier(&signal, &result, false);

   // Count detections crossing line
   for (int i = 0; i < result.bounding_boxes_count; i++) {
       if (result.bounding_boxes[i].y > DETECTION_LINE_Y) {
           vehicle_count++;
       }
   }
   ```

### Phase 5: Counting Logic

**Simple line-crossing algorithm:**

```cpp
#define DETECTION_LINE_Y 0.5  // Middle of frame

// Track centroids between frames
struct TrackedObject {
    float last_y;
    bool counted;
};

void processDetections(ei_impulse_result_t* result) {
    for (int i = 0; i < result->bounding_boxes_count; i++) {
        float y = result->bounding_boxes[i].y;

        // If centroid crossed line from top to bottom
        if (last_positions[i].last_y < DETECTION_LINE_Y &&
            y >= DETECTION_LINE_Y &&
            !last_positions[i].counted) {

            vehicle_count++;
            last_positions[i].counted = true;
        }

        last_positions[i].last_y = y;
    }
}
```

**Advanced: Hungarian algorithm for object tracking**
- Matches detections between frames
- Handles occlusion and overlapping vehicles
- Libraries: `dlib`, custom implementation

---

## Alternative Approaches

### 1. Motion Detection + Blob Counting (Simpler)

No ML required - pure image processing:

```cpp
// Frame differencing
cv::absdiff(prev_frame, curr_frame, diff);
cv::threshold(diff, binary, 25, 255, cv::THRESH_BINARY);
cv::findContours(binary, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

// Count large contours (vehicles)
for (auto& contour : contours) {
    if (cv::contourArea(contour) > MIN_VEHICLE_AREA) {
        vehicle_count++;
    }
}
```

**Pros:** No training needed, faster
**Cons:** Sensitive to shadows, lighting changes; less accurate

### 2. Background Subtraction

```cpp
// Learn background over time
cv::Ptr<cv::BackgroundSubtractor> bg_sub =
    cv::createBackgroundSubtractorMOG2();

// Apply to each frame
bg_sub->apply(frame, fg_mask);

// Count foreground blobs
```

**Pros:** Adapts to lighting changes
**Cons:** Struggles with stopped traffic

### 3. Hybrid: Motion Detection + FOMO Verification

1. Motion detection triggers capture
2. FOMO confirms if motion is a vehicle
3. Reduces inference calls, saves power

---

## Hardware Considerations

### ESP32-CAM Limitations

| Resource | Available | FOMO Usage |
|----------|-----------|------------|
| Flash | 4MB | ~200KB (model + code) |
| PSRAM | 4MB (if equipped) | ~300KB (frame buffer) |
| RAM | 520KB | ~200KB |
| CPU | 240MHz dual-core | One core for inference |

**Critical:** Use AI-Thinker ESP32-CAM with PSRAM. Without PSRAM, you cannot run FOMO.

### Camera Settings for Detection

```cpp
config.frame_size = FRAMESIZE_96X96;   // Matches FOMO input
config.pixel_format = PIXFORMAT_GRAYSCALE;  // Faster, sufficient
config.fb_count = 2;  // Double buffer
config.grab_mode = CAMERA_GRAB_LATEST;  // Always newest frame
```

### Power Optimization

```cpp
// Reduce capture rate when no motion
if (no_motion_detected) {
    delay(1000);  // 1 FPS
} else {
    delay(200);   // 5 FPS
}

// Deep sleep at night (no traffic to count)
if (hour >= 23 || hour < 5) {
    esp_deep_sleep(3600000000);  // 1 hour
}
```

---

## Expected Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Frame rate | 5-10 FPS | Sufficient for 60 km/h traffic |
| Detection accuracy | 85-95% | Depends on training data |
| False positives | < 5% | Shadows, pedestrians |
| False negatives | < 10% | Occluded vehicles |
| Power consumption | ~200mA active | With solar, sustainable |

---

## Resources

- [Edge Impulse FOMO Tutorial](https://docs.edgeimpulse.com/docs/tutorials/end-to-end-tutorials/computer-vision/object-detection/detect-objects-using-fomo)
- [Edge Impulse Object Counting](https://docs.edgeimpulse.com/docs/tutorials/advanced-inferencing/object-counting-using-fomo)
- [EloquentArduino ESP32-CAM FOMO](https://eloquentarduino.com/posts/esp32-cam-object-detection)
- [GitHub: FOMO Training Guide](https://github.com/San279/train-object-detect-FOMO-esp32)
- [DroneBot Workshop ESP32 Object Detection](https://dronebotworkshop.com/esp32-object-detect/)
