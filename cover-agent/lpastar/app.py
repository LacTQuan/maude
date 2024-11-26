import heapq
from math import inf

class Solution:
    def __init__(self, start, goal, heuristic, graph):
        """
        :param start: Starting node
        :param goal: Goal node
        :param heuristic: Heuristic function h(start, goal)
        :param graph: A dictionary representing the graph {node: [(neighbor, cost), ...]}
        """
        self.start = start
        self.goal = goal
        self.h = heuristic
        self.graph = graph
        self.g = {}
        self.rhs = {}
        self.U = []
        self.key_modifier = 0

        # Initialize g and rhs values
        for node in graph:
            self.g[node] = inf
            self.rhs[node] = inf
        self.rhs[start] = 0

        # Add the start node to the priority queue
        self._insert(start, self._calculate_key(start))

    def _calculate_key(self, s):
        """
        Calculate the key for a node.
        :param s: The node
        :return: A tuple (k1, k2) representing the priority key
        """
        return (
            min(self.g[s], self.rhs[s]) + self.h(self.start, s) + self.key_modifier,
            min(self.g[s], self.rhs[s])
        )

    def _insert(self, node, key):
        """
        Insert a node into the priority queue with a given key.
        :param node: The node
        :param key: The key
        """
        heapq.heappush(self.U, (key, node))

    def _remove(self, node):
        """
        Remove a node from the priority queue.
        :param node: The node
        """
        self.U = [(key, n) for key, n in self.U if n != node]
        heapq.heapify(self.U)

    def _top_key(self):
        """
        Get the top key of the priority queue.
        :return: The top key
        """
        return self.U[0][0] if self.U else (inf, inf)

    def _pop(self):
        """
        Pop the node with the highest priority from the queue.
        :return: The node
        """
        return heapq.heappop(self.U)[1]

    def update_vertex(self, u):
        """
        Update a vertex.
        :param u: The vertex to update
        """
        if u != self.start:
            self.rhs[u] = min(
                c + self.g[s]
                for s, c in self.graph.get(u, [])
            )
        if u in [n for _, n in self.U]:
            self._remove(u)
        if self.g[u] != self.rhs[u]:
            self._insert(u, self._calculate_key(u))

    def compute_shortest_path(self):
        """
        Compute the shortest path.
        """
        while self._top_key() < self._calculate_key(self.goal) or self.rhs[self.goal] != self.g[self.goal]:
            u = self._pop()
            if self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s, _ in self.graph.get(u, []):
                    self.update_vertex(s)
            else:
                self.g[u] = inf
                for s, _ in self.graph.get(u, []) + [(u, 0)]:
                    self.update_vertex(s)

    def main(self):
        """
        Main procedure to run the algorithm.
        """
        self.compute_shortest_path()
        while True:
            # Example: Scan graph for changes (user-defined logic for dynamic updates)
            changed_edges = self._scan_graph_for_changes()
            for u, v, new_cost in changed_edges:
                # Update the edge cost and recompute
                self._update_edge_cost(u, v, new_cost)
                self.update_vertex(u)
            self.compute_shortest_path()

    def _scan_graph_for_changes(self):
        """
        Placeholder for scanning the graph for edge changes.
        This should return a list of tuples (u, v, new_cost).
        """
        return []  # Replace with actual logic for detecting edge cost changes

    def _update_edge_cost(self, u, v, new_cost):
        """
        Update the cost of an edge in the graph.
        :param u: Start node of the edge
        :param v: End node of the edge
        :param new_cost: New cost of the edge
        """
        self.graph[u] = [(n, c) if n != v else (v, new_cost) for n, c in self.graph.get(u, [])]
