"""Simple ASCII visualization of stars and paths."""
from star_rotation_v2 import find_intersections, get_star_reachable_points

def visualize_grid(lines, source, destination, star_centers=None, reachable_points=None):
    """Create a simple ASCII visualization of the problem."""
    
    # Find bounds
    all_points = []
    for (x1, y1), (x2, y2) in lines:
        all_points.extend([(x1, y1), (x2, y2)])
    all_points.extend([source, destination])
    
    if not all_points:
        return
    
    min_x = int(min(p[0] for p in all_points)) - 1
    max_x = int(max(p[0] for p in all_points)) + 1
    min_y = int(min(p[1] for p in all_points)) - 1
    max_y = int(max(p[1] for p in all_points)) + 1
    
    # Create grid
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    
    if width > 50 or height > 50:
        print("Grid too large to visualize (>50x50)")
        return
    
    grid = [['.' for _ in range(width)] for _ in range(height)]
    
    # Mark line segments
    for (x1, y1), (x2, y2) in lines:
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steps = max(dx, dy)
        
        if steps == 0:
            continue
        
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            
            gx = x - min_x
            gy = max_y - y
            
            if 0 <= gx < width and 0 <= gy < height:
                if grid[gy][gx] == '.':
                    # Determine line character
                    if dx == 0:
                        grid[gy][gx] = '|'
                    elif dy == 0:
                        grid[gy][gx] = '-'
                    elif (x2 - x1) * (y2 - y1) > 0:
                        grid[gy][gx] = '\\'
                    else:
                        grid[gy][gx] = '/'
                elif grid[gy][gx] in '|-\\/':
                    grid[gy][gx] = '+'
    
    # Mark star centers
    if star_centers:
        for center in star_centers:
            cx, cy = int(center[0]), int(center[1])
            gx = cx - min_x
            gy = max_y - cy
            if 0 <= gx < width and 0 <= gy < height:
                grid[gy][gx] = '*'
    
    # Mark reachable points (if provided)
    if reachable_points:
        for point in reachable_points:
            px, py = int(point[0]), int(point[1])
            gx = px - min_x
            gy = max_y - py
            if 0 <= gx < width and 0 <= gy < height:
                if grid[gy][gx] == '.':
                    grid[gy][gx] = '·'
    
    # Mark source and destination
    sx, sy = int(source[0]), int(source[1])
    dx, dy = int(destination[0]), int(destination[1])
    
    sgx = sx - min_x
    sgy = max_y - sy
    dgx = dx - min_x
    dgy = max_y - dy
    
    if 0 <= sgx < width and 0 <= sgy < height:
        grid[sgy][sgx] = 'S'
    
    if 0 <= dgx < width and 0 <= dgy < height:
        grid[dgy][dgx] = 'D'
    
    # Print grid
    print(f"\nGrid ({min_x},{min_y}) to ({max_x},{max_y}):")
    print("Legend: S=Source, D=Destination, *=Star Center, |/-\\=Lines, ·=Reachable")
    print()
    
    # Print column numbers
    print("   ", end="")
    for x in range(min_x, max_x + 1):
        print(f"{x%10}", end="")
    print()
    
    # Print grid with row numbers
    for y in range(max_y, min_y - 1, -1):
        gy = max_y - y
        print(f"{y:2} ", end="")
        for gx in range(width):
            print(grid[gy][gx], end="")
        print()
    print()

def analyze_test_case(test_num, lines, source, destination):
    """Analyze and visualize a test case."""
    print(f"\n{'='*70}")
    print(f"TEST CASE {test_num}")
    print(f"{'='*70}")
    
    print(f"\nSource: {source}")
    print(f"Destination: {destination}")
    print(f"Number of line segments: {len(lines)}")
    
    # Find stars
    centers_data = find_intersections(lines)
    print(f"\nNumber of stars: {len(centers_data)}")
    
    star_reachable = {}
    for i, (center, line_indices) in enumerate(centers_data.items(), 1):
        reachable = get_star_reachable_points(center, lines, line_indices)
        star_reachable[center] = reachable
        print(f"  Star {i}: Center {center}, {len(line_indices)} lines, {len(reachable)} reachable points")
    
    # Visualize
    visualize_grid(lines, source, destination, centers_data.keys())
    
    # Check source and destination
    source_on_stars = [c for c, pts in star_reachable.items() if source in pts]
    dest_on_stars = [c for c, pts in star_reachable.items() if destination in pts]
    
    print(f"Source on {len(source_on_stars)} star(s): {source_on_stars}")
    print(f"Destination on {len(dest_on_stars)} star(s): {dest_on_stars}")
    
    return centers_data, star_reachable

if __name__ == "__main__":
    # Test 1
    lines1 = [
        ((1, 1), (3, 3)),
        ((2, 1), (2, 4)),
        ((1, 3), (3, 1)),
        ((4, 2), (10, 8)),
        ((5, 5), (7, 3)),
        ((1, 5), (1, 8)),
        ((1, 8), (2, 7)),
        ((1, 8), (2, 9))
    ]
    analyze_test_case(1, lines1, (2, 3), (2, 9))
    
    # Test 2
    lines2 = [
        ((2, 2), (3, 3)),
        ((8, 3), (8, 7)),
        ((4, 2), (3, 3)),
        ((8, 4), (7, 5)),
        ((3, 4), (3, 3)),
        ((8, 4), (9, 5))
    ]
    analyze_test_case(2, lines2, (8, 6), (8, 1))
    
    # Test 3
    analyze_test_case(3, lines2, (8, 6), (5, 5))
