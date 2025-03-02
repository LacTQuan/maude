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


from app import LazyPQ, Node

def test_lazypq_insert_remove_clear():
    pq = LazyPQ()
    node = Node(0, 0)
    pq.insert(node, (1, 1))
    pq.remove(node)
    assert node not in pq.entry_finder
    pq.clear()
    assert pq.empty()


from app import LPAStar, Node

def test_no_valid_predecessor():
    # Create a 5x5 grid with obstacles blocking all paths except the start.
    grid = [[1 for _ in range(5)] for _ in range(5)]
    grid[0][0] = 0  # Start is free
    start = Node(0, 0)
    goal = Node(4, 4)
    planner = LPAStar(grid)
    planner.max_time_step = 1
    found, path = planner.plan(start, goal)
    # Expect no path to be found since the goal is unreachable.
    assert found is False
    assert path == []


from app import LPAStar, Node

def test_no_valid_predecessor():
    # Create a 5x5 grid with obstacles blocking all paths except the start.
    grid = [[1 for _ in range(5)] for _ in range(5)]
    grid[0][0] = 0  # Start is free
    start = Node(0, 0)
    goal = Node(4, 4)
    planner = LPAStar(grid)
    planner.max_time_step = 1
    found, path = planner.plan(start, goal)
    # Expect no path to be found since the goal is unreachable.
    assert found is False
    assert path == []


from app import make_grid

def test_make_grid():
    grid = [[0 for _ in range(5)] for _ in range(5)]
    make_grid(grid)
    assert True


from app import LPAStar, Node

def test_larger_grid():
    n = 11
    grid = [[0 for _ in range(n)] for _ in range(n)]
    start = Node(0, 0)
    goal = Node(n - 1, n - 1)
    planner = LPAStar(grid)
    planner.max_time_step = 1
    found, path = planner.plan(start, goal)
    assert found is True
    assert path[-1] == start
    assert compare_coordinates(path[0], goal)


import math
from app import LPAStar, Node

def test_c_obstacle():
    grid = [[0 for _ in range(5)] for _ in range(5)]
    grid[1][0] = 1  # obstacle
    start = Node(0, 0)
    goal = Node(4, 4)
    planner = LPAStar(grid)
    planner.motions = [Node(1, 0, cost=1.0)]
    s1 = Node(1, 0)
    s2 = Node(2, 0)
    cost = planner.C(s1, s2)
    assert cost == math.inf
    s1 = Node(0,0)
    s2 = Node(1,0)
    grid[1][0] = 1
    cost = planner.C(s1,s2)
    assert cost == math.inf


from app import print_path, Node

def test_print_path():
    path = [Node(0, 0), Node(1, 1), Node(2, 2)]
    start = Node(0, 0)
    goal = Node(2, 2)
    grid = [[0 for _ in range(5)] for _ in range(5)]
    print_path(path, start, goal, grid)
    assert True  # Just check that it runs without errors


from app import LPAStar, Node

def test_same_start_goal():
    grid = [[0 for _ in range(5)] for _ in range(5)]
    start = Node(0, 0)
    goal = Node(0, 0)
    planner = LPAStar(grid)
    planner.max_time_step = 1
    found, path = planner.plan(start, goal)
    assert found is True
    assert path == [start]
    assert len(path) == 1


from app import LPAStar, Node

def test_dynamic_obstacles():
    grid = [[0 for _ in range(5)] for _ in range(5)]
    start = Node(0, 0)
    goal = Node(4, 4)
    time_discovered_obstacles = {
        1: [Node(1, 1)],
        2: [Node(2, 2)]
    }
    planner = LPAStar(grid)
    planner.max_time_step = 3
    planner.set_dynamic_obstacles(True, time_discovered_obstacles)
    found, path = planner.plan(start, goal)
    assert found is True
    assert path[-1] == start
    assert compare_coordinates(path[0], goal)


import pytest
from app import LazyPQ

def test_lazypq_top_pop_empty():
    pq = LazyPQ()
    with pytest.raises(KeyError):
        pq.top()
    with pytest.raises(KeyError):
        pq.pop()
