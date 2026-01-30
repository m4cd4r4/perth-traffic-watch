# SwanFlow Hero Section: Spline Assembly Animation Guide

Create a scroll-driven "exploded view" animation showing the SwanFlow hardware assembling as users scroll.

## Quick Start

1. **Open Spline**: [spline.design](https://spline.design/) (free account)
2. **Create new project**: File → New
3. **Follow sections below** to model, animate, and embed

---

## Part 1: Components to Model

### Priority Components (Hero Animation)

| Component | Shape in Spline | Colour | Notes |
|-----------|-----------------|--------|-------|
| **ESP32-CAM board** | Rounded box (25×25×5mm) | Green PCB (#1a5c1a) | Add gold connector pins |
| **OV2640 Camera** | Small cylinder + cube | Black lens, gold ribbon | Plugs into ESP32 |
| **Junction Box** | Rounded box (150×100×60mm) | Grey (#4a4a4a) | IP65 enclosure |
| **SIM7000A Module** | Flat rectangle (30×25×3mm) | Blue PCB (#1a3c5c) | 4G antenna connector |
| **Solar Panel** | Flat rectangle (350×250×20mm) | Dark blue (#1a2a4a) | Grid lines texture |
| **12V Battery** | Cylinder or box | Black with red/black terminals | |
| **MicroSD Card** | Tiny rectangle | Black/blue | Optional detail |

### Simplified Approach (Recommended for MVP)

Just model these 4 key parts:
1. **Camera module** (small black cylinder)
2. **ESP32 board** (green rectangle with gold pins)
3. **Junction box** (grey box with lid)
4. **Solar panel** (dark rectangle)

---

## Part 2: Modelling in Spline

### Step 1: Create the ESP32-CAM

```
1. Press "+" → Shape → Rounded Box
2. Set dimensions: 25 × 25 × 5
3. Set color: #1a5c1a (PCB green)
4. Add material: Matte
5. Name it: "ESP32-Board"

For the camera connector:
1. Add small cylinder (5 × 5 × 2)
2. Color: Gold (#d4af37)
3. Position on edge of board
4. Group together: "ESP32-CAM"
```

### Step 2: Create the OV2640 Camera

```
1. Rounded box: 8 × 8 × 6 (camera body)
2. Cylinder on front: 4 × 4 × 2 (lens)
3. Thin rectangle: 15 × 5 × 0.5 (ribbon cable)
4. Colors: Black body, dark glass lens
5. Group: "Camera-Module"
```

### Step 3: Create the Junction Box

```
1. Rounded box: 150 × 100 × 50 (base)
2. Color: #4a4a4a (grey)
3. Duplicate for lid: 150 × 100 × 10
4. Name: "JunctionBox-Base" and "JunctionBox-Lid"
```

### Step 4: Create the Solar Panel

```
1. Rounded box: 200 × 150 × 15
2. Color: #1a2a4a (dark blue)
3. Add grid lines with thin rectangles (optional)
4. Name: "Solar-Panel"
```

---

## Part 3: Setting Up the Assembly Animation

### Concept: Exploded → Assembled States

| Scroll Position | What Happens |
|-----------------|--------------|
| 0% (top) | All parts exploded/floating apart |
| 25% | Camera connects to ESP32 |
| 50% | ESP32+Camera enters junction box |
| 75% | Junction box lid closes |
| 100% | Solar panel connects, fully assembled |

### Step-by-Step Animation Setup

#### 1. Position Parts in "Exploded" State

```
Camera-Module:      Y: +100, Z: +50
ESP32-CAM:          Y: +50
JunctionBox-Lid:    Y: +80, Rotation X: 45°
JunctionBox-Base:   Y: 0 (anchor point)
Solar-Panel:        Y: -100, Z: -50
```

#### 2. Create States in Spline

```
1. Select all objects
2. Right panel → States
3. Click "+" to add state
4. Name it: "Exploded"
5. This saves current positions

6. Now move all parts to ASSEMBLED positions:
   - Camera snaps onto ESP32
   - ESP32 sits inside junction box
   - Lid closes (Rotation X: 0°)
   - Solar panel connects

7. Add new state: "Assembled"
```

#### 3. Add Scroll Trigger

```
1. Click "Events" (lightning bolt icon)
2. Add Event → Scroll
3. Set:
   - Start: "Exploded" state
   - End: "Assembled" state
   - Easing: Ease In Out
4. This creates scroll-driven interpolation!
```

---

## Part 4: Camera Setup for Hero Section

### Recommended Camera Settings

```
Camera Type: Perspective
FOV: 45°
Position: Z: 300 (pulled back to see all parts)

For scroll animation:
- Camera can also animate (zoom in as assembly completes)
- Add camera position to your states
```

### Lighting Setup

```
1. Add Environment Light (soft overall)
2. Add Directional Light:
   - Position: Above and to the right
   - Intensity: 1.5
   - Soft shadows: On
3. Optional: Add subtle rim light from behind
```

---

## Part 5: Export & Embed

### Option A: Iframe Embed (Simplest)

```html
<!-- In your HTML hero section -->
<div class="hero-3d">
  <iframe
    src="https://my.spline.design/YOUR-SCENE-ID/"
    frameborder="0"
    width="100%"
    height="600px"
    style="pointer-events: auto;"
  ></iframe>
</div>
```

### Option B: Spline React Component

```bash
npm install @splinetool/react-spline
```

```jsx
// components/HeroAssembly.jsx
import Spline from '@splinetool/react-spline';

export default function HeroAssembly() {
  return (
    <div className="hero-section" style={{ height: '100vh' }}>
      <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
    </div>
  );
}
```

### Option C: Vanilla JS Runtime

```bash
npm install @splinetool/runtime
```

```javascript
import { Application } from '@splinetool/runtime';

const canvas = document.getElementById('canvas3d');
const app = new Application(canvas);
app.load('https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode');
```

---

## Part 6: Scroll Integration with Your Site

### Method 1: Spline's Built-in Scroll (Recommended)

Spline handles scroll natively when you add a Scroll event. The iframe will respond to page scroll automatically.

### Method 2: Control from JavaScript

```javascript
import { Application } from '@splinetool/runtime';

const app = new Application(canvas);
await app.load('YOUR-SCENE-URL');

// Listen to scroll and control Spline
window.addEventListener('scroll', () => {
  const progress = window.scrollY / (document.body.scrollHeight - window.innerHeight);

  // Trigger Spline events or control variables
  app.setVariable('scrollProgress', progress);
});
```

### Method 3: GSAP ScrollTrigger + Spline Variables

```javascript
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Assuming you've exposed a "progress" variable in Spline
ScrollTrigger.create({
  trigger: ".hero-section",
  start: "top top",
  end: "bottom bottom",
  scrub: true,
  onUpdate: (self) => {
    splineApp.setVariable('assemblyProgress', self.progress);
  }
});
```

---

## Part 7: SwanFlow-Specific Styling

### Match the Cottesloe Theme

```css
.hero-section {
  background: linear-gradient(135deg, #0a1628 0%, #1a3a5c 100%);
  position: relative;
  height: 200vh; /* Gives scroll room for animation */
}

.hero-3d {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-text {
  position: absolute;
  z-index: 10;
  color: white;
  text-align: center;
}
```

### Assembly Labels (Optional)

Add floating labels that appear as each component assembles:

```jsx
<div className="component-label" style={{ opacity: scrollProgress > 0.25 ? 1 : 0 }}>
  <span className="label">ESP32-CAM</span>
  <span className="price">$12</span>
</div>
```

---

## Quick Reference: Spline Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Add shape | `+` or `Shift+A` |
| Duplicate | `Cmd/Ctrl+D` |
| Group | `Cmd/Ctrl+G` |
| Toggle wireframe | `Z` |
| Reset camera | `Numpad 0` |
| Play animation | `Space` |
| Export | `Cmd/Ctrl+E` |

---

## Resources

- **Spline**: [spline.design](https://spline.design/)
- **Spline Docs**: [docs.spline.design](https://docs.spline.design/)
- **ESP32-CAM 3D Models**: [GrabCAD ESP32](https://grabcad.com/library?query=esp32)
- **Spline + Scroll Tutorial**: [YouTube](https://www.youtube.com/results?search_query=spline+scroll+animation)
- **Spline React Package**: [@splinetool/react-spline](https://www.npmjs.com/package/@splinetool/react-spline)

---

## Next Steps

1. [ ] Create Spline account at [spline.design](https://spline.design/)
2. [ ] Model the 4 key components (ESP32, camera, box, panel)
3. [ ] Set up Exploded and Assembled states
4. [ ] Add Scroll event trigger
5. [ ] Export and embed in SwanFlow frontend
6. [ ] Test scroll behaviour on desktop and mobile

---

*Created for SwanFlow - Open-source traffic monitoring for Perth, WA*
