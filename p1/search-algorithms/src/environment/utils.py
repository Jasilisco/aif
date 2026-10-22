def path_to(node):
    """
    Rebuilds the path from the root of the search tree to a node.

    Args:
        node (Node): Last node of the path.

    Returns:
        list[Node]: Nodes from the root to the given node, in order.
    """
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return list(reversed(path))


def format_node(node, astar = False):
    """
    Formats a node as text.

    Args:
        node (Node): Node to format.
        astar (bool, optional): If True, the heuristic value h(n) is included. Defaults to False.

    Returns:
        str: "(d, g(n), op, S)" for blind search, or "(d, g(n), op, h(n), S)" for A*.
    """
    op = node.operator if node.operator is not None else "-"
    
    if not astar:
        return f"({node.depth}, {node.g}, {op}, {node.state})"
    return f"({node.depth}, {node.g}, {op}, {node.h}, {node.state})"


def _trace_content(solution, last, n_explored, n_frontier, astar):
    """
    Builds the shared trace body for console and file output.

    Args:
        solution (Node | None): Goal node, or None if no solution was found.
        last (Node): Last examined node, used when there is no solution.
        n_explored (int): Number of items in the explored list.
        n_frontier (int): Number of items in the frontier.
        astar (bool): If True, nodes include their h(n).

    Returns:
        list[str]: Trace lines without the output-specific header or footer.
    """
    lines = []
    if solution is None:
        lines += ["No solution found. Path from the initial state to the last examined node:", ""]
        node = last
    else:
        node = solution

    path = path_to(node)
    n = len(path) - 1

    for i, current in enumerate(path):
        if i > 0:
            lines.append(f"Operator {i}: {current.operator}")
        if i == 0:
            label = "Node 0 (starting node)"
        elif i == n and solution is not None:
            label = f"Node {i} (final node)"
        else:
            label = f"Node {i}"
        lines.append(f"{label}: {format_node(current, astar)}")

    lines += ["", "--- TRACE INFORMATION PARAMS ---", ""]

    if solution is not None:
        lines.append(f"Final depth: {node.depth}")
        lines.append(f"Final cost: {node.g}")

    lines.append(f"Total number of items in explored list: {n_explored}")
    lines.append(f"Total number of items in frontier: {n_frontier}")
    return lines


def print_trace(solution, last, n_explored, n_frontier, astar= False):
    """
    Prints the execution trace: the path from the initial node to the solution
    (or to the last examined node if there is no solution) and the search statistics.

    Args:
        solution (Node | None): Goal node, or None if no solution was found.
        last (Node): Last examined node.
        n_explored (int): Number of items in the explored list.
        n_frontier (int): Number of items in the frontier.
        astar (bool, optional): If True, nodes are printed with their h(n). Defaults to False.
    """
    lines = ["--- TRACE PRINTING ---", ""]
    lines.extend(_trace_content(solution, last, n_explored, n_frontier, astar))
    lines.append("")
    print("\n".join(lines))


def extract_trace(filename, algorithm, solution, last, n_explored, n_frontier, astar=False):
    """
    Builds the execution trace as text.

    Args:
        filename (str): Name of the map file.
        algorithm (str): Name of the algorithm.
        solution (Node | None): Goal node, or None if no solution was found.
        last (Node): Last examined node.
        n_explored (int): Number of items in the explored list.
        n_frontier (int): Number of items in the frontier.
        astar (bool, optional): If True, nodes include their h(n). Defaults to False.

    Returns:
        str: Complete trace.
    """
    lines = [f"--- TRACE PRINTING FOR {filename} WITH ALGORITHM {algorithm} ---", ""]
    lines.extend(_trace_content(solution, last, n_explored, n_frontier, astar))
    lines.append('--------------------------------------------------------------')

    return "\n".join(lines) + "\n"