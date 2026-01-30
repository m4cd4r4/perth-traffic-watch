# SwanFlow Scroll-Driven Assembly Animation

Apple-style scroll animation showing SwanFlow hardware assembly. As users scroll, components animate from exploded view to assembled position.

## Files

| File | Description |
|------|-------------|
| `index.html` | Standalone demo with vanilla JS + GSAP |
| `AssemblyAnimation.tsx` | React/Next.js component |
| `optimize-frames.py` | Compress frames for web (PNG/WebP) |

## Quick Start

### Option 1: Standalone Demo

1. Start a local server in this directory:
   ```bash
   python -m http.server 8080
   # or
   npx serve .
   ```

2. Open http://localhost:8080

### Option 2: React/Next.js Integration

1. Install GSAP:
   ```bash
   npm install gsap
   ```

2. Copy the component:
   ```bash
   cp AssemblyAnimation.tsx your-project/components/
   ```

3. Copy frames to public folder:
   ```bash
   # Use optimized WebP frames for best performance
   cp -r frames-webp your-project/public/assembly/
   ```

4. Use in your page:
   ```tsx
   import AssemblyAnimation from '@/components/AssemblyAnimation';

   export default function HomePage() {
     return (
       <>
         <HeroSection />
         <AssemblyAnimation
           framePath="/assembly/assembly_"
           frameExtension=".webp"
           frameCount={120}
         />
         <ContentSection />
       </>
     );
   }
   ```

## Optimizing Frames

The raw frames are ~1.5MB each (180MB total). For production, optimize them:

```bash
pip install pillow
python optimize-frames.py
```

This creates:
- `frames-optimized/` - Compressed PNG (~200-400KB each)
- `frames-webp/` - WebP format (~100-200KB each, recommended)

## Configuration

### Frame Path

Update the frame path based on where you host the images:

```javascript
// Local development
framePath: '../frames-photorealistic/assembly_'

// Production (Next.js public folder)
framePath: '/assembly/assembly_'

// CDN
framePath: 'https://cdn.example.com/swanflow/assembly_'
```

### Scroll Duration

Adjust `scrollMultiplier` to control how much scrolling is needed:

```tsx
<AssemblyAnimation
  scrollMultiplier={4}  // 400vh (default)
  // scrollMultiplier={6}  // 600vh (slower animation)
  // scrollMultiplier={3}  // 300vh (faster animation)
/>
```

### Component Labels

Labels appear at specific scroll percentages. Edit `COMPONENT_LABELS` in the component to customize:

```typescript
const COMPONENT_LABELS = [
  {
    id: 'esp32',
    text: 'ESP32-CAM',
    position: { top: '30%', left: '60%' },
    visibleRange: { start: 0.05, end: 0.20 }  // Visible 5-20% scroll
  },
  // ...
];
```

## Browser Support

- Chrome 64+
- Firefox 59+
- Safari 12+
- Edge 79+

WebP is supported in all modern browsers. For older browsers, fall back to PNG:

```javascript
const supportsWebP = document.createElement('canvas')
  .toDataURL('image/webp')
  .indexOf('data:image/webp') === 0;

const frameExtension = supportsWebP ? '.webp' : '.png';
```

## Performance Tips

1. **Use WebP format** - 60-80% smaller than PNG
2. **Lazy load** - Only load frames when section is near viewport
3. **Progressive loading** - Show low-res first frame immediately
4. **CDN hosting** - Use a CDN for faster global delivery
5. **Preconnect** - Add `<link rel="preconnect">` for CDN domain

## Frame Details

| Property | Value |
|----------|-------|
| Total frames | 120 |
| Resolution | 1920 x 1080 |
| Format | PNG (transparent background) |
| Duration | ~4 seconds at 30fps |

## Credits

- **3D Models**: GrabCAD Community
- **Rendering**: Blender Cycles (GPU accelerated)
- **Animation**: GSAP ScrollTrigger
