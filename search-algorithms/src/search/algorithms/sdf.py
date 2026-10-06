from src.search.node import Node

def dfs(problem):
    start = problem.initial
    root = Node(start, 0, 0, None, None, None)

    if problem.is_goal(start):
        return root, root, 0, 0

    frontier = [root]
    in_frontier = {start}
    explored = set()
    last = root

    while frontier:
        node = frontier.pop()

        in_frontier.remove(node.state)
        explored.add(node.state)
        last = node

        for action in reversed(problem.actions(node.state)):
            state = problem.result(node.state, action)

            if state in explored or state in in_frontier:
                continue

            child = Node(
                state,
                node.g + problem.cost(node.state, action),
                node.depth + 1,
                action,
                node,
                None
            )

            if problem.is_goal(state):
                return child, last, len(explored), len(frontier)

            frontier.append(child)
            in_frontier.add(state)

    return None, last, len(explored), len(frontier)