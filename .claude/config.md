# SwanFlow - Infrastructure Configuration

**Project**: SwanFlow (formerly Perth Traffic Watch)
**Updated**: December 23, 2025

---

## 🌐 Production URLs

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | https://swanflow.com.au | ✅ Vercel (Global CDN) |
| **Backend API** | https://45.77.233.102/traffic/api/ | ✅ Vultr Sydney VPS |
| **GitHub Repo** | https://github.com/m4cd4r4/SwanFlow | ✅ Master branch |

---

## 🖥️ Backend - Vultr Sydney VPS (Shared Infrastructure)

**Server Details:**
- **IP**: 45.77.233.102
- **Location**: Sydney, Australia
- **Provider**: Vultr
- **Plan**: 4 vCPU, 8GB RAM, 160GB SSD (~AU$60/mo)
- **OS**: Ubuntu with Docker

**⚠️ IMPORTANT**: This Vultr VPS hosts **multiple services**:
1. **SwanFlow** (Perth Traffic Watch API) - Traffic monitoring
2. **Donnacha** - Voice AI assistant (FastAPI, PostgreSQL, Redis, Whisper, Ollama)
3. **Chlann** - Messaging platform (Traefik, backend, ML, Redis, PostgreSQL, MinIO, Coturn)
4. **IT Support Server** - Remote support tool

### Services Running (Docker)

```bash
# SwanFlow API
perth-traffic-api      Up 2 days (healthy)    0.0.0.0:3001->3000/tcp

# Chlann Platform
chlann-traefik         Up                     0.0.0.0:8880->80/tcp, 8443->443/tcp
chlann-backend         Up (healthy)           0.0.0.0:4000->4000/tcp
chlann-ml              Up (healthy)           0.0.0.0:8001->8000/tcp
chlann-redis           Up (healthy)           0.0.0.0:6379->6379/tcp
chlann-postgres        Up (healthy)           0.0.0.0:15432->5432/tcp
chlann-minio           Up (healthy)           0.0.0.0:9000-9001->9000-9001/tcp
chlann-coturn          Up                     Various ports

# Donnacha Services
donnacha-backend       Up 2 days
postgres               Up 2 days              0.0.0.0:5432->5432/tcp
redis                  Up 2 days              6379/tcp
ollama                 Up 2 days              11434/tcp
whisper                Up 2 days              9000/tcp

# IT Support
it-support-server      Up 2 days (unhealthy)  0.0.0.0:8080->8080/tcp
it-support-postgres    Up 2 days (healthy)
it-support-redis       Up 2 days (healthy)

# Nginx Reverse Proxy
nginx                  Up                     0.0.0.0:80->80/tcp, 443->443/tcp
```

### Nginx Routing Configuration

Nginx acts as reverse proxy for all services:

```nginx
# SwanFlow API
https://45.77.233.102/traffic/api/*  → http://localhost:3001/api/*
https://45.77.233.102/traffic/health → http://localhost:3001/health

# Chlann Platform
https://chlann.com/*                 → http://172.21.0.1:8880/*
https://api.chlann.com/*             → http://172.21.0.1:8880/*

# Donnacha
https://45.77.233.102/*              → Donnacha backend

# CORS enabled for SwanFlow API:
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
```

### SwanFlow API Endpoints

```bash
# Base URL
https://45.77.233.102/traffic

# Endpoints
GET  /health                   # {"status":"ok","timestamp":...}
GET  /api/sites                # Arterial road monitoring sites
GET  /api/freeway/sites        # Freeway monitoring sites
GET  /api/freeway/live         # Live freeway traffic data
GET  /api/stats/:site          # Site statistics
GET  /api/detections           # Recent vehicle detections
```

### SSH Access

```bash
ssh root@45.77.233.102
# Password: (stored in vault)

# Check services
docker ps

# SwanFlow API logs
docker logs perth-traffic-api -f

# Restart SwanFlow API
docker restart perth-traffic-api

# Check nginx config
docker exec nginx cat /etc/nginx/nginx.conf
```

---

## 🎨 Frontend - Vercel

**Hosting:**
- **Platform**: Vercel
- **Domain**: swanflow.com.au (assigned via DNS)
- **CDN**: Global edge network
- **Project Name**: swanflow

**Latest Deployment:**
```
https://swanflow-gbep1dggm-m4cd4r4s-projects.vercel.app
```

**Deployment Commands:**
```bash
cd i:/Scratch/perth-traffic-watch

# Standard deploy
vercel --prod --yes

# Force deploy (skip cache)
vercel --prod --yes --force

# Assign domain
vercel alias <deployment-url> swanflow.com.au
```

**Frontend Tech Stack:**
- Vanilla HTML/CSS/JavaScript
- Leaflet.js for maps (OpenStreetMap tiles)
- Chart.js for traffic visualization
- Glassmorphism design aesthetic

**API Configuration:**
```javascript
// frontend/web-dashboard/app.js:6-8
const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:3000'
  : 'https://45.77.233.102/traffic';  // Vultr VPS
```

---

## 🗺️ Route Visualization - OSM Precision

**Critical Standard**: Route dots must trace Stirling Highway centerline with **pinpoint accuracy**.

**Coordinate Requirements:**
- **Source**: OpenStreetMap Overpass API only
- **Precision**: 6-7 decimal places (±0.111m to ±1.11cm)
- **Method**: Direct extraction from OSM road geometry
- **❌ Never approximate**: Always use OSM-exact coordinates

**Recent Corrections** (Dec 23, 2025):
- **Nedlands-City**: Fixed 2.9km-6.3km errors (dots were in Swan River!)
- **Claremont-Cottesloe**: Fixed 10km start point error + all waypoints
- **Mosman Park**: Fixed 4km latitude errors across all waypoints

**Route Corridors:**
1. Nedlands-City: Winthrop Ave → Point Lewis
2. Claremont-Cottesloe: Bunnings → Eric St
3. Mosman Park: Forrest St → Victoria St

**Process for Adding New Corridors:**
1. Query OpenStreetMap Overpass API for exact road geometry
2. Extract lat/lon pairs maintaining 6-7 decimal precision
3. Visual verification on satellite imagery overlay
4. Screenshot before deploying to production
5. Document Overpass query used

**Overpass API Example:**
```bash
https://overpass-api.de/api/interpreter?data=[out:json];
way["name"="Stirling Highway"](-32.05,115.74,-31.96,115.86);
out geom;
```

---

## 📊 Traffic Simulation

**Backend simulates realistic traffic patterns:**

**Hourly Pattern (24-hour cycle):**
- **Morning rush**: 7-9am (5.3-5.8x base rate)
- **Midday**: 10am-2pm (3.5-4.0x base rate)
- **Evening rush**: 4-6pm (5.5-6.3x base rate)
- **Night**: 12am-4am (0.3-0.5x base rate)

**Direction Bias:**
- **Northbound**: 1.3x morning, 0.7x evening (commute to city)
- **Southbound**: 0.7x morning, 1.3x evening (commute from city)

**Zone Modifiers:**
- **School zones**: 8-9am drop-off (1.8x), 3-4pm pickup (1.7x)
- **Commercial zones**: Midday boost 9am-5pm (1.1-1.5x)

**Timezone:**
- All times in **Perth timezone (AWST, UTC+8)**
- Uses `Australia/Perth` in `Date.toLocaleString()`

**Simulated Sites:**
- 22 arterial road sites (11 locations × 2 directions)
- Freeway sites (Mitchell, Kwinana, Graham Farmer - planned)

**Implementation:**
- `backend/api/live-simulator.js` - Arterial roads
- `backend/api/freeway-simulator.js` - Freeways

---

## 🔧 Local Development

**Backend:**
```bash
cd backend/api
npm install
npm run dev  # Nodemon hot reload
# Runs on http://localhost:3000
```

**Frontend:**
```bash
cd frontend/web-dashboard
python -m http.server 8000
# OR
npx serve .
# Open http://localhost:8000
```

**Database:**
- SQLite: `backend/api/traffic-watch.db`
- Auto-created on first run with schema
- Reset: `rm traffic-watch.db && npm run dev`

**Testing:**
```bash
# Health check
curl http://localhost:3000/health

# Get sites
curl http://localhost:3000/api/sites

# Get freeway live data
curl http://localhost:3000/api/freeway/live
```

---

## 🚀 Deployment Workflow

**1. Frontend Changes:**
```bash
# Make changes, test locally
cd i:/Scratch/perth-traffic-watch

# Commit
git add .
git commit -m "description"
git push origin master

# Deploy to Vercel
vercel --prod --yes

# Assign domain (if needed)
vercel alias <deployment-url> swanflow.com.au
```

**2. Backend Changes:**
```bash
# Make changes, test locally
git add backend/
git commit -m "description"
git push origin master

# SSH to server
ssh root@45.77.233.102

# Update and restart
cd /opt/perth-traffic-watch
git pull origin master
docker compose down perth-traffic-api
docker compose up -d perth-traffic-api --build

# Check logs
docker logs perth-traffic-api -f
```

**3. Route Corrections:**
```bash
# Always use OSM-exact coordinates!
# Edit frontend/web-dashboard/app.js lines ~675-745
# Test locally first
# Deploy as per frontend workflow
```

---

## 📁 Repository Structure

```
perth-traffic-watch/ (SwanFlow)
├── backend/api/
│   ├── index.js                # Express API server
│   ├── live-simulator.js       # Arterial traffic simulation
│   ├── freeway-simulator.js    # Freeway traffic simulation
│   └── traffic-watch.db        # SQLite DB (gitignored)
├── frontend/web-dashboard/
│   ├── index.html              # Dashboard UI
│   ├── app.js                  # Frontend logic + routes (lines 675-745)
│   └── styles.css              # Glassmorphism styling
├── deployment/
│   ├── README.md               # Vultr deployment guide
│   ├── docker-compose.yml      # Docker services
│   └── nginx/                  # Nginx config
├── docs/
│   ├── ROUTE_ALIGNMENT_SUMMARY.md      # Route corrections
│   ├── route-alignment-analysis.md     # Technical analysis
│   └── corrected-route-coordinates.js  # OSM coordinates
├── .claude/
│   └── config.md               # This file
└── vercel.json                 # Vercel build config
```

---

## 🐛 Troubleshooting

### Frontend shows no traffic data
**Symptoms**: Map loads but no dots, empty site dropdown
**Cause**: Backend API not responding or CORS error
**Fix**:
```bash
# Check backend health
curl https://45.77.233.102/traffic/health

# Check if API is accessible
curl https://45.77.233.102/traffic/api/sites

# If not responding, SSH and restart
ssh root@45.77.233.102
docker restart perth-traffic-api
```

### Route dots in wrong location
**Symptoms**: Dots appear in water, fields, or buildings
**Cause**: Coordinates approximated instead of OSM-exact
**Fix**: Query Overpass API, use 6-7 decimal precision
**See**: `docs/ROUTE_ALIGNMENT_SUMMARY.md`

### Frontend not updating after deploy
**Symptoms**: Changes don't appear on swanflow.com.au
**Cause**: CDN cache or browser cache serving stale files
**Fix**:
1. Deploy with `vercel --prod --yes --force` to invalidate CDN cache
2. Hard refresh browser (Ctrl+Shift+R)
3. Cache headers in `vercel.json` now set to `no-cache` for HTML and `must-revalidate` for CSS/JS

### Backend connection refused
**Symptoms**: `ERR_CONNECTION_REFUSED` or timeout
**Cause**: Container not running or nginx misconfigured
**Fix**:
```bash
ssh root@45.77.233.102
docker ps | grep perth-traffic
docker logs perth-traffic-api
docker restart nginx
```

### SSL certificate errors
**Symptoms**: HTTPS errors on 45.77.233.102
**Cause**: Let's Encrypt cert renewal failed
**Fix**:
```bash
ssh root@45.77.233.102
docker exec nginx certbot renew
docker restart nginx
```

---

## 🔒 Security & Access

**API Authentication:**
- GET endpoints: Public (read-only traffic data)
- POST endpoints: Require API key in Authorization header
- API Key: `process.env.API_KEY` (default: 'dev_key_change_in_production')

**Server Access:**
- SSH: `root@45.77.233.102` (password in vault)
- Shared with Donnacha, Chlann, IT Support services
- All services run in isolated Docker containers

**Domain & SSL:**
- swanflow.com.au → Vercel (automatic HTTPS)
- 45.77.233.102 → Let's Encrypt (auto-renewal)

---

## 📝 Development Standards

**Coordinate Precision:**
- ❌ **Never**: `-31.98, 115.78` (3-4 decimals - up to 10km errors!)
- ✅ **Always**: `-31.9834402, 115.7802709` (OSM-exact, ±11cm)

**Commit Messages:**
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Multi-line commits include Claude Code attribution

**Branch Strategy:**
- `master` = production (default branch)
- Feature branches → merge to master → delete branch
- No long-lived branches

**Route Testing:**
1. Query OSM Overpass API for exact coordinates
2. Update `app.js` routes array
3. Test locally with satellite base map
4. Screenshot each corridor for verification
5. Deploy only after visual confirmation

---

**Last Updated**: December 23, 2025
**Status**: ✅ Production deployment working with OSM-exact route corrections
