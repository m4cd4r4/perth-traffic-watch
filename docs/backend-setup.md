# SwanFlow Backend - Quick Start Instructions

## Problem
SwanFlow site is stuck on "Loading..." because the backend isn't running on the VPS.

## Solution
SSH into your VPS and start the Docker containers.

## Steps

### 1. SSH into your VPS
```bash
ssh root@45.77.233.102
```

### 2. Navigate to deployment directory
```bash
cd /opt/perth-traffic-watch/deployment
```

If the directory doesn't exist:
```bash
mkdir -p /opt/perth-traffic-watch/deployment
cd /opt/perth-traffic-watch
git clone https://github.com/m4cd4r4/SwanFlow.git .
cd deployment
```

### 3. Check if containers are running
```bash
docker compose ps
```

### 4. Start the containers
```bash
docker compose up -d
```

### 5. Verify it's working
```bash
# Check logs
docker compose logs -f api

# Test health endpoint (press Ctrl+C after you see output)
curl http://localhost/health

# Test API endpoint
curl http://localhost/api/sites | head -20
```

### 6. Test from outside
From your local machine, run:
```bash
curl http://45.77.233.102/health
curl http://45.77.233.102/api/sites
```

### 7. Check SwanFlow website
Visit https://swanflow.com.au and it should now load data!

## Troubleshooting

### If containers won't start
```bash
# View detailed logs
docker compose logs api

# Rebuild and restart
docker compose down
docker compose up -d --build
```

### If API still not responding
```bash
# Check if port 80 is listening
netstat -tlnp | grep :80

# Check firewall (if ufw is enabled)
ufw status
ufw allow 80/tcp
```

### If you need to rebuild from scratch
```bash
cd /opt/perth-traffic-watch/deployment

# Copy latest backend code
rm -rf backend
cp -r ../backend/api backend/

# Restart
docker compose down
docker compose up -d --build
```

## What Changed

The frontend now uses Vercel proxy to avoid HTTPS/HTTP mismatch:
- **Before**: `https://api.swanflow.com.au/api/*` (failed - no SSL cert)
- **After**: `https://swanflow.com.au/api/*` → Vercel proxies to `http://45.77.233.102/api/*`

This means:
- ✅ No SSL cert needed on VPS
- ✅ No mixed content errors
- ✅ Frontend can load data over HTTPS
- ⚠️ **Backend MUST be running** on VPS for proxy to work
