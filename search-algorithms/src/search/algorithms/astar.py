from src.search.node import Node
from src.environment.utils import print_trace

class Astar:
    def __init__(self, problem, h = 'chessboard'):
        self.problem = problem
        self.heuristic_weight = int(problem.cfg.board.min())
        self.h = self.weighted_chessboard_distance
        if h == 'manhattan':
            self.h = self.weighted_manhattan_distance
        
    def solve_astar(self):
        frontier = [Node(self.problem.initial, 0, 0, None, None, self.h(self.problem.initial))]
        explored = set()
        current_node = None
        while frontier:
            current_node = min(frontier, key=lambda n: ((n.h + n.g), n.h))
            frontier.remove(current_node)
            if self.problem.is_goal(current_node.state):
                return print_trace(current_node, current_node.parent, len(explored), len(frontier))
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
        return print_trace(None, current_node, len(explored), len(frontier))

    def expand_node(self, node):
        for action in self.problem.actions(node.state):
            auxS = self.problem.result(node.state, action)
            auxG = node.g + self.problem.cost(node.state, action)
            auxH = self.h(auxS)
            yield Node(auxS, auxG, node.depth + 1, action, node, auxH)       
        
    def weighted_chessboard_distance(self, state):
        return self.heuristic_weight * max(abs(state.x - self.problem.cfg.goal[0]), abs(state.y - self.problem.cfg.goal[1]))
        
    def weighted_manhattan_distance(self, state):
        return self.heuristic_weight * (abs(state.x - self.problem.cfg.goal[0]) + abs(state.y - self.problem.cfg.goal[1]))