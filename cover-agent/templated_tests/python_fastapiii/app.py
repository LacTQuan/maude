import heapq

class Node:
    def __init__(self, id):
        self.id = id
        self.g = float('inf')  # Cost to reach this node
        self.rhs = float('inf')  # One-step lookahead cost
        self.neighbors = {}  # {neighbor_node: edge_cost}
        self.parent = None  # To track the shortest path

    def __lt__(self, other):
        return (min(self.g, self.rhs), self.g) < (min(other.g, other.rhs), other.g)

class LPAStar:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.queue = []
        self.nodes = {}  # Store all nodes

    def initialize(self):
        self.start.rhs = 0
        heapq.heappush(self.queue, (self.calculate_key(self.start), self.start))

    def calculate_key(self, node):
        return (min(node.g, node.rhs), node.g)

    def update_node(self, node):
        if node.g != node.rhs:
            heapq.heappush(self.queue, (self.calculate_key(node), node))

    def compute_shortest_path(self):
        while self.queue and (
            self.queue[0][0] < self.calculate_key(self.goal) or self.goal.rhs != self.goal.g
        ):
            _, current = heapq.heappop(self.queue)
            if current.g > current.rhs:
                current.g = current.rhs
                for neighbor, cost in current.neighbors.items():
                    # Update the parent for backtracking
                    if neighbor.rhs > current.g + cost:
                        neighbor.rhs = current.g + cost
                        neighbor.parent = current  # Track the parent
                    self.update_node(neighbor)
            else:
                current.g = float('inf')
                for neighbor, cost in current.neighbors.items():
                    if neighbor.rhs == current.g + cost:
                        neighbor.rhs = min(
                            [float('inf')] + [
                                n.g + c for n, c in neighbor.neighbors.items()
                            ]
                        )
                        neighbor.parent = None  # Reset the parent if invalid
                    self.update_node(neighbor)
            self.update_node(current)

    def update_edge(self, node1, node2, new_cost):
        node1.neighbors[node2] = new_cost
        # node2.neighbors[node1] = new_cost  # Assume undirected graph
        heapq.heappush(self.queue, (self.calculate_key(node1), node1))
        # self.update_node(node2)

    def reconstruct_path(self):
        path = []
        current = self.goal
        while current is not None:
            path.append(current.id)
            current = current.parent
        path.reverse()
        return path


# Example Usage
start = Node("Start")
goal = Node("Goal")
nodeA = Node("A")
nodeB = Node("B")

start.neighbors = {nodeA: 1, nodeB: 2}
nodeA.neighbors = {goal: 3}
nodeB.neighbors = {goal: 1}

lpa = LPAStar(start, goal)
lpa.initialize()
lpa.compute_shortest_path()

# Print the initial shortest path
print("Initial shortest path:", lpa.reconstruct_path())

# Update edge weights dynamically
lpa.update_edge(nodeB, goal, 5)
lpa.compute_shortest_path()

# Print the new shortest path
print("Updated shortest path:", lpa.reconstruct_path())

