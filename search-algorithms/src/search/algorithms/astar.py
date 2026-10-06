from src.search.node import Node

class Astar:
    def __init__(self, problem, h = 'chessboard'):
        self.problem = problem
        valid_weights = problem.cfg.map[problem.cfg.map > 0]
        self.heuristic_weight = int(valid_weights.min()) if valid_weights.size > 0 else 1
        self.h = self.weighted_chessboard_distance
        if h == 'manhattan':
            self.h = self.weighted_manhattan_distance
        elif h == '0':
            self.h = self.null_heuristic
        
    def solve_astar(self):
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
        for action in self.problem.actions(node.state):
            aux_s = self.problem.result(node.state, action)
            aux_g = node.g + self.problem.cost(node.state, action)
            aux_h = self.h(aux_s)
            yield Node(aux_s, aux_g, node.depth + 1, action, node, aux_h)       

    def weighted_chessboard_distance(self, state):
        return self.heuristic_weight * max(abs(state.x - self.problem.cfg.goal[0]), abs(state.y - self.problem.cfg.goal[1]))

    def weighted_manhattan_distance(self, state):
        return self.heuristic_weight * (abs(state.x - self.problem.cfg.goal[0]) + abs(state.y - self.problem.cfg.goal[1]))

    def null_heuristic(self, state):
        return 0
