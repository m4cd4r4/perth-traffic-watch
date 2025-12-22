-- Freeway Expansion Database Migration
-- Adds tables for Mitchell & Kwinana Freeway monitoring
-- Version: 1.0
-- Created: 2025-12-19

-- Freeway monitoring sites table
CREATE TABLE IF NOT EXISTS freeway_sites (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  corridor TEXT NOT NULL,        -- 'mitchell' or 'kwinana'
  ramp_id TEXT NOT NULL,         -- 'M1', 'K4', etc.
  name TEXT NOT NULL,
  latitude REAL NOT NULL,
  longitude REAL NOT NULL,
  ramp_type TEXT,                -- 'on', 'off', 'both', 'interchange'
  direction TEXT,                -- 'northbound', 'southbound', 'both'
  lanes INTEGER DEFAULT 3,
  distance_from_bridge REAL,     -- km
  speed_limit INTEGER DEFAULT 100,
  active BOOLEAN DEFAULT 1,
  is_simulated BOOLEAN DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Freeway detection data (similar to arterial detections)
CREATE TABLE IF NOT EXISTS freeway_detections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  site_id INTEGER REFERENCES freeway_sites(id),
  site_name TEXT NOT NULL,       -- Denormalized for easier querying
  timestamp INTEGER NOT NULL,    -- milliseconds since epoch
  flow_count INTEGER,            -- vehicles in last interval (30s or 60s)
  hour_count INTEGER,            -- extrapolated to hourly
  minute_count INTEGER,          -- extrapolated to per minute
  estimated_speed REAL,          -- km/h based on flow-density algorithm
  occupancy REAL,                -- % of time sensor occupied (0-1)
  density REAL,                  -- vehicles per km
  avg_confidence REAL,           -- ML confidence
  simulation_scenario TEXT,      -- 'normal', 'incident', 'event', 'weekend'
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Simulation runs (for reproducibility and testing)
CREATE TABLE IF NOT EXISTS simulation_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scenario_name TEXT NOT NULL,
  corridor TEXT,                 -- 'mitchell', 'kwinana', or 'both'
  started_at DATETIME,
  ended_at DATETIME,
  parameters TEXT,               -- JSON string of configuration
  notes TEXT
);

-- UFD speed samples (future implementation - placeholder)
CREATE TABLE IF NOT EXISTS ufd_speed_samples (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  upstream_site_id INTEGER REFERENCES freeway_sites(id),
  downstream_site_id INTEGER REFERENCES freeway_sites(id),
  feature_hash TEXT,             -- Anonymous feature signature
  upstream_timestamp INTEGER,
  downstream_timestamp INTEGER,
  travel_time_seconds REAL,
  calculated_speed_kmh REAL,
  segment_distance_km REAL,
  confidence REAL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_freeway_sites_corridor ON freeway_sites(corridor);
CREATE INDEX IF NOT EXISTS idx_freeway_sites_ramp_id ON freeway_sites(ramp_id);
CREATE INDEX IF NOT EXISTS idx_freeway_detections_site ON freeway_detections(site_id);
CREATE INDEX IF NOT EXISTS idx_freeway_detections_timestamp ON freeway_detections(timestamp);
CREATE INDEX IF NOT EXISTS idx_freeway_detections_site_name ON freeway_detections(site_name);
CREATE INDEX IF NOT EXISTS idx_ufd_samples_upstream ON ufd_speed_samples(upstream_site_id);
CREATE INDEX IF NOT EXISTS idx_ufd_samples_downstream ON ufd_speed_samples(downstream_site_id);
