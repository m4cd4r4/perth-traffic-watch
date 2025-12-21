/**
 * Freeway Traffic Simulator
 *
 * Generates realistic real-time freeway traffic data for Mitchell & Kwinana corridors
 * Calibrated for 100 km/h multi-lane freeway conditions
 */

const Database = require('better-sqlite3');

// Configuration
const SIMULATION_ENABLED = process.env.SIMULATE_FREEWAY === 'true' || true; // Enable by default for demo
const UPDATE_INTERVAL = 60000; // 60 seconds (freeways have more stable flow)
const db = new Database('./traffic-watch.db');

// Freeway traffic patterns by hour (base vehicles per hour per lane)
// Peak capacity ~2200 veh/hr/lane for Australian freeways
const freewayPatterns = {
  // Hour: base flow per lane (veh/hr)
  0: 150,   1: 100,   2: 75,    3: 50,    4: 100,  5: 300,
  6: 800,   7: 1500,  8: 1800,  9: 1200,  10: 900, 11: 850,
  12: 950,  13: 900,  14: 850,  15: 1100, 16: 1600, 17: 1900,
  18: 1500, 19: 1000, 20: 700,  21: 500,  22: 350, 23: 200
};

// Direction modifiers for peak hours
// Mitchell: Outbound (NB) heavy in PM, Kwinana: Outbound (SB) heavy in PM
const directionModifiers = {
  mitchell: {
    northbound: {  morning: 0.7,  evening: 1.5  },  // PM peak: CBD → North
    southbound: { morning: 1.5,  evening: 0.7  }   // AM peak: North → CBD
  },
  kwinana: {
    northbound: {  morning: 1.5,  evening: 0.7  },  // AM peak: South → CBD
    southbound: { morning: 0.7,  evening: 1.5  }   // PM peak: CBD → South
  }
};

// Distance-based multipliers (closer to CBD = higher volume)
function getDistanceMultiplier(distance, corridor) {
  // Sites closer to Narrows (CBD) have higher base flow
  if (distance < 1.0) return 1.3;
  if (distance < 2.0) return 1.2;
  if (distance < 3.5) return 1.1;
  return 1.0;
}

/**
 * Freeway Speed Estimation Algorithm
 * Based on Highway Capacity Manual (HCM) speed-flow relationship
 */
function estimateFreewaySpeed(hourlyCount, lanes = 3) {
  const flowPerLane = hourlyCount / lanes;
  const capacityPerLane = 2200;
  const vcRatio = flowPerLane / capacityPerLane;

  if (vcRatio < 0.3) {
    // Free flow: 95-100 km/h
    return 100 - (vcRatio * 16.7);
  } else if (vcRatio < 0.7) {
    // Stable flow: 70-95 km/h
    return 95 - ((vcRatio - 0.3) * 62.5);
  } else if (vcRatio < 0.9) {
    // Approaching capacity: 40-70 km/h
    return 70 - ((vcRatio - 0.7) * 150);
  } else if (vcRatio < 1.0) {
    // At capacity: 20-40 km/h
    return 40 - ((vcRatio - 0.9) * 200);
  } else {
    // Over capacity (breakdown): 5-20 km/h
    return Math.max(5, 20 - ((vcRatio - 1.0) * 50));
  }
}

/**
 * Calculate occupancy (% of time sensor is occupied)
 */
function calculateOccupancy(hourlyCount, speed, lanes = 3) {
  // Occupancy = (vehicles/hour) × (vehicle length + gap) / (speed × lanes)
  // Typical vehicle length: 5m, gap at high speed: ~20m
  const vehiclesPerSecond = hourlyCount / 3600;
  const avgVehicleFootprint = 25; // meters (5m vehicle + 20m gap)
  const speedMetersPerSecond = (speed * 1000) / 3600;
  const occupancy = (vehiclesPerSecond * avgVehicleFootprint) / (speedMetersPerSecond * lanes);
  return Math.min(Math.max(occupancy, 0.01), 0.95);
}

/**
 * Calculate density (vehicles per km)
 */
function calculateDensity(hourlyCount, speed, lanes = 3) {
  // Density = Flow / Speed (per lane)
  const flowPerLane = hourlyCount / lanes;
  const density = flowPerLane / speed;
  return Math.max(density, 1);
}

/**
 * Get flow count for a site based on time and characteristics
 */
function getFlowCount(hour, site) {
  const baseFlow = freewayPatterns[hour];
  let flow = baseFlow * site.lanes;

  // Apply distance multiplier
  flow *= getDistanceMultiplier(site.distance_from_bridge, site.corridor);

  // Apply rush hour direction bias
  const directionMod = directionModifiers[site.corridor][site.direction];
  if (hour >= 6 && hour <= 9) {
    flow *= directionMod.morning;
  } else if (hour >= 16 && hour <= 19) {
    flow *= directionMod.evening;
  }

  // Weekend reduction
  const now = new Date();
  const dayOfWeek = now.getDay();
  if (dayOfWeek === 0 || dayOfWeek === 6) {
    flow *= 0.6; // 40% less traffic on weekends
  }

  // Add random variance (±15%)
  flow *= 0.85 + (Math.random() * 0.3);

  return Math.max(Math.round(flow), 0);
}

function getConfidence() {
  // Freeways have more stable conditions, higher confidence
  const hour = new Date().getHours();
  const isDay = hour >= 6 && hour <= 20;
  return isDay ? 0.85 + Math.random() * 0.10 : 0.75 + Math.random() * 0.15;
}

function simulateFreewayTraffic() {
  const now = Date.now();
  const hour = new Date().getHours();

  const insertDetection = db.prepare(`
    INSERT INTO freeway_detections (
      site_id, site_name, timestamp, flow_count, hour_count, minute_count,
      estimated_speed, occupancy, density, avg_confidence, simulation_scenario
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  // Get all freeway sites
  const sites = db.prepare(`
    SELECT * FROM freeway_sites WHERE active = 1 ORDER BY id
  `).all();

  sites.forEach(site => {
    // Calculate hourly flow
    const hourlyFlow = getFlowCount(hour, site);

    // Convert to interval flow (60 seconds)
    const intervalFlow = Math.round(hourlyFlow * (UPDATE_INTERVAL / 1000 / 3600));

    // Estimate speed based on flow
    const speed = estimateFreewaySpeed(hourlyFlow, site.lanes);

    // Calculate occupancy and density
    const occupancy = calculateOccupancy(hourlyFlow, speed, site.lanes);
    const density = calculateDensity(hourlyFlow, speed, site.lanes);

    // Extrapolate to minute count
    const minuteCount = Math.round(hourlyFlow / 60);

    const confidence = getConfidence();

    // Determine scenario
    let scenario = 'normal';
    if (speed < 30) scenario = 'severe';
    else if (speed < 50) scenario = 'heavy';
    else if (hourlyFlow > 5000) scenario = 'peak';

    insertDetection.run(
      site.id,
      site.name,
      now,
      intervalFlow,
      Math.round(hourlyFlow),
      minuteCount,
      Math.round(speed),
      Math.round(occupancy * 100) / 100,
      Math.round(density * 10) / 10,
      Math.round(confidence * 100) / 100,
      scenario
    );

    // Log significant updates
    if (intervalFlow > 5 || speed < 70) {
      const siteName = site.name.substring(0, 35).padEnd(35);
      const flowStr = `${hourlyFlow} veh/hr`.padEnd(12);
      const speedStr = `${Math.round(speed)} km/h`.padEnd(10);
      console.log(`[FREEWAY] ${siteName} | ${flowStr} | ${speedStr} | ${scenario.toUpperCase()}`);
    }
  });
}

function startFreewaySimulator() {
  if (!SIMULATION_ENABLED) {
    console.log('[FREEWAY] Freeway simulation disabled');
    return;
  }

  console.log('=================================');
  console.log('Freeway Traffic Simulator Started');
  console.log('=================================');
  console.log(`Update interval: ${UPDATE_INTERVAL / 1000}s`);
  console.log(`Corridors: Mitchell (18 sensors) + Kwinana (12 sensors)`);
  console.log(`Total: 30 virtual freeway sensors`);
  console.log('Generating real-time freeway data...\\n');

  // Run immediately on start
  setTimeout(() => {
    try {
      simulateFreewayTraffic();
    } catch (error) {
      console.error('[FREEWAY] Error:', error.message);
    }
  }, 10000); // Wait 10 seconds for server to stabilize

  // Then run on interval
  setInterval(() => {
    try {
      simulateFreewayTraffic();
    } catch (error) {
      console.error('[FREEWAY] Error:', error.message);
    }
  }, UPDATE_INTERVAL);
}

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\\n[FREEWAY] Shutting down...');
  db.close();
  process.exit(0);
});

module.exports = { startFreewaySimulator };
