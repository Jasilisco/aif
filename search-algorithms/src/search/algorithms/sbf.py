from collections import deque
from src.search.node import Node


class Sbf:
    """
    Breadth-first search.
    It finds the solution with the fewest actions, which is not necessarily the cheapest one.
    """

    def __init__(self, problem):
        """
        Stores the problem to solve.

        Args:
            problem (Problem): Problem to solve.
        """
        self.problem = problem


    def solve_sbf(self):
        """
        Runs BFS from the initial state of the problem, with a goal test when a node is generated.

        Returns:
            tuple: (solution, last, n_explored, n_frontier), where 
                solution (Node | None) is the goal node or None if there is no solution
                last (Node) is the last examined node
                n_explored (int) is the number of explored states 
                n_frontier (int) is the number of nodes left in the frontier
        """
        start = self.problem.initial
        root = Node(start, 0, 0, None, None, None)

        if self.problem.is_goal(start):
            return root, root, 0, 0

        frontier = deque([root])
        in_frontier = {start}
        explored = set()
        last = root

        while frontier:
            node = frontier.popleft()

            in_frontier.remove(node.state)
            explored.add(node.state)
            last = node

            for action in self.problem.actions(node.state):
                state = self.problem.result(node.state, action)

                if state in explored or state in in_frontier:
                    continue

                child = Node(
                    state,
                    node.g + self.problem.cost(node.state, action),
                    node.depth + 1,
                    action,
                    node,
                    None
                )

                if self.problem.is_goal(state):
                    return child, last, len(explored), len(frontier)

                frontier.append(child)
                in_frontier.add(state)

        return None, last, len(explored), len(frontier)