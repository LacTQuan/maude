#!/usr/bin/env python3
"""
Unit tests for the LPAStar planner using pytest.
Two tests are provided:
  - test_path_found: a clear grid where a valid path is expected.
  - test_no_path: a grid blocked by obstacles where no valid path exists.
"""
from app import LPAStar, Node, check_outside_boundary, compare_coordinates

# For testing purposes, we override the sleep to avoid delays.
import time
time.sleep = lambda s: None  # disable sleep during tests

def test_path_found():
    # Create a 5x5 grid with no obstacles.
    grid = [[0 for _ in range(5)] for _ in range(5)]
    start = Node(0, 0)
    goal = Node(4, 4)
    planner = LPAStar(grid)
    # For faster testing, reduce the number of iterations.
    planner.max_time_step = 1
    found, path = planner.plan(start, goal)
    # Assert that a path was found.
    assert found is True
    # Check that the path starts at the start node.
    assert path[-1] == start
    # Check that the last node in the path matches the goal (by coordinates).
    assert compare_coordinates(path[0], goal)

def test_no_path():
    # Create a 5x5 grid.
    grid = [[0 for _ in range(5)] for _ in range(5)]
    # Place a vertical wall of obstacles in column 2.
    for i in range(5):
        grid[i][2] = 1
    start = Node(0, 0)
    goal = Node(0, 4)
    planner = LPAStar(grid)
    planner.max_time_step = 1  # limit iterations for testing
    found, path = planner.plan(start, goal)
    # With a full wall between start and goal, no path should be found.
    assert found is False
    assert path == []
