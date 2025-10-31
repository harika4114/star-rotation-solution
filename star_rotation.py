from collections import defaultdict, deque
from math import gcd

def find_intersections(lines):
    """Find all intersection points where 2+ lines meet (star centers)."""
    intersections = defaultdict(list)
    
    for i, line in enumerate(lines):
        for j, other_line in enumerate(lines):
            if i >= j:
                continue
            
            point = line_intersection(line, other_line)
            if point:
                intersections[point].append(i)
                intersections[point].append(j)
    
    # Return centers where at least 2 lines meet
    centers = {}
    for point, line_indices in intersections.items():
        unique_lines = list(set(line_indices))
        if len(unique_lines) >= 2:
            centers[point] = unique_lines
    
    return centers

def line_intersection(line1, line2):
    """Find intersection point of two line segments."""
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if abs(denom) < 1e-9:
        return None
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    
    # Check if intersection is within both line segments
    if -1e-9 <= t <= 1 + 1e-9 and -1e-9 <= u <= 1 + 1e-9:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        # Round to handle floating point errors
        return (round(ix, 8), round(iy, 8))
    
    return None

def get_integer_points_on_segment(p1, p2):
    """Get all integer coordinate points on a line segment."""
    x1, y1 = p1
    x2, y2 = p2
    
    points = set()
    dx = x2 - x1
    dy = y2 - y1
    
    # Number of steps is the GCD of dx and dy
    steps = gcd(int(abs(dx)), int(abs(dy))) if dx != 0 or dy != 0 else 0
    
    if steps == 0:
        if abs(x1 - round(x1)) < 1e-6 and abs(y1 - round(y1)) < 1e-6:
            points.add((int(round(x1)), int(round(y1))))
        return points
    
    step_x = dx / steps
    step_y = dy / steps
    
    for i in range(steps + 1):
        px = x1 + i * step_x
        py = y1 + i * step_y
        
        # Check if it's close to an integer point
        if abs(px - round(px)) < 1e-6 and abs(py - round(py)) < 1e-6:
            points.add((int(round(px)), int(round(py))))
    
    return points

def rotate_point_90_clockwise(center, point):
    """Rotate a point 90 degrees clockwise around a center."""
    cx, cy = center
    px, py = point
    
    # Translate to origin
    dx = px - cx
    dy = py - cy
    
    # Rotate: (x, y) -> (y, -x)
    new_dx = dy
    new_dy = -dx
    
    # Translate back
    return (cx + new_dx, cy + new_dy)

def get_star_reachable_points(center, lines, line_indices):
    """Get all points reachable by a star through any rotation."""
    # Get the line segments that form this star
    star_lines = [lines[i] for i in line_indices]
    
    all_reachable = set()
    
    # For each of 4 rotations (0, 90, 180, 270 degrees)
    for rotation in range(4):
        # Rotate each line segment
        rotated_lines = []
        for line in star_lines:
            p1, p2 = line
            # Rotate both endpoints
            for _ in range(rotation):
                p1 = rotate_point_90_clockwise(center, p1)
                p2 = rotate_point_90_clockwise(center, p2)
            rotated_lines.append((p1, p2))
        
        # Get all integer points on rotated lines
        for p1, p2 in rotated_lines:
            points = get_integer_points_on_segment(p1, p2)
            all_reachable.update(points)
    
    return all_reachable

def chebyshev_distance(p1, p2):
    """Chebyshev distance (max of absolute differences)."""
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))

def solve(lines, source, destination):
    """Find minimum stars needed or minimum shift distance."""
    
    # Find all star centers
    centers_data = find_intersections(lines)
    
    if not centers_data:
        # No stars found
        return chebyshev_distance(source, destination)
    
    # Build mapping: center -> all reachable points
    star_reachable = {}
    for center, line_indices in centers_data.items():
        reachable = get_star_reachable_points(center, lines, line_indices)
        if reachable:
            star_reachable[center] = reachable
    
    # Find stars that contain the source
    source_stars = [center for center, points in star_reachable.items() if source in points]
    
    if not source_stars:
        # Source not on any star
        return chebyshev_distance(source, destination)
    
    # Check if destination is on a source star
    for star in source_stars:
        if destination in star_reachable[star]:
            return 1
    
    # BFS to find shortest path
    queue = deque()
    visited = set()
    
    for star in source_stars:
        queue.append((star, 1))
        visited.add(star)
    
    while queue:
        current_star, star_count = queue.popleft()
        current_reachable = star_reachable[current_star]
        
        # Try to reach other stars
        for other_star, other_reachable in star_reachable.items():
            if other_star in visited:
                continue
            
            # Check if current star can touch other star
            if current_reachable & other_reachable:
                # Check if destination is on this star
                if destination in other_reachable:
                    return star_count + 1
                
                visited.add(other_star)
                queue.append((other_star, star_count + 1))
    
    # Destination unreachable - find minimum shift
    min_dist = float('inf')
    for star in visited:
        for point in star_reachable[star]:
            dist = chebyshev_distance(point, destination)
            min_dist = min(min_dist, dist)
    
    return min_dist if min_dist != float('inf') else chebyshev_distance(source, destination)

def main():
    n = int(input())
    lines = []
    
    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        lines.append(((x1, y1), (x2, y2)))
    
    src_x, src_y = map(int, input().split())
    dest_x, dest_y = map(int, input().split())
    
    result = solve(lines, (src_x, src_y), (dest_x, dest_y))
    print(result)

if __name__ == "__main__":
    main()
