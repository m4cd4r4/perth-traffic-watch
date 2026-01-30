import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from 'remotion';

interface SwanLogoProps {
  backgroundColor?: string;
}

// Main composition
export const SwanLogo: React.FC<SwanLogoProps> = ({
  backgroundColor = '#0a1828',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Color palette
  const swanColor = '#e8f1f5';
  const accentColor = '#4A7C82';

  // Timing configuration (in seconds)
  const timing = {
    swan: 0,
    text: 2.5,
  };

  // Swan animation
  const swanOpacity = interpolate(
    frame,
    [timing.swan * fps, (timing.swan + 1) * fps],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  const swanScale = spring({
    frame: Math.max(0, frame - timing.swan * fps),
    fps,
    config: {damping: 15, stiffness: 80},
  });

  // Text animation
  const textOpacity = interpolate(
    frame,
    [timing.text * fps, (timing.text + 0.5) * fps],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  const textTranslateY = interpolate(
    frame,
    [timing.text * fps, (timing.text + 0.5) * fps],
    [30, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'Space Grotesk, system-ui, sans-serif',
      }}
    >
      {/* Swan Logo Image */}
      <div
        style={{
          opacity: swanOpacity,
          transform: `scale(${swanScale})`,
          marginBottom: '40px',
        }}
      >
        <Img
          src={staticFile('swan-logo.svg')}
          style={{
            width: '350px',
            height: 'auto',
          }}
        />
      </div>

      {/* SwanFlow text */}
      <Sequence from={timing.text * fps} premountFor={15}>
        <div
          style={{
            opacity: textOpacity,
            transform: `translateY(${textTranslateY}px)`,
          }}
        >
          <h1
            style={{
              fontSize: '72px',
              fontWeight: 700,
              margin: 0,
              color: swanColor,
              letterSpacing: '-0.02em',
            }}
          >
            SwanFlow
          </h1>
          <p
            style={{
              fontSize: '24px',
              margin: '10px 0 0 0',
              color: accentColor,
              textAlign: 'center',
              fontWeight: 400,
            }}
          >
            Real-time Traffic Intelligence
          </p>
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
