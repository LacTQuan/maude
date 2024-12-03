from app import main

def test_main():
    # 0: Free cell, 1: Obstacle
    grid = [
        [0, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
    ]
    start = (0, 0)
    goal = (3, 3)
    
    expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (3, 3)]
    actual_path = main(grid, start, goal)
    
    assert actual_path == expected_path, f"Expected {expected_path}, but got {actual_path}"

def test_no_path_found():
    # 0: Free cell, 1: Obstacle
    grid = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
    ]
    start = (0, 0)
    goal = (3, 3)

    expected_path = "No path found"
    actual_path = main(grid, start, goal)

    assert actual_path == expected_path, f"Expected {expected_path}, but got {actual_path}"

