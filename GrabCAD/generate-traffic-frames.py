"""
SwanFlow Traffic Animation Frame Generator
Generates 120 frames of road cross-section with animated traffic flow
Uses actual Perth road waypoint data from the dashboard
"""

from PIL import Image, ImageDraw
import math
from pathlib import Path

# Configuration
WIDTH = 1920
HEIGHT = 1080
FRAME_COUNT = 120
OUTPUT_DIR = Path(__file__).parent / "frames-traffic"

# Traffic colors (from dashboard getTrafficColor function)
TRAFFIC_COLORS = {
    'flowing': (16, 185, 129),     # Green - speed >= 50 km/h
    'moderate': (245, 158, 11),    # Orange - speed >= 30 km/h
    'heavy': (239, 68, 68),        # Red - speed >= 15 km/h
    'gridlock': (153, 27, 27)      # Dark red - speed < 15 km/h
}

# Road waypoints (from dashboard corridorWaypoints - using key corridors)
CORRIDOR_WAYPOINTS = {
    'Mounts Bay Rd': [
        [-31.9755360, 115.8180240], [-31.9733899, 115.8256410], [-31.9728911, 115.8265899],
        [-31.9726546, 115.8274435], [-31.9724305, 115.8289419], [-31.9722547, 115.8308715],
        [-31.9719219, 115.8321438], [-31.9715072, 115.8331964], [-31.9710934, 115.8336485],
        [-31.9704117, 115.8340935], [-31.9701018, 115.8345177], [-31.9696950, 115.8357989],
        [-31.9693711, 115.8365875], [-31.9689912, 115.8371631], [-31.9684943, 115.8377125],
        [-31.9678280, 115.8383774], [-31.9668462, 115.8390952], [-31.9662305, 115.8395033],
        [-31.9653717, 115.8398791]
    ],
    'Stirling Hwy': [
        [-31.9820, 115.7900], [-31.9834402, 115.7802709], [-31.9850921, 115.7755445],
        [-31.9870, 115.7720], [-31.9890887, 115.7685801], [-31.9910607, 115.7675329],
        [-31.9925, 115.7665], [-31.993, 115.766], [-31.994, 115.765]
    ],
    'Mitchell Fwy': [
        [-31.9617537, 115.8474375], [-31.9600697, 115.8474955], [-31.9586325, 115.8490672],
        [-31.9569363, 115.8494396], [-31.9553135, 115.8494540], [-31.9544093, 115.8488992],
        [-31.9527661, 115.8483345], [-31.9508178, 115.8490068], [-31.9493950, 115.8496822],
        [-31.9477915, 115.8501012], [-31.9460202, 115.8498387], [-31.9440531, 115.8485092],
        [-31.9412033, 115.8439939], [-31.9396551, 115.8405922], [-31.9379469, 115.8389929],
        [-31.9307069, 115.8350879], [-31.9261945, 115.8302721], [-31.9236279, 115.8269383],
        [-31.9194459, 115.8240925], [-31.9144881, 115.8233710], [-31.9106849, 115.8224215],
        [-31.9017170, 115.8208361], [-31.8990018, 115.8175891]
    ]
}

def calculate_bounds():
    """Calculate projection bounds for all corridors."""
    min_lat = min_lng = float('inf')
    max_lat = max_lng = float('-inf')

    for waypoints in CORRIDOR_WAYPOINTS.values():
        for lat, lng in waypoints:
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            min_lng = min(min_lng, lng)
            max_lng = max(max_lng, lng)

    # Add 10% padding
    lat_padding = (max_lat - min_lat) * 0.1
    lng_padding = (max_lng - min_lng) * 0.1

    min_lat -= lat_padding
    max_lat += lat_padding
    min_lng -= lng_padding
    max_lng += lng_padding

    return {
        'min_lat': min_lat,
        'max_lat': max_lat,
        'min_lng': min_lng,
        'max_lng': max_lng,
        'min_merc_n': math.log(math.tan((math.pi / 4) + (min_lat * math.pi / 180 / 2))),
        'max_merc_n': math.log(math.tan((math.pi / 4) + (max_lat * math.pi / 180 / 2)))
    }

def lat_lng_to_screen(lat, lng, bounds):
    """Mercator projection for lat/lng to screen coordinates."""
    x = (lng - bounds['min_lng']) / (bounds['max_lng'] - bounds['min_lng'])
    lat_rad = lat * math.pi / 180
    merc_n = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    y = (merc_n - bounds['min_merc_n']) / (bounds['max_merc_n'] - bounds['min_merc_n'])

    return (int(x * WIDTH), int((1 - y) * HEIGHT))

def draw_road_layer(draw, bounds, opacity=255):
    """Draw road asphalt base layer."""
    for name, waypoints in CORRIDOR_WAYPOINTS.items():
        if len(waypoints) < 2:
            continue

        screen_points = [lat_lng_to_screen(lat, lng, bounds) for lat, lng in waypoints]

        # Draw thick gray road base
        color = (31, 41, 55, opacity)
        draw.line(screen_points, fill=color, width=24, joint='curve')

def draw_lane_markings(draw, bounds, opacity=255):
    """Draw white lane markings."""
    for name, waypoints in CORRIDOR_WAYPOINTS.items():
        if len(waypoints) < 2:
            continue

        screen_points = [lat_lng_to_screen(lat, lng, bounds) for lat, lng in waypoints]

        # Draw dashed white center line
        color = (255, 255, 255, opacity)

        # Draw dashed line manually
        for i in range(len(screen_points) - 1):
            x1, y1 = screen_points[i]
            x2, y2 = screen_points[i + 1]

            # Calculate segment length and angle
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx * dx + dy * dy)

            if length == 0:
                continue

            # Normalize
            dx /= length
            dy /= length

            # Draw dashes along segment
            dash_length = 20
            gap_length = 15
            total_dash = dash_length + gap_length

            distance = 0
            while distance < length:
                dash_end = min(distance + dash_length, length)

                start_x = int(x1 + dx * distance)
                start_y = int(y1 + dy * distance)
                end_x = int(x1 + dx * dash_end)
                end_y = int(y1 + dy * dash_end)

                draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=2)
                distance += total_dash

def draw_grid(draw, opacity=255):
    """Draw blue grid overlay."""
    alpha = int(opacity * 0.15)
    color = (59, 130, 246, alpha)

    # Vertical lines
    for x in range(0, WIDTH, 100):
        draw.line([(x, 0), (x, HEIGHT)], fill=color, width=1)

    # Horizontal lines
    for y in range(0, HEIGHT, 100):
        draw.line([(0, y), (WIDTH, y)], fill=color, width=1)

def draw_traffic_flow(draw, bounds, frame_progress, opacity=255):
    """Draw animated traffic flow lines."""
    colors = [
        TRAFFIC_COLORS['flowing'],
        TRAFFIC_COLORS['moderate'],
        TRAFFIC_COLORS['heavy']
    ]

    for corridor_idx, (name, waypoints) in enumerate(CORRIDOR_WAYPOINTS.items()):
        if len(waypoints) < 2:
            continue

        screen_points = [lat_lng_to_screen(lat, lng, bounds) for lat, lng in waypoints]
        color = colors[corridor_idx % len(colors)]

        # Draw two parallel lines (NB and SB lanes)
        for direction in [1, -1]:
            # Calculate perpendicular offset
            offset_points = []
            for i, (x, y) in enumerate(screen_points):
                if i == 0:
                    offset_points.append((x, y))
                    continue

                prev_x, prev_y = screen_points[i - 1]
                dx = x - prev_x
                dy = y - prev_y
                length = math.sqrt(dx * dx + dy * dy)

                if length == 0:
                    offset_points.append((x, y))
                    continue

                # Perpendicular offset (5px)
                perp_x = -dy / length * 5 * direction
                perp_y = dx / length * 5 * direction
                offset_points.append((int(x + perp_x), int(y + perp_y)))

            # Background solid line
            bg_color = (*color, int(opacity * 0.3))
            draw.line(offset_points, fill=bg_color, width=5, joint='curve')

            # Animated dashed line
            dash_color = (*color, int(opacity * 0.9))

            # Draw animated dashes
            for i in range(len(offset_points) - 1):
                x1, y1 = offset_points[i]
                x2, y2 = offset_points[i + 1]

                dx = x2 - x1
                dy = y2 - y1
                length = math.sqrt(dx * dx + dy * dy)

                if length == 0:
                    continue

                dx /= length
                dy /= length

                # Animate dash offset
                dash_offset = (frame_progress * 20 * direction) % 20
                dash_length = 8
                gap_length = 12
                total_dash = dash_length + gap_length

                distance = -dash_offset
                while distance < length:
                    if distance >= 0:
                        dash_end = min(distance + dash_length, length)

                        start_x = int(x1 + dx * distance)
                        start_y = int(y1 + dy * distance)
                        end_x = int(x1 + dx * dash_end)
                        end_y = int(y1 + dy * dash_end)

                        draw.line([(start_x, start_y), (end_x, end_y)], fill=dash_color, width=4)

                    distance += total_dash

def generate_frame(frame_num, bounds):
    """Generate a single frame."""
    img = Image.new('RGBA', (WIDTH, HEIGHT), (10, 15, 30, 255))
    draw = ImageDraw.Draw(img)

    progress = frame_num / FRAME_COUNT

    # Frame 0-30: Road layer fades in
    if frame_num < 30:
        road_opacity = int((frame_num / 30) * 255)
        draw_road_layer(draw, bounds, road_opacity)

    # Frame 30-60: Lane markings appear
    elif frame_num < 60:
        draw_road_layer(draw, bounds, 255)
        lane_opacity = int(((frame_num - 30) / 30) * 255)
        draw_lane_markings(draw, bounds, lane_opacity)

    # Frame 60-90: Grid overlay fades in
    elif frame_num < 90:
        draw_road_layer(draw, bounds, 255)
        draw_lane_markings(draw, bounds, 255)
        grid_opacity = int(((frame_num - 60) / 30) * 255)
        draw_grid(draw, grid_opacity)

    # Frame 90-120: Traffic flow lines animate in
    else:
        draw_road_layer(draw, bounds, 255)
        draw_lane_markings(draw, bounds, 255)
        draw_grid(draw, 255)
        traffic_opacity = int(((frame_num - 90) / 30) * 255)
        draw_traffic_flow(draw, bounds, progress, traffic_opacity)

    return img

def main():
    print('\n' + '=' * 70)
    print('SwanFlow Traffic Animation Frame Generator')
    print('=' * 70)
    print(f'Generating {FRAME_COUNT} frames at {WIDTH}x{HEIGHT}...')
    print(f'Output: {OUTPUT_DIR}/')
    print('')

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Calculate projection bounds
    bounds = calculate_bounds()
    print('Map bounds calculated:')
    print(f'  Latitude: {bounds["min_lat"]:.4f} to {bounds["max_lat"]:.4f}')
    print(f'  Longitude: {bounds["min_lng"]:.4f} to {bounds["max_lng"]:.4f}')
    print('')

    # Generate frames
    import time
    start_time = time.time()

    for i in range(FRAME_COUNT):
        img = generate_frame(i, bounds)
        filename = f'assembly_{i:04d}.png'
        filepath = OUTPUT_DIR / filename

        img.save(filepath, 'PNG')

        # Progress indicator
        if (i + 1) % 10 == 0 or i == 0 or i == FRAME_COUNT - 1:
            elapsed = time.time() - start_time
            percent = (i + 1) / FRAME_COUNT * 100
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f'  [{percent:.0f}%] Frame {i + 1}/{FRAME_COUNT} - {size_mb:.2f}MB - {elapsed:.1f}s elapsed')

    total_time = time.time() - start_time

    # Calculate total size
    total_size = sum(f.stat().st_size for f in OUTPUT_DIR.glob('*.png'))
    total_mb = total_size / (1024 * 1024)

    print('')
    print('=' * 70)
    print(f'[OK] Completed in {total_time:.1f}s')
    print(f'Total size: {total_mb:.1f}MB ({FRAME_COUNT} frames)')
    print('')
    print('Next steps:')
    print('  1. Copy frames to scroll-animation directory:')
    print('     robocopy frames-traffic scroll-animation\\frames-traffic /E')
    print('')
    print('  2. Update index.html framePath:')
    print('     framePath: "frames-traffic/assembly_"')
    print('')
    print('  3. View animation:')
    print('     http://localhost:8081')
    print('=' * 70)

if __name__ == '__main__':
    main()
