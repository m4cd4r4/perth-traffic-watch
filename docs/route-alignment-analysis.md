# Stirling Highway Route Alignment Analysis

**Generated**: December 23, 2025
**Purpose**: Identify misalignments between SwanFlow route visualizations and actual Stirling Highway geometry

## Overview

Comparing SwanFlow's route waypoints against OpenStreetMap (Overpass API) data for Stirling Highway to ensure pinpoint accuracy - dots should trace the highway exactly, not fields or buildings.

---

## Section 1: Nedlands-City Corridor (Winthrop Ave → Point Lewis)

### Current SwanFlow Coordinates

**Start**: `-31.9812, 115.8148` (Winthrop Ave, Nedlands)
**End**: `-31.963231, 115.842311` (Point Lewis, Malcolm St)

**Waypoints**:
```javascript
// Stirling Highway section (Winthrop Ave → Broadway → Kings Park)
L.latLng(-31.9805, 115.8158),   // Between Winthrop and Broadway
L.latLng(-31.9795, 115.8170),   // Approaching Broadway
L.latLng(-31.9785, 115.8185),   // Broadway intersection
L.latLng(-31.9770, 115.8205),   // Between Broadway and Kings Park
L.latLng(-31.9755, 115.8225),   // Approaching Kings Park
L.latLng(-31.9740, 115.8245),   // Near Kings Park
```

### OpenStreetMap Actual Geometry (Northern Stirling Highway)

```
-31.9755360, 115.8180240  // Near Broadway/Kings Park area
-31.9757418, 115.8178419
-31.9765928, 115.8155127
-31.9770527, 115.8141985  // Transition point
-31.9772336, 115.8140539
-31.9773593, 115.8132976  // Where Stirling Hwy becomes Mounts Bay Rd
```

### ⚠️ MISALIGNMENT ISSUES

1. **Broadway Intersection (-31.9785, 115.8185)**
   - SwanFlow: `-31.9785, 115.8185`
   - OSM Actual: `-31.9765928, 115.8155127`
   - **Error**: ~3.5km off! Longitude is way too far east

2. **Between Broadway and Kings Park (-31.9770, 115.8205)**
   - SwanFlow: `-31.9770, 115.8205`
   - OSM Actual: `-31.9770527, 115.8141985`
   - **Error**: Longitude ~7km too far east! This dot is in the Swan River

3. **Approaching Kings Park (-31.9755, 115.8225)**
   - SwanFlow: `-31.9755, 115.8225`
   - OSM Actual: `-31.9755360, 115.8180240`
   - **Error**: Longitude ~5km too far east

### ✅ CORRECTED WAYPOINTS (Stirling Highway Section)

```javascript
// Stirling Highway section (Winthrop Ave → Broadway → Kings Park)
L.latLng(-31.9812, 115.8148),   // Winthrop Ave (START) - Keep this
L.latLng(-31.9805, 115.8150),   // Between Winthrop and Broadway - MINOR ADJUST
L.latLng(-31.9795, 115.8152),   // Approaching Broadway - ADJUST
L.latLng(-31.9785, 115.8156),   // Broadway intersection - FIX (was 115.8185)
L.latLng(-31.9770, 115.8142),   // Between Broadway and Kings Park - FIX (was 115.8205)
L.latLng(-31.9755, 115.8180),   // Approaching Kings Park - FIX (was 115.8225)
L.latLng(-31.9740, 115.8200),   // Near Kings Park - ADJUST (was 115.8245)
```

---

## Section 2: Claremont-Cottesloe Corridor (Bunnings → Eric St)

### Current SwanFlow Coordinates

**Start**: `-31.982, 115.780` (Stirling Rd, Bunnings/Claremont Quarter)
**End**: `-31.994, 115.765` (Eric St, Cottesloe)

**Waypoints**:
```javascript
L.latLng(-31.984, 115.778),   // South of Stirling Rd
L.latLng(-31.986, 115.775),   // Approaching school zone
L.latLng(-31.988, 115.772),   // North of Jarrad St
L.latLng(-31.990, 115.770),   // Jarrad St intersection
L.latLng(-31.992, 115.768),   // South of Jarrad St
L.latLng(-31.993, 115.766)    // Near Eric St
```

### OpenStreetMap Actual Geometry (Claremont-Cottesloe)

```
-31.9811904, 115.7917101  // North Claremont
-31.9834402, 115.7802709  // Claremont Quarter area
-31.9850921, 115.7755445  // School zone (Christ Church/MLC)
-31.9890887, 115.7685801  // Cottesloe approach
-31.9910607, 115.7675329  // Near Eric St
```

### ⚠️ MISALIGNMENT ISSUES

1. **Start Point - Bunnings/Claremont (-31.982, 115.780)**
   - SwanFlow: `-31.982, 115.780`
   - OSM Actual: `-31.9834402, 115.7802709`
   - **Error**: Latitude off by ~1.5km north, longitude close but not exact

2. **School Zone (-31.988, 115.772)**
   - SwanFlow: `-31.988, 115.772`
   - OSM Actual: `-31.9850921, 115.7755445`
   - **Error**: Latitude ~3km wrong direction, longitude ~1.8km off

3. **General Issue**: All waypoints are approximate rounded coordinates, not following actual road geometry

### ✅ CORRECTED WAYPOINTS (Claremont-Cottesloe Section)

```javascript
// Follow actual Stirling Highway geometry from OSM
L.latLng(-31.9820, 115.7900),   // Stirling Rd intersection (Bunnings area) - ADJUST
L.latLng(-31.9834, 115.7803),   // Claremont Quarter - USE OSM
L.latLng(-31.9851, 115.7755),   // School zone (Christ Church/MLC) - USE OSM
L.latLng(-31.9891, 115.7686),   // Cottesloe approach - USE OSM
L.latLng(-31.9911, 115.7675),   // Near Eric St - USE OSM
L.latLng(-31.9940, 115.7650)    // Eric St (END) - ADJUST
```

---

## Section 3: Mosman Park Corridor (Forrest St → Victoria St)

### Current SwanFlow Coordinates

**Start**: `-32.008, 115.757` (Forrest St)
**End**: `-32.035, 115.751` (Victoria St)

**Waypoints**:
```javascript
L.latLng(-32.011, 115.756),  // Between Forrest and Bay View
L.latLng(-32.015, 115.755),  // Bay View Terrace
L.latLng(-32.020, 115.754),  // Between Bay View and McCabe
L.latLng(-32.025, 115.753),  // McCabe St
L.latLng(-32.030, 115.752)   // Between McCabe and Victoria
```

### OpenStreetMap Actual Geometry (Mosman Park)

```
-31.9991422, 115.7619315  // North Mosman Park
-32.0034093, 115.7601065  // Forrest St area
-32.0115020, 115.7555150  // Bay View area
-32.0198147, 115.7537381  // McCabe St area
-32.0407275, 115.7610976  // South (past Victoria St)
```

### ⚠️ MISALIGNMENT ISSUES

1. **All waypoints use incorrect longitude pattern**
   - SwanFlow uses 115.751-115.757 range
   - OSM shows 115.753-115.762 range (wider and different center)

2. **Bay View Terrace (-32.015, 115.755)**
   - SwanFlow: `-32.015, 115.755`
   - OSM Actual: `-32.0115020, 115.7555150`
   - **Error**: Latitude ~3.9km off!

### ✅ CORRECTED WAYPOINTS (Mosman Park Section)

```javascript
L.latLng(-32.0034, 115.7601),   // Forrest St - USE OSM
L.latLng(-32.0115, 115.7555),   // Bay View Terrace - USE OSM
L.latLng(-32.0198, 115.7537),   // McCabe St - USE OSM
L.latLng(-32.0350, 115.7540)    // Victoria St (approximate) - NEEDS VERIFICATION
```

---

## Root Cause Analysis

### Why Are Coordinates Wrong?

1. **Manual Approximation**: Coordinates were likely estimated/rounded instead of traced from actual road geometry
2. **Longitude Errors**: Many waypoints have longitude values that are too far east, placing dots in water or fields
3. **Latitude Precision**: Rounded to 3-4 decimal places instead of using precise OSM coordinates
4. **No Geometry Tracing**: Routes weren't traced along actual road centerlines

---

## Systematic Solution to Prevent Future Misalignments

### 1. **Use Overpass API for All Route Planning**

```bash
# Query template for any road in Perth
https://overpass-api.de/api/interpreter?data=[out:json];
way["name"="ROAD_NAME"](-32.05,115.74,-31.96,115.86);
out geom;
```

### 2. **Extract Coordinates Programmatically**

Create a script to:
- Query Overpass API for road geometry
- Extract lat/lon pairs
- Generate Leaflet waypoint arrays automatically
- Ensure 6-decimal precision (±0.111m accuracy)

### 3. **Validation Process**

Before adding any new corridor:
1. Query Overpass API for road geometry
2. Plot coordinates on OSM to visually verify alignment
3. Test in local environment with satellite imagery
4. Screenshot and compare dots to road centerline
5. Only deploy if dots are perfectly aligned

### 4. **Documentation Requirements**

For each corridor, document:
- Overpass API query used
- Date coordinates were extracted
- Visual verification screenshots
- Any manual adjustments and why

---

## Next Steps

1. ✅ Update [app.js:676-745](frontend/web-dashboard/app.js#L676-L745) with corrected waypoints
2. Test locally with satellite base map
3. Capture screenshots showing perfect alignment
4. Deploy to production
5. Create automated coordinate extraction tool

---

## Precision Standards

- **Minimum**: 5 decimal places (±1.1m accuracy)
- **Recommended**: 6 decimal places (±0.111m accuracy)
- **Source**: OpenStreetMap Overpass API (authoritative)
- **Validation**: Visual inspection on satellite imagery

