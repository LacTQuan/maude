from app import main
def test_main():
    # Helper functions
    def is_obstacle(node):
        obstacles = {(1, 1), (1, 2), (2, 3), (3, 1)}  # Obstacles based on the grid layout
        return node in obstacles

    def successors(node):
        x, y = node
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < 5 and 0 <= ny < 5]  # Stay within bounds

    def distance(node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance

    # Test parameters
    start = (0, 0)
    goal = (4, 4)

    # Run the function
    result = main(start, goal, is_obstacle, successors, distance)

    # Expected path: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 4)]
    print("Resulting Path:", result)
    expected_path = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 4)]
    assert result == expected_path, f"Expected {expected_path}, but got {result}"

# Execute the test
test_main()
