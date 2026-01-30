# SwanFlow - Development Log

*Cross-session tracking • Refresh every 7 days • Next: 2025-12-31*

---

## Navigation

| Date | Summary |
|------|---------|
| [Dec 24](#dec-24-2025) | Route corrections, API URL fix, VPS backend config |
| [Dec 23](#dec-23-2025) | OSM-exact route coordinates, VPS documentation |

---

## Quick Status

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend | 🟢 Live | https://swanflow.vercel.app |
| Backend API | 🟢 Live | VPS 45.77.233.102:3001 |
| Map Routes | 🟢 Fixed | OSM-exact coordinates applied |
| ESP32 Cameras | 🟡 Pending | Hardware ready, not deployed |

---

## Dec 24, 2025

### Done
- ✅ Fixed frontend API URL (was pointing to non-existent swanflow.onrender.com)
- ✅ Updated to point to Vultr VPS backend (45.77.233.102:3001)
- ✅ Created VPS infrastructure documentation

### In Progress
- [ ] Verify route markers displaying correctly on live site

### Notes
**API URL Fix:**
- Frontend was calling `swanflow.onrender.com` which no longer exists
- Changed to `http://45.77.233.102:3001` (Vultr Sydney VPS)

---

## Dec 23, 2025

### Done
- ✅ Applied OSM-exact route coordinate corrections for Stirling Highway
- ✅ Corrected Mounts Bay Road coordinates
- ✅ Fixed Crawley-Nedlands route alignment
- ✅ Created comprehensive VPS documentation

### Notes
**Route Corrections Applied:**
- Stirling Highway: 156 coordinate points from OSM data
- All routes now follow actual road geometry

---

## Backlog

### Hardware Deployment (Priority 0)
- [ ] Deploy first ESP32-CAM counter at test location
- [ ] Configure camera WiFi and API endpoint
- [ ] Test vehicle detection accuracy
- [ ] Document deployment process

### Route Expansion (Priority 1)
- [ ] Add Canning Highway route
- [ ] Add Great Eastern Highway route
- [ ] Add Leach Highway route
- [ ] Research traffic hotspots for priority

### Backend Improvements (Priority 2)
- [ ] Add historical data storage
- [ ] Implement traffic trend analysis
- [ ] Add API rate limiting
- [ ] Create admin dashboard

### Frontend Enhancements (Priority 3)
- [ ] Add real-time traffic layer
- [ ] Implement route selection dropdown
- [ ] Add traffic density heatmap
- [ ] Mobile responsive improvements

---

## Reference

### Architecture
```
ESP32-CAM (Vehicle Detection)
    │
    ▼
Backend API (Node.js on VPS)
    │
    ▼
Frontend (Vercel - Static)
    │
    ▼
MapLibre GL (Route Display)
```

### Key URLs
- **Frontend**: https://swanflow.vercel.app
- **Backend API**: http://45.77.233.102:3001
- **GitHub**: https://github.com/m4cd4r4/perth-traffic-watch

### File Locations
```
I:\Scratch\perth-traffic-watch\
├── frontend/web-dashboard/     # Vercel-deployed frontend
├── backend/api/                # VPS-deployed backend
├── firmware/esp32-cam-counter/ # ESP32 firmware
└── docs/                       # Documentation
```

---

*Template: Copy a day section, add to navigation*
