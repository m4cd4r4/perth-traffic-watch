/**
 * Live Traffic Simulator
 *
 * Generates realistic real-time traffic data for demo purposes
 */

const Database = require('better-sqlite3');

// Configuration
const SIMULATION_ENABLED = process.env.SIMULATE_LIVE === 'true' || true; // Enable by default for demo
const UPDATE_INTERVAL = 30000; // 30 seconds
const db = new Database('./traffic-watch.db');

// Site definitions
const sites = [
  // Stirling Highway / Mounts Bay Road (Winthrop Ave → Point Lewis) - PoC Phase 1
  { name: 'Stirling Hwy @ Winthrop Ave (Northbound)', multiplier: 1.3, direction: 'NB' },  // High traffic - SCGH/UWA
  { name: 'Stirling Hwy @ Winthrop Ave (Southbound)', multiplier: 1.25, direction: 'SB' },
  { name: 'Stirling Hwy @ Broadway (Northbound)', multiplier: 1.15, direction: 'NB' },
  { name: 'Stirling Hwy @ Broadway (Southbound)', multiplier: 1.2, direction: 'SB' },
  { name: 'Mounts Bay Rd @ Kings Park (Northbound)', multiplier: 1.2, direction: 'NB' },
  { name: 'Mounts Bay Rd @ Kings Park (Southbound)', multiplier: 1.1, direction: 'SB' },
  { name: 'Mounts Bay Rd @ Mill Point (Northbound)', multiplier: 1.0, direction: 'NB' },
  { name: 'Mounts Bay Rd @ Mill Point (Southbound)', multiplier: 0.9, direction: 'SB' },
  { name: 'Mounts Bay Rd @ Fraser Ave (Northbound)', multiplier: 0.95, direction: 'NB' },
  { name: 'Mounts Bay Rd @ Fraser Ave (Southbound)', multiplier: 1.05, direction: 'SB' },
  { name: 'Mounts Bay Rd @ Malcolm St (Northbound)', multiplier: 0.85, direction: 'NB' },
  { name: 'Mounts Bay Rd @ Malcolm St (Southbound)', multiplier: 1.15, direction: 'SB' },

  // Stirling Hwy - Claremont to Cottesloe (Stirling Rd → Eric St) - Phase 2
  // Commercial zone (Bunnings, Claremont Quarter) - higher weekend/midday traffic
  { name: 'Stirling Hwy @ Stirling Rd (Northbound)', multiplier: 1.2, direction: 'NB', zone: 'commercial' },
  { name: 'Stirling Hwy @ Stirling Rd (Southbound)', multiplier: 1.15, direction: 'SB', zone: 'commercial' },
  // School zone (Christ Church, MLC nearby) - peak at school times
  { name: 'Stirling Hwy @ Jarrad St (Northbound)', multiplier: 1.1, direction: 'NB', zone: 'school' },
  { name: 'Stirling Hwy @ Jarrad St (Southbound)', multiplier: 1.05, direction: 'SB', zone: 'school' },
  // Residential/transition zone
  { name: 'Stirling Hwy @ Eric St (Northbound)', multiplier: 1.0, direction: 'NB' },
  { name: 'Stirling Hwy @ Eric St (Southbound)', multiplier: 0.95, direction: 'SB' },

  // Stirling Hwy - Mosman Park (Forrest St → Victoria St) - Phase 1
  { name: 'Stirling Hwy @ Forrest St (Northbound)', multiplier: 1.1, direction: 'NB' },
  { name: 'Stirling Hwy @ Forrest St (Southbound)', multiplier: 1.0, direction: 'SB' },
  { name: 'Stirling Hwy @ Bay View Terrace (Northbound)', multiplier: 1.05, direction: 'NB' },
  { name: 'Stirling Hwy @ Bay View Terrace (Southbound)', multiplier: 0.95, direction: 'SB' },
  { name: 'Stirling Hwy @ McCabe St (Northbound)', multiplier: 1.0, direction: 'NB' },
  { name: 'Stirling Hwy @ McCabe St (Southbound)', multiplier: 1.1, direction: 'SB' },
  { name: 'Stirling Hwy @ Victoria St (Northbound)', multiplier: 0.95, direction: 'NB' },
  { name: 'Stirling Hwy @ Victoria St (Southbound)', multiplier: 1.15, direction: 'SB' }
];

// Traffic patterns by hour (base vehicles per minute)
const trafficPatterns = {
  0: 0.75, 1: 0.58, 2: 0.42, 3: 0.33, 4: 0.50,
  5: 1.33, 6: 3.00, 7: 5.33, 8: 5.83, 9: 4.67,
  10: 3.67, 11: 3.50, 12: 4.00, 13: 3.83, 14: 3.50,
  15: 4.17, 16: 5.50, 17: 6.33, 18: 5.67, 19: 4.67,
  20: 3.33, 21: 2.50, 22: 1.83, 23: 1.17
};

// Direction modifiers
const directionModifiers = {
  NB: { morning: 1.3, evening: 0.7 },
  SB: { morning: 0.7, evening: 1.3 }
};

// Get current hour in Perth timezone (AWST, UTC+8)
function getPerthHour() {
  const hour = parseInt(new Date().toLocaleString('en-AU', {
    timeZone: 'Australia/Perth',
    hour: 'numeric',
    hour12: false
  }));
  // Handle midnight edge case (locale may return 24 instead of 0)
  return hour === 24 ? 0 : hour;
}

function startSimulator() {
  if (!SIMULATION_ENABLED) {
    console.log('[SIMULATOR] Live simulation disabled');
    return;
  }

  console.log('=================================');
  console.log('Live Traffic Simulator Started');
  console.log('=================================');
  console.log(`Update interval: ${UPDATE_INTERVAL / 1000}s`);
  console.log(`Sites: ${sites.length}`);
  console.log('Generating real-time traffic data...\n');

  // Run immediately on start
  setTimeout(() => {
    try {
      simulateTrafficUpdate();
    } catch (error) {
      console.error('[SIMULATOR] Error:', error.message);
    }
  }, 5000); // Wait 5 seconds for server to stabilize

  // Then run on interval
  setInterval(() => {
    try {
      simulateTrafficUpdate();
    } catch (error) {
      console.error('[SIMULATOR] Error:', error.message);
    }
  }, UPDATE_INTERVAL);
}

/**
 * Simulate a traffic update for all sites
 */
function simulateTrafficUpdate() {
  const hour = getPerthHour();
  const baseRate = trafficPatterns[hour];
  const timestamp = Date.now();

  // Determine if it's morning rush (6-9) or evening rush (16-19)
  const isMorningRush = hour >= 6 && hour <= 9;
  const isEveningRush = hour >= 16 && hour <= 19;

  const insertStmt = db.prepare(`
    INSERT INTO detections (site, timestamp, total_count, hour_count, minute_count, avg_confidence, uptime, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
  `);

  const updateTotalStmt = db.prepare(`
    SELECT MAX(total_count) as max_total FROM detections WHERE site = ?
  `);

  let updatedCount = 0;

  for (const site of sites) {
    // Get current total for this site
    const result = updateTotalStmt.get(site.name);
    const currentTotal = result?.max_total || 0;

    // Calculate traffic with multipliers
    let rate = baseRate * site.multiplier;

    // Apply direction modifiers for rush hours
    if (isMorningRush) {
      rate *= directionModifiers[site.direction]?.morning || 1.0;
    } else if (isEveningRush) {
      rate *= directionModifiers[site.direction]?.evening || 1.0;
    }

    // Apply zone modifiers
    if (site.zone === 'commercial' && (hour >= 10 && hour <= 16)) {
      rate *= 1.2; // Higher midday traffic for commercial zones
    }
    if (site.zone === 'school' && ((hour >= 8 && hour <= 9) || (hour >= 15 && hour <= 16))) {
      rate *= 1.4; // Higher school-time traffic
    }

    // Add randomness (±20%)
    rate *= 0.8 + Math.random() * 0.4;

    // Calculate counts
    const minuteCount = Math.round(rate);
    const hourCount = Math.round(rate * 60);
    const newTotal = currentTotal + minuteCount;

    // Confidence varies slightly (85-95%)
    const confidence = 0.85 + Math.random() * 0.1;

    // Uptime in seconds (simulated)
    const uptime = Math.floor((Date.now() - 1734789355000) / 1000); // Since Dec 21

    try {
      insertStmt.run(site.name, timestamp, newTotal, hourCount, minuteCount, confidence, uptime);
      updatedCount++;
    } catch (err) {
      // Site might not exist in sites table, skip silently
    }
  }

  console.log(`[SIMULATOR] Updated ${updatedCount} sites at hour ${hour} (base rate: ${baseRate.toFixed(2)} veh/min)`);
}

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n[SIMULATOR] Shutting down...');
  db.close();
  process.exit(0);
});

module.exports = { startSimulator };
