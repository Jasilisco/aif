from node import Node
from problem import is_goal, successors
 
 
def dfs(matrix, start, goal):
    """
    Depth-first search (graph search version).
 
    Args:
        matrix: 2D list containing the hardness of each cell.
        start: Initial state as (x, y, o), where o is the orientation.
        goal: Goal state as (x, y, o). If o == 8, the final orientation is irrelevant.
 
    Returns:
        A tuple containing:
            - solution: Goal node, or None if no solution is found.
            - last: Last examined node.
            - n_explored: Number of states in the explored set.
            - n_frontier: Number of nodes remaining in the frontier.
    """
 
    root = Node(start, 0, 0, None, None)
 
    if is_goal(start, goal):
        return root, root, 0, 0
 
    # LIFO stack for DFS: the last node pushed is the first one expanded
    frontier = [root]
    in_frontier = {start}
    explored = set()
    last = root
 
    while frontier:
        node = frontier.pop()
 
        in_frontier.remove(node.state)
        explored.add(node.state)
        last = node
 
        # Successors are pushed in reverse order so that the first one
        # returned by successors() (Advance) is the first to be expanded
        for operator, state, cost in reversed(successors(node.state, matrix)):
            if state in explored or state in in_frontier:
                continue
 
            child = Node(
                state,
                node.g + cost,
                node.depth + 1,
                operator
            )
 
            node.set_child(child)
 
            # Goal test when the node is generated (same criterion as BFS)
            if is_goal(state, goal):
                return child, last, len(explored), len(frontier)
 
            frontier.append(child)
            in_frontier.add(state)
 
    return None, last, len(explored), len(frontier)