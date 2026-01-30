/**
 * SwanFlow Assembly Animation Component
 *
 * React/Next.js component for scroll-driven assembly animation.
 * Uses GSAP ScrollTrigger to scrub through pre-rendered frames.
 *
 * Usage:
 *   import AssemblyAnimation from '@/components/AssemblyAnimation';
 *   <AssemblyAnimation />
 *
 * Required: npm install gsap
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register GSAP plugin
if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

interface AssemblyAnimationProps {
  /** Path to frame images (without number and extension) */
  framePath?: string;
  /** Total number of frames */
  frameCount?: number;
  /** Frame file extension */
  frameExtension?: string;
  /** Height multiplier for scroll duration (default: 4 = 400vh) */
  scrollMultiplier?: number;
}

interface ComponentLabel {
  id: string;
  text: string;
  position: { top?: string; bottom?: string; left?: string; right?: string };
  visibleRange: { start: number; end: number };
}

const COMPONENT_LABELS: ComponentLabel[] = [
  { id: 'esp32', text: 'ESP32-CAM', position: { top: '30%', left: '60%' }, visibleRange: { start: 0.05, end: 0.20 } },
  { id: 'camera', text: 'OV2640 Camera', position: { top: '20%', left: '55%' }, visibleRange: { start: 0.10, end: 0.25 } },
  { id: 'lte', text: 'SIM7000A LTE', position: { top: '35%', right: '25%' }, visibleRange: { start: 0.20, end: 0.35 } },
  { id: 'battery', text: '12V Battery', position: { bottom: '40%', left: '25%' }, visibleRange: { start: 0.30, end: 0.45 } },
  { id: 'solar', text: 'Solar Controller', position: { bottom: '30%', right: '30%' }, visibleRange: { start: 0.40, end: 0.55 } },
  { id: 'box', text: 'Junction Box', position: { bottom: '35%', left: '50%' }, visibleRange: { start: 0.50, end: 0.70 } },
  { id: 'panel', text: 'Solar Panel', position: { bottom: '20%', left: '45%' }, visibleRange: { start: 0.65, end: 0.85 } },
];

export default function AssemblyAnimation({
  framePath = '/assembly/assembly_',
  frameCount = 120,
  frameExtension = '.png',
  scrollMultiplier = 4,
}: AssemblyAnimationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const imagesRef = useRef<HTMLImageElement[]>([]);

  const [isLoading, setIsLoading] = useState(true);
  const [loadProgress, setLoadProgress] = useState(0);
  const [scrollProgress, setScrollProgress] = useState(0);

  // Format frame number with leading zeros
  const formatFrameNumber = (num: number): string => {
    return String(num).padStart(4, '0');
  };

  // Draw frame to canvas
  const drawFrame = (frameIndex: number) => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;

    const frame = Math.min(Math.max(0, Math.floor(frameIndex)), frameCount - 1);
    const img = imagesRef.current[frame];

    if (img?.complete && img.naturalWidth > 0) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    }
  };

  // Preload images
  useEffect(() => {
    let loadedCount = 0;
    const images: HTMLImageElement[] = [];

    for (let i = 0; i < frameCount; i++) {
      const img = new Image();
      const src = `${framePath}${formatFrameNumber(i)}${frameExtension}`;

      img.onload = () => {
        loadedCount++;
        setLoadProgress(Math.round((loadedCount / frameCount) * 100));

        if (loadedCount === frameCount) {
          setIsLoading(false);
          drawFrame(0);
        }
      };

      img.onerror = () => {
        loadedCount++;
        console.warn(`Failed to load frame ${i}`);
      };

      img.src = src;
      images[i] = img;
    }

    imagesRef.current = images;
  }, [framePath, frameCount, frameExtension]);

  // Initialize ScrollTrigger
  useEffect(() => {
    if (isLoading || !containerRef.current) return;

    const trigger = ScrollTrigger.create({
      trigger: containerRef.current,
      start: 'top top',
      end: 'bottom bottom',
      scrub: 0.5,
      onUpdate: (self) => {
        const frameIndex = Math.floor(self.progress * (frameCount - 1));
        drawFrame(frameIndex);
        setScrollProgress(self.progress);
      },
    });

    return () => {
      trigger.kill();
    };
  }, [isLoading, frameCount]);

  // Resize canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    canvas.width = 1920;
    canvas.height = 1080;
  }, []);

  return (
    <>
      {/* Loading overlay */}
      {isLoading && (
        <div className="fixed inset-0 bg-slate-900 flex flex-col items-center justify-center z-50">
          <div className="w-12 h-12 border-3 border-slate-700 border-t-cyan-400 rounded-full animate-spin" />
          <p className="mt-4 text-slate-500">Loading assembly... {loadProgress}%</p>
        </div>
      )}

      {/* Progress bar */}
      <div
        className="fixed top-0 left-0 h-1 bg-gradient-to-r from-cyan-400 to-emerald-400 z-50 transition-all duration-100"
        style={{ width: `${scrollProgress * 100}%` }}
      />

      {/* Animation container */}
      <div
        ref={containerRef}
        className="relative"
        style={{ height: `${scrollMultiplier * 100}vh` }}
      >
        <div className="sticky top-0 h-screen flex items-center justify-center overflow-hidden">
          <canvas
            ref={canvasRef}
            className="w-full max-w-5xl aspect-video"
          />

          {/* Component labels */}
          {COMPONENT_LABELS.map((label) => {
            const isVisible = scrollProgress >= label.visibleRange.start &&
                             scrollProgress <= label.visibleRange.end;
            return (
              <div
                key={label.id}
                className={`
                  absolute px-3 py-2 rounded-lg text-sm
                  bg-cyan-500/10 border border-cyan-500/30 text-cyan-400
                  transition-all duration-300 pointer-events-none
                  ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'}
                `}
                style={label.position}
              >
                {label.text}
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}
