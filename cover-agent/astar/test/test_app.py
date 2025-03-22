#!/usr/bin/env python3
"""
Unit tests for the AStar algorithm using pytest.
To run these tests, execute:
    pytest test_astar.py
"""

import pytest
from src.app import Node, AStar, compare_coordinates
from src.app import make_grid, print_path
from src.app import print_grid
from src.app import make_grid

def test_start_equals_goal():
    """
    Test the trivial case where the start and goal are the same.
    The expected result is an immediate success with a path containing only the start.
    """
    grid = [
        [0, 0],
        [0, 0]
    ]
    start = Node(0, 0)
    goal = Node(0, 0)
    # Set the start node's id and parent id.
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    found, path = astar.plan(start, goal)
    assert found is True, "Path should be found when start equals goal"
    # The path should consist of only one node (start).
    assert len(path) == 1
    assert compare_coordinates(path[0], start), "The only node in the path should be the start"

def test_simple_path():
    """
    Test a simple 5x5 grid with no obstacles.
    The start is at the top‐left and the goal at the bottom‐right.
    The algorithm should find a path.
    """
    n = 5
    grid = [[0 for _ in range(n)] for _ in range(n)]
    start = Node(0, 0)
    goal = Node(4, 4)
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    found, path = astar.plan(start, goal)
    assert found is True, "A path should be found in an open grid"
    # According to our conversion, the returned path is from goal to start.
    assert compare_coordinates(path[0], goal), "The first node in the path should be the goal"
    assert compare_coordinates(path[-1], start), "The last node in the path should be the start"

def test_no_path():
    """
    Test a grid where obstacles block any possible path from start to goal.
    Obstacles are represented by any non-zero cell.
    """
    grid = [
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 0]
    ]
    start = Node(0, 0)
    goal = Node(2, 2)
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    found, path = astar.plan(start, goal)
    assert found is False, "No path should be found when obstacles block the way"
    assert path == [], "The path should be empty when no path exists"


def test_no_path_outside_boundary():
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    start = Node(-1, -1)  # Outside the grid
    goal = Node(2, 2)     # Inside the grid
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    found, path = astar.plan(start, goal)
    assert found is False, "No path should be found when start is outside the grid"
    assert path == [], "The path should be empty when no path exists"


def test_edge_case_start_goal():
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    start = Node(0, 0)  # Top-left corner
    goal = Node(2, 2)   # Bottom-right corner
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    found, path = astar.plan(start, goal)
    assert found is True, "A path should be found from top-left to bottom-right"
    assert len(path) > 0, "The path should not be empty"


def test_no_path_both_outside_boundary():
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    start = Node(-1, -1)  # Outside the grid
    goal = Node(-2, -2)    # Outside the grid
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    found, path = astar.plan(start, goal)
    assert found is False, "No path should be found when both start and goal are outside the grid"
    assert path == [], "The path should be empty when no path exists"


def test_parent_node_not_found():
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    start = Node(0, 0)
    goal = Node(2, 2)
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    closed_list = {Node(0, 0), Node(1, 1), Node(2, 2)}
    # Modify the goal node's pid to point to a non-existent parent.
    for node in closed_list:
        if compare_coordinates(node, goal):
            node.pid = 999  # Non-existent ID
            break
    path = astar.convert_closed_list_to_path(closed_list, start, goal)
    assert path == [], "Path should be empty when parent node is not found"


def test_goal_not_found_in_closed_list():
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    start = Node(0, 0)
    goal = Node(2, 2)
    start.id = 0
    start.pid = 0
    astar = AStar(grid)
    closed_list = {Node(0, 0), Node(1, 1)}  # Goal is not in closed_list
    path = astar.convert_closed_list_to_path(closed_list, start, goal)
    assert path == [], "Path should be empty when goal is not found in closed list"

def test_print_grid():
    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # Call print_grid and check that it doesn't raise an exception.
    try:
        print_grid(grid)
    except Exception as e:
        assert False, f"print_grid raised an exception: {e}"
    assert True  # If no exception was raised, the test passes.


def test_make_grid_call():
    grid = [[0, 0], [0, 0]]
    try:
        make_grid(grid)
    except Exception as e:
        assert False, f"make_grid raised an exception: {e}"
    assert True


def test_print_path():
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    start = Node(0, 0)
    goal = Node(2, 2)
    path = [Node(2, 2), Node(1, 1), Node(0, 0)]  # Example path
    try:
        print_path(path, start, goal, grid)
    except Exception as e:
        assert False, f"print_path raised an exception: {e}"
    assert True


def test_path_with_obstacle():
    n = 3
    grid = [[0 for _ in range(n)] for _ in range(n)]
    grid[1][1] = 1  # Add an obstacle in the middle
    start = Node(0, 0)
    goal = Node(2, 2)
    start.id = start.x * n + start.y
    start.pid = start.id
    goal.id = goal.x * n + goal.y
    start.h_cost = abs(start.x - goal.x) + abs(start.y - goal.y)
    grid[start.x][start.y] = 0
    grid[goal.x][goal.y] = 0
    astar = AStar(grid)
    found, path = astar.plan(start, goal)
    assert found is True
    assert len(path) > 0
    assert compare_coordinates(path[0], goal)
    assert compare_coordinates(path[-1], start)



def test_main_execution():
    n = 5  # Reduced grid size for faster testing
    grid = [[0 for _ in range(n)] for _ in range(n)]
    make_grid(grid)

    # Randomly select start and goal positions.
    start = Node(0, 0)
    goal = Node(n - 1, n - 1)

    # Initialize start and goal ids.
    start.id = start.x * n + start.y
    start.pid = start.id  # For the start, set the parent id to itself.
    goal.id = goal.x * n + goal.y
    start.h_cost = abs(start.x - goal.x) + abs(start.y - goal.y)

    # Ensure start and goal cells are free.
    grid[start.x][start.y] = 0
    grid[goal.x][goal.y] = 0

    astar = AStar(grid)
    path_found, path = astar.plan(start, goal)

    assert isinstance(path_found, bool), "path_found should be a boolean"
    assert isinstance(path, list), "path should be a list"


def test_main_execution_no_random():
    n = 5  # Reduced grid size for faster testing
    grid = [[0 for _ in range(n)] for _ in range(n)]
    make_grid(grid)

    # Randomly select start and goal positions.
    start = Node(0, 0)
    goal = Node(n - 1, n - 1)

    # Initialize start and goal ids.
    start.id = start.x * n + start.y
    start.pid = start.id  # For the start, set the parent id to itself.
    goal.id = goal.x * n + goal.y
    start.h_cost = abs(start.x - goal.x) + abs(start.y - goal.y)

    # Ensure start and goal cells are free.
    grid[start.x][start.y] = 0
    grid[goal.x][goal.y] = 0

    astar = AStar(grid)
    path_found, path = astar.plan(start, goal)

    assert isinstance(path_found, bool), "path_found should be a boolean"
    assert isinstance(path, list), "path should be a list"


def test_node_equality_non_node():
    node = Node(1, 2)
    assert (node == 1) is False
