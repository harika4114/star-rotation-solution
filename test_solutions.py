import sys
import io

# Import the solution
from star_rotation_v2 import solve

def test_case(test_num, lines, source, destination, expected):
    """Test a single case."""
    result = solve(lines, source, destination)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    print(f"Test {test_num}: Expected {expected}, Got {result} - {status}")
    return result == expected

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
source1 = (2, 3)
dest1 = (2, 9)
expected1 = 3

# Test 2
lines2 = [
    ((2, 2), (3, 3)),
    ((8, 3), (8, 7)),
    ((4, 2), (3, 3)),
    ((8, 4), (7, 5)),
    ((3, 4), (3, 3)),
    ((8, 4), (9, 5))
]
source2 = (8, 6)
dest2 = (8, 1)
expected2 = 1

# Test 3
lines3 = lines2.copy()
source3 = (8, 6)
dest3 = (5, 5)
expected3 = 1

print("Running tests...\n")
test_case(1, lines1, source1, dest1, expected1)
test_case(2, lines2, source2, dest2, expected2)
test_case(3, lines3, source3, dest3, expected3)
