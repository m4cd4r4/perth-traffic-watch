# Perth Traffic Watch - Vultr Deployment

Deploy the Perth Traffic Watch API to your Vultr server for 24/7 operation.

## Server Details

- **Server**: 45.77.233.102 (Vultr Sydney)
- **API Port**: 80 (nginx) -> 3001 (container) -> 3000 (app)
- **API URL**: http://45.77.233.102/api/

## Quick Deploy

```bash
# SSH into server
ssh root@45.77.233.102

# Create directory
mkdir -p /opt/perth-traffic-watch
cd /opt/perth-traffic-watch

# Clone or copy deployment files
git clone https://github.com/m4cd4r4/perth-traffic-watch.git .
# Or scp the files

# Copy backend code to deployment folder
cp -r backend/api deployment/backend/

# Start services
cd deployment
docker compose up -d

# Check status
docker compose ps
docker compose logs -f
```

## API Endpoints

Once deployed, the API is available at:

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/sites` | List all arterial sites |
| `GET /api/freeway/sites` | List all freeway sites |
| `GET /api/freeway/live` | Live freeway traffic data |
| `GET /api/stats/:site` | Statistics for a site |
| `GET /api/detections` | Recent detections |

## Update Frontend to Use Vultr API

After deployment, update the frontend to use the Vultr API:

```javascript
// frontend/web-dashboard/app.js
const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:3000'
  : 'http://45.77.233.102';  // Vultr API
```

## Warmup Cron (Optional)

Add a cron job to ping the API and prevent cold starts (if still using Render as fallback):

```bash
# Add to crontab on Vultr
crontab -e

# Ping every 5 minutes
*/5 * * * * curl -s http://localhost/health > /dev/null
*/5 * * * * curl -s https://perth-traffic-watch.onrender.com/health > /dev/null
```

## Monitoring

```bash
# View logs
docker compose logs -f api

# Check API health
curl http://localhost/health

# View traffic data
curl http://localhost/api/freeway/live | jq

# Check container resources
docker stats
```

## Troubleshooting

### Container won't start
```bash
docker compose logs api
docker compose down
docker compose up -d --build
```

### Database issues
```bash
# The SQLite database is persisted in a Docker volume
docker volume ls
docker volume inspect perth-traffic-watch_traffic_data
```

### Reset everything
```bash
docker compose down -v  # Warning: removes data volume
docker compose up -d --build
```
