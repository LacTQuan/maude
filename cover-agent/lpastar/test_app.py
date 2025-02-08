#!/usr/bin/env python3
"""
Unit tests for the LPAStar planner using pytest.
Two tests are provided:
  - test_path_found: a clear grid where a valid path is expected.
  - test_no_path: a grid blocked by obstacles where no valid path exists.
"""

import math
import pytest
from app import LPAStar, Node, check_outside_boundary, compare_coordinates
from app import LazyPQ

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

def test_lazy_pq_pop_empty():
    pq = LazyPQ()
    with pytest.raises(KeyError):
        pq.pop()


def test_dynamic_obstacles():
    grid = [[0 for _ in range(5)] for _ in range(5)]
    start = Node(0, 0)
    goal = Node(4, 4)
    planner = LPAStar(grid)
    planner.max_time_step = 5
    time_discovered_obstacles = {
        1: [Node(1, 1)],
        2: [Node(2, 2)],
        3: [Node(3, 3)]
    }
    planner.set_dynamic_obstacles(False, time_discovered_obstacles)
    found, path = planner.plan(start, goal)
    assert isinstance(found, bool)
    assert isinstance(path, list)


def test_lazy_pq_remove_and_top():
    pq = LazyPQ()
    node = Node(0, 0)
    pq.insert(node, 1)
    pq.remove(node)
    with pytest.raises(KeyError):
        pq.top()


def test_no_path_complex():
    # Create a 5x5 grid.
    grid = [[0 for _ in range(5)] for _ in range(5)]
    # Completely surround the start node with obstacles.
    grid[0][1] = 1
    grid[1][0] = 1
    grid[1][1] = 1
    start = Node(0, 0)
    goal = Node(4, 4)
    planner = LPAStar(grid)
    planner.max_time_step = 1  # limit iterations for testing
    found, path = planner.plan(start, goal)
    # With the start node boxed in, no path should be found.
    assert found is False
    assert path == []


def test_random_obstacles():
    n = 5
    grid = [[0 for _ in range(n)] for _ in range(n)]
    start = Node(0, 0)
    goal = Node(n-1, n-1)
    planner = LPAStar(grid)
    planner.max_time_step = 5  # Allow multiple time steps for obstacle generation
    planner.set_dynamic_obstacles(True) # Enable random obstacle creation
    found, path = planner.plan(start, goal)
    # Assertions should focus on the behavior, not specific path details which can vary randomly.
    # For example, check if the planner handles the random obstacles gracefully without errors.
    assert isinstance(found, bool)  # Check if the function returns a boolean value
    assert isinstance(path, list) # Check if the function returns a list

