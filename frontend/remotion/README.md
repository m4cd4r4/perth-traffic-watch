# SwanFlow Remotion Animations

This directory contains Remotion video compositions for SwanFlow animated content.

## What's Inside

### Compositions

1. **SwanLogo** (`src/SwanLogo.tsx`)
   - Animated swan logo reveal with sequential element animations
   - Duration: 3 seconds (180 frames @ 60fps)
   - Resolution: 800x640
   - Elements animate in order: body → neck → head → beak → eye → water drop → legs → shadow → text

## Getting Started

### Preview

```bash
npm start
# or
npx remotion preview
```

This opens the Remotion Studio at [http://localhost:3000](http://localhost:3000) where you can:
- Preview all compositions
- Adjust timing and parameters
- Export frames or videos

### Render

```bash
# Render SwanLogo composition to MP4
npx remotion render SwanLogo output/swan-logo.mp4

# Render with custom settings
npx remotion render SwanLogo output/swan-logo.mp4 --codec=h264 --crf=18
```

## Project Structure

```
remotion/
├── src/
│   ├── index.ts          # Entry point
│   ├── Root.tsx          # Composition registry
│   ├── SwanLogo.tsx      # Swan logo animation
│   ├── MapZoom.tsx       # Map zoom sequence (coming soon)
│   ├── FlowLines.tsx     # Traffic flow animation (coming soon)
│   └── HeroVideo.tsx     # Main hero composition (coming soon)
├── output/               # Rendered videos go here
├── package.json
├── remotion.config.ts    # Remotion configuration
└── tsconfig.json
```

## Color Palette

- Background: `#0a1828` (dark blue)
- Swan Color: `#e8f1f5` (light blue-white)
- Accent: `#4A7C82` (teal - beak, legs, water drop)
- Dark Accent: `#1a3a3f` (eye)

## Animation Timing

| Element | Start Frame | Duration | Special Effect |
|---------|-------------|----------|----------------|
| Body | 20 | 20 | Scale spring |
| Neck | 35 | 20 | Scale spring |
| Head | 50 | 20 | Scale spring |
| Beak | 65 | 20 | Scale spring |
| Eye | 75 | 20 | Fade only |
| Water Drop | 85 | 30 | Fade + drop motion |
| Legs | 95 | 20 | Scale spring |
| Shadow | 105 | 20 | Fade only |
| Text | 120 | 30 | Fade + slide up |

## Next Compositions

- [ ] Map zoom sequence (Perth overview → Stirling Highway)
- [ ] Traffic flow lines animation
- [ ] Combined hero video for landing page
- [ ] Social media clips (15-30 sec variants)

## Resources

- [Remotion Documentation](https://www.remotion.dev/docs)
- [SwanFlow Project](../README.md)
