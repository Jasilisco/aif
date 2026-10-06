from src.search.node import Node


class Astar:
    """
    A* search. 
    Always expands the node with the lowest f(n) = g(n) + h(n), breaking ties with the lowest h(n).
    """

    def __init__(self, problem, h = 'chessboard'):
        """
        Stores the problem and selects the heuristic function.

        Args:
            problem (Problem): Problem to solve.
            h (str, optional): Heuristic to use: 'chessboard', 'manhattan' or '0'(null heuristic). 
            Defaults to 'chessboard'.
        """
        self.problem = problem
        valid_weights = problem.cfg.map[problem.cfg.map > 0]
        self.heuristic_weight = int(valid_weights.min()) if valid_weights.size > 0 else 1
        self.h = self.weighted_chessboard_distance

        if h == 'manhattan':
            self.h = self.weighted_manhattan_distance
        elif h == '0':
            self.h = self.null_heuristic

        
    def solve_astar(self):
        """
        Runs A* from the initial state of the problem, with a goal test when a node is expanded.

        Returns:
            tuple: (solution, last, n_explored, n_frontier), where
                    solution (Node | None) is the goal node or None if there is no solution
                    last (Node | None) is the last examined node (the parent of the goal if there is a solution)
                    n_explored (int)is the number of explored states 
                    n_frontier (int) the nodes left in the frontier
        """
        frontier = [Node(self.problem.initial, 0, 0, None, None, self.h(self.problem.initial))]
        explored = set()
        current_node = None

        while frontier:
            current_node = min(frontier, key=lambda n: ((n.h + n.g), n.h))
            frontier.remove(current_node)
            
            if self.problem.is_goal(current_node.state):
                return current_node, current_node.parent, len(explored), len(frontier)
            
            explored.add(current_node.state)
            for node in self.expand_node(current_node):
                if node.state not in explored:
                    repeated = next((frontier_node for frontier_node in frontier if frontier_node.state == node.state), None) 
                    if repeated is not None:
                        if (repeated.g > node.g):
                            frontier.remove(repeated)
                            frontier.append(node)
                    else:
                        frontier.append(node)
                        
        return None, current_node, len(explored), len(frontier)


    def expand_node(self, node):
        """
        Generates the successor nodes of a node, one for each available action.

        Args:
            node (Node): Node to expand.

        Yields:
            Node: Successor with its g(n), h(n), depth and operator already computed.
        """
        for action in self.problem.actions(node.state):
            aux_s = self.problem.result(node.state, action)
            aux_g = node.g + self.problem.cost(node.state, action)
            aux_h = self.h(aux_s)
            yield Node(aux_s, aux_g, node.depth + 1, action, node, aux_h)       


    def weighted_chessboard_distance(self, state):
        """
        Heuristic: Chebyshev distance to the goal multiplied by the heuristic weight.

        Args:
            state (State): State to evaluate.

        Returns:
            int: Heuristic value h(n).
        """
        return self.heuristic_weight * max(abs(state.x - self.problem.cfg.goal[0]), abs(state.y - self.problem.cfg.goal[1]))


    def weighted_manhattan_distance(self, state):
        """
        Heuristic: Manhattan distance to the goal multiplied by the heuristic weight.

        Args:
            state (State): State to evaluate.

        Returns:
            int: Heuristic value h(n).
        """
        return self.heuristic_weight * (abs(state.x - self.problem.cfg.goal[0]) + abs(state.y - self.problem.cfg.goal[1]))


    def null_heuristic(self, state):
        """
        Heuristic that is always zero, so A* behaves as uniform-cost search.

        Args:
            state (State): State to evaluate.

        Returns:
            int: Always 0.
        """
        return 0