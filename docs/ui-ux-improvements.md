# Perth Traffic Watch - UI/UX Improvement Proposal

## 📋 Overview

Comprehensive improvements to modernize the dashboard UI/UX, focusing on:
1. Simplified Light/Dark theme toggle
2. Modern site selector (replacing dropdown)
3. Interactive map with auto-pan to selected site
4. Dynamic traffic flow visualization for all networks

---

## 🎨 Theme Simplification

### Current State
- 4 themed options (Cottesloe Light/Dark, Indigenous Light/Dark)
- Dropdown selector
- Overly complex for users

### Proposed Solution
**Simple Dark/Light Mode Toggle**

```html
<!-- Replace theme dropdown with toggle switch -->
<div class="theme-toggle">
  <button id="theme-toggle-btn" class="theme-btn" aria-label="Toggle dark mode">
    <span class="icon-light">☀️</span>
    <span class="icon-dark">🌙</span>
  </button>
</div>
```

**CSS**:
```css
.theme-toggle {
  position: relative;
}

.theme-btn {
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 50px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
}

.theme-btn:hover {
  background: var(--surface-hover);
  transform: scale(1.05);
}

/* Hide inactive icon */
[data-theme="light"] .icon-dark,
[data-theme="dark"] .icon-light {
  display: none;
}

/* Mobile FAB */
@media (max-width: 768px) {
  .theme-btn {
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    padding: 0;
    justify-content: center;
  }
}
```

**JavaScript**:
```javascript
function initThemeToggle() {
  const btn = document.getElementById('theme-toggle-btn');
  const savedTheme = localStorage.getItem('theme') || 'light';

  document.documentElement.setAttribute('data-theme', savedTheme);

  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const newTheme = current === 'light' ? 'dark' : 'light';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    // Update map tiles
    if (trafficMap) updateMapTiles();
  });
}
```

**Benefits**:
- ✅ Cleaner, simpler UX
- ✅ Follows industry standard (most apps use light/dark)
- ✅ Faster switching with toggle button
- ✅ Less cognitive load for users

---

## 🗺️ Modern Site Selector

### Current State
- Basic `<select>` dropdown
- Text-only site names
- No visual hierarchy
- No search/filter capability

### Proposed Solution
**Interactive Site Cards with Search**

#### Option 1: Searchable Dropdown with Icons
```html
<div class="site-selector">
  <div class="search-wrapper">
    <input
      type="text"
      id="site-search"
      placeholder="Search sites or click to select..."
      class="site-search-input"
      autocomplete="off"
    />
    <span class="search-icon">🔍</span>
  </div>

  <div class="site-dropdown" id="site-dropdown">
    <div class="site-option" data-site-id="1" data-corridor="mitchell" data-direction="northbound">
      <div class="site-icon">🛣️</div>
      <div class="site-details">
        <div class="site-name">Mitchell Fwy @ Narrows</div>
        <div class="site-meta">
          <span class="badge">Northbound</span>
          <span class="status">🟢 Live</span>
        </div>
      </div>
      <div class="site-flow">
        <span class="flow-count">850 veh/hr</span>
        <span class="flow-speed">98 km/h</span>
      </div>
    </div>
    <!-- Repeat for all sites -->
  </div>
</div>
```

#### Option 2: Grid View with Filters
```html
<div class="site-selector-grid">
  <div class="selector-header">
    <h3>Select Monitoring Site</h3>
    <div class="filters">
      <button class="filter-btn active" data-filter="all">All (52)</button>
      <button class="filter-btn" data-filter="arterial">Arterial (22)</button>
      <button class="filter-btn" data-filter="freeway">Freeway (30)</button>
    </div>
    <input type="text" id="site-search" placeholder="Search sites..." />
  </div>

  <div class="site-grid">
    <div class="site-card" data-site="Mitchell-Narrows-NB">
      <div class="card-header">
        <span class="road-type freeway">🛣️ Freeway</span>
        <span class="status live">● Live</span>
      </div>
      <h4 class="site-title">Mitchell Fwy @ Narrows</h4>
      <div class="site-direction">Northbound</div>
      <div class="site-metrics">
        <div class="metric">
          <span class="label">Flow</span>
          <span class="value">850/hr</span>
        </div>
        <div class="metric">
          <span class="label">Speed</span>
          <span class="value">98 km/h</span>
        </div>
      </div>
    </div>
    <!-- Repeat for all sites -->
  </div>
</div>
```

**CSS for Modern Selector**:
```css
.site-search-input {
  width: 100%;
  padding: 1rem 3rem 1rem 1rem;
  font-size: 1rem;
  border: 2px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  color: var(--text);
  transition: all 0.3s ease;
}

.site-search-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.1);
}

.site-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 400px;
  overflow-y: auto;
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 12px;
  margin-top: 0.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 100;
  display: none;
}

.site-dropdown.open {
  display: block;
}

.site-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--border);
  transition: all 0.2s ease;
}

.site-option:hover {
  background: var(--surface-hover);
  transform: translateX(4px);
}

.site-option.selected {
  background: rgba(var(--primary-rgb), 0.1);
  border-left: 4px solid var(--primary);
}

.site-icon {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.site-details {
  flex: 1;
}

.site-name {
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.site-meta {
  display: flex;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.badge {
  background: var(--primary);
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 600;
}

.site-flow {
  text-align: right;
}

.flow-count {
  display: block;
  font-weight: 700;
  color: var(--primary);
}

.flow-speed {
  display: block;
  font-size: 0.85rem;
  color: var(--text-muted);
}
```

**JavaScript for Search**:
```javascript
function initModernSiteSelector() {
  const searchInput = document.getElementById('site-search');
  const dropdown = document.getElementById('site-dropdown');
  const options = dropdown.querySelectorAll('.site-option');

  // Show dropdown on focus
  searchInput.addEventListener('focus', () => {
    dropdown.classList.add('open');
  });

  // Hide dropdown on click outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.site-selector')) {
      dropdown.classList.remove('open');
    }
  });

  // Filter sites on search
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();

    options.forEach(option => {
      const siteName = option.querySelector('.site-name').textContent.toLowerCase();
      const match = siteName.includes(query);
      option.style.display = match ? 'flex' : 'none';
    });
  });

  // Select site on click
  options.forEach(option => {
    option.addEventListener('click', () => {
      const siteName = option.querySelector('.site-name').textContent;
      searchInput.value = siteName;
      dropdown.classList.remove('open');

      // Remove previous selection
      options.forEach(opt => opt.classList.remove('selected'));
      option.classList.add('selected');

      // Trigger site change
      const siteId = option.dataset.siteId;
      onSiteSelected(siteId);
    });
  });
}
```

**Benefits**:
- ✅ Visual hierarchy with icons and badges
- ✅ Live metrics visible before selection
- ✅ Search/filter capability
- ✅ Better mobile experience
- ✅ Shows site status at a glance

---

## 🗺️ Interactive Map with Auto-Pan

### Current State
- Static map view
- Manual panning only
- No automatic focus on selected site

### Proposed Solution
**Auto-Pan to Selected Site with Smooth Animation**

#### Data Structure
First, add coordinates to each site in the database initialization:

```javascript
// In init-freeway-sites.js and site definitions
const mitchellSites = [
  {
    ramp_id: 'M1-NB',
    name: 'Narrows Interchange (Northbound)',
    latitude: -31.9580,
    longitude: 115.8450,
    // ... other fields
  }
];
```

#### JavaScript Implementation
```javascript
/**
 * Pan map to selected site with smooth animation
 */
function panToSite(siteName) {
  // Find site coordinates
  const site = allSitesData.find(s => s.name === siteName);

  if (!site || !site.latitude || !site.longitude) {
    console.warn('Site coordinates not found:', siteName);
    return;
  }

  const coords = [site.latitude, site.longitude];

  // Determine appropriate zoom level based on site type
  const zoom = site.corridor ? 14 : 15; // Freeway vs arterial

  // Animate pan with smooth flyTo
  trafficMap.flyTo(coords, zoom, {
    duration: 1.5, // 1.5 seconds animation
    easeLinearity: 0.25
  });

  // Add temporary highlight marker
  addSiteHighlight(coords, siteName);
}

/**
 * Add pulsing highlight marker to selected site
 */
function addSiteHighlight(coords, siteName) {
  // Remove previous highlight
  if (window.highlightMarker) {
    trafficMap.removeLayer(window.highlightMarker);
  }

  // Create pulsing marker
  const highlightIcon = L.divIcon({
    className: 'site-highlight-marker',
    html: `
      <div class="pulse-marker">
        <div class="pulse-dot"></div>
        <div class="pulse-ring"></div>
      </div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 20]
  });

  window.highlightMarker = L.marker(coords, { icon: highlightIcon })
    .addTo(trafficMap)
    .bindPopup(`<strong>${siteName}</strong><br>Selected Site`)
    .openPopup();

  // Remove highlight after 5 seconds
  setTimeout(() => {
    if (window.highlightMarker) {
      trafficMap.closePopup();
      // Keep marker but stop pulsing
      window.highlightMarker.getElement().classList.add('faded');
    }
  }, 5000);
}

/**
 * Update site selector event listener
 */
siteSelect.addEventListener('change', async (e) => {
  currentSite = e.target.value;

  // Pan to selected site
  panToSite(currentSite);

  // Load dashboard data
  await loadDashboard();
});
```

#### CSS for Highlight Marker
```css
.site-highlight-marker {
  position: relative;
}

.pulse-marker {
  position: relative;
  width: 40px;
  height: 40px;
}

.pulse-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  background: #ff4444;
  border-radius: 50%;
  z-index: 2;
}

.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 30px;
  height: 30px;
  border: 3px solid #ff4444;
  border-radius: 50%;
  animation: pulse 2s ease-out infinite;
  z-index: 1;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
}

.site-highlight-marker.faded .pulse-ring {
  animation: none;
  opacity: 0.3;
}
```

**Benefits**:
- ✅ Automatic map centering on site selection
- ✅ Smooth animations for better UX
- ✅ Visual feedback with pulsing marker
- ✅ Context-aware zoom levels

---

## 🚗 Dynamic Traffic Flow Visualization

### Current State
- Hardcoded for Mounts Bay Road only (4 sites)
- No freeway integration
- Static HTML structure

### Proposed Solution
**Dynamic Multi-Corridor Flow Visualization**

#### New Component Structure
```html
<div class="flow-visualizer">
  <div class="flow-header">
    <h2>Traffic Flow Visualization</h2>
    <div class="corridor-selector">
      <button class="corridor-btn active" data-corridor="mounts-bay">Mounts Bay Rd</button>
      <button class="corridor-btn" data-corridor="mitchell">Mitchell Fwy</button>
      <button class="corridor-btn" data-corridor="kwinana">Kwinana Fwy</button>
      <button class="corridor-btn" data-corridor="stirling">Stirling Hwy</button>
    </div>
  </div>

  <div id="flow-canvas" class="flow-canvas">
    <!-- Dynamically generated flow diagram -->
  </div>

  <div class="flow-legend">
    <span class="legend-item"><span class="legend-color flowing"></span> Flowing (90-100 km/h)</span>
    <span class="legend-item"><span class="legend-color moderate"></span> Moderate (60-90 km/h)</span>
    <span class="legend-item"><span class="legend-color heavy"></span> Heavy (30-60 km/h)</span>
    <span class="legend-item"><span class="legend-color gridlock"></span> Gridlock (< 30 km/h)</span>
  </div>
</div>
```

#### JavaScript for Dynamic Flow
```javascript
/**
 * Corridor configurations
 */
const corridorConfigs = {
  'mounts-bay': {
    name: 'Mounts Bay Road',
    type: 'arterial',
    speedLimit: 60,
    sites: [
      { name: 'Kings Park', id: 'kings-park', position: 0 },
      { name: 'Mill Point', id: 'mill-point', position: 1 },
      { name: 'Fraser Ave', id: 'fraser', position: 2 },
      { name: 'Malcolm St', id: 'malcolm', position: 3 }
    ]
  },
  'mitchell': {
    name: 'Mitchell Freeway',
    type: 'freeway',
    speedLimit: 100,
    sites: [
      { name: 'Narrows', id: 'm1', position: 0 },
      { name: 'Malcolm St', id: 'm2', position: 1 },
      { name: 'Loftus St', id: 'm3', position: 2 },
      { name: 'Newcastle', id: 'm4', position: 3 },
      { name: 'Charles St', id: 'm5', position: 4 },
      { name: 'Vincent St', id: 'm6', position: 5 },
      { name: 'Powis St', id: 'm7', position: 6 },
      { name: 'Hutton St', id: 'm8', position: 7 },
      { name: 'Scarborough', id: 'm9', position: 8 }
    ]
  },
  'kwinana': {
    name: 'Kwinana Freeway',
    type: 'freeway',
    speedLimit: 100,
    sites: [
      { name: 'Narrows South', id: 'k1', position: 0 },
      { name: 'Mill Point Rd', id: 'k2', position: 1 },
      { name: 'South Tce', id: 'k3', position: 2 },
      { name: 'Canning Hwy', id: 'k4', position: 3 },
      { name: 'Manning Rd', id: 'k5', position: 4 },
      { name: 'Leach Hwy', id: 'k6', position: 5 }
    ]
  },
  'stirling': {
    name: 'Stirling Highway',
    type: 'arterial',
    speedLimit: 60,
    sites: [
      { name: 'Grant St', id: 'grant', position: 0 },
      { name: 'Campbell', id: 'campbell', position: 1 },
      { name: 'Eric St', id: 'eric', position: 2 },
      { name: 'Forrest St', id: 'forrest', position: 3 },
      { name: 'Bay View', id: 'bayview', position: 4 },
      { name: 'McCabe St', id: 'mccabe', position: 5 },
      { name: 'Victoria St', id: 'victoria', position: 6 }
    ]
  }
};

/**
 * Generate dynamic flow visualization
 */
function generateFlowVisualization(corridorId) {
  const config = corridorConfigs[corridorId];
  const canvas = document.getElementById('flow-canvas');

  canvas.innerHTML = ''; // Clear existing

  const flowDiagram = document.createElement('div');
  flowDiagram.className = 'flow-diagram';

  config.sites.forEach((site, index) => {
    // Create site node
    const siteNode = createFlowSiteNode(site, config.type);
    flowDiagram.appendChild(siteNode);

    // Add connector (except for last site)
    if (index < config.sites.length - 1) {
      const connector = createFlowConnector(site.id, config.type);
      flowDiagram.appendChild(connector);
    }
  });

  canvas.appendChild(flowDiagram);

  // Update with live data
  updateFlowData(corridorId);
}

/**
 * Create flow site node
 */
function createFlowSiteNode(site, type) {
  const node = document.createElement('div');
  node.className = 'flow-site';
  node.id = `flow-site-${site.id}`;

  node.innerHTML = `
    <div class="site-name">${site.name}</div>
    <div class="flow-arrows">
      <div class="flow-direction northbound">
        <span class="arrow">↑</span>
        <span class="label">NB</span>
        <span class="count" id="flow-nb-${site.id}">-</span>
        <span class="speed" id="speed-nb-${site.id}">-</span>
      </div>
      <div class="flow-direction southbound">
        <span class="arrow">↓</span>
        <span class="label">SB</span>
        <span class="count" id="flow-sb-${site.id}">-</span>
        <span class="speed" id="speed-sb-${site.id}">-</span>
      </div>
    </div>
  `;

  return node;
}

/**
 * Create flow connector with heat visualization
 */
function createFlowConnector(siteId, type) {
  const connector = document.createElement('div');
  connector.className = 'flow-connector';

  connector.innerHTML = `
    <div class="connector-line northbound" id="connector-nb-${siteId}"></div>
    <div class="connector-line southbound" id="connector-sb-${siteId}"></div>
  `;

  return connector;
}

/**
 * Update flow visualization with live data
 */
function updateFlowData(corridorId) {
  const config = corridorConfigs[corridorId];

  config.sites.forEach(site => {
    // Fetch data for each site direction
    ['northbound', 'southbound'].forEach(direction => {
      const siteName = `${config.name} @ ${site.name} (${direction})`;
      const siteData = allSitesData.find(s => s.name.includes(siteName));

      if (siteData) {
        const hourlyCount = siteData.current_hourly || 0;
        const estimatedSpeed = Math.round(estimateSpeed(hourlyCount));
        const color = getTrafficColor(hourlyCount);

        // Update count
        const countEl = document.getElementById(`flow-${direction[0]}b-${site.id}`);
        if (countEl) {
          countEl.textContent = `${hourlyCount}/hr`;
          countEl.style.color = color;
        }

        // Update speed
        const speedEl = document.getElementById(`speed-${direction[0]}b-${site.id}`);
        if (speedEl) {
          speedEl.textContent = `~${estimatedSpeed} km/h`;
          speedEl.style.color = color;
        }

        // Update connector color
        const connectorEl = document.getElementById(`connector-${direction[0]}b-${site.id}`);
        if (connectorEl) {
          connectorEl.style.background = `linear-gradient(to right, transparent, ${color}, transparent)`;
        }
      }
    });
  });
}

/**
 * Initialize corridor selector
 */
function initCorridorSelector() {
  const buttons = document.querySelectorAll('.corridor-btn');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      // Update active state
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Generate visualization
      const corridorId = btn.dataset.corridor;
      generateFlowVisualization(corridorId);
    });
  });

  // Initialize with default corridor
  generateFlowVisualization('mounts-bay');
}
```

**CSS for Dynamic Flow**:
```css
.corridor-selector {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.corridor-btn {
  padding: 0.75rem 1.5rem;
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.corridor-btn:hover {
  background: var(--surface-hover);
  transform: translateY(-2px);
}

.corridor-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.flow-diagram {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 0;
  overflow-x: auto;
}

.flow-site {
  flex-shrink: 0;
  width: 120px;
  text-align: center;
}

.flow-connector {
  flex-shrink: 0;
  width: 60px;
  height: 80px;
  position: relative;
}
```

**Benefits**:
- ✅ Supports all corridors (arterial + freeway)
- ✅ Dynamic generation based on network
- ✅ Scalable to any number of sites
- ✅ Live data updates with color coding

---

## 📐 Implementation Plan

### Phase 1: Theme Simplification (1 hour)
1. Remove 4-theme system
2. Implement light/dark toggle
3. Update CSS variables
4. Test on all devices

### Phase 2: Modern Site Selector (3 hours)
1. Design searchable dropdown component
2. Add site icons and badges
3. Implement search/filter logic
4. Test keyboard navigation and accessibility

### Phase 3: Map Auto-Pan (2 hours)
1. Add site coordinates to database
2. Implement panToSite() function
3. Create pulsing highlight marker
4. Test animations and transitions

### Phase 4: Dynamic Flow Visualization (4 hours)
1. Create corridor configurations
2. Build dynamic generation logic
3. Connect to live data APIs
4. Add corridor selector buttons
5. Test with all networks

### Total Estimated Time: 10 hours

---

## 🎯 Success Metrics

- ✅ Theme switch < 0.3s
- ✅ Site search returns results < 100ms
- ✅ Map pan animation smooth at 60fps
- ✅ Flow visualization supports 52 sites
- ✅ Mobile responsive on all devices
- ✅ WCAG 2.1 AA accessibility compliance

---

## 🖼️ Mockups & Wireframes

### Before (Current)
```
┌─────────────────────────────────────┐
│ Theme: [Dropdown with 4 options  ▼] │
│ Site:  [Long boring dropdown     ▼] │
│                                      │
│ [Static map - manual pan only]      │
│                                      │
│ Mounts Bay Road Flow (4 sites only) │
└─────────────────────────────────────┘
```

### After (Improved)
```
┌─────────────────────────────────────┐
│ [☀️ Light Mode]  [🔍 Search sites...] │
│                                      │
│ ┌─ Mitchell Fwy @ Narrows ─────┐   │
│ │ 🛣️ Northbound  🟢 Live       │   │
│ │ Flow: 850/hr  Speed: 98 km/h  │   │
│ └─────────────────────────────────┘   │
│                                      │
│ [Auto-pan map with pulsing marker]  │
│                                      │
│ Flow: [Mounts Bay] [Mitchell] [...]  │
│ [Dynamic 9-site visualization]       │
└─────────────────────────────────────┘
```

---

## 📚 References

- [Material Design - Dropdowns](https://m3.material.io/components/menus/overview)
- [Leaflet - Map Animation](https://leafletjs.com/reference.html#map-flyto)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [CSS Custom Properties Best Practices](https://web.dev/at-property/)

---

## ✅ Next Steps

1. Review and approve design proposals
2. Prioritize features (all? subset?)
3. Begin Phase 1 implementation
4. Iterate based on user feedback
