import sys

from src.environment.config import Config
from src.environment.problem import Problem
from src.search_problem.algorithms.bfs import bfs


def print_trace(solution, last, n_explored, n_frontier):
    """Prints the execution trace in the format of section 4.2 of the lab."""
    if solution is None:
        print("No solution found. Path to the last examined node:")
        end = last
    else:
        end = solution

    # Rebuild the path from the root to the end node
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()

    # Each node is printed as (d, g(n), op, S)
    for i, node in enumerate(path):
        op = node.operator if node.operator is not None else "-"
        text = f"({node.depth}, {node.g}, {op}, {node.state})"
        if i == 0:
            print("Node 0 (starting node)", text)
        else:
            print(f"Operator {i}: {node.operator}")
            print(f"Node {i}: {text}")

    if solution is not None:
        print("Total cost of the solution:", solution.g)
    print("Total number of items in explored list:", n_explored)
    print("Total number of items in frontier:", n_frontier)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        return 1

    cfg = Config(sys.argv[1])
    problem = Problem(cfg)
    print_trace(*bfs(problem))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())