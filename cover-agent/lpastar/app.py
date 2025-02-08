#!/usr/bin/env python3
"""
Python translation of the provided C++ LPA* planner.
This file contains the definitions for:
  - Node (with support for addition, equality, and printing status)
  - Helper functions: compare_coordinates, check_outside_boundary, get_motion, print_grid, make_grid, print_path
  - LazyPQ: A lazy priority queue with remove support
  - LPAStar: The planner class implementing LPA* logic.
"""

import math
import heapq
import random
import time
import copy

# -----------------------
# Helper Classes & Functions
# -----------------------

class Node:
    def __init__(self, x, y, cost=0.0, id=None, pid=None, h_cost=0.0):
        self.x = x
        self.y = y
        self.cost = cost
        # Assign id and parent id based on coordinates if not provided.
        self.id = id if id is not None else (x * 1000 + y)
        self.pid = pid if pid is not None else self.id
        self.h_cost = h_cost

    def __add__(self, other):
        # When adding two nodes (e.g. a position and a motion offset),
        # only x and y coordinates are added.
        return Node(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def print_status(self):
        print(f"Node({self.x}, {self.y}) cost: {self.cost}, id: {self.id}, pid: {self.pid}")

    def __repr__(self):
        return f"Node({self.x}, {self.y})"


def compare_coordinates(n1, n2):
    """Return True if nodes have the same coordinates."""
    return (n1.x == n2.x) and (n1.y == n2.y)


def check_outside_boundary(n, grid_size):
    """Return True if the node is outside a square grid of size grid_size."""
    return n.x < 0 or n.x >= grid_size or n.y < 0 or n.y >= grid_size


def get_motion():
    """
    Return a list of possible moves.
    In this example, we use 4-connected (up, down, left, right) motions,
    each with a cost of 1.0.
    """
    return [
        Node(-1, 0, cost=1.0),  # Up
        Node(1, 0, cost=1.0),   # Down
        Node(0, -1, cost=1.0),  # Left
        Node(0, 1, cost=1.0)    # Right
    ]


def print_grid(grid):
    """Print the 2D grid."""
    for row in grid:
        print(" ".join(str(cell) for cell in row))
    print()


def make_grid(grid):
    """
    Dummy function to mimic the MakeGrid() call from the C++ code.
    In this translation, we assume the grid is already initialized.
    """
    pass


def print_path(path, start, goal, grid):
    """Print the found path from start to goal."""
    print("Path from start to goal:")
    for node in path:
        print(f"({node.x}, {node.y})", end=" -> ")
    print("Goal")


# -----------------------
# Lazy Priority Queue
# -----------------------

class PQEntry:
    """Helper class to store node and its key."""
    def __init__(self, node, key):
        self.node = node
        self.key = key


class LazyPQ:
    """A lazy priority queue that supports insert, remove, top, and pop."""
    def __init__(self):
        self.heap = []
        self.entry_finder = {}  # Maps node to entry
        self.REMOVED = '<removed>'
        self.counter = 0

    def clear(self):
        self.heap = []
        self.entry_finder.clear()
        self.counter = 0

    def insert(self, node, key):
        if node in self.entry_finder:
            self.remove(node)
        count = self.counter
        self.counter += 1
        entry = [key, count, node]
        self.entry_finder[node] = entry
        heapq.heappush(self.heap, entry)

    def remove(self, node):
        entry = self.entry_finder.pop(node)
        entry[-1] = self.REMOVED

    def is_element_in_struct(self, node):
        return node in self.entry_finder

    def top(self):
        while self.heap and str(self.heap[0][-1]) == self.REMOVED:
            heapq.heappop(self.heap)
        if self.heap:
            key, count, node = self.heap[0]
            return PQEntry(node, key)
        raise KeyError("top from empty priority queue")

    def pop(self):
        while self.heap:
            key, count, node = heapq.heappop(self.heap)
            if str(node) != self.REMOVED:
                del self.entry_finder[node]
                return PQEntry(node, key)
        raise KeyError("pop from empty priority queue")

    def empty(self):
        return len(self.entry_finder) == 0

# -----------------------
# LPAStar Class
# -----------------------

class LPAStar:
    def __init__(self, grid):
        # Store the original grid and work on a copy.
        self.original_grid = [row[:] for row in grid]
        self.grid = [row[:] for row in grid]
        self.n = len(grid)
        self.rhs = None  # 2D grid of rhs values
        self.g = None    # 2D grid of g values
        self.time_discovered_obstacles = {}
        self.motions = []  # List of available motion primitives
        self.U = LazyPQ()  # Priority queue (open list)
        self.start = None
        self.goal = None
        self.time_step = 0
        self.max_time_step = 10
        self.create_random_obstacles = False

    def set_dynamic_obstacles(self, create_random_obstacles=False, time_discovered_obstacles={}):
        self.create_random_obstacles = create_random_obstacles
        self.time_discovered_obstacles = time_discovered_obstacles

    def is_obstacle(self, n):
        return self.grid[n.x][n.y] == 1

    @staticmethod
    def H(n1, n2):
        return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

    def get_neighbours(self, u):
        neighbours = []
        for m in self.motions:
            neighbour = u + m
            if not check_outside_boundary(neighbour, self.n):
                neighbours.append(neighbour)
        return neighbours

    def get_pred(self, u):
        return self.get_neighbours(u)

    def get_succ(self, u):
        return self.get_neighbours(u)

    def C(self, s1, s2):
        if self.is_obstacle(s1) or self.is_obstacle(s2):
            return math.inf
        # Compute the delta between nodes.
        delta = Node(s2.x - s1.x, s2.y - s1.y)
        for motion in self.motions:
            if compare_coordinates(motion, delta):
                return motion.cost
        return math.inf

    def calculate_key(self, s):
        val = min(self.g[s.x][s.y], self.rhs[s.x][s.y])
        return (val + LPAStar.H(s, self.goal), val)

    def create_grid_data(self):
        return [[math.inf for _ in range(self.n)] for _ in range(self.n)]

    def initialize(self):
        self.motions = get_motion()
        self.time_step = 0
        self.U.clear()
        self.rhs = self.create_grid_data()
        self.g = self.create_grid_data()
        self.rhs[self.start.x][self.start.y] = 0
        self.U.insert(self.start, self.calculate_key(self.start))

    def update_vertex(self, u):
        if self.grid[u.x][u.y] == 0:
            self.grid[u.x][u.y] = 2
        if not compare_coordinates(u, self.start):
            self.rhs[u.x][u.y] = math.inf
            predecessors = self.get_pred(u)
            for sprime in predecessors:
                self.rhs[u.x][u.y] = min(self.rhs[u.x][u.y], 
                                          self.g[sprime.x][sprime.y] + self.C(sprime, u))
        if self.U.is_element_in_struct(u):
            self.U.remove(u)
        if self.rhs[u.x][u.y] != self.g[u.x][u.y]:
            self.U.insert(u, self.calculate_key(u))

    def compute_shortest_path(self):
        while (not self.U.empty() and self.U.top().key < self.calculate_key(self.goal)) or \
              (self.rhs[self.goal.x][self.goal.y] != self.g[self.goal.x][self.goal.y]):
            u_entry = self.U.pop()
            u = u_entry.node
            if self.g[u.x][u.y] > self.rhs[u.x][u.y]:
                self.g[u.x][u.y] = self.rhs[u.x][u.y]
                for s in self.get_succ(u):
                    self.update_vertex(s)
            else:
                self.g[u.x][u.y] = math.inf
                for s in self.get_succ(u):
                    self.update_vertex(s)
                self.update_vertex(u)

    def detect_changes(self):
        obstacles = []
        if self.time_step in self.time_discovered_obstacles:
            discovered = self.time_discovered_obstacles[self.time_step]
            for obs in discovered:
                if not (compare_coordinates(obs, self.start) or compare_coordinates(obs, self.goal)):
                    self.grid[obs.x][obs.y] = 1
                    obstacles.append(obs)
        if self.create_random_obstacles and random.random() > 1.0 / self.n:
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            if not ((self.start.x == x and self.start.y == y) or (self.goal.x == x and self.goal.y == y)):
                self.grid[x][y] = 1
                obstacles.append(Node(x, y))
        return obstacles

    def clear_path_display(self, path):
        for node in path:
            if self.grid[node.x][node.y] == 1:  # discovered obstacle; leave it as obstacle
                self.grid[node.x][node.y] = 2  # mark as explored but not a path
        self.grid[self.start.x][self.start.y] = 3

    def update_path_display(self, path):
        for node in path:
            self.grid[node.x][node.y] = 3

    def get_new_path(self):
        current = self.goal
        path = [current]
        # Backtrack from goal to start.
        while not compare_coordinates(current, self.start):
            min_cost = math.inf
            min_node = None
            for motion in self.motions:
                new_node = current + motion
                if not check_outside_boundary(new_node, self.n):
                    if self.g[new_node.x][new_node.y] < min_cost:
                        min_cost = self.g[new_node.x][new_node.y]
                        min_node = new_node
            if min_node is None:
                break  # No valid predecessor found.
            min_node.id = min_node.x * self.n + min_node.y
            # Set the parent's id for the current node.
            path[-1].pid = min_node.id
            current = min_node
            path.append(current)
        if path:
            path_cost = path[-1].cost
            for node in path:
                node.cost = path_cost - node.cost
            path[-1].pid = path[-1].id
        return path

    def plan(self, start, goal):
        # Reset the working grid from the original.
        self.grid = [row[:] for row in self.original_grid]
        self.start = start
        self.goal = goal
        path = [start]
        self.grid[start.x][start.y] = 3
        print_grid(self.grid)
        self.initialize()
        while self.time_step < self.max_time_step:
            self.compute_shortest_path()
            if self.g[goal.x][goal.y] == math.inf:
                self.clear_path_display(path)
                print_grid(self.grid)
                print("No path exists")
                return (False, [])
            self.clear_path_display(path)
            path = self.get_new_path()
            self.update_path_display(path)
            print_grid(self.grid)
            self.time_step += 1

            # Sleep for 500 milliseconds (simulate pause_time)
            time.sleep(0.5)

            changed_nodes = self.detect_changes()
            if changed_nodes:
                for node in changed_nodes:
                    self.update_vertex(node)
        for node in path:
            node.print_status()
        print_grid(self.grid)
        return (True, path)

# -----------------------
# Main Routine (if run individually)
# -----------------------

if __name__ == "__main__":
    n = 11
    grid = [[0 for _ in range(n)] for _ in range(n)]
    make_grid(grid)

    # Create random start and goal nodes.
    start = Node(random.randint(0, n-1), random.randint(0, n-1))
    goal = Node(random.randint(0, n-1), random.randint(0, n-1))
    start.id = start.x * n + start.y
    start.pid = start.id
    goal.id = goal.x * n + goal.y
    start.h_cost = abs(start.x - goal.x) + abs(start.y - goal.y)

    # Ensure start and goal are free.
    grid[start.x][start.y] = 0
    grid[goal.x][goal.y] = 0

    start.print_status()
    goal.print_status()
    print_grid(grid)

    # Define dynamic obstacles discovered over time.
    time_discovered_obstacles = {
        1: [Node(1, 1)],
        2: [Node(2, 2)],
        3: [Node(5, 5)],
        4: [Node(6, 6), Node(7, 7), Node(8, 8), Node(9, 9), Node(10, 10), Node(7, 6)]
    }

    lpa_star = LPAStar(grid)
    lpa_star.set_dynamic_obstacles(False, time_discovered_obstacles)
    found, path_vector = lpa_star.plan(start, goal)
    print_path(path_vector, start, goal, grid)
