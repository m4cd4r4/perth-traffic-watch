# SwanFlow Development Log

## 2026-01-10 - UI Cleanup & Main Roads WA Integration Fix

### Summary
Major UI cleanup session focused on simplifying the dashboard and fixing the Main Roads WA live data integration.

### Changes Made

#### Removed Components
- **Recent Detections Table** - Replaced with Simulated Data Feed terminal
- **Hourly Traffic Flow Chart** - Removed entirely (element removed but code kept trying to use it - fixed)
- **Simulation Banner** - Removed the scrolling "Traffic flow data is simulated" banner from status panel

#### Added Components
- **Simulated Data Feed Terminal** - Live terminal showing simulated vehicle detections
  - Auto-starts on page load
  - Shows timestamp, site name, vehicle count, speed, confidence
  - 30-line buffer with auto-scroll
  - Styled with monospace font and color-coded output

- **Main Roads WA Layer Toggles** - Added to map controls
  - Incidents toggle (⚠️) with count badge
  - Roadworks toggle (🚧) with count badge
  - Click to show/hide layers on map

#### Simplified Components
- **Journey Time Trends** - Removed period selector (Today/This Week/This Month) and empty chart canvas, kept only the stats

#### Bug Fixes
1. **Chart Error** - Added null check for `traffic-chart` element since it was removed
2. **Main Roads WA Not Loading** - Chart error was breaking execution before `initMainRoadsMonitoring()` was called
   - Wrapped `loadDashboard()` in try-catch
   - Added debug logging to Main Roads initialization
3. **Perth-Only Filter** - Removed restrictive Perth metro filter, now shows ALL WA incidents/roadworks

#### Default Settings Changed
- Dark theme is now default (was light)
- Street map is now default (was auto-selecting based on theme)

### Commits
- `8fbc3f4` - fix avg_count in hourly data
- `79f48f3` - dynamic journey timeline
- `a45b604` - remove duplicate emoji
- `55a1427` - dark theme + Street map defaults
- `2ac7b90` - simulation notice and mini terminal (first attempt)
- `0a49139` - clean scrolling banner, removed mini terminal
- `84ace65` - collapsible simulated data feed section
- `708afe2` - remove simulated data banner
- `0653a42` - replace table with live terminal
- `d05da06` - remove hourly traffic flow chart
- `101c00d` - simplify Journey Time Trends + add layer toggles
- `af017f4` - add click handlers for layer toggles
- `9a8078f` - show all WA incidents (remove Perth filter)
- `4cde304` - fix chart error, improve error handling

### Technical Notes

#### Main Roads WA API
- Endpoint: `https://services2.arcgis.com/cHGEnmsJ165IBJRM/arcgis/rest/services/`
- Returns coordinates in Web Mercator (EPSG:3857), converted to WGS84 using `webMercatorToWGS84()`
- Fetches: Incidents, Roadworks, Closures, Events
- Refresh interval: 5 minutes

#### Files Modified
- `frontend/web-dashboard/index.html` - HTML structure changes
- `frontend/web-dashboard/app.js` - JavaScript logic updates
- `frontend/web-dashboard/styles.css` - CSS for new components
