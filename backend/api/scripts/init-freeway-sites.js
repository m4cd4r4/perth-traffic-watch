/**
 * Freeway Sites Initialization
 * Populates 30 virtual monitoring sites for Mitchell & Kwinana Freeways
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const dbPath = path.join(__dirname, '..', 'traffic-watch.db');
const db = new Database(dbPath);

console.log('===============================================');
console.log('Freeway Traffic Watch - Site Initialization');
console.log('===============================================\n');

// Run migration to create tables
console.log('Running database migration...');
const migrationSQL = fs.readFileSync(
  path.join(__dirname, '..', 'migrations', '001-add-freeway-tables.sql'),
  'utf8'
);
db.exec(migrationSQL);
console.log('✓ Migration complete\n');

// Mitchell Freeway sites (9 locations × 2 directions = 18 sensors)
const mitchellSites = [
  {
    ramp_id: 'M1-NB', name: 'Narrows Interchange (Northbound)', direction: 'northbound',
    ramp_type: 'interchange', distance: 0.0, lat: -31.9580, lon: 115.8450, lanes: 4
  },
  {
    ramp_id: 'M1-SB', name: 'Narrows Interchange (Southbound)', direction: 'southbound',
    ramp_type: 'interchange', distance: 0.0, lat: -31.9580, lon: 115.8452, lanes: 4
  },
  {
    ramp_id: 'M2-NB', name: 'Malcolm Street (Northbound)', direction: 'northbound',
    ramp_type: 'on', distance: 0.5, lat: -31.9540, lon: 115.8470, lanes: 3
  },
  {
    ramp_id: 'M2-SB', name: 'Malcolm Street (Southbound)', direction: 'southbound',
    ramp_type: 'off', distance: 0.5, lat: -31.9540, lon: 115.8472, lanes: 3
  },
  {
    ramp_id: 'M3-NB', name: 'Loftus Street (Northbound)', direction: 'northbound',
    ramp_type: 'both', distance: 1.0, lat: -31.9500, lon: 115.8480, lanes: 3
  },
  {
    ramp_id: 'M3-SB', name: 'Loftus Street (Southbound)', direction: 'southbound',
    ramp_type: 'both', distance: 1.0, lat: -31.9500, lon: 115.8482, lanes: 3
  },
  {
    ramp_id: 'M4-NB', name: 'Newcastle/Roe Street (Northbound)', direction: 'northbound',
    ramp_type: 'interchange', distance: 1.5, lat: -31.9450, lon: 115.8510, lanes: 3
  },
  {
    ramp_id: 'M4-SB', name: 'Newcastle/Roe Street (Southbound)', direction: 'southbound',
    ramp_type: 'interchange', distance: 1.5, lat: -31.9450, lon: 115.8512, lanes: 3
  },
  {
    ramp_id: 'M5-NB', name: 'Charles Street (Northbound)', direction: 'northbound',
    ramp_type: 'both', distance: 2.0, lat: -31.9400, lon: 115.8530, lanes: 3
  },
  {
    ramp_id: 'M5-SB', name: 'Charles Street (Southbound)', direction: 'southbound',
    ramp_type: 'both', distance: 2.0, lat: -31.9400, lon: 115.8532, lanes: 3
  },
  {
    ramp_id: 'M6-NB', name: 'Vincent Street (Northbound)', direction: 'northbound',
    ramp_type: 'both', distance: 2.5, lat: -31.9350, lon: 115.8540, lanes: 3
  },
  {
    ramp_id: 'M6-SB', name: 'Vincent Street (Southbound)', direction: 'southbound',
    ramp_type: 'both', distance: 2.5, lat: -31.9350, lon: 115.8542, lanes: 3
  },
  {
    ramp_id: 'M7-NB', name: 'Powis Street (Northbound)', direction: 'northbound',
    ramp_type: 'both', distance: 3.0, lat: -31.9300, lon: 115.8520, lanes: 3
  },
  {
    ramp_id: 'M7-SB', name: 'Powis Street (Southbound)', direction: 'southbound',
    ramp_type: 'both', distance: 3.0, lat: -31.9300, lon: 115.8522, lanes: 3
  },
  {
    ramp_id: 'M8-NB', name: 'Hutton Street (Northbound)', direction: 'northbound',
    ramp_type: 'both', distance: 4.0, lat: -31.9200, lon: 115.8500, lanes: 3
  },
  {
    ramp_id: 'M8-SB', name: 'Hutton Street (Southbound)', direction: 'southbound',
    ramp_type: 'both', distance: 4.0, lat: -31.9200, lon: 115.8502, lanes: 3
  },
  {
    ramp_id: 'M9-NB', name: 'Scarborough Beach Road (Northbound)', direction: 'northbound',
    ramp_type: 'interchange', distance: 5.0, lat: -31.9100, lon: 115.8480, lanes: 3
  },
  {
    ramp_id: 'M9-SB', name: 'Scarborough Beach Road (Southbound)', direction: 'southbound',
    ramp_type: 'interchange', distance: 5.0, lat: -31.9100, lon: 115.8482, lanes: 3
  }
];

// Kwinana Freeway sites (6 locations × 2 directions = 12 sensors)
const kwinanaSites = [
  {
    ramp_id: 'K1-NB', name: 'Narrows South (Northbound)', direction: 'northbound',
    ramp_type: 'on', distance: 0.0, lat: -31.9620, lon: 115.8460, lanes: 3
  },
  {
    ramp_id: 'K1-SB', name: 'Narrows South (Southbound)', direction: 'southbound',
    ramp_type: 'off', distance: 0.0, lat: -31.9620, lon: 115.8462, lanes: 3
  },
  {
    ramp_id: 'K2-NB', name: 'Mill Point Road (Northbound)', direction: 'northbound',
    ramp_type: 'both', distance: 0.6, lat: -31.9680, lon: 115.8550, lanes: 3
  },
  {
    ramp_id: 'K2-SB', name: 'Mill Point Road (Southbound)', direction: 'southbound',
    ramp_type: 'both', distance: 0.6, lat: -31.9680, lon: 115.8552, lanes: 3
  },
  {
    ramp_id: 'K3-NB', name: 'South Terrace/Judd St (Northbound)', direction: 'northbound',
    ramp_type: 'both', distance: 1.5, lat: -31.9780, lon: 115.8620, lanes: 3
  },
  {
    ramp_id: 'K3-SB', name: 'South Terrace/Judd St (Southbound)', direction: 'southbound',
    ramp_type: 'both', distance: 1.5, lat: -31.9780, lon: 115.8622, lanes: 3
  },
  {
    ramp_id: 'K4-NB', name: 'Canning Highway (Northbound)', direction: 'northbound',
    ramp_type: 'interchange', distance: 3.0, lat: -31.9950, lon: 115.8600, lanes: 3
  },
  {
    ramp_id: 'K4-SB', name: 'Canning Highway (Southbound)', direction: 'southbound',
    ramp_type: 'interchange', distance: 3.0, lat: -31.9950, lon: 115.8602, lanes: 3
  },
  {
    ramp_id: 'K5-NB', name: 'Manning Road (Northbound)', direction: 'northbound',
    ramp_type: 'off', distance: 4.5, lat: -32.0100, lon: 115.8580, lanes: 3
  },
  {
    ramp_id: 'K5-SB', name: 'Manning Road (Southbound)', direction: 'southbound',
    ramp_type: 'on', distance: 4.5, lat: -32.0100, lon: 115.8582, lanes: 3
  },
  {
    ramp_id: 'K6-NB', name: 'Leach Highway (Northbound)', direction: 'northbound',
    ramp_type: 'interchange', distance: 5.5, lat: -32.0220, lon: 115.8560, lanes: 3
  },
  {
    ramp_id: 'K6-SB', name: 'Leach Highway (Southbound)', direction: 'southbound',
    ramp_type: 'interchange', distance: 5.5, lat: -32.0220, lon: 115.8562, lanes: 3
  }
];

// Insert sites
const insertSite = db.prepare(`
  INSERT INTO freeway_sites (
    corridor, ramp_id, name, latitude, longitude,
    ramp_type, direction, lanes, distance_from_bridge,
    speed_limit, active, is_simulated
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

const insertDetection = db.prepare(`
  INSERT INTO freeway_detections (
    site_id, site_name, timestamp, flow_count, hour_count, minute_count,
    estimated_speed, occupancy, density, avg_confidence, simulation_scenario
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

console.log('Populating Mitchell Freeway sites...');
const mitchellTransaction = db.transaction(() => {
  mitchellSites.forEach(site => {
    const result = insertSite.run(
      'mitchell',
      site.ramp_id,
      site.name,
      site.lat,
      site.lon,
      site.ramp_type,
      site.direction,
      site.lanes,
      site.distance,
      100, // speed limit
      1,   // active
      1    // is_simulated
    );

    // Create initial detection record
    const now = Date.now();
    insertDetection.run(
      result.lastInsertRowid,
      site.name,
      now,
      0, 0, 0,        // flow counts
      95,             // initial speed (free flow)
      0.05,           // low occupancy
      5,              // low density
      0.85,           // confidence
      'normal'        // scenario
    );
  });
});
mitchellTransaction();
console.log(`✓ Created ${mitchellSites.length} Mitchell Freeway sensors\n`);

console.log('Populating Kwinana Freeway sites...');
const kwinanaTransaction = db.transaction(() => {
  kwinanaSites.forEach(site => {
    const result = insertSite.run(
      'kwinana',
      site.ramp_id,
      site.name,
      site.lat,
      site.lon,
      site.ramp_type,
      site.direction,
      site.lanes,
      site.distance,
      100, // speed limit
      1,   // active
      1    // is_simulated
    );

    // Create initial detection record
    const now = Date.now();
    insertDetection.run(
      result.lastInsertRowid,
      site.name,
      now,
      0, 0, 0,        // flow counts
      95,             // initial speed (free flow)
      0.05,           // low occupancy
      5,              // low density
      0.85,           // confidence
      'normal'        // scenario
    );
  });
});
kwinanaTransaction();
console.log(`✓ Created ${kwinanaSites.length} Kwinana Freeway sensors\n`);

// Summary
const totalMitchell = db.prepare('SELECT COUNT(*) as count FROM freeway_sites WHERE corridor = ?').get('mitchell');
const totalKwinana = db.prepare('SELECT COUNT(*) as count FROM freeway_sites WHERE corridor = ?').get('kwinana');
const totalSites = totalMitchell.count + totalKwinana.count;

console.log('===============================================');
console.log('Freeway sites initialized successfully!');
console.log('===============================================');
console.log(`Mitchell Freeway: ${totalMitchell.count} sensors`);
console.log(`Kwinana Freeway: ${totalKwinana.count} sensors`);
console.log(`TOTAL: ${totalSites} virtual monitoring sites`);
console.log('===============================================\n');

db.close();
process.exit(0);
