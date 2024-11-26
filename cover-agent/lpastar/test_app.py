from app import Solution

def test_main():
    # Define a heuristic function (Manhattan distance for grid)
    def heuristic(node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        return abs(x1 - x2) + abs(y1 - y2)

    # Define a small grid-like graph
    graph = {
        (0, 0): [((0, 1), 1), ((1, 0), 1)],
        (0, 1): [((0, 0), 1), ((0, 2), 1), ((1, 1), 1)],
        (0, 2): [((0, 1), 1), ((1, 2), 1)],
        (1, 0): [((0, 0), 1), ((1, 1), 1), ((2, 0), 1)],
        (1, 1): [((0, 1), 1), ((1, 0), 1), ((1, 2), 1), ((2, 1), 1)],
        (1, 2): [((0, 2), 1), ((1, 1), 1), ((2, 2), 1)],
        (2, 0): [((1, 0), 1), ((2, 1), 1)],
        (2, 1): [((1, 1), 1), ((2, 0), 1), ((2, 2), 1)],
        (2, 2): [((1, 2), 1), ((2, 1), 1)],
    }

    # Define start and goal nodes
    start = (0, 0)
    goal = (2, 2)

    # Initialize the D* Lite algorithm
    d_star = Solution(start, goal, heuristic, graph)

    # Run the algorithm
    d_star.compute_shortest_path()

    # Extract the shortest path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = min(
            (neighbor for neighbor, _ in graph[current]),
            key=lambda neighbor: d_star.g.get(neighbor, inf),
        )
    path.append(start)
    path.reverse()

    # Print the results
    print("Shortest Path:", path)
    print("Cost of Shortest Path:", d_star.g[goal])

