import heapq
import random

def compare_coordinates(n1, n2):
    """Return True if two nodes have the same (x,y) coordinates."""
    return n1.x == n2.x and n1.y == n2.y

def check_outside_boundary(node, n):
    """Return True if the node is outside the grid boundary (grid is n x n)."""
    return node.x < 0 or node.x >= n or node.y < 0 or node.y >= n

def get_motion():
    """
    Returns a list of possible motions as Node objects.
    Here we use four-connectivity: right, down, left, up.
    The cost for each move is assumed to be 1.
    """
    return [Node(0, 1, 1),  # move right
            Node(1, 0, 1),  # move down
            Node(0, -1, 1), # move left
            Node(-1, 0, 1)] # move up

class Node:
    def __init__(self, x, y, cost=0, id=None, pid=None):
        self.x = x
        self.y = y
        self.cost = cost
        # id and pid (parent id) are assigned later in the algorithm
        self.id = id
        self.pid = pid

    def __add__(self, other):
        # When adding a motion to a node, add coordinates and accumulate cost.
        return Node(self.x + other.x, self.y + other.y, self.cost + other.cost)

    def __eq__(self, other):
        # Two nodes are considered equal if they share the same (x, y) coordinates.
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        # Hash based on coordinates (so that sets and dicts use (x,y)).
        return hash((self.x, self.y))

    def __lt__(self, other):
        # For priority queue: compare nodes by cost.
        return self.cost < other.cost

    def __repr__(self):
        return f"Node(x={self.x}, y={self.y}, cost={self.cost}, id={self.id}, pid={self.pid})"

class Planner:
    def __init__(self, grid):
        # Store the original grid (2D list) and grid size (assumed square).
        self.original_grid = [row[:] for row in grid]
        self.grid = [row[:] for row in grid]
        self.n = len(grid)

class Dijkstra(Planner):
    def __init__(self, grid):
        super().__init__(grid)

    def plan(self, start, goal):
        """
        Runs a Dijkstra-like search on the grid.
        Returns a tuple (found, path) where found is a Boolean indicating if a
        path was found and path is a list of Node objects representing the path
        from goal to start (reverse order).
        """
        # Reset grid to its original state.
        self.grid = [row[:] for row in self.original_grid]
        open_list = []  # Priority queue for nodes to explore.
        closed_list = set()  # Set to keep track of visited nodes.
        motion = get_motion()

        # Start with the starting node.
        heapq.heappush(open_list, start)

        # Main loop of the search.
        while open_list:
            current = heapq.heappop(open_list)
            # Compute and update the id from (x,y)
            current.id = current.x * self.n + current.y

            # If this node has already been expanded, skip it.
            if current in closed_list:
                continue

            # If we have reached the goal, add to closed_list, mark grid, and backtrack.
            if compare_coordinates(current, goal):
                closed_list.add(current)
                self.grid[current.x][current.y] = 2
                return True, self.convert_closed_list_to_path(closed_list, start, goal)

            # Mark the current cell as visited (here using value 2).
            self.grid[current.x][current.y] = 2

            # Explore neighbors (motions).
            for m in motion:
                new_point = current + m
                if new_point in closed_list:
                    continue

                new_point.id = self.n * new_point.x + new_point.y
                new_point.pid = current.id

                # If the neighbor is the goal, push it and break (prioritize reaching the goal).
                if compare_coordinates(new_point, goal):
                    heapq.heappush(open_list, new_point)
                    break

                if check_outside_boundary(new_point, self.n):
                    continue  # Skip if outside grid.

                if self.grid[new_point.x][new_point.y] != 0:
                    continue  # Skip if cell is an obstacle or already visited.

                heapq.heappush(open_list, new_point)

            closed_list.add(current)

        # No path found.
        return False, []

    def convert_closed_list_to_path(self, closed_list, start, goal):
        """
        Converts the closed list (visited nodes) into a path from goal to start.
        Backtracks from the goal node using the stored parent ids (pid).
        """
        current = None
        # Find the node in closed_list that matches the goal coordinates.
        for node in closed_list:
            if compare_coordinates(node, goal):
                current = node
                break

        if current is None:
            print("Error in calculating path")
            return []

        path = []
        # Backtrack until we reach the start.
        while not compare_coordinates(current, start):
            path.append(current)
            parent_x = current.pid // self.n
            parent_y = current.pid % self.n
            parent_node = None
            for node in closed_list:
                if node.x == parent_x and node.y == parent_y:
                    parent_node = node
                    break
            if parent_node is None:
                print("Error in calculating path")
                return []
            current = parent_node

        path.append(start)
        return path

if __name__ == '__main__':
    # Example usage similar to the C++ main() under BUILD_INDIVIDUAL.
    n = 11
    grid = [[0 for _ in range(n)] for _ in range(n)]
    # (Optionally, you could modify grid here to add obstacles.)

    # Randomly generate start and goal nodes.
    start = Node(random.randint(0, n - 1), random.randint(0, n - 1), 0)
    goal = Node(random.randint(0, n - 1), random.randint(0, n - 1), 0)

    # Compute ids for start and goal.
    start.id = start.x * n + start.y
    start.pid = start.id
    goal.id = goal.x * n + goal.y

    # Ensure that start and goal positions are free.
    grid[start.x][start.y] = 0
    grid[goal.x][goal.y] = 0

    print("Start:", start)
    print("Goal:", goal)

    planner = Dijkstra(grid)
    found, path = planner.plan(start, goal)
    print("Path found:", found)
    print("Path:", path)
