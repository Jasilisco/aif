from collections import deque

from src.search_problem.node import Node


def bfs(problem):
    """
    Breadth-first search.

    Args:
        problem: Problem instance (initial state, actions, result, cost, is_goal).

    Returns:
        A tuple containing:
            - solution: Goal node, or None if no solution is found.
            - last: Last examined node.
            - n_explored: Number of states in the explored set.
            - n_frontier: Number of nodes remaining in the frontier.
    """

    root = Node(problem.initial)

    if problem.is_goal(root.state):
        return root, root, 0, 0

    # FIFO queue for BFS
    frontier = deque([root])
    in_frontier = {root.state}
    explored = set()
    last = root

    while frontier:
        node = frontier.popleft()

        in_frontier.remove(node.state)
        explored.add(node.state)
        last = node

        for action in problem.actions(node.state):
            state = problem.result(node.state, action)

            # Repeated-state check
            if state in explored or state in in_frontier:
                continue

            # The cost is computed from the parent state, before applying the action
            cost = problem.cost(node.state, action)

            child = Node(
                state,
                node.g + cost,
                node.depth + 1,
                action,
                node
            )

            # Goal test when the node is generated
            if problem.is_goal(state):
                return child, last, len(explored), len(frontier)

            frontier.append(child)
            in_frontier.add(state)

    return None, last, len(explored), len(frontier)