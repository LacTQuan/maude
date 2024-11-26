import heapq

class Node:
    def __init__(self, position, cost=0, h_cost=0):
        self.position = position  # (x, y) coordinates
        self.cost = cost  # Cost to reach this node
        self.h_cost = h_cost  # Heuristic cost to goal
        self.parent = None  # To trace the path back

    def __lt__(self, other):
        return (self.cost + self.h_cost) < (other.cost + other.h_cost)


def heuristic(node, goal):
    # Example: Using Manhattan distance as a heuristic
    return abs(node.position[0] - goal.position[0]) + abs(node.position[1] - goal.position[1])


def get_successors(node, grid):
    successors = []
    rows, cols = len(grid), len(grid[0])
    x, y = node.position
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 1:  # Check bounds and obstacles
            successors.append(Node((nx, ny)))
    return successors


def reconstruct_path(goal_node):
    path = []
    current = goal_node
    while current:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Reverse the path


def main(grid, start, goal):
    start_node = Node(start)
    goal_node = Node(goal)
    
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if current_node.position == goal_node.position:
            return reconstruct_path(current_node)
        
        closed_list.add(current_node.position)
        
        for successor in get_successors(current_node, grid):
            if successor.position in closed_list:
                continue
            
            successor.parent = current_node
            successor.cost = current_node.cost + 1  # Assuming uniform cost for simplicity
            successor.h_cost = heuristic(successor, goal_node)
            
            # Check if the successor is already in open list with a better cost
            in_open_list = any(
                node for node in open_list if node.position == successor.position
                and (node.cost + node.h_cost) <= (successor.cost + successor.h_cost)
            )
            if in_open_list:
                continue
            
            heapq.heappush(open_list, successor)
    
    return "No path found"
