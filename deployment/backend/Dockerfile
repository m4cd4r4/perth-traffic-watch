# Perth Traffic Watch API - Production Dockerfile

FROM node:18-alpine

# Install build dependencies for better-sqlite3
RUN apk add --no-cache python3 make g++ curl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Initialize database and freeway sites on first run
# The entrypoint script will handle this

# Expose API port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start the API server
CMD ["node", "index.js"]
