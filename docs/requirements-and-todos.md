# Requirements & To-Do List

## Project Scope: 4 Prototype Units

**Location:** Mounts Bay Road, Perth (UWA to Narrows Bridge)
**Timeline:** MVP prototype phase
**Budget:** ~$300 hardware + ~$20/month connectivity

---

## Hardware Requirements

### Per Unit Components
- [ ] ESP32-CAM (AI-Thinker) with PSRAM - **Critical: Must have PSRAM for FOMO**
- [ ] SIM7000A LTE-M module
- [ ] 18650 battery (3000mAh+) with BMS
- [ ] 5W 6V solar panel
- [ ] IP65 junction box (Bunnings)
- [ ] Cable glands (PG7/PG9) x2
- [ ] LTE antenna (SMA)
- [ ] Mounting hardware

### Tools Required
- [ ] Soldering iron + solder
- [ ] Step drill bit (for camera hole)
- [ ] Multimeter
- [ ] Wire strippers
- [ ] Silicone sealant

### Quantity: 4 Units + Spares
| Item | Qty | Unit Cost | Total |
|------|-----|-----------|-------|
| ESP32-CAM | 5 | $8 | $40 |
| SIM7000A | 5 | $15 | $75 |
| 18650 + BMS | 5 | $7 | $35 |
| Solar panel | 5 | $10 | $50 |
| Junction box | 5 | $12 | $60 |
| Hardware/misc | - | - | $40 |
| **Total** | | | **~$300** |

---

## Software Requirements

### ML Model (Edge Impulse FOMO)

**Training Data:**
- [ ] 100+ images of vehicles (various angles, lighting)
- [ ] 20-30 background images (empty road)
- [ ] Labeled with bounding boxes (single class: "vehicle")

**Model Specifications:**
| Parameter | Value |
|-----------|-------|
| Input size | 96x96 grayscale |
| Model | FOMO MobileNetV2 0.1 |
| Quantization | INT8 |
| Target size | < 100KB |
| Inference time | < 200ms |

**Output:** Centroids (x, y) of detected vehicles - not bounding boxes

### Firmware (ESP32)

**Core Features:**
- [ ] Camera initialization (96x96 grayscale)
- [ ] FOMO model inference
- [ ] Line-crossing detection algorithm
- [ ] Vehicle counting logic
- [ ] SIM7000A LTE-M communication
- [ ] JSON payload transmission
- [ ] Battery voltage monitoring
- [ ] Deep sleep / power management

**Data Payload:**
```json
{
  "sensor_id": "PTW-001",
  "timestamp": 1702500000,
  "count": 42,
  "interval_sec": 60,
  "battery_v": 3.85,
  "rssi": -75
}
```

### Backend API

**Endpoints:**
- [ ] `POST /api/data` - Receive sensor data
- [ ] `GET /api/sensors` - List all sensors
- [ ] `GET /api/traffic/{sensor_id}` - Get traffic data
- [ ] `GET /api/traffic/realtime` - WebSocket for live updates

**Storage:**
- Time-series database (InfluxDB, TimescaleDB, or simple SQLite for MVP)
- 30-day retention minimum

### Frontend Dashboard

**Features:**
- [ ] Map view with sensor locations
- [ ] Real-time traffic density indicators (color-coded)
- [ ] Historical charts (hourly, daily, weekly)
- [ ] "Should I drive?" simple answer

---

## Connectivity Requirements

### IoT SIM (Recommended: M2MSIM.com.au)
- [ ] Order 4x SIMs from M2MSIM or Cmobile
- [ ] Activate on portal
- [ ] Note APN settings
- [ ] Test connectivity before deployment

**Data Budget:**
- ~25 MB/month per sensor
- ~100 MB/month total for 4 sensors
- Estimated cost: $16-40/month

---

## Deployment Requirements

### Site Survey (Mounts Bay Road)
- [ ] Walk the route: UWA to Narrows Bridge (~3km)
- [ ] Identify 4 mounting locations with:
  - Private property access (fence, building, pole)
  - Clear view of both lanes
  - Sun exposure for solar
  - Height: 2-4m for optimal angle
- [ ] Document each location (photos, GPS coords)
- [ ] Contact property owners for permission

### Mounting Considerations
| Factor | Requirement |
|--------|-------------|
| Height | 2-4m above ground |
| Angle | ~30-45° downward |
| Field of view | Both lanes visible |
| Solar exposure | South-facing preferred (southern hemisphere) |
| Security | Not easily accessible |

---

## To-Do List (Ordered)

### Phase 1: Hardware Acquisition (Week 1)

- [ ] **Order components from AliExpress/eBay**
  - 5x ESP32-CAM (AI-Thinker with PSRAM)
  - 5x SIM7000A modules
  - 5x 18650 batteries + BMS boards
  - 5x 5W solar panels
  - LTE antennas, cables, connectors

- [ ] **Buy from Bunnings**
  - 5x IP65 junction boxes
  - Cable glands
  - Mounting brackets
  - Silicone sealant
  - Step drill bit

- [ ] **Order IoT SIMs**
  - Register at m2msim.com.au or cmobile.com.au
  - Order 4x SIMs
  - Activate accounts

### Phase 2: ML Model Development (Week 1-2)

- [ ] **Create Edge Impulse account**
  - Sign up at edgeimpulse.com (free tier)

- [ ] **Collect training data**
  - Option A: Record video at Mounts Bay Rd, extract frames
  - Option B: Use COCO/UA-DETRAC datasets

- [ ] **Label images**
  - Upload to Edge Impulse
  - Draw bounding boxes on vehicles
  - Single class: "vehicle"

- [ ] **Train FOMO model**
  - 96x96 grayscale
  - FOMO MobileNetV2 0.1
  - 30-50 training cycles
  - Learning rate 0.001

- [ ] **Export model**
  - Arduino library format
  - INT8 quantization
  - EON Compiler enabled

- [ ] **Test on single ESP32-CAM**
  - Verify inference works
  - Measure inference time
  - Check accuracy

### Phase 3: Firmware Development (Week 2-3)

- [ ] **Set up development environment**
  - Install PlatformIO
  - Configure ESP32-CAM board

- [ ] **Implement core firmware**
  - Camera capture loop
  - FOMO inference integration
  - Line-crossing counter
  - Battery monitoring

- [ ] **Implement LTE communication**
  - SIM7000A initialization
  - APN configuration
  - HTTP POST to backend

- [ ] **Implement power management**
  - Deep sleep between transmissions
  - Night mode (reduced operation)
  - Solar charging logic

- [ ] **Bench test complete system**
  - Run for 24+ hours
  - Verify data transmission
  - Check power consumption

### Phase 4: Enclosure Assembly (Week 3)

- [ ] **Prepare junction boxes**
  - Drill camera hole (step drill)
  - Install cable glands
  - Mount ESP32-CAM internally
  - Wire battery + BMS
  - Connect solar panel
  - Seal with silicone

- [ ] **Test weatherproofing**
  - Water spray test
  - Heat test (direct sun)

- [ ] **Assemble 4 complete units**

### Phase 5: Backend & Frontend (Week 2-3, parallel)

- [ ] **Set up backend**
  - Node.js/Python API
  - Database (SQLite for MVP)
  - Data ingestion endpoint
  - Basic authentication

- [ ] **Deploy backend**
  - Railway, Fly.io, or Vercel (free tier)

- [ ] **Build frontend dashboard**
  - Map with sensor markers
  - Real-time data display
  - Simple traffic indicator

- [ ] **Deploy frontend**
  - Vercel (free tier)

### Phase 6: Site Survey & Permissions (Week 3-4)

- [ ] **Walk Mounts Bay Road**
  - Identify 4+ potential sites
  - Take photos
  - Record GPS coordinates

- [ ] **Contact property owners**
  - Explain project
  - Request permission
  - Get written consent

- [ ] **Prepare consent forms**
  - Print copies
  - Collect signatures

### Phase 7: Field Deployment (Week 4-5)

- [ ] **Install sensors**
  - Mount at approved locations
  - Orient for optimal view
  - Secure solar panels

- [ ] **Verify connectivity**
  - Check LTE signal
  - Confirm data reaching backend

- [ ] **Monitor initial operation**
  - 48-hour observation period
  - Adjust positions if needed
  - Fix any issues

### Phase 8: Validation & Iteration (Week 5+)

- [ ] **Validate accuracy**
  - Manual count vs sensor count
  - Calculate error rate
  - Identify failure modes

- [ ] **Iterate on model**
  - Collect more training data from deployed sensors
  - Retrain if accuracy < 85%

- [ ] **Public launch**
  - Announce on GitHub
  - Share dashboard URL
  - Invite community feedback

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Detection accuracy | > 85% |
| Uptime | > 95% |
| Data latency | < 2 minutes |
| Battery life (cloudy) | > 3 days |
| Unit cost | < $60 |
| Monthly running cost | < $50 total |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Poor LTE signal | Test before mounting; use external antenna |
| Solar insufficient | Use larger panel (10W) or dual battery |
| ML accuracy too low | Collect more local training data |
| Vandalism/theft | Mount high; use security screws |
| Permission denied | Have backup locations identified |
| Weather damage | IP65 rating; silicone sealing |

---

## Future Enhancements (Post-MVP)

- [ ] Additional sensors on other routes
- [ ] Direction detection (inbound vs outbound)
- [ ] Vehicle classification (car/truck/bus)
- [ ] Speed estimation
- [ ] Mobile app
- [ ] API for third-party integration
- [ ] Main Roads WA partnership
