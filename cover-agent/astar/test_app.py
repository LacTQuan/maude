#!/usr/bin/env python3
"""
Unit tests for the AStar algorithm using pytest.
To run these tests, execute:
    pytest test_astar.py
"""

import pytest
from app import Node, AStar, compare_coordinates
from app import make_grid, print_path
from app import print_grid
from app import make_grid

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
