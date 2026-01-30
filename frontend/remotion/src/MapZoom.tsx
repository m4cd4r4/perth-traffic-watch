import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

interface MapZoomProps {
  startZoom?: number;
  endZoom?: number;
  centerLat?: number;
  centerLng?: number;
}

export const MapZoom: React.FC<MapZoomProps> = ({
  startZoom = 11,
  endZoom = 14,
  centerLat = -31.9505,
  centerLng = 115.8605,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  // Smooth zoom animation using spring
  const zoomProgress = spring({
    frame,
    fps,
    config: {
      damping: 100,
      stiffness: 50,
    },
  });

  const currentZoom = interpolate(zoomProgress, [0, 1], [startZoom, endZoom]);

  // Scale factor for visual zoom effect
  const scale = interpolate(
    currentZoom,
    [startZoom, endZoom],
    [1, Math.pow(2, endZoom - startZoom)]
  );

  // Fade in at start, fade out at end
  const opacity = interpolate(
    frame,
    [0, 30, durationInFrames - 30, durationInFrames],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a1828',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
      }}
    >
      {/* Map visualization placeholder */}
      <div
        style={{
          width: '100%',
          height: '100%',
          position: 'relative',
          overflow: 'hidden',
          backgroundColor: '#1a2332',
        }}
      >
        {/* Perth metro area representation */}
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            width: '100%',
            height: '100%',
            transform: `translate(-50%, -50%) scale(${scale})`,
            transition: 'transform 0.1s ease-out',
          }}
        >
          {/* Simplified road network - Stirling Highway highlighted */}
          <svg
            width="100%"
            height="100%"
            viewBox="0 0 800 600"
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
            }}
          >
            {/* Background roads (Perth metro) */}
            <g opacity={interpolate(currentZoom, [11, 14], [0.8, 0.3])}>
              {/* Horizontal roads */}
              <line
                x1="100"
                y1="200"
                x2="700"
                y2="200"
                stroke="#4a5568"
                strokeWidth="2"
              />
              <line
                x1="100"
                y1="300"
                x2="700"
                y2="300"
                stroke="#4a5568"
                strokeWidth="2"
              />
              <line
                x1="100"
                y1="400"
                x2="700"
                y2="400"
                stroke="#4a5568"
                strokeWidth="2"
              />

              {/* Vertical roads */}
              <line
                x1="300"
                y1="100"
                x2="300"
                y2="500"
                stroke="#4a5568"
                strokeWidth="2"
              />
              <line
                x1="500"
                y1="100"
                x2="500"
                y2="500"
                stroke="#4a5568"
                strokeWidth="2"
              />
            </g>

            {/* Stirling Highway - main focus */}
            <g>
              {/* Background line */}
              <path
                d="M 200 150 Q 350 200, 400 300 T 600 450"
                fill="none"
                stroke="#2D8B94"
                strokeWidth="6"
                opacity="0.4"
              />

              {/* Animated dashed line */}
              <path
                d="M 200 150 Q 350 200, 400 300 T 600 450"
                fill="none"
                stroke="#4FC3D4"
                strokeWidth="4"
                strokeDasharray="12 8"
                strokeDashoffset={-frame * 0.5}
                opacity="0.9"
              />
            </g>

            {/* Monitoring sites - dots along the route */}
            {[0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1].map((t, i) => {
              // Calculate position along the curve
              const x = interpolate(t, [0, 1], [200, 600]);
              const y = 150 + Math.sin(t * Math.PI) * 150 + t * 300;

              const siteOpacity = interpolate(
                frame,
                [60 + i * 5, 80 + i * 5],
                [0, 1],
                {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
              );

              return (
                <g key={i} opacity={siteOpacity}>
                  {/* Outer glow */}
                  <circle
                    cx={x}
                    cy={y}
                    r="8"
                    fill="#4FC3D4"
                    opacity="0.3"
                  />
                  {/* Inner dot */}
                  <circle
                    cx={x}
                    cy={y}
                    r="4"
                    fill="#4FC3D4"
                  />
                </g>
              );
            })}
          </svg>

          {/* Map details that appear as we zoom */}
          <div
            style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              opacity: interpolate(currentZoom, [11, 14], [0, 1]),
              fontSize: '14px',
              color: '#a0aec0',
              fontFamily: 'Space Grotesk, sans-serif',
            }}
          >
            <div style={{textAlign: 'center', marginBottom: '20px'}}>
              <div style={{fontSize: '18px', fontWeight: 600, color: '#4FC3D4'}}>
                Stirling Highway Corridor
              </div>
              <div style={{fontSize: '12px', marginTop: '5px'}}>
                18 Monitoring Sites • 6km Coverage
              </div>
            </div>
          </div>
        </div>

        {/* Zoom level indicator */}
        <div
          style={{
            position: 'absolute',
            bottom: '30px',
            left: '30px',
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: '14px',
            color: '#718096',
            backgroundColor: 'rgba(26, 35, 50, 0.8)',
            padding: '8px 12px',
            borderRadius: '4px',
          }}
        >
          Zoom: {currentZoom.toFixed(1)}
        </div>
      </div>
    </AbsoluteFill>
  );
};
