#!/usr/bin/env python3
"""
This file is a Python translation of the provided C++ A* code.
It implements a simple A* (greedy best-first) search over a grid.
"""

import heapq
import random
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Node:
    x: int
    y: int
    id: int = 0    # Unique identifier, computed as x * n + y
    pid: int = 0   # Parent id
    h_cost: int = 0  # Heuristic cost (here, Manhattan distance)

    def __add__(self, other):
        # Allow adding a motion (as a Node with offset values) to the current node.
        return Node(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        # Two nodes are considered the same (for our closed list) if they have the same coordinates.
        return hash((self.x, self.y))

    def __lt__(self, other):
        # For the priority queue: compare based on the heuristic cost.
        return self.h_cost < other.h_cost

class Planner:
    def __init__(self, grid: List[List[int]]):
        # Save a copy of the original grid and store the grid dimensions.
        self.original_grid = [row[:] for row in grid]
        self.grid = [row[:] for row in grid]
        self.n = len(grid)

def get_motion() -> List[Node]:
    """
    Returns a list of possible moves (4-connected grid).
    Each move is represented as a Node with the corresponding offset.
    """
    # Movements: up, down, left, right.
    return [Node(-1, 0), Node(1, 0), Node(0, -1), Node(0, 1)]

def check_outside_boundary(node: Node, n: int) -> bool:
    """Return True if the node is outside the grid boundaries."""
    return node.x < 0 or node.x >= n or node.y < 0 or node.y >= n

def compare_coordinates(node1: Node, node2: Node) -> bool:
    """Return True if node1 and node2 share the same coordinates."""
    return node1.x == node2.x and node1.y == node2.y

class AStar(Planner):
    def __init__(self, grid: List[List[int]]):
        super().__init__(grid)

    def plan(self, start: Node, goal: Node) -> Tuple[bool, List[Node]]:
        """
        Executes the A* (greedy best-first) search.
        Returns a tuple: (True, path_list) if the goal is found,
        otherwise (False, empty_list).
        """
        # Reset grid to the original configuration.
        self.grid = [row[:] for row in self.original_grid]
        open_list = []  # priority queue (heap)
        closed_list = set()  # set of visited nodes

        motion = get_motion()
        heapq.heappush(open_list, start)

        # Main loop
        while open_list:
            current = heapq.heappop(open_list)
            current.id = current.x * self.n + current.y

            if current in closed_list:
                continue

            if compare_coordinates(current, goal):
                closed_list.add(current)
                self.grid[current.x][current.y] = 2
                return True, self.convert_closed_list_to_path(closed_list, start, goal)

            self.grid[current.x][current.y] = 2  # Mark current as opened/visited.

            for m in motion:
                new_point = current + m
                if new_point in closed_list:
                    continue
                new_point.id = new_point.x * self.n + new_point.y
                new_point.pid = current.id
                new_point.h_cost = abs(new_point.x - goal.x) + abs(new_point.y - goal.y)
                if compare_coordinates(new_point, goal):
                    heapq.heappush(open_list, new_point)
                    break
                if check_outside_boundary(new_point, self.n):
                    continue  # Out of boundary.
                if self.grid[new_point.x][new_point.y] != 0:
                    continue  # Skip obstacles or already visited.
                heapq.heappush(open_list, new_point)

            closed_list.add(current)
        return False, []

    def convert_closed_list_to_path(self, closed_list: set, start: Node, goal: Node) -> List[Node]:
        """
        Reconstructs the path from goal to start using the parent pointers (pid)
        stored in the nodes in the closed list.
        """
        current = None
        # Find the node in closed_list that matches the goal.
        for node in closed_list:
            if compare_coordinates(node, goal):
                current = node
                break
        if current is None:
            print("Error: Goal not found in closed list")
            return []

        path = []
        # Traverse backwards from goal to start.
        while not compare_coordinates(current, start):
            path.append(current)
            # Reconstruct the parent coordinates from the stored pid.
            parent = Node(current.pid // self.n, current.pid % self.n)
            parent_node = None
            for node in closed_list:
                if compare_coordinates(node, parent):
                    parent_node = node
                    break
            if parent_node is None:
                print("Error in calculating path")
                return []
            current = parent_node
        path.append(start)
        return path

def make_grid(grid: List[List[int]]):
    """
    A dummy grid creation function.
    In the original C++ code, obstacles may be added here.
    For simplicity, this version leaves the grid unchanged.
    """
    pass

def print_grid(grid: List[List[int]]):
    """Prints the grid row by row."""
    for row in grid:
        print(" ".join(map(str, row)))

def print_path(path: List[Node], start: Node, goal: Node, grid: List[List[int]]):
    """
    Prints the grid with the path marked (using the value 8).
    The path is taken as returned (from goal to start).
    """
    grid_copy = [row[:] for row in grid]
    for node in path:
        grid_copy[node.x][node.y] = 8  # Mark path cells with an 8.
    print("Grid with path:")
    print_grid(grid_copy)

if __name__ == '__main__':
    # Example usage similar to the C++ main inside BUILD_INDIVIDUAL.
    n = 11
    grid = [[0 for _ in range(n)] for _ in range(n)]
    make_grid(grid)

    # Randomly select start and goal positions.
    start = Node(random.randint(0, n - 1), random.randint(0, n - 1))
    goal = Node(random.randint(0, n - 1), random.randint(0, n - 1))

    # Initialize start and goal ids.
    start.id = start.x * n + start.y
    start.pid = start.id  # For the start, set the parent id to itself.
    goal.id = goal.x * n + goal.y
    start.h_cost = abs(start.x - goal.x) + abs(start.y - goal.y)

    # Ensure start and goal cells are free.
    grid[start.x][start.y] = 0
    grid[goal.x][goal.y] = 0

    print("Start:", start)
    print("Goal:", goal)
    print("Initial Grid:")
    print_grid(grid)

    astar = AStar(grid)
    path_found, path = astar.plan(start, goal)

    if path_found:
        print("\nPath found:")
        for node in path:
            print(node)
        print()
        print_path(path, start, goal, grid)
    else:
        print("No path found.")
