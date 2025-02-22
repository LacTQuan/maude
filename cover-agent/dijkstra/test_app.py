import pytest
from app import Node, Dijkstra

def test_simple_path():
    """
    Test case 1:
    A simple 3x3 grid with no obstacles. The start is at (0,0) and the goal is at (2,2).
    We expect the planner to find a path.
    Note: The returned path is in reverse order (goal to start).
    """
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    start = Node(0, 0, 0)
    goal = Node(2, 2, 0)
    planner = Dijkstra(grid)
    found, path = planner.plan(start, goal)
    
    assert found is True, "Path should be found in a clear grid."
    # Check that the path starts at the goal and ends at the start.
    assert path[0] == goal, "Path should start with the goal node."
    assert path[-1] == start, "Path should end with the start node."
    # Optionally, check that the length of the path is reasonable (at least Manhattan distance + 1)
    manhattan_distance = abs(goal.x - start.x) + abs(goal.y - start.y)
    assert len(path) >= manhattan_distance + 1

def test_no_path():
    """
    Test case 2:
    A 3x3 grid where the start is completely blocked off.
    Start is at (0,0) and obstacles are placed so that there is no valid move.
    The planner should return that no path is found.
    """
    grid = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    start = Node(0, 0, 0)
    goal = Node(2, 2, 0)
    planner = Dijkstra(grid)
    found, path = planner.plan(start, goal)

    assert found is False, "No path should be found if the start is blocked."
    assert path == [], "Path should be empty when no path is found."

def test_obstacle_detour():
    """
    Test case 3:
    A 3x3 grid with a vertical obstacle in the middle.
    The start is at (0,0) and the goal is at (2,2). A detour is required.
    We expect the planner to find a valid path.
    """
    grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    start = Node(0, 0, 0)
    goal = Node(2, 2, 0)
    planner = Dijkstra(grid)
    found, path = planner.plan(start, goal)

    assert found is True, "A path should be found around the obstacle."
    assert path[0] == goal, "Path should start with the goal node."
    assert path[-1] == start, "Path should end with the start node."


def test_goal_not_found():
    planner = Dijkstra([[0]])
    closed_list = set()
    start = Node(0, 0, 0)
    goal = Node(1, 1, 0)
    path = planner.convert_closed_list_to_path(closed_list, start, goal)
    assert path == []


def test_node_repr():
    node = Node(1, 2, 3, 4, 5)
    expected_repr = "Node(x=1, y=2, cost=3, id=4, pid=5)"
    assert repr(node) == expected_repr
