import heapq

class Node:
    def __init__(self, state, cost=0, parent=None):
        self.state = state  # Unique identifier for the node
        self.cost = cost  # Cost to reach this node
        self.parent = parent  # Reference to the parent node for path reconstruction

    def __lt__(self, other):
        return self.cost < other.cost  # Comparison based on cost for priority queue

def main(start, goal, is_obstacle, successors, distance):
    """
    Find the path from start to goal using a cost-based search algorithm.

    :param start: The start node/state
    :param goal: The goal node/state
    :param is_obstacle: Function to check if a node/state is an obstacle
    :param successors: Function to generate successors for a node/state
    :param distance: Function to calculate distance between two nodes/states
    :return: A list representing the path from start to goal, or 'No path' if none exists
    """
    open_list = []  # Priority queue for nodes to be explored
    closed_list = set()  # Set for already explored nodes
    heapq.heappush(open_list, Node(start, cost=0))  # Add the start node to the open list

    while open_list:
        current_node = heapq.heappop(open_list)  # Get the node with the lowest cost
        
        # Check if the goal has been reached
        if current_node.state == goal:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]  # Reverse the path to get the correct order
        
        closed_list.add(current_node.state)

        for succ_state in successors(current_node.state):
            # if succ_state == goal:
            #     return [current_node.state, goal]
            
            if is_obstacle(succ_state) or succ_state in closed_list:
                continue

            succ_cost = current_node.cost + distance(current_node.state, succ_state)
            succ_node = Node(succ_state, cost=succ_cost, parent=current_node)
            
            # Check if a better path already exists in the open list
            existing_node = next((n for n in open_list if n.state == succ_state), None)
            if existing_node and existing_node.cost <= succ_cost:
                continue
            
            # Add the new node to the open list
            heapq.heappush(open_list, succ_node)

    return "No path"